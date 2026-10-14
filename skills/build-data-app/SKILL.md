---
name: build-data-app
description: "Creates, updates, and deletes Altertable-hosted data apps through MCP (beta). Use by default for any Altertable data app request; use build-local-data-app only when the user explicitly wants local development or a CLI scaffold."
compatibility: Requires the Altertable MCP server
metadata:
  author: Altertable
  status: beta
  requires: "altertable-mcp"
---

# Build a data app

Build Altertable-hosted data apps through MCP, even when a local environment is available. Use `build-local-data-app` only when the user explicitly wants local development or a CLI scaffold, including converting a hosted app to a local one.

Before writing code, read [the data-app AGENTS.md](https://github.com/altertable-ai/data-app/blob/main/AGENTS.md) and its links, then start from its single-file example; the app is one `index.tsx`. Use `query-altertable` to find and verify data, and `analyze-product-behavior` for product analytics metrics.

## Workflow

Run every command with `run_sandbox_command` in one sandbox, and call `terminate_sandbox` when done. Its `altertable` CLI is already authenticated.

1. Call `create_sandbox`. Keep the source at `/workspace/app/index.tsx`.
2. New app: start from the example. Existing app: download its source first, passing the environment slug from `initialize`:
   `altertable --json api --env <environment> "/environments/{environment}/data_apps/<slug>" | jq -r .data_app.index_tsx > /workspace/app/index.tsx`
3. Write the app and verify its queries against live data. Make targeted edits (`rg`, `sed`, `python3`, `git apply`); never resend the whole file.
4. Run `altertable app validate --file /workspace/app/index.tsx`. Fix errors and warnings until none remain.
5. Save:
   - New app: `altertable app publish --title <title> --file /workspace/app/index.tsx`
   - Existing app: `altertable app update <slug> --file /workspace/app/index.tsx`
6. Return the app URL, and open it if you have a local browser or shell. The sandbox cannot run the app, so fix runtime issues the user reports and repeat from step 4.

Call `delete_data_app` only when the user explicitly asks to delete an app.
