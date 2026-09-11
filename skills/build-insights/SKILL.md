---
name: build-insights
compatibility: Requires Altertable MCP server; saving or updating requires read-write access
description: "Renders, drafts, creates, and updates Altertable Insights. Use when the user wants a reusable SQL, semantic, funnel, retention, or segmentation analysis rather than a one-off answer."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Build Insights

An Insight is a persistent analysis and visualization over lakehouse data. It does not need to represent an anomaly or recommendation; it can be a reusable metric, table, or behavioral analysis.

## Choose the Definition

- **Semantic:** governed measures and dimensions already defined on a semantic model.
- **SQL:** custom DuckDB logic, joins, or calculations.
- **Funnel:** ordered product-event progression.
- **Retention:** starting and returning events across cohort offsets.
- **Segmentation:** product-event metrics over time with property breakdowns.

Inspect catalogs, semantic models, events, and traits before constructing the definition. Use the live MCP schema for exact fields and enums.

## Render, Draft, or Persist

| Intent | Tool |
| --- | --- |
| Show a non-persisted result in conversation | `render_insight` |
| Iterate in the Altertable UI | `draft_insight` |
| Save a new Insight | `create_insight` |
| Change an existing Insight | `update_insight` |
| Execute and inspect a saved Insight | `view_insight` |

Default to rendering or drafting while the definition is unsettled. Create or update only when the user requests persistence and the MCP connection has read-write access.

## SQL Contract

For SQL Insights, follow the current tool schema: pass `kind: sql`, `sql_definition`, and `sql_parameters`. Map `x_axis_columns` and `y_axis_columns` to aliases actually returned by the query. Visualization options alone do not define the axes.

Validate the SQL by running a bounded form through `query_lakehouse` before rendering. Keep variables explicit and ensure defaults produce a valid, useful view.

For semantic, funnel, retention, and segmentation Insights, pass the definition matching `kind`. Product-behavior definitions also require the current `from`, `to`, and `interval` parameters when rendered.

## Workflow

1. Call `initialize` and inspect the source objects.
2. Use `list_insights` to find reusable or conflicting existing work.
3. Build the smallest definition that answers the intended reusable question.
4. Render or draft it and verify values, labels, axes, filters, variables, and empty states.
5. Create or update only after intent and permissions are clear.
6. Execute the saved Insight with `view_insight` and verify the returned definition and results.

Use a stable descriptive title rather than encoding a transient conclusion. Describe the metric, population, timeframe behavior, and important caveats. Do not copy source data or credentials into descriptions.
