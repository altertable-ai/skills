# `MATCH_RECOGNIZE`

Source: [Altertable documentation](https://altertable.ai/docs/lakehouse/features/match-recognize)

`MATCH_RECOGNIZE` finds sequences of rows that match a regular-expression-like pattern. Use it for funnels, customer journeys, state transitions, sessions, anomaly shapes, and other ordered event-stream problems that are difficult to express with self-joins and window functions.

Run these statements through Altertable's SQL engine.

## First example

Suppose an event table contains one row for each user action:

```sql
WITH events(user_id, ts, event) AS (
    VALUES
        (1, TIMESTAMP '2024-01-01 10:00:00', 'view'),
        (1, TIMESTAMP '2024-01-01 10:01:00', 'click'),
        (1, TIMESTAMP '2024-01-01 10:02:00', 'view'),
        (2, TIMESTAMP '2024-01-01 10:00:00', 'view')
)
SELECT *
FROM events
MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES
        A.ts AS view_ts,
        B.ts AS click_ts
    PATTERN (A B)
    DEFINE
        A AS event = 'view',
        B AS event = 'click'
)
ORDER BY user_id, view_ts;
```

This query finds a `view` immediately followed by a `click` for each user:

- `PARTITION BY user_id` creates an independent sequence for each user.
- `ORDER BY ts` defines the order in which rows are consumed.
- `A` and `B` are pattern variables that describe row roles.
- `DEFINE` specifies which rows qualify for each role.
- `PATTERN (A B)` requires two consecutive rows: an `A` row followed by a `B` row.
- `MEASURES` defines the columns in each result row.

Matches are non-overlapping. After a match is emitted, matching resumes after the last consumed row. Rows that cannot start a complete match are skipped.

## Operator syntax

The supported `FROM`-clause shape is:

```sql
FROM input_relation [input_alias]
MATCH_RECOGNIZE (
    [PARTITION BY partition_column [, ...]]
    [ORDER BY input_column [ASC | DESC] [NULLS FIRST | NULLS LAST] [, ...]]
    [MEASURES measure_expression AS output_name [, ...]]
    [ONE ROW PER MATCH | ALL ROWS PER MATCH
        [SHOW EMPTY MATCHES | OMIT EMPTY MATCHES | WITH UNMATCHED ROWS]]
    [AFTER MATCH SKIP
        PAST LAST ROW | TO NEXT ROW | TO FIRST variable | TO LAST variable]
    PATTERN (row_pattern) [WITHIN interval_expression]
    [SUBSET subset_name = (variable [, ...]) [, ...]]
    [DEFINE pattern_variable AS boolean_expression [, ...]]
)
[match_alias]
```

`PATTERN` is required. `ORDER BY`, `MEASURES`, `PARTITION BY`, `SUBSET`, and `DEFINE` are optional, but the query must produce at least one output column.

The source relation must appear immediately before `MATCH_RECOGNIZE`. The result can be aliased after the clause:

```sql
SELECT m.user_id, m.start_ts
FROM events AS e
MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES A.ts AS start_ts
    PATTERN (A)
    DEFINE A AS event = 'view'
) AS m;
```

Common SQL constructs such as CTEs, subqueries, joins, outer filters, grouping, and aliases can surround the operator.

## Define the row sequence

### `PARTITION BY`

`PARTITION BY` splits the input into independent streams. A pattern never crosses a partition boundary:

```sql
PARTITION BY user_id, channel
```

The partition columns appear in the output before the measure columns. Without `PARTITION BY`, the entire input is treated as one partition.

### `ORDER BY`

`ORDER BY` defines the sequence that the pattern consumes:

```sql
ORDER BY ts, sequence_number
```

It supports input columns and `ASC`, `DESC`, `NULLS FIRST`, and `NULLS LAST`. If the primary ordering column can tie, add a stable secondary column so matching is deterministic.

When `ORDER BY` is omitted, rows keep their input order within each partition. Add an outer `ORDER BY` when result order matters, especially when the query uses multiple partitions or multiple threads.

### `DEFINE`

`DEFINE` maps pattern variables to Boolean predicates:

```sql
DEFINE
    A AS event = 'view',
    B AS event = 'click',
    C AS event NOT IN ('view', 'click')
```

The predicate is evaluated against the current input row. A `NULL` predicate does not match; only `TRUE` qualifies. An undefined pattern variable matches every row, but explicitly defining every variable makes the query intent clearer.

## Write patterns

Pattern variables represent row roles. The pattern language supports:

- `A` — one row matching variable `A`
- `A B` — concatenation
- `A | B` — alternation
- `(A B)` — grouping
- `A*`, `A+`, `A?` — greedy repetition
- `A{n}`, `A{n,}`, `A{n,m}` — bounded repetition
- `A*?`, `A+?`, `A??`, and similar forms — reluctant repetition
- `PERMUTE(A, B, …)` — any ordering of the listed variables
- `^` and `$` — partition-start and partition-end anchors
- `{- A -}` — exclusion from `ALL ROWS PER MATCH` output

Patterns can be composed:

```sql
PATTERN ((A B) | (A C* B) | A)
```

Alternatives are evaluated from left to right. In the example above, a complete `A B` match is preferred, then `A C* B`, then the single-row `A` fallback. Repetition is greedy by default.

## Return match results

### `MEASURES`

`MEASURES` defines the output columns. Every expression needs an alias:

```sql
MEASURES
    A.ts AS start_ts,
    B.ts AS end_ts,
    B.ts - A.ts AS elapsed
```

In a measure, `A.column` returns the value from the last row assigned to `A`. An unqualified column such as `ts` returns the value from the last row of the whole match.

Pattern expressions also support navigation and pattern functions, including:

- `PREV`, `NEXT`, `FIRST`, and `LAST`
- `CLASSIFIER()`
- `MATCH_NUMBER()`
- Pattern aggregates such as `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`
- Top-level `RUNNING` and `FINAL` prefixes, such as `RUNNING LAST(value)` or `FINAL COUNT(*)`

If a variable did not participate in the selected alternative, referencing it produces `NULL`.

### Rows per match

`ONE ROW PER MATCH` is the default and emits one summary row for each successful match:

```sql
ONE ROW PER MATCH
```

`ALL ROWS PER MATCH` emits one row for each matched input row. It supports modifiers for empty and unmatched rows:

```sql
ALL ROWS PER MATCH SHOW EMPTY MATCHES
ALL ROWS PER MATCH OMIT EMPTY MATCHES
ALL ROWS PER MATCH WITH UNMATCHED ROWS
```

With `ONE ROW PER MATCH`, the output contains partition columns followed by measure columns. With `ALL ROWS PER MATCH`, the output also includes order columns and remaining input columns.

### `AFTER MATCH SKIP`

Choose where matching resumes after a match:

```sql
AFTER MATCH SKIP PAST LAST ROW
AFTER MATCH SKIP TO NEXT ROW
AFTER MATCH SKIP TO FIRST variable
AFTER MATCH SKIP TO LAST variable
```

`PAST LAST ROW` is the default. A skip target that does not advance the search, or that refers to a missing variable, raises an error.

### `SUBSET`

Create a union variable that refers to multiple pattern variables:

```sql
SUBSET milestone = (A, B)
```

Union variables can be used in `MEASURES`, `DEFINE`, and `AFTER MATCH SKIP TO FIRST` or `TO LAST`.

## Bound a match by time

Add `WITHIN` after `PATTERN` to require that a match completes within an interval:

```sql
PATTERN (A B C) WITHIN INTERVAL 30 SECOND
```

The interval is inclusive: the last timestamp can equal the first timestamp plus the interval. `WITHIN` requires an ascending temporal first `ORDER BY` key, such as `DATE`, `TIMESTAMP`, or `TIMESTAMPTZ`. The interval must be a non-null, strictly positive, foldable DuckDB `INTERVAL`.

## Practical patterns

### Funnel with filler events

Use a repeated variable when unrelated events may occur between two milestones:

```sql
SELECT *
FROM events
MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES
        A.ts AS view_ts,
        B.ts AS click_ts
    PATTERN (A C* B)
    DEFINE
        A AS event = 'view',
        B AS event = 'click',
        C AS event NOT IN ('view', 'click')
)
ORDER BY user_id, view_ts;
```

`C*` consumes zero or more filler rows. It cannot consume rows that do not match `C`, and the trailing `B` still needs to complete the pattern.

### Preferred path with a fallback

Use an alternation when a longer match should win, but a shorter match should still produce a result:

```sql
SELECT *
FROM events
MATCH_RECOGNIZE (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES
        A.ts AS start_ts,
        B.ts AS click_ts
    PATTERN ((A B) | A)
    DEFINE
        A AS event = 'view',
        B AS event = 'click'
)
ORDER BY user_id, start_ts;
```

When a `view` is followed by a `click`, `(A B)` wins and consumes both rows. When no click follows, the query falls back to `A`, producing a row with `click_ts = NULL`.

## Pattern recognition in windows

Pattern recognition is also supported in named or inline window structures. A pattern window produces one result row per input row:

```sql
SELECT
    user_id,
    value OVER w,
    label OVER w
FROM events
WINDOW w AS (
    PARTITION BY user_id
    ORDER BY ts
    MEASURES
        RUNNING LAST(value) AS value,
        CLASSIFIER() AS label
    ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
    AFTER MATCH SKIP PAST LAST ROW
    SEEK
    PATTERN (A B+)
    DEFINE B AS value < PREV(B.value)
);
```

Window pattern frames must start at `CURRENT ROW`. The frame can end at `CURRENT ROW`, a constant `n FOLLOWING`, or `UNBOUNDED FOLLOWING`. `INITIAL` and `SEEK`, `AFTER MATCH SKIP`, and `SUBSET` are supported in pattern windows.

Anchors and `MATCH_NUMBER()` are not supported in windows. Ordinary window functions over the matched frame currently cover `SUM`, `COUNT`, `AVG`, `MIN`, and `MAX`.
