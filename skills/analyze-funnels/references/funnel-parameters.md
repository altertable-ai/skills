# Funnel Parameters

Use the `render_insight` or `create_insight` MCP schema. Both calls require a funnel definition. Use at least two events to measure conversion through a journey. A rendered funnel requires top-level `from`, `to`, and `interval` values. A saved funnel does not consume these preview-only fields.

## Minimal Rendered Funnel

```yaml
kind: funnel
title: Signup funnel
from: "2026-06-01T00:00:00Z"
to: "2026-07-01T00:00:00Z"
interval: daily
funnel_definition:
  events:
    - key: signup-started
      name: signup_started
    - key: signup-completed
      name: signup_completed
```

Events are evaluated chronologically in the order listed.

## Completion Window

Set the maximum seconds allowed between the first and final events:

```yaml
funnel_definition:
  events:
    - key: checkout-started
      name: checkout_started
    - key: purchase-completed
      name: purchase_completed
  completed_within_seconds: 1800
```

Omit `completed_within_seconds` when no maximum completion time is required.

## Event Property Filters

Each event can filter event properties, user traits, or semantic segments. Property and trait filters use an operator plus a `values` array.

```yaml
funnel_definition:
  events:
    - key: product-viewed
      name: product_viewed
      property_filters:
        - property: category
          operator: "="
          values: [books]
    - key: purchase-completed
      name: purchase_completed
      user_trait_filters:
        - trait: plan
          operator: in
          values: [pro, enterprise]
```

Use `list_events` and `list_user_traits` to confirm names. Read the live MCP schema for the complete operator set.

## Breakdowns

Use `breakdowns` on the funnel definition to compare an event property or user trait:

```yaml
funnel_definition:
  events:
    - key: signup-started
      name: signup_started
    - key: signup-completed
      name: signup_completed
  breakdowns:
    - property: device_type
      limit: 10
      include_other: true
```

When rendering, keep the analysis period in the top-level `from`, `to`, and `interval` fields.
