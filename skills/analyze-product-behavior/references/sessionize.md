# `SESSIONIZE`

Source: [Altertable documentation](https://altertable.ai/docs/lakehouse/features/sessionize)

`SESSIONIZE` assigns ordered rows to sessions separated by a period of inactivity. Use it to label events with a session ID or to calculate one result row per session without building the usual `lag`, cumulative-sum, and grouping pipeline.

Run these statements through Altertable's SQL engine.

## First example

Suppose an event table contains one row for each user action:

```sql
WITH events(user_id, ts, event) AS (
    VALUES
        (1, TIMESTAMP '2024-01-01 10:00:00', 'view'),
        (1, TIMESTAMP '2024-01-01 10:10:00', 'click'),
        (1, TIMESTAMP '2024-01-01 10:50:00', 'purchase'),
        (2, TIMESTAMP '2024-01-01 10:00:00', 'view')
)
SELECT
    user_id,
    ts,
    event,
    session_start,
    session_end,
    session_id
FROM events
SESSIONIZE (
    PARTITION BY user_id
    ORDER BY ts
    GAP INTERVAL 30 MINUTE
)
ORDER BY user_id, ts;
```

The first two events for user `1` belong to session `1` because they are 10 minutes apart. The 40-minute gap before `purchase` starts session `2`. Session IDs restart at `1` for each user.

- `PARTITION BY user_id` creates an independent event stream for each user.
- `ORDER BY ts` defines event order.
- `GAP INTERVAL 30 MINUTE` starts a new session after more than 30 minutes of inactivity.
- `session_start` and `session_end` contain the first and last time-key values in the session.
- `session_id` is a 1-based number within each partition.

## Operator syntax

The supported `FROM`-clause shape is:

```sql
FROM input_relation [input_alias]
SESSIONIZE (
    [PARTITION BY partition_column [, ...]]
    ORDER BY time_column [, tie_breaker_column ...]
    GAP interval_expression
    [MEASURES measure_expression AS output_name [, ...]]
    [ONE ROW PER SESSION]
)
[session_alias]
```

`ORDER BY` and `GAP` are required. `PARTITION BY` is optional. `MEASURES` can only be used with `ONE ROW PER SESSION`.

The source relation must appear immediately before `SESSIONIZE`. The result can be aliased after the clause:

```sql
SELECT s.user_id, s.session_id
FROM events AS e
SESSIONIZE (
    PARTITION BY user_id
    ORDER BY ts
    GAP INTERVAL 30 MINUTE
) AS s;
```

Common SQL constructs such as CTEs, subqueries, joins, outer filters, grouping, and aliases can surround the operator.

## How sessions are formed

Within each partition, `SESSIONIZE` sorts rows by the `ORDER BY` columns and compares each time-key value with the preceding value. A new session starts when:

```text
current_time > previous_time + GAP
```

Equality stays in the current session. With a 30-minute gap, events exactly 30 minutes apart belong to the same session; an event 30 minutes and one second later starts a new one.

The comparison uses consecutive events, not the session start. A session can therefore last longer than the gap as long as each event arrives within the gap after the previous event.

## Choose the output mode

### Preserve every input row

Row-preserving mode is the default. It returns the input columns in their original order, followed by `session_start`, `session_end`, and `session_id`:

```sql
SELECT *
FROM events
SESSIONIZE (
    PARTITION BY user_id
    ORDER BY ts
    GAP INTERVAL 30 MINUTE
);
```

Every row in the same session receives the same metadata. `session_start` and `session_end` are the first and last time-key values, not calculated window boundaries such as `session_end + GAP`.

Use this mode when downstream logic still needs individual events:

```sql
WITH labeled_events AS (
    SELECT *
    FROM events
    SESSIONIZE (
        PARTITION BY user_id
        ORDER BY ts, event_id
        GAP INTERVAL 30 MINUTE
    )
)
SELECT *
FROM labeled_events
WHERE session_id = 1
ORDER BY user_id, ts, event_id;
```

### Return one row per session

Add `ONE ROW PER SESSION` to emit session metadata without preserving the input rows:

```sql
SELECT *
FROM events
SESSIONIZE (
    PARTITION BY user_id
    ORDER BY ts
    GAP INTERVAL 30 MINUTE
    ONE ROW PER SESSION
)
ORDER BY user_id, session_id;
```

The output contains, in order:

1. The `PARTITION BY` columns, when present.
2. `session_start`, `session_end`, and `session_id`.
3. The explicitly declared `MEASURES`, when present.

No event count is added automatically. Add `count(*)` as a measure when you need one.

## Calculate session measures

`MEASURES` calculates values across all rows in a session. Every measure needs an `AS` alias, and the clause requires `ONE ROW PER SESSION`:

```sql
WITH events(user_id, ts, event, amount) AS (
    VALUES
        (1, TIMESTAMP '2024-01-01 10:00:00', 'view', 0),
        (1, TIMESTAMP '2024-01-01 10:10:00', 'purchase', 49),
        (1, TIMESTAMP '2024-01-01 10:50:00', 'view', 0)
)
SELECT *
FROM events
SESSIONIZE (
    PARTITION BY user_id
    ORDER BY ts
    GAP INTERVAL 30 MINUTE
    MEASURES
        count(*) AS event_count,
        sum(amount) AS revenue,
        FIRST(event) AS first_event,
        event AS last_event,
        list(event) AS events
    ONE ROW PER SESSION
)
ORDER BY user_id, session_id;
```

Measure expressions support:

- Aggregates such as `count`, `sum`, `avg`, `min`, `max`, `list`, and `count(DISTINCT ...)`.
- `FIRST(expression)` and `LAST(expression)` for values from the first and last rows.
- A bare input column, which returns its value from the last row of the session.
- `PARTITION BY` columns, which are constant throughout a session.
- Constants, scalar functions, and arithmetic composed from these values.

Measures use whole-session semantics. Pattern-only expressions from `MATCH_RECOGNIZE`, including pattern variables, `CLASSIFIER()`, `MATCH_NUMBER()`, `PREV`, `NEXT`, `RUNNING`, and `FINAL`, are not supported.

Aggregate `FILTER` clauses and aggregate-local `ORDER BY` clauses are not supported in `SESSIONIZE` measures. When you need them, preserve the sessionized rows and aggregate by the partition columns and `session_id` in an outer query.

## Define the event streams

### `PARTITION BY`

`PARTITION BY` splits the input into independent event streams:

```sql
PARTITION BY user_id, device_id
```

Sessions never cross a partition boundary. Without `PARTITION BY`, the entire input is treated as one stream.

Partition expressions must be input columns. In summary mode, partition columns appear first in the result and can be referenced directly in measures.

### `ORDER BY`

The first `ORDER BY` column is the time key:

```sql
ORDER BY ts, event_id
```

It must be an ascending input column with a `DATE`, `TIMESTAMP`, or `TIMESTAMPTZ` type. Supported timestamp precisions include seconds, milliseconds, microseconds, and nanoseconds.

Additional columns are tie-breakers. Add a stable tie-breaker when multiple events can have the same timestamp and their relative order matters.

### `GAP`

`GAP` sets the maximum inactivity period within a session:

```sql
GAP INTERVAL 30 MINUTE
```

The expression must be a non-null, strictly positive, foldable DuckDB `INTERVAL`. Dynamic per-row gaps are not supported.

## Output names and ordering

The metadata names `session_start`, `session_end`, and `session_id` are reserved. In row-preserving mode, an input column cannot use one of these names. In summary mode, partition columns and measure aliases cannot use them, and measure aliases cannot duplicate partition columns or each other.

Result order is not guaranteed. Add an outer `ORDER BY` whenever downstream behavior depends on row order:

```sql
SELECT *
FROM events
SESSIONIZE (
    PARTITION BY user_id
    ORDER BY ts, event_id
    GAP INTERVAL 30 MINUTE
)
ORDER BY user_id, session_id, ts, event_id;
```
