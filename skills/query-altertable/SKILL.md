---
name: query-altertable
compatibility: Requires Altertable MCP server
description: "Inspects Altertable catalogs and runs controlled DuckDB SQL across managed and external data. Use for exact queries, raw results, schema inspection, federated joins, query validation, plans, or optimization."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Query the Lakehouse

Altertable exposes managed tables and external sources through one governed DuckDB SQL layer. Use this skill when the caller needs direct control over the query or its evidence; use the `ask-altertable` skill for the faster conversational path.

## Inspect Before Querying

For business metrics and KPIs, start with `list_semantic_metrics`. When a metric matches, query its semantic view with the `use-semantic-layer` skill rather than rebuilding the aggregation. Use `expression` only to explain or distinguish metrics. If no metrics match, continue below.

1. Call `list_catalogs` to identify the available managed and external catalogs.
2. Call `get_catalog` for candidate schemas and tables. Start with its automatic or overview detail, then request specific tables or columns.
3. Profile only selected tables when sampled null rates, cardinality, ranges, and frequent values will change the query.
4. Endorsement status: `verified` tables are preferred when several could answer; `draft` (the default) is fully usable; `excluded` tables are omitted from default discovery and used only when the request names them. Name an excluded table in `get_catalog` `tables` to inspect it.

Never infer a table or column from a plausible name. Fully qualify data as `catalog.schema.table` so environment defaults cannot redirect a query.

## Execute Deliberately

1. Write DuckDB SQL using only inspected identifiers. SELECT only the columns the question named. Do not project anything they did not ask for.
2. Always write `AS` before column and table aliases. DuckDB rejects a bare alias that is a keyword, and common names such as `cost`, `name`, `value`, `type`, `year`, `rows`, `first`, and `last` are keywords.
3. Cast every named parameter explicitly, as in `$member::VARCHAR` and `$org::VARCHAR`. DuckDB cannot always infer their types. Bind them through `query_lakehouse` `params`.
4. Parenthesize `->>` before `=`. `properties->>'x' = $org` is misparsed because `->>` binds next to `=`. Write `(properties->>'x') = $org::VARCHAR`.
5. Add explicit time bounds and a small `LIMIT` during exploration.
6. Use `validate_sql` when binding or syntax is uncertain.
7. Use `explain_sql` before a potentially expensive scan or join.
8. Run the statement with `query_lakehouse`.

Do not turn a read request into DDL or data modification. Mutating SQL requires explicit user intent and read-write access.

## Keep Results Small

Every returned row enters the conversation and is reread on each later turn. Return the smallest result that answers the question.

- Compute totals, rates, baselines, percentiles, rankings, and joins in SQL over the full relevant population. Never fetch raw rows to count, rank, or scan them yourself.
- Fetch raw rows only as a few targeted examples or IDs, with filters, a deterministic `ORDER BY`, and `LIMIT`. Avoid `SELECT *` on wide tables such as spans, logs, and events.
- A truncated or limited result is a preview, not the population: the first rows say nothing about the rest. When `query_lakehouse` reports truncation, aggregate, narrow, or project instead of paging. Paginate with the returned offset only to return a specific page that was asked for, after a deterministic `ORDER BY`.
- When it matters, state the population analyzed (filters, time window, row count) separately from the rows shown.
- For a full export, such as every row as CSV, keep the rows out of the conversation. Run `count(*)` over the export query, then give the row count and the exact [Altertable CLI](https://altertable.ai/docs/developer-tooling/cli) command, `altertable query --format csv --output <file> "<SQL>"`. Use `--format parquet` for typed columns.

## Altertable-Specific SQL

Altertable extends DuckDB with operators and catalog features for event streams, text retrieval, history, and storage layout:

- `MATCH_RECOGNIZE` matches ordered row patterns for funnels, journeys, state transitions, and anomaly shapes. Partition by the entity, order deterministically, describe the pattern, and use `WITHIN` when the sequence has a conversion window. It is beta.
- `SESSIONIZE` groups ordered rows when consecutive events are separated by more than an inactivity gap. It can preserve each event with session metadata or return one row per session with measures. It is beta.
- Full-text search indexes free-form text with `TNVYX` and queries it with `@@`. Combine it with structured and time predicates to narrow logs, traces, tickets, documents, or event text.
- Time travel reads full table state at a snapshot version or timestamp. Data change feeds return row-level inserts, updates, and deletions between bounds; committed transactions create the snapshots shared by both.
- Semantic views (`SEMANTIC_VIEW(...)`, `AGG(...)`) compute governed metrics at their own grain without fan-out; the `use-semantic-layer` skill covers them.
- Views and macros store reusable query logic. Partitioning and sorted tables shape new writes; `OPTIMIZE TABLE` rewrites existing files to compact them and apply the current layout.

Use `search_docs` when you need detailed syntax or semantics, especially for beta operators and persistent catalog changes.

Federated SQL can join Altertable catalogs and external connections in one DuckDB statement. Fully qualify each relation and confirm join-key uniqueness before trusting row counts or aggregates.
