# Semantic Insights

Semantic Insights query governed measures and dimensions. Call `get_catalog` first and copy the exact catalog, schema, table, and projection names.

## Measure and Dimension

```yaml
kind: semantic
title: Revenue by region
semantic_definition:
  dimension_refs:
    - catalog: commerce
      schema: public
      table: orders
      projection: region
  measure_refs:
    - measure_reference:
        catalog: commerce
        schema: public
        table: orders
        projection: revenue
```

## Dimension Filter

```yaml
semantic_definition:
  dimension_refs:
    - catalog: commerce
      schema: public
      table: orders
      projection: region
  measure_refs:
    - measure_reference:
        catalog: commerce
        schema: public
        table: orders
        projection: revenue
  dimension_filters:
    - dimension_ref:
        catalog: commerce
        schema: public
        table: orders
        projection: status
      operator: "="
      values: [completed]
```

Use `pivot_dimension_refs` for breakdowns and `limit` to cap result rows. Read the live MCP schema for advanced filters and custom measures.
