---
name: build-local-data-app
description: "Creates local Altertable data apps with the CLI for data exploration and analysis (beta). Use when the user asks for an exploration, a data app, or interactive data discovery, and mentions local."
compatibility: Requires Altertable CLI app commands and authorized lakehouse access
metadata:
  author: Altertable
  status: beta
---

# Build a local data app

Use the CLI scaffold and follow its generated `AGENTS.md` for source analysis, runtime APIs, implementation, and visual checks. Use `build-remote-data-app` for a hosted app through MCP.

1. Check `altertable app --help` and confirm the organization and environment with `altertable --profile <profile> profile show`. Prefer CLI queries for faster discovery and verification; check `query --help` and use the app's profile. If using MCP, call `initialize` and reconcile its scope with the CLI profile: their credentials are separate. MCP supports authoring, not app runtime.
2. Run `altertable --profile <profile> app create <name> --dir <path>`. Verify `app.json` scope against the available connections and build one source-backed answer. A connected scaffold proves only that its starter probe succeeded; verify the selected dataset and actual operation.
3. Run `altertable --profile <profile> app check --dir <path>`, then add `--lakehouse` for live checks. The live check executes fixed `app.json` fixtures; choose inputs that exercise the app's actual operation. Start `app dev` with the same profile and directory, inspect the rendered app, and compare its default view with an executed query.

If CLI querying is unavailable, use MCP for bounded source discovery. Report missing app commands, lakehouse credentials, or credential-store access before retrying setup; preserve the verified query and scope for resumption. Create a `--without-profile` scaffold only for a requested offline prototype; its scope contains placeholders and local checks cannot verify live data access. Report unrun checks and avoid claiming a runnable app while its runtime is blocked.
