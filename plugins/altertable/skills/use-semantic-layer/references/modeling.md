# Semantic View Modeling

Source: [`semantic_layer` README](https://github.com/altertable-ai/duckdb-semantic_layer#defining-a-semantic-view)

Read this before writing a `CREATE SEMANTIC VIEW`, explaining a definition returned by `DESCRIBE SEMANTIC VIEW`, or porting a Snowflake semantic view.

## Statement

```sql
CREATE [ OR REPLACE | OR ALTER ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  TABLES ( <logical table> [, ...] )
  [ RELATIONSHIPS ( <relationship> [, ...] ) ]
  [ FACTS ( <fact> [, ...] ) ]
  [ DIMENSIONS ( <dimension> [, ...] ) ]
  [ METRICS ( <metric> [, ...] ) ]
  [ COMMENT = '<text>' ]
```

The definition is validated on creation: tables and columns must exist, keys and relationships must be consistent, the relationship graph must be acyclic, and expressions must type-check and respect the aggregation rules. Member types are recorded then; after a source type changes, re-create the view.

```sql
CREATE SEMANTIC VIEW memory.main.sales
  TABLES (
    orders    AS lake.main.orders      PRIMARY KEY (o_orderkey) TIME (o_orderdate),
    customers AS lake.main.customer    PRIMARY KEY (c_custkey),
    lines     AS lake.main.lineitem    PRIMARY KEY (l_orderkey, l_linenumber)
  )
  RELATIONSHIPS (
    orders_to_customers AS orders (o_custkey) REFERENCES customers,
    lines_to_orders     AS lines (l_orderkey) REFERENCES orders
  )
  FACTS (
    lines.net_price   AS l_extendedprice * (1 - l_discount),
    orders.line_count AS COUNT(lines.l_linenumber)
  )
  DIMENSIONS (
    customers.segment AS c_mktsegment
  )
  METRICS (
    lines.revenue        AS SUM(lines.net_price),
    lines.revenue_ly     OFFSET (metric_time.day BY INTERVAL 1 YEAR) AS lines.revenue,
    lines.revenue_ytd    CUMULATIVE (metric_time.day TO YEAR) AS SUM(lines.net_price),
    orders.avg_lines     AS AVG(orders.line_count),
    customers.customers  AS COUNT(*),
    revenue_per_customer AS lines.revenue / customers.customers,
    revenue_growth       AS lines.revenue / lines.revenue_ly - 1
  )
  COMMENT = 'Order revenue and customers'
```

## Logical Tables

```sql
[ <alias> AS ] { <table or view> | ( <select query> ) }
  [ PRIMARY KEY ( <column> [, ...] ) ]
  [ UNIQUE ( <column> [, ...] ) ] [...]
  [ CONSTRAINT [ <name> ] DISTINCT RANGE BETWEEN <start column> AND <end column> EXCLUSIVE ]
  [ TIME ( <column> ) ]
  [ WITH SYNONYMS [ = ] ( '<synonym>' [, ...] ) ]
  [ COMMENT = '<text>' ]
```

The alias, by default the table name, is how the rest of the definition refers to the table. Fully qualify sources as `catalog.schema.table`.

## Relationships

```sql
[ <name> AS ] <table> ( <column> [, ...] ) REFERENCES <referenced table>
  [ ( { [ ASOF ] <column> [, ...] | BETWEEN <start column> AND <end column> EXCLUSIVE } ) ]
```

- A relationship is many-to-one or one-to-one. Referenced columns default to the referenced table's primary key, or its only unique key.
- Unnamed relationships are named `<from>_to_<to>`.
- Joins only follow relationships toward the "one" side, so they never multiply the rows a metric aggregates. Declare keys truthfully: a false primary key silently breaks that guarantee.

## Facts, Dimensions, and Metrics

```sql
-- facts: row-level values before aggregation
[ PRIVATE | PUBLIC ] <table>.<fact> AS <expression> [ WITH SYNONYMS ( ... ) ] [ COMMENT = '<text>' ]

-- dimensions: row-level attributes to group and filter by
<table>.<dimension> AS <expression> [ WITH SYNONYMS ( ... ) ] [ COMMENT = '<text>' ]

-- metrics: aggregates
[ PRIVATE | PUBLIC ] [ <table>. ]<metric>
  [ USING ( <relationship> [, ...] ) ]
  [ NON ADDITIVE BY ( <dimension> [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] ) ]
  [ FILTER ( WHERE <condition> ) ]
  [ OFFSET ( <dimension> BY <interval> ) ]
  [ CUMULATIVE ( <dimension> [ OVER <interval> | TO <date part> ] [ FIRST | LAST | AVERAGE ] ) ]
  AS <expression> [ WITH SYNONYMS ( ... ) ] [ COMMENT = '<text>' ]
```

- **Facts and dimensions** are row-level expressions of their table. They may read its columns and the facts and dimensions of tables it references. They may also aggregate rows of a table that references them: `orders.line_count AS COUNT(lines.l_linenumber)`.
- **Table metrics** (`<table>.<metric>`) aggregate their table's rows. Aggregates may nest to aggregate a finer table first: `customers.avg_order_total AS AVG(SUM(orders.o_totalprice))`.
- **Derived metrics** (no table prefix) combine metrics from different tables, each at its own grain: `revenue_per_customer AS lines.revenue / customers.customers`.
- **`PRIVATE`** facts and metrics can be referenced by other definitions but not queried.
- Bare names resolve to a member of the expression's own table, then a column of that table, then a name unique in the view.
- Aggregate SQL macros count as aggregates. Window functions are not allowed in facts or dimensions.

## Advanced Modeling

### Role-Playing Relationships (`USING`)

```sql
RELATIONSHIPS (
  departure AS flights (departure_airport) REFERENCES airports,
  arrival   AS flights (arrival_airport)   REFERENCES airports
)
METRICS (
  flights.departures USING (departure) AS COUNT(*),
  flights.arrivals   USING (arrival)   AS COUNT(*)
)
```

Without `USING`, `TIME` defaults win, then direct relationships beat detours at every hop, and any remaining ambiguity is rejected. Pin an intended detour with `USING`, because adding a direct relationship later can change the selected path.

### Many-to-Many Bridges

A table with relationships to two tables bridges them:

```sql
TABLES (authors PRIMARY KEY (author_id), books PRIMARY KEY (book_id),
        book_authors PRIMARY KEY (book_id, author_id))
RELATIONSHIPS (book_authors (author_id) REFERENCES authors,
               book_authors (book_id) REFERENCES books)
```

- `books.total_pages` can be grouped by `authors.country`; each book counts once per group, and totals without bridged dimensions are unchanged.
- Any table with relationships to both sides is a bridge, fact tables included: `customers.customer_count` by `products.category` through `sales` counts customers who bought in each category.
- A dimension stored on the bridge itself is rejected. Rows without a bridge row get NULL bridged dimensions, and a `WHERE` on bridged tables keeps only rows with a match.
- Prefer a bridge over finer tables that reference it. Select a bridge explicitly with `USING (<relationship>)`.

### Semi-Additive Metrics (`NON ADDITIVE BY`)

```sql
METRICS (accounts.balance NON ADDITIVE BY (dates.day) AS SUM(balance))
```

Within each group, only rows of the last snapshot in the given order are aggregated. Use it for balances, inventory, and headcount.

### Metric Filters (`FILTER`)

```sql
METRICS (
  invoices.revenue AS SUM(amount),
  costs.cost       AS SUM(cost),
  margin AS (invoices.revenue - costs.cost) / invoices.revenue,
  enterprise_margin FILTER (WHERE accounts.segment = 'enterprise') AS margin
)
```

The filter restricts every aggregate the metric is built from, nested metrics included; nested filters combine with `AND`. Every table the condition reads must be reachable from each filtered aggregate's table.

### Time Spine (`TIME`)

```sql
TABLES (
  invoices  PRIMARY KEY (invoice_id)  TIME (invoiced_at),
  shipments PRIMARY KEY (shipment_id) TIME (ordered_at)
)
RELATIONSHIPS (shipped AS shipments (shipped_at) REFERENCES metric_time)
DIMENSIONS (metric_time.weekday AS dayofweek(day))
METRICS (
  shipments.booked AS SUM(booked),
  shipments.shipped_amount USING (shipped) AS SUM(booked)
)
```

- `TIME (<column>)` declares a table's aggregation date (`DATE`, `TIMESTAMP`, or `TIMESTAMPTZ`). The view gains a logical table `metric_time` keyed by `day`, with `week` (Monday start), `month`, `quarter`, and `year` dimensions.
- Further calendar dimensions, such as a fiscal quarter, can be defined on `metric_time` from `day`; facts and metrics cannot.
- `metric_time` is never scanned. Each table reads its own time column; a line item inherits its order's date through an ordinary relationship. A query reading only the spine is rejected, and days without facts are absent from ordinary aggregates.
- To aggregate by another date, declare `<name> AS <table> (<column>) REFERENCES metric_time` and select it with `USING (<name>)`.

### Offsets and Cumulative Metrics

`OFFSET (<dimension> BY <interval>)` and `CUMULATIVE (<dimension> [OVER <interval> | TO <date part>] [FIRST | LAST | AVERAGE])` define what `time_shift()` and `cumulative()` compute at query time; [query syntax](query-syntax.md#query-time-transforms) describes their semantics. Use `metric_time.day` or another day-grain dimension for cumulative windows, because anchors over a fine-grained timestamp grow quadratically. Offset and cumulative metrics cannot be referenced by facts or dimensions, and a cumulative metric cannot wrap an offset, cumulative, or semi-additive metric.

### Time-Dependent and Range Relationships

- `ASOF` joins each row to the latest referenced row at or before its value: `orders (o_cust_id, o_ord_date) REFERENCES addresses (ca_cust_id, ASOF ca_start_date)`.
- Range relationships find the containing range: `events (ts) REFERENCES periods (BETWEEN start_time AND end_time EXCLUSIVE)`, with `CONSTRAINT DISTINCT RANGE BETWEEN start_time AND end_time EXCLUSIVE` on `periods`. NULL bounds are open. The lookup runs on distinct values and is much cheaper than a range join.

### Window Function Metrics

```sql
METRICS (
  sales.avg_7_days AS AVG(sales.total_quantity) OVER (
    PARTITION BY EXCLUDING dates.day ORDER BY dates.day
    RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW
  )
)
```

They run over the aggregated rows, so the dimensions they use must be requested; `SHOW SEMANTIC DIMENSIONS ... FOR METRIC` marks them `required`.

## Materializations

The extension can store metric aggregates at a chosen grain and answer matching queries from them transparently, with incremental refresh for DuckLake sources:

```sql
ALTER SEMANTIC VIEW <view> ADD MATERIALIZATION [IF NOT EXISTS] <name>
  [REFRESH_MODE = AUTO | FULL | INCREMENTAL] [IN <database>[.<schema>]]
  AS DIMENSIONS <dimension> [, ...] METRICS <metric> [, ...]
ALTER SEMANTIC VIEW <view> REFRESH MATERIALIZATION <name> [AUTO | FULL | INCREMENTAL]
ALTER SEMANTIC VIEW <view> SET MAX_STALENESS = <seconds>
SHOW SEMANTIC MATERIALIZATIONS [IN <view>]
```

Materializations write tables into a storage database: add, refresh, or drop one only when the user asks. Semi-additive, offset, cumulative, and bridged metrics cannot be materialized.

## Other DDL

- `ALTER SEMANTIC VIEW [IF EXISTS] <name> RENAME TO <new name>`, `SET COMMENT = '<text>'`, `UNSET COMMENT`, and `DROP SEMANTIC VIEW [IF EXISTS] <name>` change or remove a view; run them only when the user asks.
- Semantic views share the namespace of tables and views and appear in `information_schema` and `duckdb_views()` as placeholder views tagged `semantic_view`, with one typed column per public fact, dimension, and metric. Reading the placeholder as a plain table fails; use `SEMANTIC_VIEW(...)` or `AGG(...)`.

## Snowflake Compatibility

Snowflake definitions and queries run as written, with these exceptions:

- Accepted and kept only as metadata: `WITH SYNONYMS`, `LABELS = (FILTER)`, `SAMPLE_VALUES`, `IS_ENUM`, `WITH CORTEX SEARCH SERVICE`, `AI_SQL_GENERATION`, `AI_QUESTION_CATEGORIZATION`, `AI_VERIFIED_QUERIES`, `[WITH] TAG`, `COPY GRANTS`, and a materialization's `WAREHOUSE`.
- Not supported: `GET_DDL`, YAML import or export, window functions in facts and dimensions, `INFORMATION_SCHEMA.SEMANTIC_*` views, `SHOW ... TERSE / STARTS WITH / LIMIT`, `ALTER ... SET TAG`, materialization `WHERE` filters, `SUSPEND` / `RESUME MATERIALIZATION`, background refreshes, and privileges.
- Different: `CREATE OR ALTER` behaves like `CREATE OR REPLACE`; `MAX_STALENESS` is in seconds; expressions may reference physical columns of other logical tables directly.
- Extensions beyond Snowflake, modeled on dbt MetricFlow: metric `FILTER`, `OFFSET`, and `CUMULATIVE` clauses, `TIME` and `metric_time`, the query-time `time_shift()` and `cumulative()` functions, and `AGG(<metric>) FILTER (WHERE ...)`. A Snowflake view ported here runs, but a definition using these extensions will not run on Snowflake.
