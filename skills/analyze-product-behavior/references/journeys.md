# `JOURNEYS`

Source: [Altertable documentation](https://altertable.ai/docs/lakehouse/features/journeys)

`JOURNEYS` discovers observed paths over an identity partition. Use it when you need the routes from a start event to an end event, the sequences after a start, or the sequences before an end — including users who never convert.

Run these statements through Altertable's SQL engine.

## First example

Suppose an event table contains one row for each user action:

```sql
WITH events(user_id, ts, event_id, event) AS (
    VALUES
        (1, TIMESTAMP '2024-01-01 10:00:00', 1, 'Homepage'),
        (1, TIMESTAMP '2024-01-01 10:01:00', 2, 'Signup'),
        (1, TIMESTAMP '2024-01-01 10:02:00', 3, 'Docs'),
        (1, TIMESTAMP '2024-01-01 10:03:00', 4, 'Checkout'),
        (1, TIMESTAMP '2024-01-01 10:04:00', 5, 'Purchase'),
        (2, TIMESTAMP '2024-01-01 10:00:00', 1, 'Signup'),
        (2, TIMESTAMP '2024-01-01 10:01:00', 2, 'Docs'),
        (2, TIMESTAMP '2024-01-01 10:02:00', 3, 'Checkout'),
        (2, TIMESTAMP '2024-01-01 10:03:00', 4, 'Purchase'),
        (3, TIMESTAMP '2024-01-01 10:00:00', 1, 'Pricing'),
        (3, TIMESTAMP '2024-01-01 10:01:00', 2, 'Signup'),
        (3, TIMESTAMP '2024-01-01 10:02:00', 3, 'Create project'),
        (3, TIMESTAMP '2024-01-01 10:03:00', 4, 'Purchase'),
        (4, TIMESTAMP '2024-01-01 10:00:00', 1, 'Docs'),
        (4, TIMESTAMP '2024-01-01 10:01:00', 2, 'Signup'),
        (4, TIMESTAMP '2024-01-01 10:02:00', 3, 'Docs'),
        (4, TIMESTAMP '2024-01-01 10:03:00', 4, 'Docs')
)
SELECT
    path,
    converted,
    truncated,
    count AS journey_count,
    avg_duration
FROM events
JOURNEYS (
    PARTITION BY user_id
    ORDER BY ts, event_id
    STEP event
    PATHS BETWEEN (event = 'Signup') AND (event = 'Purchase')
    MEASURED AS UNIQUES
    WITHIN INTERVAL 1 DAY
    MAX STEPS 9
    COLLAPSE REPEATS
)
ORDER BY journey_count DESC, path;
```

The query starts at each user's first signup and follows events to the earliest purchase within one day. Events before signup are excluded. User 4 signed up and never purchased, so that path stays in the result as an incomplete journey. Consecutive documentation visits collapse into one step.

```text
path                                  converted  truncated  journey_count
[Signup, Docs, Checkout, Purchase]    true       false      2
[Signup, Create project, Purchase]    true       false      1
[Signup, Docs]                        false      false      1
```

- `PARTITION BY user_id` creates an independent sequence for each user.
- `ORDER BY ts, event_id` defines event order, with `event_id` breaking timestamp ties.
- `STEP event` is the value stored in each path position.
- `PATHS BETWEEN` keeps events from signup through purchase, or through the end of the window when purchase is missing.
- `MEASURED AS UNIQUES` counts one path per user.
- `COLLAPSE REPEATS` merges consecutive identical steps.

## Operator syntax

The supported `FROM`-clause shape is:

```sql
FROM input_relation [input_alias]
JOURNEYS (
    PARTITION BY identity_column [, ...]
    ORDER BY time_column [, tie_breaker_column ...]
    STEP expression
    [EXPAND BY property WHEN (predicate)]
    PATHS STARTING WITH (predicate)
      | PATHS ENDING WITH (predicate)
      | PATHS BETWEEN (start_predicate) AND (end_predicate)
    [MEASURED AS UNIQUES | EVENT TOTALS]
    [WITHIN interval_expression | WITHIN SESSION session_column]
    [MAX STEPS n]
    [COLLAPSE REPEATS]
    [EXCLUDE WHEN (predicate)]...
    [REQUIRE (predicate)]...
)
[journeys_alias]
```

`PARTITION BY`, `ORDER BY`, `STEP`, and one `PATHS` mode are required. `MEASURED AS` defaults to `UNIQUES`. `MAX STEPS` defaults to `9`.

The source relation must appear immediately before `JOURNEYS`. The result can be aliased after the clause:

```sql
SELECT j.path, j.count
FROM events AS e
JOURNEYS (
    PARTITION BY user_id
    ORDER BY ts, event_id
    STEP event
    PATHS STARTING WITH (event = 'Signup')
) AS j;
```

Common SQL constructs such as CTEs, subqueries, joins, outer filters, grouping, and aliases can surround the operator.

## Choose a path mode

### `PATHS BETWEEN`

Start at a start event and scan forward for an end event. This is the signup-to-purchase shape:

```sql
PATHS BETWEEN (event = 'Signup') AND (event = 'Purchase')
```

`converted` is `true` when an end event occurs inside the window, and `false` when the path drops off. `JOURNEYS` uses the first start event. It does not skip that start to pick a later start that would convert.

With `UNIQUES`, the first start is the only start. With `EVENT TOTALS`, each unused start begins a new instance. After a conversion, the next instance resumes after the end event. After a drop-off, it resumes after the start event.

### `PATHS STARTING WITH`

Start at a start event and keep the following visible steps. `converted` is `NULL` because there is no end condition:

```sql
PATHS STARTING WITH (event = 'Signup')
```

`UNIQUES` uses the first start. `EVENT TOTALS` starts a path at every start event. Those paths may overlap in the source rows.

### `PATHS ENDING WITH`

End at an end event and look backward for the visible steps that precede it. `converted` is `NULL`:

```sql
PATHS ENDING WITH (event = 'Purchase')
```

`UNIQUES` uses the last end event. `EVENT TOTALS` ends a path at every end event, looking backward within the window.

## Count uniques or every occurrence

`MEASURED AS UNIQUES` emits one instance per identity. `MEASURED AS EVENT TOTALS` emits every selected start or end:

```sql
MEASURED AS UNIQUES
MEASURED AS EVENT TOTALS
```

Use `UNIQUES` when you want one path per user. Use `EVENT TOTALS` when the same user can start or complete the journey more than once and each attempt should count.

## Result columns

`JOURNEYS` aggregates identical paths. The output does not keep one row per user.

| Column                                           | Description                                                                                                                             |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `path`                                           | `LIST` of steps, or `LIST<STRUCT(event, property)>` after `EXPAND BY`. Retained visible steps after exclusion, collapse, and truncation |
| `converted`                                      | `BOOLEAN`. `true` or `false` for `PATHS BETWEEN`; `NULL` for starting-only and ending-only modes                                        |
| `truncated`                                      | `BOOLEAN`. `true` when the visible path exceeded `MAX STEPS`                                                                            |
| `count`                                          | `BIGINT`. Identities for `UNIQUES`, or selected occurrences for `EVENT TOTALS`                                                          |
| `min_duration` / `avg_duration` / `max_duration` | `INTERVAL`. Duration of the raw span from the first row to the last row, including excluded events                                      |

Duration is `timestamp(end_row) - timestamp(start_row)` of that raw span. A drop-off uses the last row still inside the window.

## Define the event streams

### `PARTITION BY`

`PARTITION BY` is required. It splits the input into independent identities:

```sql
PARTITION BY user_id
PARTITION BY user_id, app_id
```

A path never crosses a partition boundary. Partition expressions must be input columns.

### `ORDER BY`

`ORDER BY` is required. The first column is the time key:

```sql
ORDER BY ts, event_id
```

It must be an ascending input column with a `DATE`, `TIMESTAMP`, or `TIMESTAMPTZ` type. Additional columns are tie-breakers. Add a stable tie-breaker when multiple events can share a timestamp.

### `STEP`

`STEP` is the value stored in each path position. It can be any scalar expression over the input row:

```sql
STEP event
STEP concat(event, ':', page)
```

A null step is omitted from the visible path. The row can still sit in the raw time span when other predicates match the original row.

### `EXPAND BY`

`EXPAND BY` splits a step by a property when a predicate is true:

```sql
STEP event
EXPAND BY plan WHEN (event = 'Checkout')
```

Matching events become `STRUCT(event, property)`. Non-matching events keep a null `property`. Different property values are different steps, so Checkout on `pro` and Checkout on `free` are distinct paths. A null `WHEN` predicate is false. A true predicate with a null property still emits a visible expanded step.

Anchor, exclusion, and requirement predicates evaluate against the original input row, not the expanded struct.

## Bound a path

### `WITHIN`

`WITHIN` requires the path to finish inside a clock window:

```sql
WITHIN INTERVAL 1 DAY
```

The interval is inclusive: an end event at exactly `start_time + interval` still converts. One unit later does not. The expression must be a non-null, strictly positive, foldable DuckDB `INTERVAL`.

Without `WITHIN` or `WITHIN SESSION`, a BETWEEN drop-off runs to the end of the partition.

### `WITHIN SESSION`

`WITHIN SESSION` keeps the path inside one session value instead of a clock window:

```sql
WITHIN SESSION session_id
```

The start and end must share the same session column value. A null session value is a session break. You cannot combine `WITHIN` and `WITHIN SESSION`.

Assign session IDs first with `SESSIONIZE` when the source table does not already have them.

### `MAX STEPS`

`MAX STEPS` limits the retained visible path. The default is `9`:

```sql
MAX STEPS 9
```

Paths of 9 visible steps or fewer are untruncated. Longer paths keep the first 9 steps and set `truncated = true`. Conversion and duration still use the full raw span.

### `COLLAPSE REPEATS`

`COLLAPSE REPEATS` merges consecutive identical visible steps after expansion and exclusion:

```sql
COLLAPSE REPEATS
```

Repeated documentation visits become one `Docs` step. After `EXPAND BY`, the same event with different property values does not collapse.

## Filter events on a path

### `EXCLUDE WHEN`

`EXCLUDE WHEN` hides matching rows from the visible path. They remain in the raw time span and still consume window time:

```sql
EXCLUDE WHEN (event = 'Heartbeat')
```

An excluded start or end still bounds the span. You can repeat the clause.

### `REQUIRE`

`REQUIRE` keeps a candidate only when every required predicate appears in the raw span:

```sql
REQUIRE (event = 'Checkout')
```

If a requirement is missing:

- `PATHS BETWEEN` with `UNIQUES` emits a drop-off.
- `PATHS BETWEEN` with `EVENT TOTALS` skips that start and resumes after it.
- Starting-only and ending-only modes skip the candidate.

You can repeat the clause.

## Practical patterns

### Split Checkout by plan

Use `EXPAND BY` when the same event should become different steps for different property values:

```sql
SELECT path, converted, count
FROM events
JOURNEYS (
    PARTITION BY user_id
    ORDER BY ts, event_id
    STEP event
    EXPAND BY plan WHEN (event = 'Checkout')
    PATHS BETWEEN (event = 'Signup') AND (event = 'Purchase')
    MEASURED AS EVENT TOTALS
    WITHIN INTERVAL 1 DAY
    COLLAPSE REPEATS
)
ORDER BY count DESC, path;
```

### Paths after every start

`EVENT TOTALS` counts every start event, including overlapping attempts by the same user:

```sql
SELECT path, count
FROM events
JOURNEYS (
    PARTITION BY user_id
    ORDER BY ts, event_id
    STEP event
    PATHS STARTING WITH (event = 'Signup')
    MEASURED AS EVENT TOTALS
    WITHIN INTERVAL 1 DAY
    MAX STEPS 9
)
ORDER BY count DESC, path;
```
