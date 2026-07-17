# Funnel Insights

Funnel Insights measure conversion through chronological events. Confirm event names with `list_events` before rendering.

## Required Shape

```yaml
kind: funnel
title: Checkout conversion
from: "2026-06-01T00:00:00Z"
to: "2026-07-01T00:00:00Z"
interval: daily
funnel_definition:
  events:
    - key: product-viewed
      name: product_viewed
    - key: checkout-started
      name: checkout_started
    - key: purchase-completed
      name: purchase_completed
```

Use at least two events to measure conversion through a journey.

## Completion Limit

```yaml
funnel_definition:
  events:
    - key: checkout-started
      name: checkout_started
    - key: purchase-completed
      name: purchase_completed
  completed_within_seconds: 1800
```

## Filter a Step

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
```

## Compare a Property

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
```

Render first. Save only when the user wants a persistent Insight.
