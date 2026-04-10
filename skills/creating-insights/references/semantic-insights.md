# Semantic Insights Reference

Creating insights from the semantic layer.

## When to Use Semantic Insights

- Standard metrics defined in semantic models
- Consistent business logic across reports
- Dimension-based analysis
- When SQL complexity isn't needed

## Workflow

### 1. Select Source

Choose the semantic source containing relevant measures:
- `events` for event metrics
- `pageviews` for web analytics
- Custom sources for business data

### 2. Choose Measures

Select one or more measures:
- `event_count` for totals
- `unique_users` for distinct counts
- Custom measures as defined

### 3. Add Dimensions

Group results by dimensions:
- Time dimensions with breakdowns
- Categorical dimensions
- Related dimensions via joins

### 4. Apply Filters

Filter to relevant data:
- Time range
- Specific values
- Exclude conditions

### 5. Preview and Create

Validate results and create discovery.

## Insight Parameters

### Required

| Parameter | Description |
|-----------|-------------|
| `source_slug` | Semantic source to query |
| `measures` | List of measure names |

### Optional

| Parameter | Description |
|-----------|-------------|
| `dimensions` | Grouping dimensions |
| `filters` | Filter conditions |
| `timeframe` | Time range |
| `limit` | Max results |
| `sort` | Sort order |

## Dimension Selection

### Direct Dimensions

From the selected source:

```yaml
dimensions:
  - name: event
  - name: timestamp
    breakdown: Day
```

### Related Dimensions

Via relations to other sources:

```yaml
dimensions:
  - source: identities
    name: country
```

### Timestamp Breakdowns

For time-based grouping:

```yaml
dimensions:
  - name: timestamp
    breakdown: Day  # Hour, Day, Week, Month, Quarter, Year
```

## Filter Syntax

### Equality

```yaml
filters:
  - dimension: event
    operator: Eq
    value: "purchase"
```

### Comparison

```yaml
filters:
  - dimension: amount
    operator: Gte
    value: 100
```

### Contains

```yaml
filters:
  - dimension: page_url
    operator: Contains
    value: "/checkout"
```

### In List

```yaml
filters:
  - dimension: status
    operator: In
    values: ["active", "pending"]
```

### Time Range

```yaml
timeframe:
  from: "2024-01-01"
  to: "2024-01-31"
```

## Visualization Selection

### Time Series

For timestamp dimension with breakdown:
- **Line**: Continuous trend
- **Area**: Volume over time
- **Bar**: Period comparison

### Categorical

For string dimensions:
- **Bar**: Compare categories
- **BarList**: Ranked list
- **Pie**: Distribution

### Single Value

No dimensions (aggregate only):
- **Metric**: Big number display

### Multiple Dimensions

Two dimensions:
- **Table**: Full detail
- **Grouped Bar**: Category comparison

## Common Patterns

### Daily Active Users

```yaml
source: events
measures: [unique_users]
dimensions:
  - name: timestamp
    breakdown: Day
timeframe:
  relative: last_30_days
visualization: Line
```

### Events by Type

```yaml
source: events
measures: [event_count]
dimensions:
  - name: event
visualization: BarList
```

### Users by Country

```yaml
source: events
measures: [unique_users]
dimensions:
  - source: identities
    name: country
visualization: Bar
```

### Filtered Metrics

```yaml
source: events
measures: [event_count, unique_users]
filters:
  - dimension: event
    operator: Eq
    value: "purchase"
timeframe:
  relative: last_7_days
visualization: Metric
```

## Best Practices

### Choose Appropriate Granularity

- Daily for short-term trends
- Weekly for medium-term
- Monthly for long-term

### Limit Dimensions

- 1-2 dimensions for insights
- More dimensions → use Table

### Filter Early

- Apply relevant filters
- Reduces data processed
- Improves performance

### Use Relations Wisely

- Only join when needed
- Adds query complexity
- May affect performance

## Troubleshooting

### No Data Returned

- Check filter conditions
- Verify time range
- Confirm source has data

### Unexpected Values

- Review measure definition
- Check filter logic
- Verify dimension mapping

### Slow Performance

- Narrow time range
- Reduce dimensions
- Remove unnecessary joins
