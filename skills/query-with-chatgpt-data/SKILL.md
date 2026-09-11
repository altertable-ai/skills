---
name: query-with-chatgpt-data
compatibility: Requires the Altertable MCP server
description: "Use when ChatGPT Work's @Data agent, the ChatGPT Data agent, or a Codex workflow coordinating with @Data needs Altertable as a governed read-only source. Do not use for ordinary Altertable analysis."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Query Altertable with ChatGPT Data

Altertable supplies governed catalogs, semantic context, and query evidence; ChatGPT Data owns the investigation narrative and dashboard.

## Read-Only Workflow

1. Call `initialize` and apply the returned organization, environment, and knowledge context.
2. Call `list_catalogs`, then inspect candidate tables with `get_catalog`.
3. Prefer verified semantic measures and dimensions. Avoid excluded models and personally identifiable sample values.
4. Write bounded DuckDB SQL with fully qualified `catalog.schema.table` names and explicit date ranges.
5. Use `validate_sql` for non-trivial statements, then execute with `query_lakehouse`.
6. Run focused corroborating queries when needed to test likely drivers or data-quality concerns.
7. Return the metric definition, date range, sources, SQL or query description, results, and unsupported conclusions to ChatGPT Data.

Do not interpret `@Data` as a catalog name. Do not claim causation from a single breakdown.

## Boundary

This adapter is read-only. Do not call write or persistence tools, including Altertable draft, create, update, scheduling, ingestion, or table-mutation tools. ChatGPT owns the dashboard; do not create an Altertable dashboard merely because the requested output is a ChatGPT dashboard.

If the user requests an Altertable write, explain the boundary and let the host route that request to the appropriate Altertable workflow rather than silently changing this adapter's permissions.
