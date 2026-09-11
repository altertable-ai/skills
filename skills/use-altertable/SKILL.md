---
name: use-altertable
compatibility: Requires Altertable MCP server for live platform operations
description: "Provides Altertable's foundational operating model, environment and catalog concepts, DuckDB conventions, and MCP-versus-CLI choices. Use for platform orientation, setup, tool selection, or any Altertable workflow needing shared context."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Use Altertable

Altertable is one governed data runtime for managed lakehouse tables, live external catalogs, applications, analytics, and agents. The same organization, environment, permissions, semantic context, and data layer are available through the app, MCP, CLI, APIs, SDKs, and SQL adapters.

## Operating Model

- An organization owns membership, billing, service accounts, and environments.
- An environment is an isolated workspace with its own catalogs, credentials, compute, data, analyses, tasks, and notification settings.
- Catalogs can be Altertable-managed databases or external systems queried live through the same SQL namespace.
- Workers execute DuckDB SQL. Cross-catalog joins are federated automatically.
- Semantic models define governed measures, dimensions, timestamps, filters, and relations.
- Knowledge entries provide maintained source material; memories capture reusable context learned from work.
- Insights are saved analyses; dashboards arrange insights and shared variables; Tasks run recurring work and produce Findings delivered through Notifications.

## MCP Invariants

1. Call `initialize` before every other Altertable MCP tool. Apply its environment and knowledge context throughout the task.
2. Use `list_catalogs` to enumerate available data sources.
3. Use `get_catalog` to inspect schemas, tables, columns, semantic models, and endorsement state before writing SQL.
4. Refer to tables as `catalog.schema.table` and write DuckDB dialect.
5. Use `search_docs` for current platform behavior and the live tool schema for arguments. Do not rely on remembered parameter names.
6. Confirm whether the connection is read-only or read-write before attempting persistence. Never treat authentication as authorization for an unrequested write.

## Choose the Surface

| Need | Default |
| --- | --- |
| Fast analytical answer or follow-up | Altertable Agent through `ask` |
| Exact SQL, raw evidence, validation, or plans | Direct MCP query tools |
| Interactive draft or governed platform object | Direct MCP artifact tools |
| Terminal automation, CI, ingestion, or structured JSON | Altertable CLI |
| Application integration | HTTP API, SDK, or SQL adapter |

Use the narrowest workflow that satisfies the request. Do not reproduce a multi-tool investigation when `ask` can answer it, and do not delegate when exact query or mutation control is the point of the task.

## Current Documentation

Search the live docs rather than copying large reference sections into the conversation. Useful starting points are [Altertable documentation](https://altertable.ai/docs), [MCP tools](https://altertable.ai/docs/api-references/mcp-tools), [Lakehouse](https://altertable.ai/docs/lakehouse), and the [CLI guide](https://altertable.ai/docs/developer-tooling/cli).
