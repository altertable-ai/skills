---
name: build-remote-data-app
description: "Creates, validates, updates, and deletes remote Altertable data apps through MCP. Use when the user requests a remote or hosted Altertable data app, or an Altertable data app without a local coding environment or CLI."
compatibility: Requires the Altertable MCP server
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Build a remote data app

Build a hosted Altertable data app through MCP with no local coding environment or Altertable CLI required. Use `build-local-data-app` when the user requests a local app or the CLI scaffold.

## Source contract

- Author one source file, `index.ts`, and pass its complete contents as the MCP `index_tsx` argument. The tools describe this source as `index.tsx`; the argument carries source text, not a file path or project directory.
- Import only `@altertable/data-app`, `react`, and `react-dom`. Keep components, styles, and helpers in that single file. Do not add relative imports, other packages, package installation, or a local build pipeline.
- Consult [the data-app repository](https://github.com/altertable-ai/data-app) for the current runtime entry point, exports, and data-access API. Use `search_docs` and the live MCP schema for current tool arguments, including required metadata such as a title.
- Do not invent runtime exports or query APIs. If the repository or docs do not provide the needed contract, identify the missing detail and continue source discovery that does not depend on it. Do not substitute the local CLI scaffold for a remote app.

## Build and validate

1. Apply `use-altertable` for initialization, organization and environment scope, catalog inspection, and governed DuckDB SQL. Establish the app's question and inspect the actual source data before authoring its data path. MCP queries support source discovery; use the documented data-app runtime API for the app's live data access.
2. Write the single-file app using the verified runtime contract and allowed imports. Keep credentials out of source. Show loading, empty, and error states where the app accesses live data.
3. Call `validate_data_app` with `index_tsx`. This checks the source without saving and returns `{ errors }`. Repair the reported errors and validate the revised source until `errors` is empty. If errors cannot be resolved with the supported contract, report the blocker without claiming the app is valid.

Validation checks bundling; it does not prove live queries, permissions, data correctness, or the rendered experience. Distinguish those checks in the handoff.

## Save and maintain

Create or update only within the user's requested scope. A validation or preview request does not authorize saving an app.

- For a requested new app, call `create_data_app` with the validated `index_tsx` and any metadata required by the live schema. It returns `{ slug, url }`. Return the actual URL and retain the slug for follow-up changes.
- For a requested edit, resolve the existing slug and obtain its current source from available context or supported retrieval before making changes. Validate the complete replacement source, then call `update_data_app` with `slug` and `index_tsx`. It returns `{ slug, url }`. Update that app instead of creating a duplicate.
- Use `delete_data_app` with `slug` only for an explicit deletion request targeting that app. It returns `{}`; report the tool's confirmed outcome.

If a remote app tool is unavailable, report that capability gap. Do not install the CLI or require a terminal to complete this workflow. When the returned URL can be opened, inspect the rendered app and exercise its intended data interaction; otherwise report that runtime verification remains pending.
