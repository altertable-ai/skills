# Dimensions and Breakdowns

Segmentation insights compare event series through event properties and user traits. Discover valid names with `list_events` and `list_user_traits`.

## Event Properties

Filter a property on an event series:

```yaml
segmentation_definition:
  events:
    - key: purchases-by-currency
      name: purchase_completed
      property_filters:
        - property: currency
          operator: "="
          values: [EUR]
```

Break down results by a property:

```yaml
segmentation_definition:
  events:
    - key: page-views
      name: page_view
      breakdowns:
        - property: page_path
          limit: 20
          include_other: true
```

## User Traits

Filter or break down by identity traits:

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
```

A breakdown must specify either `property` or `trait`, never both.
