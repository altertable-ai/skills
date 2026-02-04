# Funnel Insights Reference

Creating conversion funnel insights.

## When to Use Funnel Insights

- Analyzing conversion flows
- Identifying drop-off points
- Measuring process completion
- Optimizing user journeys

## Workflow

### 1. Define Funnel Steps

List the events in order:
1. First step (entry point)
2. Intermediate steps
3. Final step (conversion)

### 2. Set Parameters

Configure:
- Conversion window
- Ordering mode
- Time range

### 3. Preview Funnel

View:
- Step counts
- Conversion rates
- Drop-off percentages

### 4. Create Discovery

Save with funnel visualization.

## Funnel Parameters

### Required

| Parameter | Description |
|-----------|-------------|
| `steps` | Ordered list of events |

### Optional

| Parameter | Description |
|-----------|-------------|
| `conversion_window` | Time allowed between steps |
| `ordering` | Strict sequence or any order |
| `timeframe` | Analysis period |
| `filters` | Additional conditions |
| `breakdown` | Segment funnel by dimension |

## Step Definition

### Basic Steps

```yaml
steps:
  - event: page_view
  - event: add_to_cart
  - event: checkout_started
  - event: purchase_completed
```

### Steps with Filters

```yaml
steps:
  - event: page_view
    filters:
      - property: page_type
        operator: Eq
        value: "product"
  - event: add_to_cart
```

## Ordering Modes

### Strict Ordering

Events must happen in exact sequence:

```yaml
ordering: Strict
```

User must do: Step 1 → Step 2 → Step 3

### Any Ordering

Events can happen in any order:

```yaml
ordering: Any
```

User can do: Step 2 → Step 1 → Step 3 (still counts)

## Conversion Window

Time allowed for user to complete funnel:

```yaml
conversion_window:
  value: 7
  unit: days
```

### Common Windows

| Use Case | Window |
|----------|--------|
| Quick actions | 1 hour |
| Session-based | 30 minutes |
| Day-based | 24 hours |
| Consideration | 7 days |
| Long process | 30 days |

## Funnel Metrics

### Per Step

- **Entered**: Users who reached this step
- **Completed**: Users who moved to next step
- **Dropped**: Users who didn't continue
- **Conversion Rate**: % who continued

### Overall

- **Start**: Users at step 1
- **End**: Users at final step
- **Overall Conversion**: End / Start
- **Total Drop-off**: 1 - Overall Conversion

## Common Funnel Patterns

### E-commerce Checkout

```yaml
steps:
  - event: product_viewed
  - event: add_to_cart
  - event: checkout_started
  - event: payment_submitted
  - event: order_completed
conversion_window:
  value: 24
  unit: hours
ordering: Strict
```

### Signup Flow

```yaml
steps:
  - event: signup_page_viewed
  - event: signup_form_started
  - event: email_verified
  - event: profile_completed
conversion_window:
  value: 7
  unit: days
```

### Feature Adoption

```yaml
steps:
  - event: feature_discovered
  - event: feature_tried
  - event: feature_used_repeatedly
conversion_window:
  value: 14
  unit: days
```

### Onboarding

```yaml
steps:
  - event: account_created
  - event: first_project_created
  - event: first_invite_sent
  - event: first_value_moment
conversion_window:
  value: 30
  unit: days
```

## Breakdown Analysis

Segment funnel by dimension:

```yaml
breakdown:
  dimension: device_type
```

Shows separate funnels for:
- Mobile
- Desktop
- Tablet

### Common Breakdowns

- `device_type` - Compare mobile vs desktop
- `traffic_source` - Compare acquisition channels
- `user_segment` - Compare user types
- `experiment_variant` - Compare A/B tests

## Visualization

### Funnel Chart

Default visualization showing:
- Step-by-step flow
- Width proportional to count
- Drop-off between steps

### Metrics Display

Shows for each step:
- Absolute count
- Conversion rate
- Drop-off rate

### Table View

Detailed data:
- Step name
- Users entered
- Users completed
- Conversion %
- Drop-off %

## Analysis Patterns

### Identify Bottlenecks

Look for:
- Largest drop-off points
- Unexpected conversions
- Step duration outliers

### Compare Segments

Using breakdown:
- Which segment converts best?
- Where do segments diverge?
- What drives the difference?

### Track Over Time

Compare funnels across periods:
- Is conversion improving?
- Did changes help?
- Seasonal patterns?

## Best Practices

### Step Selection

- Start with clear entry point
- End with definitive conversion
- 3-7 steps is optimal
- Each step should be meaningful

### Conversion Windows

- Match user expectation
- Consider decision complexity
- Test different windows

### Interpretation

- Don't over-optimize early steps
- Consider user intent
- Look for unexpected patterns

## Troubleshooting

### Low Conversion

- Check step definitions
- Verify events are firing
- Consider conversion window

### Missing Data

- Ensure events are tracked
- Check event names exactly
- Verify time range coverage

### Unexpected Patterns

- Review step order
- Check for duplicate events
- Verify user identification
