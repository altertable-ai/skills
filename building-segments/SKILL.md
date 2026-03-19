---
name: building-segments
compatibility: Requires Altertable MCP server
description: Creates user segments and cohorts using filters and dimensions. Use when segmenting users, building cohorts, filtering populations, defining audiences, or when asked about user groups.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Building Segments

## Quick Start

To build a segment:
1. Clarify what user group the user wants to isolate
2. Identify the primary dimension and filters from available semantic models
3. Preview the segmentation insight via the Altertable MCP server to validate
4. Create the segmentation insight (or segmentation insight discovery to save and share it)

## When to Use This Skill

- User asks to define a cohort or audience
- Comparing user groups (e.g., free vs paid, active vs churned)
- Filtering a population for deeper analysis
- Building a segment as input for a funnel, retention, or other insight

## Core Workflow

### Step 1: Understand the Objective

Ask the user (or infer from context) what group they want to isolate:
- Who are my most valuable users?
- Which users are at risk of churning?
- Who should receive this campaign?

### Step 2: Identify Available Dimensions

List semantic models and get connection details via the Altertable MCP server to discover which dimensions and traits are available for filtering. Match the user's criteria to actual dimension names.

### Step 3: Build the Segment Definition

A segment consists of:

```yaml
segment:
  name: segment-name
  description: Human-readable description
  primary_dimension_ref:
    source: source-slug
    name: dimension-name
  filters:
    - dimension: dimension-name
      operator: Eq
      value: "value"
```

All filters use AND logic -- every condition must be true.

### Step 4: Preview and Validate

Preview the segmentation insight via the Altertable MCP server to check:
- Is the segment size reasonable? (not zero, not everyone)
- Do the results match the user's expectation?
- Are edge cases handled (NULLs, test accounts)?

If the preview looks wrong, adjust filters and preview again.

### Step 5: Create the Insight

Once validated:
- Create a segmentation insight to save the segment as a chart
- Or create a segmentation insight discovery to save it as a discovery that flows through the approval workflow

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
- **Not checking dimension names** -- list semantic models to confirm exact dimension names before building filters

## Reference Files

- [Filter operators](references/filter-operators.md) - Read for detailed operator behavior, type rules, NULL semantics, and combining patterns
- [Dimension references](references/dimension-refs.md) - Read for dimension types, source-qualified references, JSON paths, and join behavior
- [Cohort patterns](references/cohort-patterns.md) - Read for ready-made segment definitions (lifecycle, value, subscription, behavioral, risk cohorts)
