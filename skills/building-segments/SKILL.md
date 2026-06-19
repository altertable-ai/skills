---
name: building-segments
compatibility: Requires Altertable MCP server
description: Builds segmentation insights with filters, dimensions, and breakdowns. Use when segmenting users, comparing event metrics by properties, building cohorts, or defining audiences.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Building Segments

## Quick Start

To build a segment:
1. Clarify what user group the user wants to isolate
2. Select events/metrics and aggregation to compare across segments
3. Identify breakdown dimensions and filters from `get_catalog` semantic details, `list_events`, and `list_user_traits`
4. Render the segmentation insight with `render_insight` to validate
5. Save with `create_insight`, or create a discovery when the finding should enter the review/notification workflow

## When to Use This Skill

- User asks to define a cohort or audience
- Comparing user groups (e.g., free vs paid, active vs churned)
- Comparing event behavior across properties (e.g., feature usage by plan, region, device)
- Filtering a population for deeper analysis
- Building a segment as input for a funnel, retention, or other insight

## Core Workflow

### Step 1: Understand the Objective

Ask the user (or infer from context) what group they want to isolate:
- Who are my most valuable users?
- Which users are at risk of churning?
- Who should receive this campaign?

### Step 2: Identify Available Dimensions

Use the Altertable MCP server to discover which dimensions and traits are available for filtering:

- `get_catalog` for semantic dimensions, measures, and table columns
- `list_events` for event names and event statistics
- `list_user_traits` for user attributes that can drive segmentation

Match the user's criteria to actual dimension or trait names.

### Step 3: Build the Segment Definition

A segmentation setup typically includes:

```yaml
segment:
  name: segment-name
  description: Human-readable description
  event_definitions:
    - event: "event_name"
  aggregation_mode: Count
  primary_dimension_ref:
    source: source-slug
    name: dimension-name
  breakdowns:
    - source: source-slug
      name: plan_type
  filters:
    - dimension: dimension-name
      operator: Eq
      value: "value"
```

All filters use AND logic -- every condition must be true.

### Step 4: Preview and Validate

Render the segmentation insight via `render_insight` to check:
- Is the segment size reasonable? (not zero, not everyone)
- Do the results match the user's expectation?
- Are edge cases handled (NULLs, test accounts)?

If the preview looks wrong, adjust filters and preview again.

### Step 5: Create the Insight

Once validated:
- Use `create_insight` with `kind: segmentation` to save the segment as a chart
- Use `create_discovery` when the validated finding should flow through the review and notification workflow

## Filter Operators

| Category | Operators | Use for |
|----------|-----------|---------|
| Equality | `Eq`, `Ne` | Exact match or exclusion |
| Comparison | `Gt`, `Gte`, `Lt`, `Lte` | Numeric ranges, date ranges |
| String | `StartsWith`, `EndsWith`, `Contains` (and `Not` variants) | Partial text matching |
| List | `In`, `NotIn` | Multiple discrete values |
| Null | `IsNull`, `IsNotNull` | Checking for missing data |
| IP | `IpMatches`, `IpNotMatches` | CIDR range filtering |

See [Filter operators reference](references/filter-operators.md) for detailed behavior, type rules, and examples per operator.

## Common Pitfalls

- **Not previewing before creating** -- always preview to catch filter mistakes before saving
- **Using wrong operator for the type** -- e.g., `Contains` on a numeric dimension, or `Gt` on a string
- **Forgetting NULL handling** -- equality operators don't match NULL; use `IsNull`/`IsNotNull` explicitly
- **Overly broad segments** -- if the segment includes most users, the filters are likely too loose
- **Missing exclusion criteria** -- always consider whether test accounts, internal users, or bots should be excluded
- **Not checking dimension names** -- inspect semantic model details and traits to confirm exact names before building filters

## Reference Files

- [Filter operators](references/filter-operators.md) - Read for detailed operator behavior, type rules, NULL semantics, and combining patterns
- [Dimension references](references/dimension-refs.md) - Read for dimension types, source-qualified references, JSON paths, and join behavior
- [Cohort patterns](references/cohort-patterns.md) - Read for ready-made segment definitions (lifecycle, value, subscription, behavioral, risk cohorts)
