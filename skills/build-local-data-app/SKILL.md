---
name: build-local-data-app
description: "Builds local Altertable data apps with the CLI (beta). Use for local data exploration, analysis, or interactive discovery."
compatibility: Requires Altertable CLI app commands and authorized lakehouse access
metadata:
  author: Altertable
  status: beta
---

# Build a local data app

Follow the CLI scaffold's generated `AGENTS.md` for implementation and visual checks. Use `build-remote-data-app` for hosted apps.

1. Check `altertable app --help` and confirm scope with `altertable --profile <profile> profile show`. Prefer CLI queries for speed, using the same profile. For MCP fallback, call `initialize` and reconcile scope; its credentials are separate.
2. Run `altertable --profile <profile> app create <name> --dir <path>`. Verify `app.json` scope and the selected data, then build the app. A connected scaffold confirms only its starter probe.
3. Run `altertable --profile <profile> app check --dir <path>`, then add `--lakehouse` to execute the fixed `app.json` fixtures against live data. Choose fixtures that exercise the actual operation. Start `app dev` with the same profile and directory, inspect the app, and compare its default view with a query result.

If CLI access is blocked, report the failed command and use MCP for source discovery; MCP does not provide the app runtime. Use `--without-profile` only for a requested offline prototype: its scope contains placeholders and local checks cannot verify live data access. Report unrun checks and runtime blockers.
