---
name: querying-lakehouse
compatibility: Requires Altertable MCP server
description: Writes and executes DuckDB SQL queries against Altertable's analytical database. Use when analyzing data, building reports, aggregating metrics, exploring tables, or when the user asks about data in connections.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Querying the Lakehouse

Altertable uses the DuckDB SQL dialect. Under the hood, queries run on hosted DuckDB workers over Parquet files stored in distributed object storage.

## Quick Start

```sql
-- Discover table shape
DESCRIBE catalog.schema.table

-- Statistical profile (min, max, avg, nulls, unique counts)
SUMMARIZE catalog.schema.table

-- Basic query pattern
SELECT column1, column2
FROM catalog.schema.table
WHERE condition
LIMIT 100
```

Always qualify table names with `catalog.schema.table` format.

## When to Use This Skill

- User asks to query or analyze data
- Need to explore table contents
- Building reports or aggregations
- Validating data quality
- Joining data across tables
- User mentions SQL, query, or data analysis

## Core Workflow

### Step 1: Understand the Data

Before writing queries:

- List available connections
- Get schema details for relevant connections
- Check if semantic models already define needed metrics
- When column names are unknown, discover the table shape first:

```sql
DESCRIBE catalog.schema.table
-- or
SELECT * FROM catalog.schema.table LIMIT 1
```

### Step 2: Validate SQL Syntax

Always validate queries before execution:

- Catches syntax errors early
- Identifies missing tables or columns
- Saves time on large queries

### Step 3: Explain Complex Queries

For complex queries, use the `explain_sql` tool to get the execution plan. This tool analyzes a DuckDB SQL query and returns execution plan information including table scan estimates and file statistics. Use it to understand query performance characteristics before execution.

The tool returns:

- Table scan details (table name, estimated rows, filters applied)
- Total files and bytes in scanned tables
- Estimated files and bytes that will be scanned
- Optionally, the raw EXPLAIN plan (set `include_plan: true`)

### Step 4: Execute and Analyze

Run the query and interpret results:

- Check row counts
- Verify data types
- Look for unexpected nulls or values

### Step 5: Render as a Chart (Optional)

When the user wants the result visualized rather than just tabular, call `preview_insight` with the SQL kind. In MCP clients that support MCP Apps, this surfaces a built-in chart UI for the result instead of a raw table.

## DuckDB SQL Dialect Patterns

### Date and Time Functions

```sql
-- Current date/time
SELECT current_date, current_timestamp

-- Date arithmetic
SELECT date_add(current_date, INTERVAL 7 DAY)
SELECT current_date - INTERVAL '30 days'

-- Date truncation
SELECT date_trunc('month', timestamp_column)
SELECT date_trunc('week', timestamp_column)

-- Date parts
SELECT year(date_column), month(date_column), day(date_column)
SELECT extract(dow FROM timestamp_column)  -- day of week
```

### Aggregations

```sql
-- Basic aggregations
SELECT
  COUNT(*) as total_rows,
  COUNT(DISTINCT user_id) as unique_users,
  SUM(amount) as total_amount,
  AVG(amount) as avg_amount,
  MIN(created_at) as first_event,
  MAX(created_at) as last_event
FROM events

-- Grouped aggregations
SELECT
  date_trunc('day', timestamp) as day,
  COUNT(*) as events
FROM events
GROUP BY 1
ORDER BY 1
```

### Window Functions

```sql
-- Row numbering
SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as event_seq
FROM events

-- Running totals
SELECT
  date,
  amount,
  SUM(amount) OVER (ORDER BY date) as running_total
FROM daily_sales

-- Lag/Lead for comparisons
SELECT
  date,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY date) as prev_day_revenue,
  revenue - LAG(revenue, 1) OVER (ORDER BY date) as change
FROM daily_revenue
```

### CTEs (Common Table Expressions)

```sql
WITH daily_users AS (
  SELECT
    date_trunc('day', timestamp) as day,
    COUNT(DISTINCT user_id) as users
  FROM events
  GROUP BY 1
),
weekly_avg AS (
  SELECT AVG(users) as avg_daily_users
  FROM daily_users
)
SELECT
  d.day,
  d.users,
  w.avg_daily_users
FROM daily_users d
CROSS JOIN weekly_avg w
```

### JSON Operations

```sql
-- Extract from JSON using arrow operators
SELECT
  properties->>'page_url' as page_url,
  properties->>'referrer' as referrer,
  (properties->>'amount')::FLOAT as amount
FROM events

-- Use json_extract_string_property when properties may exist as columns or in JSON
-- Automatically uses column if it exists, falls back to JSON extraction
SELECT
  json_extract_string_property(events.properties_bucketed, '$.page_url') as page_url,
  json_extract_string_property(events.properties_bucketed, '$.referrer') as referrer
FROM events

-- Check JSON field exists
SELECT * FROM events
WHERE properties ? 'campaign'

-- JSON array operations
SELECT
  json_array_length(items) as item_count
FROM orders
```

## Query Patterns

### Time-Based Analysis

```sql
-- Last 7 days
SELECT * FROM events
WHERE timestamp >= current_date - INTERVAL '7 days'

-- Specific date range
SELECT * FROM events
WHERE timestamp BETWEEN '2024-01-01' AND '2024-01-31'

-- Compare periods
WITH current_period AS (
  SELECT COUNT(*) as events
  FROM events
  WHERE timestamp >= current_date - INTERVAL '7 days'
),
previous_period AS (
  SELECT COUNT(*) as events
  FROM events
  WHERE timestamp >= current_date - INTERVAL '14 days'
    AND timestamp < current_date - INTERVAL '7 days'
)
SELECT
  c.events as current_events,
  p.events as previous_events,
  (c.events - p.events)::FLOAT / NULLIF(p.events, 0) * 100 as pct_change
FROM current_period c, previous_period p
```

### Funnel Analysis

```sql
WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event ='page_view' THEN 1 ELSE 0 END) as step1,
    MAX(CASE WHEN event ='add_to_cart' THEN 1 ELSE 0 END) as step2,
    MAX(CASE WHEN event ='checkout' THEN 1 ELSE 0 END) as step3,
    MAX(CASE WHEN event ='purchase' THEN 1 ELSE 0 END) as step4
  FROM events
  WHERE timestamp >= current_date - INTERVAL '30 days'
  GROUP BY user_id
)
SELECT
  SUM(step1) as page_views,
  SUM(step2) as add_to_cart,
  SUM(step3) as checkout,
  SUM(step4) as purchase
FROM funnel
```

### Cohort Analysis

```sql
WITH user_cohorts AS (
  SELECT
    user_id,
    date_trunc('month', MIN(timestamp)) as cohort_month
  FROM events
  GROUP BY user_id
),
activity AS (
  SELECT
    e.user_id,
    c.cohort_month,
    date_trunc('month', e.timestamp) as activity_month
  FROM events e
  JOIN user_cohorts c ON e.user_id = c.user_id
)
SELECT
  cohort_month,
  activity_month,
  COUNT(DISTINCT user_id) as users
FROM activity
GROUP BY 1, 2
ORDER BY 1, 2
```

## Common Pitfalls

- **Missing table qualification**: Always use `catalog.schema.table`
- **PostgreSQL vs DuckDB syntax**: Use DuckDB syntax; some functions differ (e.g., `DATEADD` vs `date_add`)
- **Large result sets**: Always use `LIMIT` when exploring
- **Not validating first**: Validate SQL before executing large queries
- **Implicit type coercion**: Be explicit with casts (e.g., `::FLOAT`)
- **NULL handling**: Use `COALESCE` or `NULLIF` appropriately

## Reference Files

- [DuckDB functions](references/duckdb-functions.md)
- [Altertable DuckDB functions](references/altertable-duckdb-functions.md)
- [Friendly DuckDB SQL](references/friendly-duckdb-sql.md)
- [Query patterns](references/query-patterns.md)
- [Optimization tips](references/optimization.md)
