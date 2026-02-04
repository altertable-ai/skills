# Query Patterns Reference

Common SQL patterns for data analysis in the Lakehouse.

## Time Series Analysis

### Daily Metrics

```sql
SELECT
  date_trunc('day', timestamp) as day,
  COUNT(*) as events,
  COUNT(DISTINCT user_id) as unique_users
FROM events
WHERE timestamp >= current_date - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1
```

### Weekly Aggregation

```sql
SELECT
  date_trunc('week', timestamp) as week_start,
  SUM(amount) as weekly_revenue
FROM orders
GROUP BY 1
ORDER BY 1
```

### Month-over-Month Comparison

```sql
WITH monthly AS (
  SELECT
    date_trunc('month', timestamp) as month,
    COUNT(*) as events
  FROM events
  GROUP BY 1
)
SELECT
  month,
  events,
  LAG(events) OVER (ORDER BY month) as prev_month,
  events - LAG(events) OVER (ORDER BY month) as change,
  ROUND((events - LAG(events) OVER (ORDER BY month))::FLOAT /
        NULLIF(LAG(events) OVER (ORDER BY month), 0) * 100, 2) as pct_change
FROM monthly
ORDER BY month
```

### Moving Averages

```sql
SELECT
  date,
  value,
  AVG(value) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) as moving_avg_7d
FROM daily_metrics
```

## Cohort Analysis

### User Cohorts by First Activity

```sql
WITH user_first_activity AS (
  SELECT
    user_id,
    date_trunc('month', MIN(timestamp)) as cohort_month
  FROM events
  GROUP BY user_id
),
user_activity AS (
  SELECT
    e.user_id,
    ufa.cohort_month,
    date_trunc('month', e.timestamp) as activity_month,
    date_diff('month', ufa.cohort_month, date_trunc('month', e.timestamp)) as months_since_cohort
  FROM events e
  JOIN user_first_activity ufa ON e.user_id = ufa.user_id
)
SELECT
  cohort_month,
  months_since_cohort,
  COUNT(DISTINCT user_id) as active_users
FROM user_activity
GROUP BY 1, 2
ORDER BY 1, 2
```

### Retention Rate

```sql
WITH cohort_sizes AS (
  SELECT
    date_trunc('month', MIN(timestamp)) as cohort_month,
    COUNT(DISTINCT user_id) as cohort_size
  FROM events
  GROUP BY user_id
),
monthly_retention AS (
  -- ... cohort analysis query from above
)
SELECT
  m.cohort_month,
  m.months_since_cohort,
  m.active_users,
  c.cohort_size,
  ROUND(m.active_users::FLOAT / c.cohort_size * 100, 2) as retention_rate
FROM monthly_retention m
JOIN cohort_sizes c ON m.cohort_month = c.cohort_month
```

## Funnel Analysis

### Basic Funnel

```sql
SELECT
  COUNT(DISTINCT CASE WHEN event ='page_view' THEN user_id END) as step1_pageview,
  COUNT(DISTINCT CASE WHEN event ='signup_start' THEN user_id END) as step2_signup,
  COUNT(DISTINCT CASE WHEN event ='signup_complete' THEN user_id END) as step3_complete,
  COUNT(DISTINCT CASE WHEN event ='first_purchase' THEN user_id END) as step4_purchase
FROM events
WHERE timestamp >= current_date - INTERVAL '30 days'
```

### Ordered Funnel (Strict Sequence)

```sql
WITH user_events AS (
  SELECT
    user_id,
    event,
    timestamp,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as event_order
  FROM events
  WHERE event IN ('page_view', 'add_to_cart', 'checkout', 'purchase')
    AND timestamp >= current_date - INTERVAL '30 days'
),
funnel_progress AS (
  SELECT
    user_id,
    MAX(CASE WHEN event ='page_view' THEN event_order END) as step1_order,
    MAX(CASE WHEN event ='add_to_cart' THEN event_order END) as step2_order,
    MAX(CASE WHEN event ='checkout' THEN event_order END) as step3_order,
    MAX(CASE WHEN event ='purchase' THEN event_order END) as step4_order
  FROM user_events
  GROUP BY user_id
)
SELECT
  COUNT(DISTINCT user_id) as total_users,
  COUNT(DISTINCT CASE WHEN step1_order IS NOT NULL THEN user_id END) as step1,
  COUNT(DISTINCT CASE WHEN step2_order > step1_order THEN user_id END) as step2,
  COUNT(DISTINCT CASE WHEN step3_order > step2_order AND step2_order > step1_order THEN user_id END) as step3,
  COUNT(DISTINCT CASE WHEN step4_order > step3_order AND step3_order > step2_order THEN user_id END) as step4
FROM funnel_progress
```

## Segmentation

### User Segmentation by Activity

```sql
WITH user_activity AS (
  SELECT
    user_id,
    COUNT(*) as total_events,
    COUNT(DISTINCT date_trunc('day', timestamp)) as active_days,
    MAX(timestamp) as last_activity
  FROM events
  WHERE timestamp >= current_date - INTERVAL '90 days'
  GROUP BY user_id
)
SELECT
  CASE
    WHEN active_days >= 30 THEN 'Power User'
    WHEN active_days >= 7 THEN 'Regular User'
    WHEN active_days >= 1 THEN 'Casual User'
    ELSE 'Inactive'
  END as segment,
  COUNT(*) as users,
  AVG(total_events) as avg_events,
  AVG(active_days) as avg_active_days
FROM user_activity
GROUP BY 1
ORDER BY 2 DESC
```

### RFM Segmentation

```sql
WITH rfm AS (
  SELECT
    user_id,
    date_diff('day', MAX(timestamp), current_date) as recency,
    COUNT(*) as frequency,
    SUM(amount) as monetary
  FROM orders
  WHERE timestamp >= current_date - INTERVAL '365 days'
  GROUP BY user_id
),
rfm_scores AS (
  SELECT
    user_id,
    NTILE(5) OVER (ORDER BY recency DESC) as r_score,  -- Lower recency = better
    NTILE(5) OVER (ORDER BY frequency) as f_score,
    NTILE(5) OVER (ORDER BY monetary) as m_score
  FROM rfm
)
SELECT
  r_score || f_score || m_score as rfm_segment,
  COUNT(*) as users
FROM rfm_scores
GROUP BY 1
ORDER BY 1
```

## Attribution Analysis

### First Touch Attribution

```sql
WITH first_touch AS (
  SELECT
    user_id,
    properties->>'utm_source' as source,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp) as rn
  FROM events
  WHERE properties->>'utm_source' IS NOT NULL
)
SELECT
  source,
  COUNT(DISTINCT user_id) as users
FROM first_touch
WHERE rn = 1
GROUP BY 1
ORDER BY 2 DESC
```

### Last Touch Attribution

```sql
WITH last_touch AS (
  SELECT
    user_id,
    properties->>'utm_source' as source,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) as rn
  FROM events
  WHERE properties->>'utm_source' IS NOT NULL
)
SELECT
  source,
  COUNT(DISTINCT user_id) as users
FROM last_touch
WHERE rn = 1
GROUP BY 1
ORDER BY 2 DESC
```

## Data Quality Checks

### Null Value Analysis

```sql
SELECT
  'column_name' as column,
  COUNT(*) as total_rows,
  COUNT(column_name) as non_null,
  COUNT(*) - COUNT(column_name) as null_count,
  ROUND((COUNT(*) - COUNT(column_name))::FLOAT / COUNT(*) * 100, 2) as null_pct
FROM table_name
```

### Duplicate Detection

```sql
SELECT
  column1, column2,
  COUNT(*) as occurrences
FROM table_name
GROUP BY 1, 2
HAVING COUNT(*) > 1
ORDER BY 3 DESC
```

### Value Distribution

```sql
SELECT
  column_name,
  COUNT(*) as count,
  ROUND(COUNT(*)::FLOAT / SUM(COUNT(*)) OVER () * 100, 2) as pct
FROM table_name
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20
```

## Performance Patterns

### Sampling for Exploration

```sql
-- Random sample (approximately 1%)
SELECT * FROM large_table
USING SAMPLE 1%

-- Fixed size sample
SELECT * FROM large_table
USING SAMPLE 10000 ROWS
```

### Avoiding Full Scans

```sql
-- Add LIMIT for exploration
SELECT * FROM events LIMIT 100

-- Use date filters first
SELECT * FROM events
WHERE timestamp >= current_date - INTERVAL '7 days'
  AND event ='purchase'
```

### Efficient Joins

```sql
-- Filter before joining
WITH filtered_events AS (
  SELECT * FROM events
  WHERE timestamp >= current_date - INTERVAL '30 days'
)
SELECT e.*, u.name
FROM filtered_events e
JOIN users u ON e.user_id = u.id
```
