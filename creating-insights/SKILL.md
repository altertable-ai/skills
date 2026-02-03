---
name: creating-insights
compatibility: Altertable
description: Creates discoveries with insights that flow through the approval workflow. Use when generating findings, creating visualizations, surfacing patterns, or when the user asks to save or share analysis results.
---

# Creating Insights

## Quick Start

To create an insight:
1. Analyze data to identify a finding
2. Choose the appropriate insight type (SQL, Semantic, Segmentation, Funnel, FYI)
3. Preview the insight to validate
4. Create the discovery with visualization

## When to Use This Skill

- Found a notable pattern or anomaly
- User asks to save or share findings
- Creating a visualization from analysis
- Surfacing automated discoveries
- Generating reports or dashboards content

## Insight Types

| Type | Use Case | Visualization |
|------|----------|---------------|
| SQL | Custom query results | Yes |
| Semantic | Metrics from semantic layer | Yes |
| Segmentation | User cohort analysis | Yes |
| Funnel | Conversion analysis | Yes |
| FYI | Informational findings | No |

## Core Workflow

### Step 1: Identify the Finding

Before creating an insight:
- What is the key observation?
- Is it significant enough to share?
- What action should it drive?

### Step 2: Choose Insight Type

Select based on the analysis:
- **SQL Insight**: Custom query with specific logic
- **Semantic Insight**: Standard metrics from semantic models
- **Segmentation Insight**: User segments and cohorts
- **Funnel Insight**: Step-by-step conversion analysis
- **FYI Discovery**: Text-only observations

### Step 3: Preview and Validate

Always preview before creating:
- Verify data is correct
- Check visualization renders properly
- Ensure timeframe is appropriate

### Step 4: Create Discovery

Create with:
- Clear, actionable title
- Concise description
- Appropriate visualization
- Relevant metadata

## Discovery States

Discoveries flow through an approval workflow:

```
pending_visualization_generation
         ↓
    pending_admin_review  →  admin_rejected
         ↓
    pending_review
         ↓
  accepted | rejected | ignored
```

### States Explained

| State | Description |
|-------|-------------|
| `pending_visualization_generation` | Generating chart |
| `pending_admin_review` | Awaiting admin approval |
| `pending_review` | Awaiting user review |
| `accepted` | User accepted the finding |
| `rejected` | User rejected as not useful |
| `ignored` | User ignored/dismissed |
| `admin_rejected` | Admin filtered out |

## Creating SQL Insights

For custom query-based insights:

```
1. Write and validate SQL query
2. Preview SQL insight with the query
3. Choose appropriate visualization
4. Create discovery with insight
```

### SQL Insight Parameters

- `query`: The SQL query
- `connection_slug`: Which connection to query
- `visualization`: Chart type (Line, Bar, Table, etc.)

### Best Practices

- Use CTEs for readability
- Include time filters
- Limit result size for performance
- Add column aliases for display

## Creating Semantic Insights

For metrics from the semantic layer:

```
1. Select source and measures
2. Add dimensions for grouping
3. Apply filters
4. Preview and validate
5. Create discovery
```

### Semantic Insight Parameters

- `source_slug`: Semantic source to query
- `measures`: List of measures to aggregate
- `dimensions`: Dimensions for grouping
- `filters`: Filter conditions
- `visualization`: Chart type

## Creating Segmentation Insights

For user cohort analysis:

```
1. Define the segment criteria
2. Choose primary dimension
3. Set time range
4. Preview segment results
5. Create discovery
```

### Segmentation Parameters

- `primary_dimension_ref`: Main grouping dimension
- `filters`: Segment criteria
- `timeframe`: Analysis period

## Creating Funnel Insights

For conversion analysis:

```
1. Define funnel steps (events)
2. Set conversion window
3. Choose ordering (strict/any)
4. Preview funnel metrics
5. Create discovery
```

### Funnel Parameters

- `steps`: Ordered list of events
- `conversion_window`: Time allowed between steps
- `ordering`: Strict sequence or any order

## Creating FYI Discoveries

For informational findings without visualization:

```
1. Write clear title
2. Provide detailed description
3. Add supporting context
4. Create FYI discovery
```

### FYI Use Cases

- Text-based observations
- Recommendations
- Warnings or alerts
- Context for other findings

## Writing Effective Titles

Good titles are:
- **Actionable**: "Revenue dropped 15% last week"
- **Specific**: Include key metric and timeframe
- **Concise**: Under 100 characters

### Examples

| Good | Bad |
|------|-----|
| "Mobile conversion rate dropped 20% in Q4" | "Conversion issue" |
| "New users from organic search up 3x" | "Traffic increase" |
| "Cart abandonment spikes on weekends" | "Weekend pattern" |

## Writing Descriptions

Include:
- **What**: The key observation
- **Context**: Comparison or benchmark
- **Impact**: Business significance
- **Recommendation**: Suggested action

### Example

> Mobile conversion rate dropped from 3.2% to 2.5% over the past month,
> a 20% decline. This coincides with the checkout redesign launched on
> March 1st. Consider A/B testing the previous checkout flow.

## Visualization Selection

| Data Type | Recommended |
|-----------|-------------|
| Time series | Line, Area |
| Comparison | Bar, BarList |
| Distribution | Pie, Bar |
| Single metric | Metric |
| Detailed data | Table |
| Funnel | Funnel (built-in) |

## Common Pitfalls

- Creating insights without clear value
- Vague titles that don't convey the finding
- Missing context in descriptions
- Wrong visualization for data type
- Not previewing before creating
- Creating duplicates of existing insights

## Reference Files

- [SQL insights](references/sql-insights.md)
- [Semantic insights](references/semantic-insights.md)
- [Segmentation insights](references/segmentation-insights.md)
- [Funnel insights](references/funnel-insights.md)
- [FYI discoveries](references/fyi-discoveries.md)
