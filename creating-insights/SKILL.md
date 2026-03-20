---
name: creating-insights
compatibility: Requires Altertable MCP server
description: Creates discoveries with insights that flow through the approval workflow. Use when generating findings, creating visualizations, surfacing patterns, or when the user asks to save or share analysis results.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Creating Insights

## Quick Start

To create an insight:
1. Analyze data to identify a finding
2. Choose the appropriate insight type (SQL, Semantic, Segmentation, Funnel, Retention, FYI)
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
| Segmentation | Event metrics over time, compared across property-based segments | Yes |
| Funnel | Conversion analysis | Yes |
| Retention | Do users come back after an event? | Yes |
| FYI | Informational findings | No |

## Core Workflow

### Step 1: Identify the Finding

Before creating an insight:
- What is the key observation?
- Is it significant enough to share?
- What action should it drive?

### Step 2: Choose Insight Type

Before choosing, triage through these questions:

1. **Does this need a visualization?** No → **FYI**. Yes → continue.
2. **Is the metric available in the semantic layer?** Yes → **Semantic**. Not sure → check the model first.
3. **Is the finding about sequential user behavior** (steps, conversion, drop-off)? Yes → **Funnel**.
4. **Is the finding about whether users come back** after a starting event? Yes → **Retention**.
5. **Is the finding about comparing event metrics across cohorts or property breakdowns** (without ordered step dependencies)? Yes → **Segmentation**.
6. **Does it require custom joins, calculations, or raw data not covered above?** Yes → **SQL**.

Select based on the analysis:
- **Funnel Insight**: Sequential steps, progression, conversion, drop-off between stages
- **Retention Insight**: Whether users return after a starting event (start event → returning event over time)
- **Semantic Insight**: Standard metrics from semantic models, trends, breakdowns
- **SQL Insight**: Custom query with specific logic, joins, calculations not in the semantic layer
- **Segmentation Insight**: Event analysis over time with breakdowns by event, user, or session properties to compare segment behavior
- **FYI Discovery**: Text-only observations, no visualization needed

See the [`deciding-actions`](../deciding-actions/SKILL.md) skill for the full decision matrix and disambiguation rules.

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

For segment and cohort comparisons:

```
1. Select the events/metrics to analyze
2. Choose aggregation (count, unique users, sum, average)
3. Add breakdowns by event, user, or session properties
4. Set filters and time range
5. Preview segment results
6. Create discovery
```

### Segmentation Parameters

- `event_definitions`: Which events to analyze
- `aggregation_mode`: How to aggregate results (count, unique users, sum, average)
- `breakdowns`: Properties used to compare segments
- `filters`: Segment/filter criteria
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

## Creating Retention Insights

For analyzing whether users come back after a starting event:

```
1. Define the start event
2. Define the returning event
3. Set time range
4. Preview retention results
5. Create discovery
```

### Retention Parameters

- `start_event`: The initial event that begins the retention window
- `returning_event`: The event that counts as a return
- `timeframe`: Analysis period

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

**Descriptions must be 200 characters or less.**

Include:
- **What**: The key observation
- **Context**: Comparison or benchmark
- **Impact**: Business significance
- **Recommendation**: Suggested action (if space permits)

### Example

> Mobile conversion dropped 20% (3.2% to 2.5%) last month, coinciding with the March 1st checkout redesign. Consider A/B testing the previous flow.

## Visualization Selection

| Data Type | Recommended |
|-----------|-------------|
| Time series | Line, Area |
| Comparison | Bar, BarList |
| Distribution | Pie, Bar |
| Single metric | Metric |
| Detailed data | Table |
| Funnel | Funnel (built-in) |
| Retention | Retention (built-in) |

## Common Pitfalls

- Creating insights without clear value
- Vague titles that don't convey the finding
- Missing context in descriptions
- Wrong visualization for data type
- Not previewing before creating
- Creating duplicates of existing insights

## Troubleshooting Rejected Discoveries

**If `admin_rejected`:**
- Review admin feedback for rejection reason
- Check if finding meets quality threshold
- Refine: make title more specific, add context to description
- Re-create with improvements

**If `rejected` by user:**
- Finding may not be actionable enough
- Consider: Is the insight significant? Is timing relevant?
- Refine: strengthen the "so what" - why should they care?
- Add clearer recommendation or next step

**Common rejection reasons and fixes:**

| Reason | Fix |
|--------|-----|
| "Already known" | Search for existing insights before creating |
| "Not actionable" | Add specific recommendation |
| "Too vague" | Include concrete numbers and timeframes |
| "Wrong audience" | Check if insight matches user's domain |
| "Stale data" | Verify timeframe is current |

## Reference Files

- [SQL insights](references/sql-insights.md)
- [Semantic insights](references/semantic-insights.md)
- [Segmentation insights](references/segmentation-insights.md)
- [Funnel insights](references/funnel-insights.md)
- [Retention insights](references/retention-insights.md)
- [FYI discoveries](references/fyi-discoveries.md)
