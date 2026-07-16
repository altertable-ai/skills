---
name: query-product-events
compatibility: Requires Altertable MCP server
description: Queries product analytics events and identities stored in Altertable. Use when inspecting tracked events, event properties, identities, traits, aliases, counts, or raw and identity-resolved product behavior.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Query Product Events

Use the official Altertable documentation as the source of truth for current Product Analytics tables, views, MCP tools, and SQL behavior.

## Quick Start

1. Call `initialize` before other Altertable MCP tools.
2. Read the Product Analytics documentation to choose the raw or identity-resolved table.
3. Inspect the current catalog with `get_catalog` instead of assuming columns or property types.
4. Validate the SQL, then execute it with `query_lakehouse`.
5. Explain the result with a clear time range and counting unit.

## Official Documentation

- [Product Analytics tables and views](https://altertable.ai/docs/product-analytics)
- [Tracking product events](https://altertable.ai/docs/product-analytics/tracking)
- [Identifying users](https://altertable.ai/docs/product-analytics/identifying)
- [Model Context Protocol](https://altertable.ai/docs/query-data/mcp)
- [SQL engine](https://altertable.ai/docs/analytical-database/sql-engine)

## Common Pitfalls

- Confirm whether the question needs raw or identity-resolved data.
- Distinguish event counts from unique identities and sessions.
- Apply an explicit time range and environment filter where relevant.
- Inspect JSON property types before casting or aggregating them.
- Validate table and column names against the current catalog.
