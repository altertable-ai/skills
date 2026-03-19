---
name: analyzing-charts
compatibility: Requires Altertable MCP server
description: Interprets chart data to identify patterns, anomalies, and trends. Use when analyzing visualizations, extracting insights from charts, explaining what data shows, or when asked about patterns in graphs.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Analyzing Charts

## Quick Start

When analyzing a chart:
1. Identify the chart type and what it measures
2. Look for patterns (trends, seasonality, anomalies)
3. Quantify observations with specific numbers
4. Provide actionable interpretation

## When to Use This Skill

- User asks "what does this chart show?"
- Analyzing visualization results
- Identifying trends or anomalies
- Explaining patterns in data
- Generating insights from visual data

## Chart Types

| Type | Best For | Look For |
|------|----------|----------|
| Line | Time series trends | Direction, inflection points |
| Bar | Category comparison | Relative sizes, outliers |
| Area | Volume over time | Growth, composition |
| Pie | Distribution | Proportions, dominance |
| Table | Detailed data | Patterns, sorting |
| Metric | Single values | Change from baseline |
| BarList | Ranked items | Top performers, long tail |

## Analysis Framework

### 1. Describe What You See

Start with objective observations:
- What is being measured?
- What is the time range?
- What are the key dimensions?

### 2. Identify Patterns

Look for:
- **Trends**: Upward, downward, flat
- **Seasonality**: Weekly, monthly, yearly cycles
- **Anomalies**: Spikes, drops, outliers
- **Inflection points**: Where direction changes

### 3. Quantify Observations

Always include numbers:
- Absolute values
- Percentage changes
- Comparisons to baselines

### 4. Provide Interpretation

Explain significance:
- Why might this be happening?
- What are the implications?
- What actions should be considered?

## Pattern Recognition

### Trend Patterns

#### Upward Trend
- Consistent growth over time
- Look for: slope, acceleration/deceleration
- Note: sustainability, growth rate

#### Downward Trend
- Consistent decline over time
- Look for: rate of decline, stabilization
- Note: severity, projected impact

#### Flat/Stable
- No significant change
- Look for: volatility within range
- Note: whether stability is expected

### Seasonality Patterns

#### Weekly Cycles
- Weekday vs weekend differences
- Monday dips, Friday spikes
- Note: business day patterns

#### Monthly Cycles
- Beginning/end of month patterns
- Billing cycles, payroll effects
- Note: calendar effects

#### Yearly Cycles
- Holiday impacts
- Seasonal business patterns
- Note: YoY comparisons

### Anomaly Patterns

#### Spikes
- Sudden increase
- Look for: magnitude, duration
- Consider: campaigns, events, bugs

#### Drops
- Sudden decrease
- Look for: recovery pattern
- Consider: outages, issues, seasonality

#### Outliers
- Values far from normal range
- Look for: explanation
- Consider: data quality, real events

## Analysis by Chart Type

### Line Charts

Focus on:
- Overall trend direction
- Volatility/smoothness
- Inflection points
- Comparisons between lines

Questions to answer:
- Is the metric growing or declining?
- Are there regular patterns?
- Where are the peaks and troughs?

### Bar Charts

Focus on:
- Relative bar heights
- Ordering (if applicable)
- Gaps between categories
- Outlier categories

Questions to answer:
- Which category leads/lags?
- Is distribution expected?
- Are there surprising values?

### Pie Charts

Focus on:
- Dominant segments
- Small segments
- Unexpected proportions

Questions to answer:
- Is any segment too dominant?
- Are proportions as expected?
- Has composition changed?

### Tables

Focus on:
- Sorting patterns
- Extreme values
- Null/missing data
- Relationships between columns

Questions to answer:
- What patterns emerge?
- Are there data quality issues?
- What correlations exist?

## Quantification Guidelines

### Describing Changes

| Change | Description |
|--------|-------------|
| +/-5% | Slight change |
| +/-10-20% | Moderate change |
| +/-20-50% | Significant change |
| +/-50%+ | Dramatic change |
| 2x | Doubled |
| 3x | Tripled |

### Time Comparisons

- **WoW**: Week-over-week
- **MoM**: Month-over-month
- **QoQ**: Quarter-over-quarter
- **YoY**: Year-over-year

### Statistical Context

- Compare to historical average
- Note standard deviation if known
- Reference typical ranges

## Communication Patterns

### Good Insight Format

```
[What]: Revenue increased 23% this week
[Context]: From $45,000 to $55,350
[Comparison]: This is 15% above the 4-week average
[Interpretation]: Likely driven by the holiday promotion
[Recommendation]: Consider extending the campaign
```

### Avoid Vague Statements

| Bad | Good |
|-----|------|
| "Revenue went up" | "Revenue increased 23% to $55,350" |
| "There's a trend" | "Daily active users grew 5% WoW for 6 consecutive weeks" |
| "Something changed" | "Conversion dropped from 3.2% to 2.1% on March 15" |

## Common Pitfalls

- Making claims without numbers
- Ignoring context (seasonality, events)
- Confusing correlation with causation
- Over-interpreting normal variance
- Missing obvious anomalies
- Not considering data quality issues

## Reference Files

- [Chart types detail](references/chart-types.md)
- [Visualizations guide](references/visualizations.md)
- [Anomaly patterns](references/anomaly-patterns.md)
