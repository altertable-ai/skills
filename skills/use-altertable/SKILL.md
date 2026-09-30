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

## What Altertable Is

Altertable is an AI-native data platform: DuckDB compute and lakehouse storage sit behind a governed SQL layer that humans, applications, analytics, and agents can share. The useful conceptual flow is:

```text
Data → Catalogs → Semantic models + knowledge → Insights/Dashboards
    → Tasks → Findings/Notifications → Memories and better future analysis
```

The conversational Altertable Agent handles an open-ended question or investigation. Insights and Dashboards are persistent analysis artifacts. Tasks are scheduled work attached to a context such as an Insight, Dashboard, connection, database, segment, or semantic model; when scheduled work finds something worth attention, it produces a Finding delivered through Notifications.

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

For most Altertable work, start with `ask` for a completed analytical answer or `query_lakehouse` for direct SQL and raw evidence.

| Need | Default |
| --- | --- |
| Fast analytical answer or follow-up | `ask` |
| Exact SQL, raw evidence, validation, or plans | `query_lakehouse` |
| Governed platform object | Relevant artifact tool |
| Hosted Altertable data app without a local coding environment | `build-remote-data-app` through MCP |
| Local Altertable data app or CLI scaffold | `build-local-data-app` |
| Terminal automation, CI, ingestion, or structured JSON | Altertable CLI |
| Application integration | HTTP API, SDK, or SQL adapter |

Use the narrowest workflow that satisfies the request. Do not reproduce a multi-tool investigation when `ask` can answer it, and do not delegate when exact query or mutation control is the point of the task.

## Set Up the CLI When Needed

The plugin supplies skills and hosted MCP access, not a local CLI executable. Use MCP for agent work it can complete directly. When the user requests terminal automation, CI, local file ingestion, or CLI setup, follow this path:

1. Check whether `altertable` is already on PATH in the execution environment where the command must run. A CLI installed in a hosted or temporary environment is not installed on the user's computer.
2. If it is missing, explain why the CLI is needed and where it would be installed. Do not install the CLI unless the user explicitly asks. When authorized, follow the current [CLI guide](https://altertable.ai/docs/developer-tooling/cli) for a supported installer, npm package, or release binary; do not assume a package manager or platform.
3. Verify that the installed command runs. CLI authentication is separate from MCP authentication: use browser login, specifying the target with `altertable login --org <organization> --env <environment>` when it is known. Then check `altertable profile status` and `altertable catalogs`. Query and ingestion commands also require lakehouse credentials.
4. Use the CLI's `--agent` preset for structured output in agent-driven scripts. Check current command help before using changing flags. Never expose profile credentials or tokens in chat or logs.

If the execution environment has no terminal or persistent installation path, continue through MCP where it supports the task and explain the remaining CLI requirement.

## Current Documentation

Search the live docs rather than copying large reference sections into the conversation. Useful starting points are [Altertable documentation](https://altertable.ai/docs), [MCP tools](https://altertable.ai/docs/api-references/mcp-tools), [Lakehouse](https://altertable.ai/docs/lakehouse), and the [CLI guide](https://altertable.ai/docs/developer-tooling/cli).
