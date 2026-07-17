# Cohort Comparison Patterns

Altertable MCP exposes cohort comparisons through segmentation insights. It does not expose a separate cohort or audience creation tool.

## Compare Paid Plans

```yaml
kind: segmentation
title: Weekly feature usage by paid plan
from: "2026-06-01T00:00:00Z"
to: "2026-07-01T00:00:00Z"
interval: weekly
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

## Compare Regions

```yaml
segmentation_definition:
  events:
    - key: purchases-by-country
      name: purchase_completed
      breakdowns:
        - trait: country
          limit: 10
          include_other: true
```

## Filter High-Value Events

```yaml
segmentation_definition:
  events:
    - key: high-value-purchases
      name: purchase_completed
      property_filters:
        - property: amount
          operator: ">="
          values: [1000]
```

## Filter One Event Series by a Saved Segment

Find the segment slug with `search_entities`. Pass a nonempty `query` such as the segment name or description and `node_types: [segment]`, then apply the returned slug to the event series:

```yaml
segmentation_definition:
  events:
    - key: enterprise-feature-usage
      name: feature_used
      segment_filters:
        - segment_slug: SGM-123
          including: true
```

## Compare Saved Segments Across Event Series

Top-level `segmented_by` groups apply their filters across the event series:

```yaml
segmentation_definition:
  events:
    - key: feature-usage
      name: feature_used
  segmented_by:
    - key: enterprise
      filters:
        - segment_filter:
            segment_slug: SGM-123
            including: true
    - key: self-serve
      filters:
        - segment_filter:
            segment_slug: SGM-456
            including: true
```

Render the insight first. Save it only when the user wants a persistent chart.
