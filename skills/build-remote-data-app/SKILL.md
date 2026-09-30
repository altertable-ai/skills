---
name: build-remote-data-app
description: "Creates, validates, updates, and deletes remote Altertable data apps through MCP. Use when the user requests a remote or hosted Altertable data app, or an Altertable data app without a local coding environment or CLI."
compatibility: Requires the Altertable MCP server
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Build a remote data app

Build a hosted Altertable data app through MCP; no local coding environment or Altertable CLI is required. Use `build-local-data-app` for a requested local app or scaffold. Apply `use-altertable` for shared platform context.

## Source contract

- Author one `index.ts` file and pass its complete source text as `index_tsx` (the tools call this `index.tsx`).
- Import only `@altertable/data-app`, `react`, and `react-dom`; keep components, styles, and helpers in the same file.
- Consult [the data-app repository](https://github.com/altertable-ai/data-app) for runtime exports and data-access APIs, and the live MCP schema for tool arguments and required metadata. Report missing contracts or unavailable tools instead of guessing.

## Workflow

1. Call `validate_data_app` with `index_tsx`. It checks bundling without saving and returns `{ errors }`. Fix reported errors and revalidate until the list is empty; report any unresolved blocker.
2. For a requested new app, call `create_data_app` with the validated source and required metadata. For an edit, obtain the existing app's source, validate the complete replacement, and call `update_data_app` with its `slug` and `index_tsx`.
3. Both writes return `{ slug, url }`. Return the actual URL and retain the slug for follow-up edits. A validation or preview request alone does not authorize either write.

Call `delete_data_app` with the app's `slug` only for an explicit deletion request; it returns `{}`.

Bundling validation leaves live data access and rendering unverified. When the URL can be opened, inspect the app and exercise its intended data interaction; otherwise report runtime verification as pending.
