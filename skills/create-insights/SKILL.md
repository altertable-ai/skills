---
name: create-insights
compatibility: Requires Altertable MCP server
description: Creates, drafts, renders, and saves Altertable insights. Use when generating findings, creating visualizations, or saving and sharing analysis results.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Creating Insights

## Quick Start

1. Choose SQL, semantic, segmentation, funnel, or retention.
2. Discover valid tables, measures, dimensions, events, and traits.
3. Call `render_insight` to validate the definition without saving it.
4. Call `create_insight` only when the user wants a persistent chart.

## When to Use This Skill

- The user asks to save or share an analysis
- A finding needs a chart or table
- The user wants to preview or draft an Insight
- An existing query should become a reusable Insight

## Choose the Insight Kind

| Kind | Use when |
| --- | --- |
| `sql` | The analysis needs custom DuckDB SQL, unmodeled joins, or an unsupported grain or window |
| `semantic` | The requested metric, dimensions, relations, or inline measure fit the semantic layer |
| `segmentation` | The user wants event metrics over time, filters, or property and trait breakdowns |
| `funnel` | The user wants conversion through chronological event steps |
| `retention` | The user wants to know whether users return after a starting event |

Use the `decide-actions` skill when the correct kind remains ambiguous.

## Shared Input Contract

Every call requires:

- `title`: human-readable and no longer than 80 characters
- `kind`: one supported kind
- the matching definition field or `sql_statement`

`description` is optional. `visualization_options` is optional when rendering and for saved funnel, segmentation, and retention Insights. Saved semantic Insights require `visualization_options`. Saved SQL Insights require both `sql_parameters` and `visualization_options`.

When rendering funnel, segmentation, or retention Insights, `render_insight` requires top-level `from`, `to`, and `interval` values. Rendered funnel and segmentation Insights can also use `compare_to`. Saved Insights do not consume these preview-only fields.

The live MCP schema is the source of truth for nested options and enum values.

## SQL Insight

Validate the query with `query_lakehouse`, then render it:

```yaml
kind: sql
title: Daily revenue
sql_statement: |
  SELECT order_date, SUM(revenue) AS revenue
  FROM commerce.main.orders
  GROUP BY order_date
  ORDER BY order_date
```

## Semantic Insight

Use `get_catalog` to discover the exact projection names:

```yaml
kind: semantic
title: Orders by country
semantic_definition:
  dimension_refs:
    - catalog: commerce
      schema: public
      table: orders
      projection: country
  measure_refs:
    - measure_reference:
        catalog: commerce
        schema: public
        table: orders
        projection: count
```

## Segmentation Insight

Each event series requires a unique `key`. Property and trait filters, and breakdowns, belong inside that series:

```yaml
kind: segmentation
title: Feature usage by plan
from: "2026-06-01T00:00:00Z"
to: "2026-07-01T00:00:00Z"
interval: daily
segmentation_definition:
  events:
    - key: feature-usage
      name: feature_used
      breakdowns:
        - trait: plan
```

## Funnel Insight

List events chronologically. Use `completed_within_seconds` when the journey has a completion limit:

```yaml
kind: funnel
title: Signup conversion
from: "2026-06-01T00:00:00Z"
to: "2026-07-01T00:00:00Z"
interval: daily
funnel_definition:
  events:
    - key: signup-started
      name: signup_started
    - key: signup-completed
      name: signup_completed
  completed_within_seconds: 86400
```

## Retention Insight

```yaml
kind: retention
title: Weekly product retention
from: "2026-06-01T00:00:00Z"
to: "2026-07-01T00:00:00Z"
interval: weekly
retention_definition:
  start_event:
    key: signup-completed
    name: signup_completed
  returning_event:
    key: product-opened
    name: product_opened
```

## Workflow

### Preview

Use `render_insight` for an ephemeral result or `draft_insight` while the user is iterating in the UI. Confirm that the data, period, and grouping match the request.

### Save

Use `create_insight` only after the preview is correct and the user wants persistence. Use a concise title and a description that explains what the Insight measures.

### Share a Finding

Create a discovery separately when the result is a meaningful change, anomaly, root cause, or recommendation that should enter review.

## Common Pitfalls

- Saving before rendering the definition
- Sending a definition that does not match `kind`
- Omitting top-level time fields when rendering funnel, segmentation, or retention
- Copying event names, trait names, or semantic projections without discovery
- Passing visualization settings outside `visualization_options`
- Creating an Insight when the user only asked for an ad hoc answer

## References

- [SQL insights](references/sql-insights.md)
- [Semantic insights](references/semantic-insights.md)
- [Segmentation insights](references/segmentation-insights.md)
- [Funnel insights](references/funnel-insights.md)
