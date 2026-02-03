# Insight Selection Reference

Detailed guide for choosing the right insight type.

## Insight Types Overview

| Type | Purpose | Data Source | Best For |
|------|---------|-------------|----------|
| Funnel | Conversion analysis | Events | Step-by-step flows |
| Semantic | Metric analysis | Semantic model | Standard analytics |
| SQL | Custom queries | Raw tables | Complex/custom needs |
| Segmentation | User grouping | Events + traits | Targeting/cohorts |
| FYI | Information only | None | Acknowledgments |

## Funnel Insight Deep Dive

### When to Use

✓ User journey analysis
✓ Conversion rate calculation
✓ Drop-off identification
✓ Step completion rates
✓ Time between steps

### When NOT to Use

✗ Simple metric queries
✗ Non-sequential analysis
✗ Aggregate totals only
✗ No clear step sequence

### Signal Words

| Strong Signal | Moderate Signal |
|---------------|-----------------|
| conversion | users who completed |
| funnel | step by step |
| drop-off | journey |
| abandon | flow |
| complete rate | path |

### Example Questions → Funnel

- "What's our signup conversion rate?" → Funnel
- "Where do users drop off in checkout?" → Funnel
- "How long does onboarding take?" → Funnel
- "What % complete the tutorial?" → Funnel

## Semantic Insight Deep Dive

### When to Use

✓ Metric trends over time
✓ Dimension breakdowns
✓ Period comparisons
✓ Standard KPIs
✓ Aggregations (sum, count, avg)

### When NOT to Use

✗ Data not in semantic model
✗ Complex multi-table joins
✗ Custom calculations
✗ Raw data exploration

### Signal Words

| Strong Signal | Moderate Signal |
|---------------|-----------------|
| how many | total |
| trend | over time |
| breakdown | by category |
| compare | vs |
| daily/weekly/monthly | growth |

### Example Questions → Semantic

- "How many orders this week?" → Semantic
- "Revenue trend by month" → Semantic
- "Breakdown by country" → Semantic
- "Compare Q1 vs Q2" → Semantic

## SQL Insight Deep Dive

### When to Use

✓ Complex joins required
✓ Custom calculations
✓ Data not in semantic model
✓ One-off analysis
✓ Raw data exploration
✓ Advanced aggregations

### When NOT to Use

✗ Simple metrics (use semantic)
✗ Standard breakdowns (use semantic)
✗ Step analysis (use funnel)
✗ User grouping (use segmentation)

### Signal Words

| Strong Signal | Moderate Signal |
|---------------|-----------------|
| join | specific table |
| custom | calculate |
| raw | query |
| complex | advanced |

### Example Questions → SQL

- "Join orders with inventory" → SQL
- "Custom LTV calculation" → SQL
- "Query the raw events table" → SQL
- "Calculate 90-day rolling average" → SQL

## Segmentation Insight Deep Dive

### When to Use

✓ Defining user groups
✓ Building audiences
✓ Cohort creation
✓ Behavioral targeting
✓ User filtering

### When NOT to Use

✗ Counting metrics (use semantic)
✗ Flow analysis (use funnel)
✗ Custom queries (use SQL)

### Signal Words

| Strong Signal | Moderate Signal |
|---------------|-----------------|
| users who | segment |
| cohort | group of |
| audience | target |
| filter users | people that |

### Example Questions → Segmentation

- "Users who purchased twice" → Segmentation
- "Create a cohort of churned users" → Segmentation
- "Segment by engagement level" → Segmentation

## FYI Discovery Deep Dive

### When to Use

✓ Acknowledging input
✓ Confirming understanding
✓ Status updates
✓ No analysis needed
✓ Simple responses

### When NOT to Use

✗ User asked a question
✗ Analysis is expected
✗ Insight would add value

### Signal Words

| Strong Signal | Moderate Signal |
|---------------|-----------------|
| thanks | ok |
| got it | sure |
| understood | noted |
| will do | acknowledged |

## Decision Flowchart

```
START
  │
  ▼
Does user expect data/analysis?
  │
  ├─NO──► FYI DISCOVERY
  │
  ▼ YES
Is it about user steps/journey?
  │
  ├─YES──► FUNNEL INSIGHT
  │
  ▼ NO
Is it about defining user groups?
  │
  ├─YES──► SEGMENTATION INSIGHT
  │
  ▼ NO
Is data in semantic model?
  │
  ├─YES──► SEMANTIC INSIGHT
  │
  ▼ NO
  │
  └──────► SQL INSIGHT
```

## Mixed Scenarios

Sometimes questions need multiple approaches:

| Question | Approach |
|----------|----------|
| "Conversion by country" | Funnel + Semantic dimension |
| "Revenue from high-value segment" | Segmentation + Semantic |
| "Custom metric trend" | SQL for metric, visualize as trend |
| "Users who converted + their LTV" | Funnel + SQL join |
