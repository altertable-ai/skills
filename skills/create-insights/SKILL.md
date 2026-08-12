---
name: create-insights
compatibility: Requires Altertable MCP server
description: "Drafts, renders, and saves insights of every type (SQL, semantic, segmentation, funnel, retention). Use to build, preview, or share a visualization. Returns a saved insight."
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Creating Insights

## Quick Start

To create an insight:

1. Analyze data to identify a finding
2. Choose the appropriate insight type (SQL, Semantic, Segmentation, Funnel, Retention)
3. Render or draft the insight to validate it
4. Save the insight with `create_insight` when the user wants a persistent chart

## When to Use This Skill

- Found a notable pattern or anomaly
- User asks to save or share findings
- Creating a visualization from analysis
- Generating reports or dashboards content

## Insight Types

| Type         | Use Case                                                         | Visualization |
| ------------ | ---------------------------------------------------------------- | ------------- |
| SQL          | Custom query results                                             | Yes           |
| Semantic     | Metrics from semantic layer                                      | Yes           |
| Segmentation | Event metrics over time, compared across property-based segments | Yes           |
| Funnel       | Conversion analysis                                              | Yes           |
| Retention    | Do users come back after an event?                               | Yes           |

## Core Workflow

### Step 1: Identify the Finding

Before creating an insight:

- What is the key observation?
- Is it significant enough to share?
- What action should it drive?

### Step 2: Choose Insight Type

Before choosing, triage through these questions:

1. **Is the metric available in the semantic layer?** Yes → **Semantic**. Not sure → check the model first.
2. **Is the finding about sequential user behavior** (steps, conversion, drop-off)? Yes → **Funnel**.
3. **Is the finding about whether users come back** after a starting event? Yes → **Retention**.
4. **Is the finding about comparing event metrics across cohorts or property breakdowns** (without ordered step dependencies)? Yes → **Segmentation**.
5. **Does it require custom joins, calculations, or raw data not covered above?** Yes → **SQL**.

Select based on the analysis:

- **Funnel Insight**: Sequential steps, progression, conversion, drop-off between stages
- **Retention Insight**: Whether users return after a starting event (start event → returning event over time)
- **Semantic Insight**: Standard metrics from semantic models, trends, breakdowns
- **SQL Insight**: Custom query with specific logic, joins, calculations not in the semantic layer
- **Segmentation Insight**: Event analysis over time with breakdowns by event, user, or session properties to compare segment behavior

See the [`decide-actions`](../decide-actions/SKILL.md) skill for the full decision matrix and disambiguation rules.

### Step 3: Preview and Validate

Always render or draft before creating:

- Verify data is correct
- Check visualization renders properly
- Ensure timeframe is appropriate

Use `render_insight` when the user wants to inspect a chart without saving it. Use `draft_insight` when the user is iterating on a chart in the UI. Use `create_insight` only when the user wants a saved insight.

### Step 4: Save the Output

Use the current MCP tools:

- `create_insight` saves SQL, semantic, segmentation, funnel, or retention insights. Dispatch on `kind` and provide the matching definition (`sql_statement`, `semantic_definition`, `segmentation_definition`, `funnel_definition`, or `retention_definition`).

Create each saved insight with:

- Clear, actionable title
- Concise description
- Appropriate visualization
- Relevant metadata

## Creating SQL Insights

For custom query-based insights:

```
1. Write and validate SQL query
2. Render SQL insight with the query
3. Choose appropriate visualization
4. Create insight
```

### SQL Insight Parameters

- `kind`: `sql`
- `sql_statement`: The DuckDB SQL query
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
5. Create insight
```

### Semantic Insight Parameters

- `kind`: `semantic`
- `semantic_definition`: Semantic model, measures, dimensions, filters, and visualization settings
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
5. Render segment results
6. Create insight
```

### Segmentation Parameters

- `kind`: `segmentation`
- `segmentation_definition`: Events, aggregation, breakdowns, filters, and visualization settings
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
4. Render funnel metrics
5. Create insight
```

### Funnel Parameters

- `kind`: `funnel`
- `funnel_definition`: Steps, filters, conversion window, and ordering
- `steps`: Ordered list of events
- `conversion_window`: Time allowed between steps
- `ordering`: Strict sequence or any order

## Creating Retention Insights

For analyzing whether users come back after a starting event:

```
1. Define the start event
2. Define the returning event
3. Set time range
4. Render retention results
5. Create insight
```

### Retention Parameters

- `kind`: `retention`
- `retention_definition`: Starting event, returning event, filters, and retention settings
- `start_event`: The initial event that begins the retention window
- `returning_event`: The event that counts as a return
- `timeframe`: Analysis period

## Writing Effective Titles

Good titles are:

- **Actionable**: "Revenue dropped 15% last week"
- **Specific**: Include key metric and timeframe
- **Concise**: Under 100 characters

### Examples

| Good                                       | Bad                |
| ------------------------------------------ | ------------------ |
| "Mobile conversion rate dropped 20% in Q4" | "Conversion issue" |
| "New users from organic search up 3x"      | "Traffic increase" |
| "Cart abandonment spikes on weekends"      | "Weekend pattern"  |

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

| Data Type     | Recommended          |
| ------------- | -------------------- |
| Time series   | Line, Area           |
| Comparison    | Bar, BarList         |
| Distribution  | Pie, Bar             |
| Single metric | Metric               |
| Detailed data | Table                |
| Funnel        | Funnel (built-in)    |
| Retention     | Retention (built-in) |

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
