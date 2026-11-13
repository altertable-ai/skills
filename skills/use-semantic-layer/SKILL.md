---
name: use-semantic-layer
compatibility: Requires Altertable MCP server
description: "Discovers, queries, verifies, and creates Altertable semantic views with SEMANTIC_VIEW(...) and AGG(...), including breakdowns, metric filters, period-over-period, running totals, and fan-out-safe metrics across joined tables. Use for governed metrics and KPIs, defining reusable metrics, or Snowflake semantic view syntax."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Use the Semantic Layer

Altertable serves governed metrics as semantic views, powered by its open-source [`semantic_layer` DuckDB extension](https://github.com/altertable-ai/duckdb-semantic_layer). The syntax is Snowflake's semantic views, extended with time intelligence, metric filters, many-to-many bridges, and a query-by-name form.

A semantic query names the dimensions and metrics it wants. The extension generates the joins, aggregates each metric at its own grain, and rejects combinations that would fan out. When a governed metric answers the question, query it through its semantic view instead of rebuilding the aggregation in SQL.

Metrics are defined in **Knowledge**, by hand or imported from connected sources, and each semantic layer is served as a semantic view named `memory.main.<view_name>`.

## Discover

1. Call `list_semantic_metrics`. Match the request against each metric's name, label, description, and `ai_context`. Keep its `view_name`, its member (`<table alias>.<metric>`), and its `dimensions`.
2. Answer structural questions with read-only statements through `query_lakehouse`. Each is a table expression, so project only the needed columns:
   - `SHOW SEMANTIC METRICS IN memory.main.<view>`: metrics with their types, synonyms, and comments.
   - `SHOW SEMANTIC DIMENSIONS IN memory.main.<view> FOR METRIC <alias>.<metric>`: exactly the dimensions that metric can be grouped by. `required = true` marks dimensions a window metric needs.
   - `DESCRIBE SEMANTIC VIEW memory.main.<view>`: tables, keys, relationships, and expressions, one property per row. Filter on `object_kind`.
   - `SHOW SEMANTIC VIEWS IN SCHEMA memory.main`: every view loaded in the session.

## Query

Both forms compile to the same SQL. Always qualify the view as `memory.main.<view>`.

```sql
SELECT * FROM SEMANTIC_VIEW(
  memory.main.sales
  DIMENSIONS customers.segment, date_trunc('month', orders.created_at) AS month
  METRICS orders.revenue, orders.revenue / customers.customer_count AS revenue_per_customer
  WHERE orders.created_at >= TIMESTAMP '2026-01-01'
)
ORDER BY month, segment
```

```sql
SELECT customers.segment, AGG(orders.revenue) AS revenue
FROM memory.main.sales
WHERE orders.status = 'paid'
GROUP BY ALL
HAVING AGG(orders.revenue) > 1000
ORDER BY revenue DESC
LIMIT 10
```

- `SEMANTIC_VIEW(...)` is a table expression: join it with other tables, wrap it, or use it in CTEs. Choose it when the result feeds further SQL.
- The query-by-name form reads like `GROUP BY` SQL: `GROUP BY` items become dimensions and metrics are wrapped in `AGG(...)`. `HAVING`, window functions, and `QUALIFY` evaluate over the aggregated rows. It does not support `SELECT *`, joins with the view, or `ROLLUP`/`CUBE`/`GROUPING SETS`; produce subtotals with `UNION ALL` of separately grouped queries.
- `WHERE` filters rows before aggregation and accepts only dimensions, facts, and uncorrelated subqueries. Filter on metric values with `HAVING` or in an outer query.
- `DIMENSIONS` accepts expressions over dimensions, such as `date_trunc('month', <time member>) AS month`. `METRICS` accepts expressions over metrics, each aggregated at its own grain before they combine.
- Ad-hoc aggregates over dimensions or facts are allowed: `COUNT(DISTINCT orders.status) AS statuses`. In the query-by-name form, an ad-hoc aggregate must read a column (`COUNT(orders.id)`, not `COUNT(*)`).
- Write `AS` before every alias and alias every computed item.

### Query-Time Metric Filters

`AGG(orders.revenue) FILTER (WHERE orders.status = 'paid') AS paid_revenue` filters a metric without defining a new one. The condition is added to every aggregate the metric is built from, nested metrics included. Unlike `WHERE`, it removes no groups: a group without matching rows shows 0 or NULL beside the unfiltered metrics. The condition reads row-level values only.

### The Grain Rule

A dimension can group a metric only if it lies on the metric's table, on a table that table references (many-to-one), or across a many-to-many bridge. Otherwise the binder rejects the query:

```text
Invalid dimension specified: The dimension entity 'orders' must be related to and have an equal or
lower level of granularity compared to the base metric or dimension entity 'customers'.
```

Treat this as a semantic answer, not a syntax problem. Do not bypass it with hand-written joins, which reintroduce the fan-out the view prevents. Pick a dimension from `SHOW SEMANTIC DIMENSIONS ... FOR METRIC`, use a metric on the finer table, or explain why the breakdown is undefined.

## Time Intelligence

Query-time transforms add period comparisons and accumulations to any metric:

```sql
SELECT * FROM SEMANTIC_VIEW(
  memory.main.sales
  DIMENSIONS date_trunc('month', orders.created_at) AS month
  METRICS orders.revenue,
          time_shift(orders.revenue, INTERVAL 1 YEAR, dimension := orders.created_at) AS revenue_ly,
          orders.revenue / time_shift(orders.revenue, INTERVAL 1 YEAR, dimension := orders.created_at) - 1 AS yoy,
          cumulative(orders.revenue, to_date := 'year', dimension := orders.created_at) AS revenue_ytd
  WHERE orders.created_at >= TIMESTAMP '2026-01-01' AND orders.created_at < TIMESTAMP '2026-07-01'
)
ORDER BY month
```

- `dimension` defaults to `metric_time.day` only when the view declares `TIME`; otherwise pass a time member defined as a plain column. Group by it or by an expression of it, such as `date_trunc`, at any grain.
- A positive `time_shift` interval reads the past. Shifted metrics also produce periods after the last data, so bound the time range at both ends with `WHERE` on the same column. `WHERE` selects the periods to report, while the shifted metric still reads the earlier rows it needs.
- `cumulative` takes `to_date := 'week' | 'month' | 'quarter' | 'year'` or `trailing_window := INTERVAL '7 days'`, plus `period := 'last'` (default), `'first'`, or `'average'` for the value reported per coarser group. It computes from rows, so distinct counts stay exact and gaps do not shorten windows.
- `cumulative` anchors on every distinct value of the dimension. Over a raw timestamp of a large table, cost grows quadratically. Bound the range tightly; for an additive metric, prefer `SUM(AGG(m)) OVER (ORDER BY month)` in the query-by-name form.
- Never compare periods with `LAG`: it reads the previous existing row, so a missing period silently changes the comparison. Use `time_shift`.
- Transforms belong in `METRICS`, or in the query-by-name select list, `HAVING`, `QUALIFY`, and `ORDER BY` with metrics wrapped in `AGG(...)`. They are rejected in `WHERE`, `DIMENSIONS`, and inside `AGG(...)`. Put a filter inside the call: `time_shift(AGG(m) FILTER (WHERE ...), ...)`.

Read [query syntax](references/query-syntax.md) for window functions, `PARTITION BY EXCLUDING`, row-level `FACTS` queries, name resolution, and every transform constraint.

## Verify

- `SELECT sql FROM semantic_view_sql('<semantic query>')` returns the expanded DuckDB SQL without running it. Use it to explain how a number is computed, audit joins, or debug unexpected rows; double the single quotes inside the literal.
- State the metric's source (view and member) with the answer, so the user can tell a governed number from an ad-hoc one.

## Create a Semantic View

When no governed metric fits a business question that will come back, create a semantic view instead of leaving the logic in one-off SQL. Read [modeling](references/modeling.md) before writing the definition.

1. Inspect the source tables with `get_catalog`. Confirm every declared primary key is actually unique: a false key silently breaks fan-out protection.
2. Write `CREATE SEMANTIC VIEW` with fully qualified sources, many-to-one relationships, and one metric per business definition. Declare `TIME (<column>)` on fact tables to get `metric_time.day` / `week` / `month` / `quarter` / `year` and a default `dimension` for transforms.
3. Add a `COMMENT` and `WITH SYNONYMS` to the view and its members so later agents and users can find them.
4. Run it with `query_lakehouse` and reuse the returned `session_id`. Query the new view and compare one result with a hand-written aggregate before relying on it.

Confirm the view name and metric definitions with the user before creating it. Never replace an existing view with `CREATE OR REPLACE` unless the user asked to change it.
