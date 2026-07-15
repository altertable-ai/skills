# Query Optimization Reference

Tips for writing efficient queries in the DuckDB Lakehouse.

## Query Execution Basics

### Understanding Explain Plans

Always analyze complex queries before execution:

```sql
EXPLAIN ANALYZE
SELECT ...
```

Look for:
- **Scan operators**: How much data is being read
- **Join algorithms**: Hash joins are usually efficient
- **Sort operators**: Can be expensive for large datasets
- **Aggregate operators**: Check if pushed down

## Filtering Strategies

### Filter Early

Apply filters as early as possible in the query:

```sql
-- Good: Filter before aggregation
SELECT user_id, COUNT(*)
FROM events
WHERE timestamp >= current_date - INTERVAL '7 days'  -- Filter first
GROUP BY user_id

-- Bad: Filter after aggregation
SELECT user_id, cnt
FROM (
  SELECT user_id, COUNT(*) as cnt
  FROM events
  GROUP BY user_id
)
WHERE cnt > 10  -- Filtering after processing all data
```

### Use Partition Pruning

If tables are partitioned by date, always include date filters:

```sql
-- Enables partition pruning
SELECT * FROM events
WHERE timestamp >= '2024-01-01'
  AND timestamp < '2024-02-01'
```

### Avoid Functions on Filtered Columns

```sql
-- Bad: Function prevents index use
SELECT * FROM events
WHERE YEAR(timestamp) = 2024

-- Good: Range comparison
SELECT * FROM events
WHERE timestamp >= '2024-01-01'
  AND timestamp < '2025-01-01'
```

## Join Optimization

### Join Order Matters

Put smaller tables first (or let the optimizer choose):

```sql
-- Let optimizer choose join order
SELECT *
FROM small_table s
JOIN large_table l ON s.id = l.small_id
```

### Reduce Data Before Joining

```sql
-- Good: Aggregate before joining
WITH daily_events AS (
  SELECT user_id, date_trunc('day', timestamp) as day, COUNT(*) as events
  FROM events
  WHERE timestamp >= current_date - INTERVAL '30 days'
  GROUP BY 1, 2
)
SELECT u.name, d.*
FROM daily_events d
JOIN users u ON d.user_id = u.id

-- Bad: Join then aggregate
SELECT u.name, date_trunc('day', e.timestamp) as day, COUNT(*)
FROM events e
JOIN users u ON e.user_id = u.id
WHERE e.timestamp >= current_date - INTERVAL '30 days'
GROUP BY 1, 2
```

### Avoid Cross Joins

```sql
-- Bad: Implicit cross join
SELECT * FROM table1, table2 WHERE table1.id = table2.fk_id

-- Good: Explicit join
SELECT * FROM table1
JOIN table2 ON table1.id = table2.fk_id
```

## Aggregation Optimization

### Use Approximate Functions

For large datasets where exact counts aren't needed:

```sql
-- Fast approximate unique count
SELECT APPROX_COUNT_DISTINCT(user_id) as approx_users
FROM events

-- Exact (slower)
SELECT COUNT(DISTINCT user_id) as exact_users
FROM events
```

### Pre-aggregate in CTEs

```sql
WITH daily_summary AS (
  SELECT
    date_trunc('day', timestamp) as day,
    user_id,
    COUNT(*) as events
  FROM events
  GROUP BY 1, 2
)
SELECT
  day,
  COUNT(DISTINCT user_id) as users,
  SUM(events) as total_events
FROM daily_summary
GROUP BY 1
```

### Avoid SELECT *

Only select columns you need:

```sql
-- Bad: Selects all columns
SELECT * FROM events

-- Good: Select only needed columns
SELECT user_id, event, timestamp FROM events
```

## Memory Management

### Use LIMIT for Exploration

```sql
-- Always limit when exploring
SELECT * FROM large_table LIMIT 100
```

### Break Up Large Queries

Instead of processing all data at once:

```sql
-- Process in chunks by date
WITH date_range AS (
  SELECT generate_series(
    '2024-01-01'::date,
    '2024-12-31'::date,
    INTERVAL '1 month'
  ) as month_start
)
SELECT
  month_start,
  (SELECT COUNT(*) FROM events
   WHERE timestamp >= month_start
     AND timestamp < month_start + INTERVAL '1 month') as events
FROM date_range
```

### Use Sampling for Development

```sql
-- Develop queries on sample, then run on full data
SELECT * FROM large_table
USING SAMPLE 1%
```

## Common Anti-Patterns

### Avoid DISTINCT When Not Needed

```sql
-- Bad: Unnecessary DISTINCT
SELECT DISTINCT user_id FROM users

-- Good: If user_id is already unique
SELECT user_id FROM users
```

### Avoid Correlated Subqueries

```sql
-- Bad: Correlated subquery (runs for each row)
SELECT
  u.user_id,
  (SELECT COUNT(*) FROM events e WHERE e.user_id = u.user_id) as event_count
FROM users u

-- Good: Join with aggregation
SELECT u.user_id, COALESCE(e.event_count, 0) as event_count
FROM users u
LEFT JOIN (
  SELECT user_id, COUNT(*) as event_count
  FROM events
  GROUP BY user_id
) e ON u.user_id = e.user_id
```

### Avoid OR in Join Conditions

```sql
-- Bad: OR in join
SELECT * FROM a JOIN b ON a.x = b.x OR a.y = b.y

-- Good: UNION approach
SELECT * FROM a JOIN b ON a.x = b.x
UNION
SELECT * FROM a JOIN b ON a.y = b.y
```

### Avoid Functions in GROUP BY

```sql
-- Bad: Function computed twice
SELECT
  date_trunc('day', timestamp) as day,
  COUNT(*)
FROM events
GROUP BY date_trunc('day', timestamp)

-- Good: Reference by position or alias
SELECT
  date_trunc('day', timestamp) as day,
  COUNT(*)
FROM events
GROUP BY 1
```

## DuckDB-Specific Optimizations

### Use Native Types

DuckDB is optimized for native types:

```sql
-- Good: Native date comparison
WHERE timestamp >= DATE '2024-01-01'

-- Avoid: String comparison
WHERE timestamp >= '2024-01-01'
```

### Leverage Parallel Execution

DuckDB automatically parallelizes queries. Ensure:
- Large tables are read in full (not row-by-row)
- Aggregations can be distributed

### Use QUALIFY for Window Filtering

```sql
-- Good: QUALIFY (DuckDB specific)
SELECT *
FROM events
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) = 1

-- Alternative: Subquery
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) as rn
  FROM events
) WHERE rn = 1
```

## Monitoring Query Performance

### Check Execution Time

```sql
-- DuckDB shows timing automatically
-- Look for queries taking > 10 seconds

EXPLAIN ANALYZE SELECT ...
```

### Identify Bottlenecks

Look for:
1. **Full table scans** on large tables
2. **Sort operations** on unindexed columns
3. **Memory spills** to disk
4. **Cartesian products** from bad joins
