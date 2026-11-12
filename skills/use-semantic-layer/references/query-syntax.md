# Semantic Query Syntax

Source: [`semantic_layer` README](https://github.com/altertable-ai/duckdb-semantic_layer#querying)

Read this when a semantic query needs window functions, row-level facts, unusual name resolution, or a transform outside the common patterns in `SKILL.md`. Examples use `memory.main.sales`; replace the view, members, and time column with those returned by discovery.

## `SEMANTIC_VIEW(...)`

```sql
SELECT ... FROM SEMANTIC_VIEW(
  <semantic view>
  [ DIMENSIONS <expression> [ [ AS ] <alias> ] [, ...] ]
  [ METRICS <expression> [ [ AS ] <alias> ] [, ...] ]
  [ FACTS <expression> [ [ AS ] <alias> ] [, ...] ]
  [ WHERE <condition> ]
) [ AS <alias> ]
```

- Output has one column per requested item, in clause order, named after the member or its alias.
- `DIMENSIONS` items are expressions over dimensions and facts.
- `METRICS` items are metrics, expressions over metrics, ad-hoc aggregates over dimensions or facts, `AGG(<metric>) FILTER (WHERE ...)`, and the transforms below.
- `<table>.*` selects every public member of that kind on a logical table.
- `FACTS` returns row-level values, grouped by `DIMENSIONS` when both are given. `FACTS` and `METRICS` cannot be combined.
- `WHERE` runs before aggregation and may reference dimensions, facts, and uncorrelated subqueries, never metrics.
- The clause can be joined, filtered, ordered, and used in CTEs, `CREATE TABLE AS`, `INSERT ... SELECT`, views, `EXPLAIN`, and prepared statements.
- Alias any select item that contains a `SEMANTIC_VIEW(...)` subquery; otherwise it is named after its internal form.

## Query by Name

```sql
SELECT customers.segment, AGG(orders.revenue), AGG(orders.avg_order) * 2 AS double_avg
FROM memory.main.sales
WHERE orders.order_year >= 2025
GROUP BY customers.segment
HAVING AGG(orders.revenue) > 1000
ORDER BY 2 DESC
```

- `GROUP BY` expressions become dimensions. Without aggregation, the select list is evaluated as facts, row by row.
- `AGG(...)` takes exactly one metric or expression over metrics and ad-hoc aggregates (`AGG(orders.revenue + 1)`), without `DISTINCT` or `ORDER BY`. Other aggregate functions over dimensions or facts are ad-hoc metrics.
- `WHERE` cannot contain metrics or aggregates. `HAVING` filters after aggregation; without `GROUP BY` it aggregates the whole view into one row.
- Names can be bare, qualified (`customers.segment`, `sales.segment`, `memory.main.sales.segment`), or quoted as BI tools write them (`"customers.segment"`). Every spelling of a name is the same group.
- `WHERE` and later select items can read select aliases (`SELECT AGG(m) AS r, r * 2`). A view member takes precedence over an alias; lambda parameters take precedence over both.
- The form works in subqueries, CTEs, `CREATE TABLE AS`, `INSERT`, `COPY`, `PIVOT`, `SET VARIABLE`, table macros, and inside the `WHERE` of `SEMANTIC_VIEW(...)`.
- Subqueries can read the view's columns, qualified by its name or alias, in the select list, `HAVING`, `QUALIFY`, and `ORDER BY`. In an aggregated query those columns must be grouped. They cannot appear in `WHERE` or `GROUP BY`.
- `USING SAMPLE` is supported only in row-level queries without `WHERE`.
- Not supported: joins with the view, `SELECT *`, `TABLESAMPLE`, column alias lists (`FROM sales AS s(a, b)`), `AT (...)`, `ROLLUP`, `CUBE`, and `GROUPING SETS`. `GROUPING(...)` is always 0. A DuckDB view cannot be defined over this form; use `SEMANTIC_VIEW(...)` instead.
- Semantic queries cannot reference columns of an outer query.

## Window Functions and `QUALIFY`

In an aggregated by-name query, windows read the finished groups and their metrics. `HAVING` filters groups before windows run and `QUALIFY` filters after:

```sql
SELECT customers.segment, date_trunc('year', orders.created_at) AS year,
       AGG(orders.revenue) / SUM(AGG(orders.revenue)) OVER (PARTITION BY year) AS share,
       RANK() OVER (PARTITION BY EXCLUDING customers.segment ORDER BY AGG(orders.revenue) DESC) AS rnk
FROM memory.main.sales
GROUP BY ALL
QUALIFY rnk <= 3
```

- `PARTITION BY EXCLUDING d` partitions by every group except `d`.
- `AGG(...)` and the transforms are not window functions: write `SUM(AGG(m)) OVER (...)`, not `AGG(m) OVER (...)`.
- Without aggregation, windows run over fact rows at the grain of the finest table among every fact the query reads, including those in `WHERE`, `ORDER BY`, `QUALIFY`, and window keys. Reading a finer fact therefore changes the row count: `SELECT customers.segment FROM sales` returns one row per customer, while adding `WHERE orders.amount > 0` returns one row per order.

## Query-Time Transforms

```sql
time_shift(<metric>, <interval> [, dimension := <dimension>])
cumulative(<metric> [, trailing_window := <interval> | to_date := '<date part>']
                    [, period := 'first' | 'last' | 'average'] [, dimension := <dimension>])
```

| Call | Equivalent definition clause |
| --- | --- |
| `time_shift(m, INTERVAL 1 YEAR)` | `OFFSET (metric_time.day BY INTERVAL 1 YEAR)` |
| `time_shift(m, INTERVAL 1 MONTH, dimension := invoices.invoice_date)` | `OFFSET (invoices.invoice_date BY INTERVAL 1 MONTH)` |
| `cumulative(m)` | `CUMULATIVE (metric_time.day)`, a running total |
| `cumulative(m, trailing_window := INTERVAL 7 DAYS)` | `CUMULATIVE (metric_time.day OVER INTERVAL 7 DAYS)` |
| `cumulative(m, to_date := 'month')` | `CUMULATIVE (metric_time.day TO MONTH)` |
| `cumulative(m, to_date := 'year', period := 'first')` | `CUMULATIVE (metric_time.day TO YEAR FIRST)` |
| `cumulative(m, period := 'average')` | `CUMULATIVE (metric_time.day AVERAGE)` |

- `dimension` defaults to `metric_time.day` only when the view declares `TIME`. Otherwise pass it. It must be a dimension defined as a plain column of its table; the error lists the valid ones.
- `trailing_window` and `to_date` are mutually exclusive. `trailing_window` is a positive interval, or a positive number for a numeric column. `period` defaults to `'last'`; `'average'` requires a metric computed from a single aggregate.
- In `SEMANTIC_VIEW(...)`, transforms go in `METRICS`. By name, they go in the select list, `HAVING`, `QUALIFY`, and `ORDER BY`, with metrics inside wrapped in `AGG(...)`: `time_shift(AGG(orders.revenue), INTERVAL 1 YEAR, dimension := orders.created_at)`.
- They are rejected in `DIMENSIONS`, `FACTS`, `WHERE`, inside an aggregate argument (including `AGG(time_shift(...))`), and in view definitions.
- `time_shift(cumulative(...))` is allowed. `cumulative()` cannot wrap another transform or a metric that uses `OFFSET`, `CUMULATIVE`, or `NON ADDITIVE BY`.
- A window function can wrap a transform; a transform's metric argument cannot contain a window function.
- `FILTER`, `DISTINCT`, and `ORDER BY` go on the aggregate inside the call, never on the call itself.
- Only unqualified calls are transforms. Calling either function outside a semantic query fails.
- Transforms are never materialized. Plain metrics in the same query can still read materializations.

### Offset Semantics

- For a group dated *t*, the shifted metric reads rows dated *t − interval*. A negative interval looks forward.
- Every dimension computed from the shifted column moves with it, so the offset works at any grain. A `WHERE` on that column selects the reported periods; the shifted metric still reads the earlier rows.
- The query needs a dimension or `WHERE` condition computed from the shifted column. It cannot read other columns of a separate date table in the same query, because those stored values do not move.
- A `DATE` moves by whole days. Nested offsets apply innermost first, so a month-end shifted twice by one month can differ from one shift by two months.
- The metric's own aggregates and filters read stored, unshifted values.

### Cumulative Semantics

- For an anchor date *t*, the window holds rows dated up to *t*: all of them, those within the trailing interval (*t − interval < date ≤ t*), or those since the start of *t*'s `to_date` period.
- Anchors are the dimension's dates that have rows in their window, up to the latest date of the metric's rows after other `WHERE` conditions. A `WHERE` on the time column selects anchors whose windows can still read earlier rows.
- At a coarser grain, or without a time dimension, the reported value is the one at each group's last anchor (`'last'`), first anchor (`'first'`), or the average over anchors (`'average'`). MetricFlow's `period_agg` defaults to `first`.
- `SUM`, `COUNT`, `AVG`, `MIN`, `MAX`, and `DISTINCT` aggregates are pre-aggregated by date. Other aggregates, such as `MEDIAN`, read every row once per anchor in its window.
- A filtered metric keeps its anchors and reports 0 or NULL where its window only holds filtered-out rows.

## Query-Time Metric Filters

`AGG(<metric>) FILTER (WHERE <condition>)` works in both forms and composes with transforms:

```sql
SELECT * FROM SEMANTIC_VIEW(memory.main.finance
  DIMENSIONS date_trunc('month', invoices.invoiced_at) AS month
  METRICS margin, AGG(margin) FILTER (WHERE accounts.segment = 'enterprise') AS enterprise_margin)
```

- The condition is combined with `AND` into every aggregate the metric is built from, together with nested metrics' own filters.
- It reads dimensions, facts, and columns reachable from each aggregate's table, never aggregates, metrics, or windows. It reads stored values, not values moved by an offset.
- Groups are kept: a filtered metric is 0 or NULL where nothing matches.
- Semi-additive metrics are the exception: the condition filters their rows before the last snapshot is picked, like `WHERE`, so a group without matching rows disappears unless another metric produces it.
- Ad-hoc aggregates keep their own `FILTER`: `SUM(orders.amount) FILTER (WHERE ...)`.

## Generated SQL

```sql
SELECT sql FROM semantic_view_sql('SELECT * FROM SEMANTIC_VIEW(memory.main.sales DIMENSIONS customers.segment METRICS orders.revenue)')
```

The expansion shows each aggregation block (one per home table), the joins it follows, bridge subqueries, and any materialization tables it reads. `SET semantic_view_materializations = false` forces reads from the sources.
