---
name: build-data-app
description: "Creates, validates, updates, and deletes Altertable data apps through MCP (beta). Use by default when the user requests an Altertable data app; use build-local-data-app only for explicitly requested local development or a CLI scaffold."
compatibility: Requires the Altertable MCP server, including its sandbox tools
metadata:
  author: Altertable
  status: beta
  requires: "altertable-mcp"
---

# Build a data app

Build an Altertable data app through MCP, even when a local coding environment is available. Use `build-local-data-app` only for explicitly requested local development or a CLI scaffold. Apply `use-altertable` for shared platform context and `query-altertable` for source discovery and SQL verification.

For apps involving product events, funnels, retention, sessions, journeys, or behavioral cohorts, apply [`analyze-product-behavior`](../analyze-product-behavior/SKILL.md) before designing metrics or queries.

## Read the authoring instructions

Before authoring or changing source, **read [the data-app repository's AGENTS.md](https://github.com/altertable-ai/data-app/blob/main/AGENTS.md) and follow its links** for the intended workflow. Retrieve the document contents and start from the single-file example linked by the guide. Follow its instructions to produce one `index.tsx`.

To convert an existing app to a local app, retrieve its source and use `build-local-data-app` to adapt it to the CLI scaffold, preserving its queries and UI.

`queries` is an object mapping each query ID to SQL (`{}` when the app has none). `variables` is an array (`[]` when none). On update, provided queries or variables replace the full set.

## Workflow

Work in one sandbox so the full `index.tsx` is written once and never re-sent as a tool argument. `create_sandbox` preconfigures `altertable` with lakehouse credentials and `ALTERTABLE_API_KEY` for the management API.

1. Initialize the intended scope, inspect the live tool schema, read the upstream instructions, and discover source data. Establish the documented runtime contract before promising live interactions.
2. Call `create_sandbox` once. Keep `/workspace/app/index.tsx`, `/workspace/app/queries.json`, and `/workspace/app/variables.json` as the working files, and run every step below through `run_sandbox_command`.
3. Write the source once. For an edit, fetch the existing app into those files first; do not overwrite source you have not retrieved. Inspect with `rg` or `sed` and apply small patches instead of regenerating the file.
4. Validate from disk: `altertable app validate --file /workspace/app/index.tsx --queries /workspace/app/queries.json --variables /workspace/app/variables.json`. Fix errors with targeted patches and rerun until `errors` is empty; review warnings.
5. Persist only when the user asked to save. A validation or preview request alone does not authorize persistence. Saving re-checks the source, so do not validate again first.
   - New app: `altertable app publish --title <title> --file /workspace/app/index.tsx --queries /workspace/app/queries.json --variables /workspace/app/variables.json`
   - Edit: `altertable app update <slug> --file /workspace/app/index.tsx` (add `--queries` or `--variables` only when those sets change)
6. Return the actual URL from the save command and retain its slug for follow-up edits. Call `terminate_sandbox` when finished.
7. Open the returned URL when possible and exercise the documented runtime checks, including actual live data, scope, filters, loading, errors, and refresh. Compare results with an independent query. Validation alone does not verify rendering or data access; report any runtime verification pending.

Call `delete_data_app` only for an explicit deletion request, using the app's slug.
