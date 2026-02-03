# Chart Types Reference

Detailed guide to each chart type available in Altertable.

## SQL Charts

Custom SQL query visualized as a chart.

### When to Use
- Complex calculations
- Cross-database queries
- Ad-hoc analysis
- Custom logic

### Data Format
Query results with:
- One or more dimension columns
- One or more measure columns

### Analysis Tips
- Check SQL logic for correctness
- Verify aggregation level
- Consider query performance

## Semantic Charts

Metrics from the semantic layer.

### When to Use
- Standard business metrics
- Consistent definitions
- Reusable analysis
- Simple aggregations

### Data Format
- Dimensions from semantic sources
- Measures as defined
- Filters as specified

### Analysis Tips
- Understand measure definitions
- Check filter application
- Consider dimension cardinality

## Segmentation Charts

User cohort and segment analysis.

### When to Use
- User group comparison
- Cohort analysis
- Population breakdown
- Audience sizing

### Data Format
- Primary dimension for grouping
- Count or measure per segment
- Optional time breakdown

### Analysis Tips
- Check segment definitions
- Verify filter logic
- Consider segment overlap

## Funnel Charts

Conversion flow analysis.

### When to Use
- Conversion optimization
- User journey analysis
- Drop-off identification
- Process measurement

### Data Format
- Ordered steps
- Count per step
- Conversion rates
- Time between steps

### Analysis Tips
- Verify step definitions
- Check conversion window
- Consider ordering mode

## Visualization Types

### Line

**Best for**: Time series, trends

```
Value
  |     ___/\___
  |   _/        \
  |__/           \__
  +------------------
        Time
```

**Analysis focus**:
- Trend direction
- Rate of change
- Volatility
- Seasonality

### Bar

**Best for**: Category comparison

```
Value
  |  ___
  | |   |  ___
  | |   | |   |  ___
  | |   | |   | |   |
  +------------------------
    Cat A Cat B Cat C
```

**Analysis focus**:
- Relative sizes
- Ordering
- Outliers
- Distribution shape

### Area

**Best for**: Volume over time, stacked comparison

```
Value
  |   ████████
  |  █████████████
  | ████████████████
  +------------------
        Time
```

**Analysis focus**:
- Total volume
- Composition over time
- Growth patterns

### Pie

**Best for**: Part-to-whole relationships

```
    ╭─────────╮
   ╱     A     ╲
  │  ╲        ╱  │
  │    ╲  B ╱    │
  │      ╲╱      │
   ╲      C     ╱
    ╰─────────╯
```

**Analysis focus**:
- Dominant segments
- Distribution balance
- Small segments

### Table

**Best for**: Detailed data, multiple dimensions

```
| Category | Count | Revenue | CVR  |
|----------|-------|---------|------|
| A        | 1,234 | $45,678 | 3.2% |
| B        | 2,345 | $67,890 | 2.8% |
```

**Analysis focus**:
- Patterns across columns
- Sorting insights
- Extreme values
- Data quality

### Metric

**Best for**: Single KPIs

```
┌─────────────────┐
│     12,345      │
│   Total Users   │
│    ▲ +15%       │
└─────────────────┘
```

**Analysis focus**:
- Current value
- Change from baseline
- Goal progress

### BarList

**Best for**: Ranked lists, top N

```
Page A     ████████████  45%
Page B     ████████      32%
Page C     ████          15%
Other      ██             8%
```

**Analysis focus**:
- Top performers
- Long tail
- Concentration

## Choosing the Right Type

| Question | Chart Type |
|----------|------------|
| How does X change over time? | Line, Area |
| How do categories compare? | Bar, BarList |
| What's the distribution? | Pie, Bar |
| What's the single value? | Metric |
| Need full detail? | Table |
| Conversion flow? | Funnel |
