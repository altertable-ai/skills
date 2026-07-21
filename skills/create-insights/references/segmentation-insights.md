# Segmentation Insights

Segmentation Insights analyze event series over time. Each event requires a unique `key`. Property and trait filters, and breakdowns, belong inside that event entry.

## Minimal Shape

```yaml
kind: segmentation
title: Daily product views
from: "2026-06-01T00:00:00Z"
to: "2026-07-01T00:00:00Z"
interval: daily
segmentation_definition:
  events:
    - key: product-views
      name: product_viewed
```

## Compare Events

```yaml
segmentation_definition:
  events:
    - key: product-views
      name: product_viewed
    - key: purchases
      name: purchase_completed
```

## Filter and Break Down

```yaml
segmentation_definition:
  events:
    - key: feature-usage
      name: feature_used
      user_trait_filters:
        - trait: plan
          operator: in
          values: [pro, enterprise]
      breakdowns:
        - trait: plan
          limit: 10
          include_other: true
```

Use `list_events` and `list_user_traits` to confirm names. Read the live schema before overriding aggregation defaults.
