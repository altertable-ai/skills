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

## Read the authoring instructions

Before authoring or changing source, **read [the data-app repository's AGENTS.md](https://github.com/altertable-ai/data-app/blob/main/AGENTS.md) and follow its links** for the intended workflow. Retrieve the document contents and start from the single-file example linked by the guide. Follow its instructions to produce one `index.tsx`.

To convert an existing app to a local app, retrieve its source and use `build-local-data-app` to adapt it to the CLI scaffold, preserving its queries and UI.

## Workflow

1. Initialize the intended scope, inspect the live tool schema, read the upstream instructions, and discover source data. Establish the documented runtime contract before promising live interactions.
2. Produce single-file browser source, `queries.json`, and `variables.json` following the [package contract](https://github.com/altertable-ai/data-app/blob/main/docs/contract.md). Keep SQL out of browser source. Validate registration per the contract, then call `validate_data_app` with `index_tsx`. Fix errors and revalidate until `errors` is empty; review warnings.
3. Create a requested new app with `create_data_app` and required metadata; for edits, retrieve the existing source and registration, validate the replacements, and use `update_data_app` with the app's slug. When submitting source, both `create_data_app` and `update_data_app` require queries and variables for the same app revision as a complete replacement, including removals and empty collections. Use the live tool schema for argument names; report an integration blocker if registration fields are unsupported.
4. Return the actual URL supplied by the write tool and retain its slug for follow-up edits. A validation or preview request alone does not authorize persistence.
5. Open the returned URL when possible and exercise the documented runtime checks, including actual live data, scope, filters, loading, errors, and refresh. Compare results with an independent query. Validation alone does not verify rendering or data access; report any runtime verification pending.

Call `delete_data_app` only for an explicit deletion request, using the app's slug.
