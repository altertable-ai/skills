---
name: query-lakehouse
compatibility: Requires Altertable MCP server
description: "Inspects Altertable catalogs and runs controlled DuckDB SQL across managed and external data. Use for exact queries, raw results, schema inspection, federated joins, query validation, plans, or optimization."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Query the Lakehouse

Altertable exposes managed tables and external sources through one governed DuckDB SQL layer. Use this skill when the caller needs direct control over the query or its evidence; use the `ask` skill for the faster conversational path.

## Inspect Before Querying

1. Call `list_catalogs` to identify the available managed and external catalogs.
2. Call `get_catalog` for candidate schemas and tables. Start with its automatic or overview detail, then request specific tables or columns.
3. Profile only selected tables when sampled null rates, cardinality, ranges, and frequent values will change the query.
4. Prefer verified semantic measures and dimensions when they express the requested business definition. Treat draft definitions cautiously and do not use excluded models.

Never infer a table or column from a plausible name. Fully qualify data as `catalog.schema.table` so environment defaults cannot redirect a query.

`list_catalogs` may return Altertable databases and external connections such as warehouses or databases. Pass the returned machine identifier to `get_catalog`; do not substitute the display name. Built-in catalogs such as Product Analytics or OpenTelemetry exist only when enabled for the environment.

## Execute Deliberately

1. Write DuckDB SQL using only inspected identifiers. SELECT only the columns the question named. Do not project anything they did not ask for.
2. Add explicit time bounds and a small `LIMIT` during exploration.
3. Use `validate_sql` when binding or syntax is uncertain.
4. Use `explain_sql` before a potentially expensive scan or join.
5. Run the statement with `query_lakehouse`.
6. If the result is truncated, repeat the same statement with the returned offset. Include a deterministic `ORDER BY` before paginating.
7. Use `optimize_sql` only when performance matters and compare its proven rewrite with the original semantics.

Do not turn a read request into DDL or data modification. Mutating SQL requires explicit user intent and read-write access.

## Altertable-Specific SQL

Use `search_docs` before applying platform extensions:

- `MATCH_RECOGNIZE` for ordered event sequences and bounded funnels;
- `SESSIONIZE` for inactivity-gap session construction;
- time travel for snapshot- or timestamp-bounded historical reads;
- data change feeds for inserts, updates, and deletions between snapshots;
- macros, full-text search, views, partitioning, sorted tables, and table optimization.

Do not approximate a sequence funnel with independent per-user event flags: that loses ordering and conversion-window semantics.

Cross-catalog federated queries can join multiple catalogs in one DuckDB statement. Inspect both sides first, make join grain explicit, and verify that the join does not multiply rows unexpectedly.

Follow the live tool schema for arguments and result fields rather than copying their current names into the workflow.
