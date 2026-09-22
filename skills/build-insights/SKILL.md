---
name: build-insights
compatibility: Requires Altertable MCP server; saving or updating requires read-write access
description: "Renders, creates, updates, and explains Altertable Insights. Use only when the user explicitly requests an Altertable Insight or asks to work on an existing one; do not use for generic or client-native charts, analyses, reports, or visualizations."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Build Insights

An Insight is a persistent analysis and visualization over lakehouse data. It does not need to represent an anomaly or recommendation; it can be a reusable metric, table, or behavioral analysis.

## Routing Boundary

Use this skill only when the intended object or renderer is Altertable: the user explicitly requests an Altertable Insight or identifies an existing one. A generic request for a chart, analysis, report, or visualization does not imply an Altertable Insight. Prefer the client's native analysis or visualization capability unless the user explicitly wants an Altertable Insight.

Prefer `render_insight` on user-facing surfaces so the user can inspect the chart as well as the returned results. Use `execute_insight` when the caller cannot or should not attach the Insight Viewer, such as a subagent. `create_insight` and `update_insight` save an Insight only when `dry_run` is omitted or false, and that save requires explicit user intent.

## Choose the Definition

- **Semantic:** governed measures and dimensions already defined on a semantic model.
- **SQL:** custom DuckDB logic, joins, or calculations unavailable in native definitions.
- **Funnel:** ordered product-event progression.
- **Retention:** starting and returning events across cohort offsets.
- **Segmentation:** product-event metrics over time with property breakdowns, identity-attribute filters, or behavioral cohort comparisons.

Choose the kind from the question: ordered progression and drop-off → Funnel; return behavior after a starting event → Retention; event metrics compared across properties or cohorts → Segmentation; governed measures and dimensions → Semantic; logic unavailable in native definitions → SQL. Check the semantic model before choosing SQL for a standard business metric.

Before choosing SQL for identity attributes or “did X / did not do X” cohorts, check Segmentation's `dimension_filter` and `performed_event_filter`. A related-table filter or same-identity self-join does not by itself require a SQL Insight. Read [analyze-product-behavior](../analyze-product-behavior/SKILL.md#native-cohort-and-identity-filters) for relation support, cohort periods, and the boundary between raw breakdowns and derived dimensions. Choose each dashboard widget's kind independently.

Inspect catalogs, semantic models, events, and traits before constructing the definition. Use the live MCP schema for exact fields and enums.

## Render or Persist

`render_insight` and `execute_insight` each run exactly one Insight. Pass exactly one of `insight` or `definition`. `insight` selects a saved Insight by slug and may override `as_of`, `from`, `to`, or `variable_overrides`. `definition` is a complete non-persisted Insight and does not create or update one. Put kind-specific fields, including any required `from`, `to`, and `interval`, inside `definition`. Use the live schema for those fields.

| Intent | Tool |
| --- | --- |
| Show a saved or unsaved Insight to the user | `render_insight` |
| Run an Insight without attaching the viewer | `execute_insight` |
| Read a saved Insight without running it | `read_resource` at `altertable://ontology/entities/{slug}` |
| Save a new Insight | `create_insight` |
| Change an existing Insight | `update_insight` |
| Validate a create or update without saving | `create_insight` or `update_insight` with `dry_run: true` |

`render_insight` attaches the Insight Viewer. `dry_run: true` validates `create_insight` or `update_insight` and rolls the write back. A successful dry run returns an empty slug and URL; an invalid definition still fails. Omit `dry_run` only when the user requests persistence and the MCP connection has read-write access. Do not treat an empty slug as a saved Insight.

## Existing Insights

When the user asks what an existing chart or saved analysis shows, call `list_insights` to locate it. Read the stored definition with `read_resource` when filters, timeframe, grain, or variables are the question. Execute it by passing `insight` to `render_insight` on a user-facing surface or `execute_insight` when no viewer should be attached; do not rebuild its definition. Explain the stored definition separately from the executed result, and state when a result is sampled or approximate.

## SQL Contract

For SQL Insights, follow the live MCP schema for the SQL definition, variables, and visualization contract. Map chart axes to aliases actually returned by the query; visualization options alone do not define them.

Validate the SQL by running a bounded form through `query_lakehouse` before `render_insight` or `execute_insight`. Keep variables explicit and ensure defaults produce a valid, useful view.

For semantic, funnel, retention, and segmentation Insights, use the matching definition from the live schema. Supply the required timeframe and interval inside `definition` for product-behavior kinds.

## Workflow

1. Inspect the source objects and use `list_insights` to find reusable or conflicting existing work.
2. Build the smallest definition that answers the intended reusable question.
3. Run it with `render_insight` on a user-facing surface or `execute_insight` when no viewer should be attached. Verify values, labels, axes, filters, variables, and empty states.
4. Validate with `dry_run: true` before saving when the definition is not yet confirmed. Create or update without `dry_run` only after intent and permissions are clear.
5. After a persisted save, read the saved Insight with `read_resource` and run it with the surface-appropriate execution tool. Verify the stored definition and the results.

Use a stable descriptive title rather than encoding a transient conclusion. Describe the metric, population, timeframe behavior, and important caveats. Do not copy source data or credentials into descriptions.
