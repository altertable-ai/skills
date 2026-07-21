# Insight Selection Reference

Detailed guide for choosing the right insight type.

## Insight Types Overview

| Type | Purpose | Data Source | Best For |
|------|---------|-------------|----------|
| Funnel | Conversion analysis | Events | Step-by-step flows |
| Retention | Return behavior | Events | Churn/repeat analysis |
| Semantic | Metric analysis | Semantic model | Standard analytics |
| SQL | Custom queries | Raw tables | Identity rows and custom/unmodeled needs |
| Segmentation | Event comparison | Events + traits | Aggregate behavior by properties or traits |

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
✓ Inline measure calculations on modeled tables

### When NOT to Use

✗ Data not in semantic model
✗ Joins not covered by modeled relations
✗ Calculations that need an unsupported grain or window
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

✓ Unmodeled or custom joins required
✓ Calculations that need an unsupported grain or window
✓ Data not in semantic model
✓ One-off analysis
✓ Raw data exploration
✓ Aggregations not expressible as an inline measure on a modeled table

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

- "Join orders with inventory when no modeled relation exists" → SQL
- "Custom LTV calculation" → SQL
- "Query the raw events table" → SQL
- "Calculate 90-day rolling average" → SQL

## Segmentation Insight Deep Dive

### When to Use

✓ Comparing aggregate event metrics across properties or traits
✓ Breaking down an event series by an event property or user trait
✓ Comparing behavior for existing cohorts or segments
✓ Filtering aggregate event series

### When NOT to Use

✗ Non-event metrics already defined in the semantic layer (use semantic)
✗ Flow analysis (use funnel)
✗ Custom queries (use SQL)
✗ Returning individual users or membership lists (use SQL)

### Signal Words

| Strong Signal | Moderate Signal |
|---------------|-----------------|
| event behavior by | segment |
| compare cohorts | group comparison |
| breakdown | property or trait |

### Example Questions → Segmentation

- "Compare purchase activity for free and paid plans" → Segmentation
- "Compare churned users with active users by feature usage" → Segmentation
- "Break down signup events by engagement level" → Segmentation

## Non-Analysis Responses

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
  ├─NO──► RESPOND WITHOUT DISCOVERY
  │
  ▼ YES
Is it about user steps/journey?
  │
  ├─YES──► FUNNEL INSIGHT
  │
  ▼ NO
Does it require individual rows or a membership list?
  │
  ├─YES──► SQL INSIGHT
  │
  ▼ NO
Is it about comparing aggregate event behavior across groups?
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
| "Conversion by country" | Funnel with an event property or user trait breakdown |
| "Revenue from high-value segment" | Semantic with an existing segment filter |
| "Custom metric trend" | Semantic with an inline measure on a modeled table; SQL when the calculation is unsupported |
| "LTV for users who converted" | SQL unless the converter group is already modeled as a segment |
