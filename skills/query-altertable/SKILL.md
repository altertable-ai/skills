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

1. Call `list_catalogs` to identify the available managed and external catalogs.
2. Call `get_catalog` for candidate schemas and tables. Start with its automatic or overview detail, then request specific tables or columns.
3. Profile only selected tables when sampled null rates, cardinality, ranges, and frequent values will change the query.
4. Prefer verified semantic measures and dimensions when they express the requested business definition. Treat unverified definitions cautiously and do not use excluded models.

Never infer a table or column from a plausible name. Fully qualify data as `catalog.schema.table` so environment defaults cannot redirect a query.

## Execute Deliberately

1. Write DuckDB SQL using only inspected identifiers. SELECT only the columns the question named. Do not project anything they did not ask for.
2. Add explicit time bounds and a small `LIMIT` during exploration.
3. Use `validate_sql` when binding or syntax is uncertain.
4. Use `explain_sql` before a potentially expensive scan or join.
5. Run the statement with `query_lakehouse`.
6. If the result is truncated, repeat the same statement with the returned offset. Include a deterministic `ORDER BY` before paginating.

Do not turn a read request into DDL or data modification. Mutating SQL requires explicit user intent and read-write access.

## Altertable-Specific SQL

Altertable extends DuckDB with operators and catalog features for event streams, text retrieval, history, and storage layout:

- `MATCH_RECOGNIZE` matches ordered row patterns for funnels, journeys, state transitions, and anomaly shapes. Partition by the entity, order deterministically, describe the pattern, and use `WITHIN` when the sequence has a conversion window. It is beta.
- `SESSIONIZE` groups ordered rows when consecutive events are separated by more than an inactivity gap. It can preserve each event with session metadata or return one row per session with measures. It is beta.
- Full-text search indexes free-form text with `TNVYX` and queries it with `@@`. Combine it with structured and time predicates to narrow logs, traces, tickets, documents, or event text.
- Time travel reads full table state at a snapshot version or timestamp. Data change feeds return row-level inserts, updates, and deletions between bounds; committed transactions create the snapshots shared by both.
- Views and macros store reusable query logic. Partitioning and sorted tables shape new writes; `OPTIMIZE TABLE` rewrites existing files to compact them and apply the current layout.

Use `search_docs` when you need detailed syntax or semantics, especially for beta operators and persistent catalog changes.

Federated SQL can join Altertable catalogs and external connections in one DuckDB statement. Fully qualify each relation and confirm join-key uniqueness before trusting row counts or aggregates.
