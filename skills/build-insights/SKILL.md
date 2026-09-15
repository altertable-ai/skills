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

Do not call `render_insight` as a rendering convenience merely because Altertable supplied the data. `create_insight` and `update_insight` are persistent writes and require explicit user intent.

## Choose the Definition

- **Semantic:** governed measures and dimensions already defined on a semantic model.
- **SQL:** custom DuckDB logic, joins, or calculations unavailable in native definitions.
- **Funnel:** ordered product-event progression.
- **Retention:** starting and returning events across cohort offsets.
- **Segmentation:** product-event metrics with property breakdowns, identity-attribute filters, or behavioral cohort comparisons.

Choose the kind from the question: ordered progression and drop-off → Funnel; return behavior after a starting event → Retention; event metrics compared across properties or cohorts → Segmentation; governed measures and dimensions → Semantic; logic unavailable in native definitions → SQL. Check the semantic model before choosing SQL for a standard business metric.

Before choosing SQL for identity attributes or “did X / did not do X” cohorts, check Segmentation's `dimension_filter` and `performed_event_filter`. A related-table filter or same-identity self-join does not by itself require a SQL Insight. Read [analyze-product-behavior](../analyze-product-behavior/SKILL.md#native-cohort-and-identity-filters) for relation support, cohort periods, and the boundary between raw breakdowns and derived dimensions. Choose each dashboard widget's kind independently.

Inspect catalogs, semantic models, events, and traits before constructing the definition. Use the live MCP schema for exact fields and enums.

## Render or Persist

| Intent | Tool |
| --- | --- |
| Preview an unsaved Altertable Insight | `render_insight` |
| Save a new Insight | `create_insight` |
| Change an existing Insight | `update_insight` |
| Execute and inspect a saved Insight | `view_insight` |

Default to rendering while the definition is unsettled. Create or update only when the user requests persistence and the MCP connection has read-write access.

## Existing Insights

When the user asks what an existing chart or saved analysis shows, call `list_insights` to locate it and `view_insight` to execute it. Explain the returned definition, filters, timeframe, grain, and result rather than rebuilding a duplicate. Saved metadata alone is not current query evidence; distinguish it from the executed result and state when a result is sampled or approximate.

## SQL Contract

For SQL Insights, follow the live MCP schema for the SQL definition, variables, and visualization contract. Map chart axes to aliases actually returned by the query; visualization options alone do not define them.

Validate the SQL by running a bounded form through `query_lakehouse` before rendering. Keep variables explicit and ensure defaults produce a valid, useful view.

For semantic, funnel, retention, and segmentation Insights, use the matching definition from the live schema. Supply the required timeframe and interval when rendering product-behavior definitions.

## Workflow

1. Inspect the source objects and use `list_insights` to find reusable or conflicting existing work.
2. Build the smallest definition that answers the intended reusable question.
3. Render it and verify values, labels, axes, filters, variables, and empty states.
4. Create or update only after intent and permissions are clear.
5. Execute the saved Insight with `view_insight` and verify the returned definition and results.

Use a stable descriptive title rather than encoding a transient conclusion. Describe the metric, population, timeframe behavior, and important caveats. Do not copy source data or credentials into descriptions.
