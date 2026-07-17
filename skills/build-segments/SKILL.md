---
name: build-segments
compatibility: Requires Altertable MCP server
description: Builds segmentation insights with filters and breakdowns. Use when comparing aggregate event metrics by properties or user traits.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Building Segments

## Quick Start

To build a segmentation insight:
1. Clarify which event behavior and groups the user wants to compare
2. Select events/metrics and aggregation to compare across segments
3. Identify breakdown dimensions and filters from `get_catalog` semantic details, `list_events`, and `list_user_traits`
4. Render the segmentation insight with `render_insight` to validate
5. Save with `create_insight`, or create a discovery when the finding should enter the review/notification workflow

## When to Use This Skill

- Comparing event activity between existing groups (e.g., free vs paid, active vs churned)
- Comparing event behavior across properties (e.g., feature usage by plan, region, device)
- Filtering and breaking down aggregate event series
- Use SQL when the user needs identity rows or a membership list. There is no MCP tool for creating a saved audience

## Core Workflow

### Step 1: Understand the Objective

Ask the user (or infer from context) what behavior and groups they want to compare:
- How does feature usage differ by plan?
- Which regions generate the most purchase events?
- Is checkout activity lower for churned users than active users?

### Step 2: Identify Available Dimensions

Use the Altertable MCP server to discover which dimensions and traits are available for filtering:

- `get_catalog` for semantic dimensions, measures, and table columns
- `list_events` for event names and event statistics
- `list_user_traits` for user attributes that can drive segmentation
- `search_entities` with a nonempty `query` such as the segment name or description, plus `node_types: [segment]`, for existing segment slugs

Match the user's criteria to actual dimension or trait names.

### Step 3: Build the Segmentation Definition

A segmentation insight contains one or more event series. Each series requires a unique `key`. Property filters, trait filters, saved-segment filters, and breakdowns belong on the series. Top-level `segmented_by` groups can compare filtered cohorts across all event series.

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
      user_trait_filters:
        - trait: plan
          operator: in
          values: [pro, enterprise]
      breakdowns:
        - trait: plan
```

See [Cohort patterns](references/cohort-patterns.md) for executable examples of series-level `segment_filters` and top-level `segmented_by` comparisons.

### Step 4: Preview and Validate

Render the segmentation insight via `render_insight` to check:
- Do the event series return data at the expected scale?
- Do the aggregation and breakdown values match the user's question?
- Are edge cases handled (NULLs, test accounts)?

If the preview looks wrong, adjust filters and preview again.

### Step 5: Create the Insight

Once validated:
- Use `create_insight` with `kind: segmentation` to save the comparison as a chart
- Use `create_discovery` when the validated finding should flow through the review and notification workflow

## Filter Operators

| Category | Operators | Use for |
|----------|-----------|---------|
| Equality | `=`, `!=` | Exact match or exclusion |
| Comparison | `>`, `>=`, `<`, `<=` | Numeric and date comparisons |
| Range | `between` | Date or timestamp ranges expressed as one range object |
| String | `starts_with`, `ends_with`, `contains` and their `not_` variants | Partial text matching |
| List | `in`, `not_in` | Multiple discrete values |
| Null | `is_null`, `is_not_null` | Checking for missing data |
| IP | `ip_matches`, `ip_not_matches` | CIDR range filtering |

See [Filter operators reference](references/filter-operators.md) for detailed behavior, type rules, and examples per operator.

## Common Pitfalls

- **Not previewing before creating**: Always preview to catch filter mistakes before saving
- **Using wrong operator for the type**: For example, `contains` on a numeric property, or `>` on a string
- **Forgetting NULL handling**: Equality operators don't match NULL. Use `is_null` or `is_not_null` explicitly
- **Expecting identity rows**: Segmentation returns aggregate event series. Use SQL for individual users or memberships
- **Missing exclusion criteria**: Consider whether test accounts, internal users, or bots should be excluded
- **Not checking dimension names**: Inspect semantic model details and traits to confirm exact names before building filters

## Reference Files

- [Filter operators](references/filter-operators.md) - Read for detailed operator behavior, type rules, NULL semantics, and combining patterns
- [Dimensions and breakdowns](references/dimension-refs.md) - Read when filtering event properties or user traits
- [Cohort patterns](references/cohort-patterns.md) - Read for segmentation insight examples
