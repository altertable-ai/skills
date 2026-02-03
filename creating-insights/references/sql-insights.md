# SQL Insights Reference

Creating insights from custom SQL queries.

## When to Use SQL Insights

- Complex calculations not in semantic layer
- Ad-hoc analysis with specific logic
- Cross-database queries
- Custom aggregations or transformations

## Workflow

### 1. Write the Query

```sql
WITH daily_metrics AS (
  SELECT
    date_trunc('day', timestamp) as day,
    COUNT(*) as events,
    COUNT(DISTINCT user_id) as users
  FROM catalog.schema.events
  WHERE timestamp >= current_date - INTERVAL '30 days'
  GROUP BY 1
)
SELECT
  day,
  events,
  users,
  events::FLOAT / NULLIF(users, 0) as events_per_user
FROM daily_metrics
ORDER BY day
```

### 2. Validate the Query

Before creating the insight:
- Run validation to check syntax
- Execute on sample to verify results
- Check for reasonable output size

### 3. Preview the Insight

Preview shows:
- Query results
- Visualization preview
- Any warnings or issues

### 4. Create the Discovery

Provide:
- Title: Clear, actionable statement
- Description: Context and recommendations
- Connection: Which data source
- Visualization: Appropriate chart type

## Query Best Practices

### Use CTEs for Clarity

```sql
WITH
  -- Step 1: Get raw data
  raw_events AS (
    SELECT * FROM events
    WHERE timestamp >= current_date - INTERVAL '30 days'
  ),
  -- Step 2: Aggregate
  daily_summary AS (
    SELECT
      date_trunc('day', timestamp) as day,
      COUNT(*) as total
    FROM raw_events
    GROUP BY 1
  )
-- Final output
SELECT * FROM daily_summary ORDER BY day
```

### Include Time Filters

Always filter to relevant time range:

```sql
WHERE timestamp >= current_date - INTERVAL '30 days'
  AND timestamp < current_date
```

### Alias Columns for Display

```sql
SELECT
  date_trunc('day', timestamp) as "Date",
  COUNT(*) as "Total Events",
  COUNT(DISTINCT user_id) as "Unique Users"
```

### Handle NULLs

```sql
SELECT
  COALESCE(category, 'Unknown') as category,
  COUNT(*) as count
```

### Limit Results

For large datasets:

```sql
SELECT * FROM results
ORDER BY metric DESC
LIMIT 100
```

## Visualization Mapping

### Time Series Data

Use Line or Area:

```sql
SELECT
  date_trunc('day', timestamp) as day,  -- X-axis
  COUNT(*) as events                     -- Y-axis
FROM events
GROUP BY 1
ORDER BY 1
```

### Categorical Comparison

Use Bar or BarList:

```sql
SELECT
  category,           -- X-axis
  SUM(amount) as total  -- Y-axis
FROM orders
GROUP BY 1
ORDER BY 2 DESC
```

### Single Value

Use Metric:

```sql
SELECT
  COUNT(DISTINCT user_id) as "Active Users"
FROM events
WHERE timestamp >= current_date - INTERVAL '7 days'
```

### Detailed Data

Use Table:

```sql
SELECT
  order_id,
  customer_name,
  amount,
  status
FROM orders
ORDER BY created_at DESC
LIMIT 50
```

## Common Patterns

### Week-over-Week Comparison

```sql
WITH current_week AS (
  SELECT COUNT(*) as events
  FROM events
  WHERE timestamp >= date_trunc('week', current_date)
),
previous_week AS (
  SELECT COUNT(*) as events
  FROM events
  WHERE timestamp >= date_trunc('week', current_date) - INTERVAL '7 days'
    AND timestamp < date_trunc('week', current_date)
)
SELECT
  c.events as "This Week",
  p.events as "Last Week",
  ROUND((c.events - p.events)::FLOAT / NULLIF(p.events, 0) * 100, 1) as "% Change"
FROM current_week c, previous_week p
```

### Top N Analysis

```sql
SELECT
  page_path,
  COUNT(*) as views,
  COUNT(DISTINCT user_id) as visitors
FROM pageviews
WHERE timestamp >= current_date - INTERVAL '7 days'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10
```

### Cohort Retention

```sql
WITH cohorts AS (
  SELECT
    user_id,
    date_trunc('month', MIN(timestamp)) as cohort_month
  FROM events
  GROUP BY 1
)
SELECT
  c.cohort_month,
  date_diff('month', c.cohort_month, date_trunc('month', e.timestamp)) as months_since,
  COUNT(DISTINCT e.user_id) as active_users
FROM events e
JOIN cohorts c ON e.user_id = c.user_id
GROUP BY 1, 2
ORDER BY 1, 2
```

## Error Handling

### Query Too Large

If results are too large:
- Add LIMIT clause
- Narrow time range
- Increase aggregation level

### Timeout

For slow queries:
- Add date filters first
- Use approximate functions
- Simplify joins

### Invalid Syntax

- Run validation before preview
- Check column names exist
- Verify table qualification
