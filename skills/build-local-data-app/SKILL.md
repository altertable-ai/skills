---
name: build-local-data-app
description: "Builds local Altertable data apps with the CLI (beta). Use only when the user explicitly requests a local data app, local development, or a CLI scaffold. Default to build-data-app for other Altertable data app requests."
compatibility: Requires Altertable CLI app commands and authorized lakehouse access
metadata:
  author: Altertable
  status: beta
---

# Build a local data app

Build a local Altertable data app from the CLI scaffold only when explicitly requested. Use `build-data-app` for other Altertable data app requests. Apply `use-altertable` for shared platform context and `query-altertable` for source discovery and SQL verification.

## Read the authoring instructions

Before authoring or changing source, **read [the data-app repository's AGENTS.md](https://github.com/altertable-ai/data-app/blob/main/AGENTS.md) and follow its links** for the local workflow. Retrieve the document contents and start from the CLI scaffold.

To convert a local app to an Altertable-hosted app, use `build-data-app` to adapt the existing source to its single-file workflow, preserving its queries and UI.

## Workflow

1. Check `altertable app --help` and confirm scope with `altertable --profile <profile> profile show`. Prefer CLI queries for speed, using the same profile. For MCP fallback, call `initialize` and reconcile scope; its credentials are separate.
2. For a new app, run `altertable --profile <profile> app create <name> --dir <path>`. For an edit, inspect the existing source first. Verify the app configuration scope and the selected data. A connected scaffold confirms only its starter probe.
3. Author the app following the upstream instructions. Declare `queries` and `variables` on operations using the same contract as hosted apps, then execute with `query(id, values)`. Export the complete maps with `getDataAppRegistration()`. Keep SQL in declarations and variable values in calls; Bun validates and builds statements before sending them through the CLI proxy. Local registration lives in app source and does not require a hosted create/update call. Define check inputs that exercise its actual operations.
4. Run `altertable --profile <profile> app check --dir <path>`, then add `--lakehouse` to execute the checks against live data. Fix failures and rerun the checks.
5. Start `app dev` with the same profile and directory. Open the local URL and verify live data, scope, filters, loading, errors, and refresh. Compare results with an independent query; report any runtime verification pending.

If CLI access is blocked, report the failed command and use MCP for source discovery. MCP cannot run the local scaffold; use `build-data-app` if the user requests switching to an Altertable-hosted app. Use `--without-profile` only for a requested offline prototype: its scope contains placeholders and local checks cannot verify live data access. Report unrun checks and runtime blockers.
