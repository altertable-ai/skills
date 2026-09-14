---
name: build-dashboards
compatibility: Requires Altertable MCP server; saving or updating requires read-write access
description: "Creates and updates persistent Altertable Dashboards composed of Insights, text, sections, variables, and grid positions. Use only when the user requests an Altertable-hosted dashboard or changes to an existing Altertable Dashboard; do not use for generic or client-native dashboards, reports, or visualizations."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Build Dashboards

Dashboards are persistent Altertable objects that arrange saved or inline Insights with explanatory text, sections, grid positions, and shared variables. Build them when several analyses need a reusable coordinated view in Altertable.

## Routing Boundary

Use this skill only when the intended destination is Altertable: the user explicitly asks for an Altertable dashboard, identifies an existing Altertable dashboard, or requests Altertable-specific dashboard capabilities such as Insight widgets or shared variables. A generic request for a dashboard, report, visualization, or interactive artifact does not imply Altertable persistence. Prefer the client's native dashboard or artifact capability unless the user explicitly wants the result created or maintained in Altertable.

Do not call `create_dashboard` as a rendering convenience or merely because Altertable supplied the data. Creating an Altertable Dashboard is a persistent write and requires explicit user intent.

Keep dashboard copy concise. Use text widgets only for context needed to interpret or act on the data.

## Workflow

1. Confirm the intended environment and write scope.
2. Use `list_insights` and `view_insight` to reuse valid existing analyses. Build or repair missing Insights before laying them out.
3. Use `view_dashboard` when changing an existing dashboard. Preserve widgets and variables the user did not ask to replace.
4. Define the audience, operating question, refresh cadence, and shared filters.
5. Arrange the most decision-relevant metrics first, followed by drivers and diagnostic detail.
6. Call `create_dashboard` for an explicitly requested new dashboard, or `update_dashboard` for an existing slug.
7. Retrieve the result and visually verify it when layout correctness matters.

## Altertable Objects

- Insight widgets can reference saved Insight slugs or contain inline Insight definitions.
- Text widgets explain definitions, caveats, or decisions without creating another query.
- Section widgets group related charts.
- Variables apply shared values across widgets through explicit mappings.
- Labels support organization and retrieval.

Use the live tool schema for widget kinds, grid coordinates, variable definitions, and mappings. Do not invent a dashboard JSON shape from an old example.

## Update Semantics

Widget and variable lists replace current values when supplied to `update_dashboard`. Read the existing dashboard first, merge intended changes locally, and send the complete retained lists. Omitting a field leaves it unchanged.

Do not silently create duplicate Insights to populate a dashboard. Reuse an existing Insight when its definition and variables match; use an inline definition for dashboard-specific analysis when supported and appropriate.

## Verification

- Every referenced Insight resolves and executes.
- Variable defaults and mappings work across all intended widgets.
- Grid positions do not overlap unintentionally.
- Titles, units, time grains, and filters are consistent.
- Empty and partial-data states remain understandable.
- The dashboard contains no sensitive raw values that aggregates could replace.

Attach a scheduled Task only when the user requests recurring monitoring; use `configure-tasks` for that operation.
