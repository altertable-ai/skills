# Segmentation Insights Reference

Creating insights from user segments and cohorts.

## When to Use Segmentation Insights

- Analyzing user groups
- Comparing cohort behavior
- Identifying user characteristics
- Building target audiences

## Workflow

### 1. Define Segment Criteria

Determine what defines the segment:
- User properties (traits)
- Behavior patterns (events)
- Combinations of both

### 2. Choose Primary Dimension

Select the main grouping:
- Time-based (signup date)
- Property-based (plan type)
- Behavior-based (first event)

### 3. Set Filters

Add conditions to narrow the population:
- Include criteria (must have)
- Exclude criteria (must not have)

### 4. Preview and Validate

Check segment size and composition.

### 5. Create Discovery

Save as insight with visualization.

## Segment Parameters

### Required

| Parameter | Description |
|-----------|-------------|
| `primary_dimension_ref` | Main grouping dimension |

### Optional

| Parameter | Description |
|-----------|-------------|
| `filters` | Segment criteria |
| `timeframe` | Analysis period |
| `comparison_segment` | Compare to another segment |

## Filter Operators

### Equality

```yaml
filters:
  - dimension: subscription_tier
    operator: Eq
    value: "premium"
```

### Comparison

```yaml
filters:
  - dimension: total_purchases
    operator: Gte
    value: 5
```

### String Matching

```yaml
filters:
  - dimension: email
    operator: Contains
    value: "@company.com"
```

### List Membership

```yaml
filters:
  - dimension: country
    operator: In
    values: ["US", "CA", "UK"]
```

### Null Checks

```yaml
filters:
  - dimension: last_purchase_date
    operator: IsNotNull
```

### IP Matching

```yaml
filters:
  - dimension: ip_address
    operator: IpMatches
    value: "192.168.0.0/16"
```

## Common Segment Patterns

### By Subscription Tier

```yaml
primary_dimension_ref: subscription_tier
filters:
  - dimension: status
    operator: Eq
    value: "active"
```

### By Signup Cohort

```yaml
primary_dimension_ref:
  name: created_at
  breakdown: Month
timeframe:
  relative: last_12_months
```

### Power Users

```yaml
primary_dimension_ref: user_id
filters:
  - dimension: event_count
    operator: Gte
    value: 100
  - dimension: last_active
    operator: Gte
    value: "2024-01-01"
```

### Churned Users

```yaml
filters:
  - dimension: last_active
    operator: Lt
    value: "2024-01-01"
  - dimension: status
    operator: Ne
    value: "cancelled"
```

### Geographic Segments

```yaml
primary_dimension_ref: country
filters:
  - dimension: region
    operator: In
    values: ["EMEA", "APAC"]
```

## Visualization

### Segment Distribution

```yaml
visualization: Pie
```

Shows proportion of each segment value.

### Segment Size Over Time

```yaml
primary_dimension_ref:
  name: created_at
  breakdown: Week
visualization: Line
```

Shows segment growth over time.

### Segment Comparison

```yaml
visualization: Bar
```

Compares segment sizes side by side.

### Detailed Breakdown

```yaml
visualization: Table
```

Full segment detail with counts.

## Advanced Patterns

### Multi-Condition Segments

Combine multiple criteria:

```yaml
filters:
  # Must be premium
  - dimension: tier
    operator: Eq
    value: "premium"
  # Must be active
  - dimension: status
    operator: Eq
    value: "active"
  # Must have purchased
  - dimension: purchase_count
    operator: Gte
    value: 1
```

### Exclusion Segments

Define who to exclude:

```yaml
filters:
  # Exclude test accounts
  - dimension: email
    operator: NotContains
    value: "@test.com"
  # Exclude internal users
  - dimension: is_internal
    operator: Ne
    value: true
```

### Behavioral Segments

Based on actions taken:

```yaml
filters:
  - dimension: has_completed_onboarding
    operator: Eq
    value: true
  - dimension: days_since_signup
    operator: Lte
    value: 7
```

## Best Practices

### Clear Definitions

- Document what defines the segment
- Be specific about criteria
- Consider edge cases

### Meaningful Comparisons

- Compare similar populations
- Control for confounding factors
- Use appropriate time windows

### Actionable Segments

- Segments should drive action
- Too many segments = analysis paralysis
- Focus on high-impact groups

### Regular Validation

- Verify segment sizes make sense
- Check for data quality issues
- Monitor for drift over time

## Troubleshooting

### Empty Segment

- Check filter logic (AND vs OR)
- Verify dimension values exist
- Widen criteria

### Unexpected Size

- Review all filter conditions
- Check for NULL handling
- Verify dimension cardinality

### Overlapping Segments

- Ensure mutually exclusive criteria
- Use explicit exclusions
- Document overlap if intentional
