---
name: build-local-data-app
description: "Builds and runs Altertable data apps locally with the CLI (beta). Use only when the user explicitly wants local development or a CLI scaffold; use build-data-app for any other Altertable data app request."
compatibility: Requires Altertable CLI app commands and authorized lakehouse access
metadata:
  author: Altertable
  status: beta
---

# Build a local data app

Build Altertable data apps locally with the CLI, only when the user explicitly wants local development or a CLI scaffold. Use `build-data-app` for any other request, including converting a local app to a hosted one.

Before writing code, read [the data-app AGENTS.md](https://github.com/altertable-ai/data-app/blob/main/AGENTS.md) and its links, then start from the CLI scaffold. Use `query-altertable` to find and verify data, and `analyze-product-behavior` for product analytics metrics.

## Workflow

Pass the same `--profile <profile>` to every `altertable` command.

1. Run `altertable profile show` to confirm the organization and environment, and `altertable app --help` for available commands.
2. New app: `altertable app create <name> --dir <path>`. Existing app: read its source first.
3. Write the app and verify its queries against live data. Define check inputs that exercise those queries.
4. Run `altertable app check --dir <path>`, then again with `--lakehouse` to run against live data. Fix failures until both pass.
5. Run `altertable app dev --dir <path>`.
6. Open the local URL and verify data, filters, loading, and error states. Fix runtime issues and repeat from step 4.

If the CLI is blocked, report the failing command. MCP can help discover data but cannot run a local app, and its credentials are separate from the CLI profile's, so confirm both target the same organization and environment. Use `--without-profile` only for a requested offline prototype; it cannot verify live data. Report any check you could not run.
