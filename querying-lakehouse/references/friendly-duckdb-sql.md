# Friendly DuckDB SQL Reference

Idiomatic DuckDB syntax extensions beyond standard SQL. Prefer these for concise, readable queries.

Adapted from [duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills) (MIT License).

## Table of Contents

- [Compact Clauses](#compact-clauses)
- [Query Features](#query-features)
- [Expressions and Types](#expressions-and-types)
- [Joins](#joins)
- [Data Reshaping](#data-reshaping)
- [Data Modification](#data-modification)

## Compact Clauses

```sql
-- FROM-first: implicit SELECT *
FROM events WHERE user_id = 42

-- GROUP BY ALL: auto-groups by all non-aggregate columns
SELECT date_trunc('day', timestamp), COUNT(*)
FROM events
GROUP BY ALL

-- ORDER BY ALL: orders by all columns
SELECT name, age FROM users ORDER BY ALL

-- SELECT * EXCLUDE: drop columns from wildcard
SELECT * EXCLUDE (internal_id, debug_flag) FROM events

-- SELECT * REPLACE: transform a column in place
SELECT * REPLACE (lower(email) AS email) FROM users

-- UNION ALL BY NAME: combine tables with different column orders
SELECT name, age FROM table_a
UNION ALL BY NAME
SELECT age, name, extra_col FROM table_b

-- Percentage LIMIT
FROM events LIMIT 10%

-- Prefix aliases
SELECT total: COUNT(*), first_seen: MIN(timestamp)
FROM events

-- Trailing commas allowed in SELECT lists
SELECT
  name,
  age,
FROM users
```

## Query Features

```sql
-- count() without *
SELECT count() FROM events

-- Reusable aliases in WHERE / GROUP BY / HAVING
SELECT date_trunc('day', timestamp) AS day, COUNT(*) AS n
FROM events
GROUP BY day
HAVING n > 100

-- Lateral column aliases
SELECT i + 1 AS j, j + 2 AS k

-- COLUMNS(*): apply expressions across columns
SELECT MIN(COLUMNS(*)) FROM numbers
SELECT COLUMNS('user_.*') FROM events  -- regex filter
SELECT COLUMNS(* EXCLUDE timestamp) FROM events

-- FILTER clause for conditional aggregation
SELECT
  count() FILTER (WHERE status = 'active') AS active,
  count() FILTER (WHERE status = 'churned') AS churned
FROM users

-- Top-N per group
SELECT max(revenue, 3) AS top_3_revenues FROM sales  -- returns list
SELECT arg_max(product, revenue, 3) AS top_products FROM sales

-- DESCRIBE and SUMMARIZE
DESCRIBE events                -- column names and types
SUMMARIZE events               -- statistical profile

-- SET VARIABLE
SET VARIABLE cutoff = current_date - INTERVAL '30 days';
SELECT * FROM events WHERE timestamp >= getvariable('cutoff')
```

## Expressions and Types

```sql
-- Dot operator chaining
SELECT 'hello world'.upper().replace('WORLD', 'DUCKDB')
SELECT col.trim().lower() FROM raw_input

-- List comprehensions
SELECT [x * 2 FOR x IN list_col]

-- List/string slicing (1-indexed, negative indexing supported)
SELECT col[1:3], col[-1]

-- STRUCT.* notation
SELECT s.* FROM (SELECT {'a': 1, 'b': 2} AS s)

-- Square bracket list literals
SELECT [1, 2, 3] AS ids

-- format() for string building
SELECT format('{} had {} events', user_id, event_count)
```

## Joins

```sql
-- ASOF join: approximate match on ordered data (e.g., timestamps)
SELECT *
FROM trades t
ASOF JOIN quotes q
  ON t.symbol = q.symbol
  AND t.timestamp >= q.timestamp

-- POSITIONAL join: match rows by position, not keys
SELECT * FROM table_a POSITIONAL JOIN table_b

-- LATERAL join: reference prior table in subquery
SELECT *
FROM users u,
LATERAL (SELECT * FROM events e WHERE e.user_id = u.id LIMIT 5) recent
```

## Data Reshaping

```sql
-- PIVOT: long to wide
PIVOT sales ON product USING SUM(amount)

-- UNPIVOT: wide to long
UNPIVOT monthly_metrics
ON jan, feb, mar
INTO NAME month VALUE amount
```

## Data Modification

```sql
-- CREATE OR REPLACE TABLE (no DROP needed)
CREATE OR REPLACE TABLE summary AS
SELECT date_trunc('day', timestamp) AS day, count() AS n
FROM events
GROUP BY ALL

-- INSERT BY NAME: match columns by name, not position
INSERT INTO target BY NAME
SELECT col_b, col_a FROM source

-- Upsert patterns
INSERT OR REPLACE INTO users VALUES (1, 'alice', 'alice@example.com')
INSERT OR IGNORE INTO users VALUES (1, 'alice', 'alice@example.com')
```
