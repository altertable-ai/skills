---
name: build-data-app
description: "Creates, validates, updates, and deletes Altertable data apps through MCP (beta). Use by default when the user requests an Altertable data app; use build-local-data-app only for explicitly requested local development or a CLI scaffold."
compatibility: Requires the Altertable MCP server
metadata:
  author: Altertable
  status: beta
  requires: "altertable-mcp"
---

# Build a data app

Build an Altertable data app through MCP, even when a local coding environment is available. Use `build-local-data-app` only for explicitly requested local development or a CLI scaffold. Apply `use-altertable` for shared platform context and `query-altertable` for source discovery and SQL verification.

For apps involving product events, funnels, retention, sessions, journeys, or behavioral cohorts, apply [`analyze-product-behavior`](../analyze-product-behavior/SKILL.md) before designing metrics or queries.

## Read the authoring instructions

Before authoring or changing source, **read [the data-app repository's AGENTS.md](https://github.com/altertable-ai/data-app/blob/main/AGENTS.md) and follow its links** for the intended workflow. Retrieve the document contents and start from the single-file example linked by the guide. Follow its instructions to produce one `index.tsx` whose `defineDataApp()` call declares the app's static manifest, including its SQL queries and their parameters. Saving source replaces the app's queries with the ones its manifest declares.

To convert an existing app to a local app, retrieve its source and use `build-local-data-app` to adapt it to the CLI scaffold, preserving its queries and UI.

## Workflow

Work in one sandbox so the full `index.tsx` is written once and edited in place, never re-sent as a tool argument. The sandbox includes the Altertable CLI (`altertable`), already authenticated for the current environment's lakehouse and management API. Run it, and every other command below, through `run_sandbox_command`.

1. Initialize the intended scope, inspect the live tool schema, read the upstream instructions, and discover source data. Establish the documented runtime contract before promising live interactions.
2. Call `create_sandbox` once and keep the source at `/workspace/app/index.tsx`.
3. Write the source once. For an edit, retrieve the saved source first and do not overwrite source you have not retrieved: `altertable --json api "/environments/$ALTERTABLE_ENV/data_apps/<slug>" | jq -r .data_app.index_tsx > /workspace/app/index.tsx`. Locate code with `rg -n`, read only the relevant ranges with `sed -n`, and make targeted edits with `sed -i`, `python3`, or `git apply` instead of regenerating the file.
4. Validate from disk with `altertable app validate --file /workspace/app/index.tsx`, which exits non-zero only for errors, so read its output for warnings too. Fix errors and warnings with targeted edits and rerun until none remain.
5. Persist only when the user asked to save. A data app cannot yet be previewed without saving it, so when the user asks only to validate or preview, ask before saving. Saving re-checks the source, so do not validate again first.
   - New app: `altertable app publish --title <title> --file /workspace/app/index.tsx`
   - Edit: `altertable app update <slug> --file /workspace/app/index.tsx`
6. Return the actual URL from the save command and retain its slug for follow-up edits.
7. Open the returned URL when possible and exercise the documented runtime checks, including actual live data, scope, filters, loading, errors, and refresh. When you need to confirm that a saved app loads its initial state, such as after fixing a broken app, call `take_screenshot` with its slug. Compare results with an independent query. Validation alone does not verify rendering or data access; report any runtime verification pending.
8. Fix runtime issues in the same working file and repeat steps 4–7.
9. Call `terminate_sandbox` when finished in any case.

Call `delete_data_app` only for an explicit deletion request, using the app's slug.
