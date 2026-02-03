# Funnel Parameters Reference

Configuring funnels for accurate analysis.

## Step Configuration

### Basic Steps

Define steps by event name:

```yaml
steps:
  - event_name: page_view
  - event_name: signup_started
  - event_name: signup_completed
```

### Steps with Properties

Filter steps by event properties:

```yaml
steps:
  - event_name: page_view
    filters:
      - property: page_type
        operator: Eq
        value: "landing"
  - event_name: button_click
    filters:
      - property: button_id
        operator: Eq
        value: "cta_signup"
```

### Recommended Step Count

| Use Case | Steps |
|----------|-------|
| Quick conversion | 3-4 |
| Standard funnel | 4-6 |
| Detailed journey | 6-8 |
| Complex process | 8-10 |

More steps = more detail but more noise.

## Conversion Window

### Time-Based Windows

```yaml
conversion_window:
  value: 7
  unit: days
```

Available units:
- `minutes`
- `hours`
- `days`

### Choosing the Right Window

| Journey Type | Recommended Window |
|--------------|-------------------|
| Impulse purchase | 1 hour |
| Session action | 30 minutes |
| Daily decision | 24 hours |
| Considered purchase | 7 days |
| B2B sales | 30 days |

### Window Impact

**Too short**:
- Miss legitimate conversions
- Undercount conversion rate
- Useful for urgent actions

**Too long**:
- Include unrelated conversions
- Dilute attribution
- Less actionable insights

## Ordering Mode

### Strict Ordering

Events must happen in exact sequence:

```yaml
ordering: strict
```

User journey:
```
Step 1 → Step 2 → Step 3 ✓
Step 2 → Step 1 → Step 3 ✗
```

**Use for**:
- Linear processes
- Checkout flows
- Sequential requirements

### Any Ordering

Events can happen in any order:

```yaml
ordering: any
```

User journey:
```
Step 1 → Step 2 → Step 3 ✓
Step 2 → Step 1 → Step 3 ✓
```

**Use for**:
- Non-linear journeys
- Feature exploration
- Flexible workflows

## Time Range

### Analysis Period

```yaml
timeframe:
  from: "2024-01-01"
  to: "2024-01-31"
```

### Relative Periods

```yaml
timeframe:
  relative: last_30_days
```

Options:
- `last_7_days`
- `last_14_days`
- `last_30_days`
- `last_90_days`
- `this_month`
- `last_month`

## Filters

### Global Filters

Apply to entire funnel:

```yaml
filters:
  - dimension: device_type
    operator: Eq
    value: "mobile"
```

All users in funnel must match.

### Step-Specific Filters

Apply to individual steps:

```yaml
steps:
  - event_name: page_view
    filters:
      - property: page_path
        operator: StartsWith
        value: "/products/"
```

## Breakdown Dimension

Segment funnel by a dimension:

```yaml
breakdown:
  dimension: device_type
```

Creates separate funnels per value:
- Mobile funnel
- Desktop funnel
- Tablet funnel

### Common Breakdowns

| Dimension | Insight |
|-----------|---------|
| `device_type` | Mobile vs desktop behavior |
| `traffic_source` | Channel performance |
| `user_segment` | Audience comparison |
| `experiment_variant` | A/B test results |
| `country` | Geographic differences |

## Advanced Configuration

### Exclusion Events

Exclude users who did certain actions:

```yaml
exclusions:
  - event_name: cancelled
```

### Hold-out Steps

Optional steps that don't break the funnel:

```yaml
steps:
  - event_name: checkout_started
  - event_name: apply_coupon
    optional: true
  - event_name: payment_submitted
```

### Counting Method

How to count users:

```yaml
counting: unique_users
```

Options:
- `unique_users` - Each user once
- `sessions` - Each session
- `events` - Each occurrence

## Best Practices

### Step Definition

- Use specific events
- Add property filters when needed
- Avoid ambiguous events

### Window Selection

- Match user behavior
- Test different windows
- Consider your business cycle

### Breakdown Usage

- One dimension at a time
- Low cardinality dimensions
- Meaningful segments

### Time Range

- Sufficient sample size
- Stable period (no major changes)
- Compare similar periods
