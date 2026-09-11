---
name: query-with-chatgpt-data
compatibility: Requires the Altertable MCP server
description: "Use when ChatGPT Work's @Data agent, the ChatGPT Data agent, or a Codex workflow coordinating with @Data needs to inspect or query Altertable. Do not use for ordinary Altertable analysis that does not involve ChatGPT Data."
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Query Altertable with ChatGPT Data

Use Altertable as a governed, read-only data source for ChatGPT Data. Altertable
provides catalogs, semantic context, and query results; ChatGPT owns the
investigation narrative and dashboard.

## Quick Start

1. Call `initialize` before any other Altertable tool.
2. Call `list_catalogs` to discover the connected data sources.
3. Call `get_catalog` for the relevant schemas, tables, columns, measures, and
   dimensions.
4. Use `validate_sql` when a query is non-trivial or the schema is uncertain.
5. Execute read-only DuckDB SQL with `query_lakehouse`.
6. Return the evidence ChatGPT needs to explain or visualize the result.

Always use fully qualified `catalog.schema.table` names in SQL.

## When to Use This Skill

- The user invokes `@Data` and names Altertable as a source.
- ChatGPT Work's Data agent needs Altertable catalogs, schemas, or semantic
  definitions.
- A Codex workflow is preparing or testing an Altertable connection for
  ChatGPT Data.
- The requested output is a ChatGPT report or dashboard backed by Altertable
  query results.

Do not use this adapter for ordinary Altertable questions that do not involve
ChatGPT Data. Route those through `ask`.

## Read-Only Workflow

### 1. Establish Context

Call `initialize`. Apply the returned organization, environment, and knowledge
context throughout the analysis.

If the business question, metric, period, or intended source is genuinely
ambiguous, ask one focused clarification. Do not interpret `@Data` as the name
of a catalog.

### 2. Discover Before Querying

Call `list_catalogs`, then inspect likely sources with `get_catalog`. Prefer
verified semantic measures and dimensions. Ignore excluded tables and avoid
returning personally identifiable sample values.

Start with an overview for a wide catalog, then request columns or full semantic
details only for candidate tables.

### 3. Query and Corroborate

Write DuckDB SQL using the discovered names. Use bounded exploratory queries,
explicit date ranges, and deterministic ordering. Validate non-trivial SQL
before execution.

Call `query_lakehouse` for the baseline result, then run focused follow-up
queries when needed to test likely drivers. Distinguish observed association
from causation.

### 4. Hand Evidence Back to ChatGPT

Return:

- the metric definition and date range used
- the catalogs and tables queried
- the SQL or a concise description of each query
- the relevant results and comparisons
- caveats, missing context, and unsupported conclusions

ChatGPT owns the dashboard. Do not call `render_insight`, `draft_insight`,
`draft_dashboard`, or other Altertable artifact tools merely because the user
wants a ChatGPT dashboard.

## Write Requests

Do not call write or persistence tools from this workflow. If a request asks to
create a table, save an Altertable insight or dashboard, schedule a task, or
publish a discovery, explain that this ChatGPT Data adapter is read-only. Do not
silently switch to a write-capable Altertable workflow.

## Common Pitfalls

- Treating `@Data` as an Altertable catalog instead of the host agent
- Skipping `initialize`
- Guessing tables or columns before calling `get_catalog`
- Routing a ChatGPT dashboard request to Altertable artifact creation
- Using PostgreSQL syntax instead of DuckDB SQL
- Returning PII when aggregate evidence is sufficient
- Claiming causation from a single breakdown
- Persisting drafts, insights, dashboards, tasks, discoveries, or tables
