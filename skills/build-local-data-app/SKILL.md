---
name: build-local-data-app
description: "Creates local Altertable data apps with the CLI for data exploration and analysis (beta). Use when the user asks for an exploration, a data app, or interactive data discovery, and mentions local."
compatibility: Requires Altertable CLI app commands and authorized lakehouse access
metadata:
  author: Altertable
  status: beta
---

# Build a local data app

Use the CLI scaffold for a local app. Its generated `AGENTS.md` covers source analysis, runtime APIs, code, and visual checks. This skill handles scope and verification across MCP and CLI.

Use `build-remote-data-app` for a hosted Altertable data app through MCP without a local coding environment or CLI.

Prefer querying through the CLI when available for faster source discovery and verification. Use `altertable --profile <profile> query --help` for the current command contract and keep the same profile as the app. Fall back to MCP when CLI querying is unavailable.

1. Check `altertable app --help` for the app commands. Confirm organization and environment through MCP `initialize` when connected and `altertable --profile <profile> profile show`. These use separate credentials; resolve mismatches before querying.
2. Run `altertable --profile <profile> app create <name> --dir <path>`. Compare `app.json` scope with the available connections; offline scaffolds contain placeholders. Connected proves only that the starter probe succeeded. Validate the selected dataset and actual operation. Follow the generated `AGENTS.md` to build one source-backed answer. MCP supports authoring, not app runtime.
3. Run `altertable --profile <profile> app check --dir <path>` and `app check --lakehouse` with the same profile. The live check executes fixed `app.json` operation fixtures; choose inputs that exercise the real operation. Start `app dev` and compare the default view with an executed query. Report checks that could not run.

If app commands are missing, lakehouse credentials fail, or the shell cannot access the credential store, identify that blocker before retrying login or installation. Continue bounded source discovery through MCP and record the verified query and scope for resumption. When app commands exist but live access does not, create a `--without-profile` scaffold only if an offline prototype was requested; local checks cannot verify its live data path. Report the blocked command and next action, and do not claim a runnable app.
