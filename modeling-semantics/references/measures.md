# Measures Reference

Complete guide to defining measures in semantic sources.

## Measure Definition

```yaml
measures:
  - name: measure_name        # Required: unique identifier
    kind: Count               # Required: aggregation type
    sql: column_expression    # Required for most kinds
    description: "..."        # Optional: human-readable description
    hidden: false             # Optional: hide from UI
    formatter: "..."          # Optional: display format
```

## Measure Kinds

### Count

Counts all rows.

```yaml
- name: total_orders
  kind: Count
  description: Total number of orders
```

Generated SQL: `COUNT(*)`

### CountDistinct

Counts unique values.

```yaml
- name: unique_users
  kind: CountDistinct
  sql: user_id
  description: Number of unique users
```

Generated SQL: `COUNT(DISTINCT user_id)`

### Sum

Sums numeric values.

```yaml
- name: total_revenue
  kind: Sum
  sql: amount
  description: Total revenue in dollars
```

Generated SQL: `SUM(amount)`

### Average

Calculates mean of values.

```yaml
- name: avg_order_value
  kind: Average
  sql: amount
  description: Average order value
```

Generated SQL: `AVG(amount)`

### Min

Finds minimum value.

```yaml
- name: first_order_date
  kind: Min
  sql: order_date
  description: Date of first order
```

Generated SQL: `MIN(order_date)`

### Max

Finds maximum value.

```yaml
- name: last_order_date
  kind: Max
  sql: order_date
  description: Date of most recent order
```

Generated SQL: `MAX(order_date)`

### Expression

Custom SQL expression for complex calculations.

```yaml
- name: conversion_rate
  kind: Expression
  sql: |
    COUNT(DISTINCT CASE WHEN converted THEN user_id END)::FLOAT /
    NULLIF(COUNT(DISTINCT user_id), 0)
  description: Percentage of users who converted
```

## Expression Patterns

### Ratio/Percentage

```yaml
- name: click_through_rate
  kind: Expression
  sql: |
    COUNT(DISTINCT CASE WHEN event ='click' THEN user_id END)::FLOAT /
    NULLIF(COUNT(DISTINCT CASE WHEN event ='impression' THEN user_id END), 0) * 100
```

### Conditional Sum

```yaml
- name: refunded_amount
  kind: Expression
  sql: SUM(CASE WHEN status = 'refunded' THEN amount ELSE 0 END)
```

### Weighted Average

```yaml
- name: weighted_score
  kind: Expression
  sql: SUM(score * weight) / NULLIF(SUM(weight), 0)
```

### Percentile

```yaml
- name: median_amount
  kind: Expression
  sql: PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount)
```

### Running Total Window

```yaml
- name: cumulative_revenue
  kind: Expression
  sql: SUM(SUM(amount)) OVER (ORDER BY date_trunc('day', created_at))
```

## NULL Handling

Always handle NULL values in expressions:

### Using NULLIF

Prevent division by zero:

```yaml
- name: avg_with_nullif
  kind: Expression
  sql: SUM(value) / NULLIF(COUNT(*), 0)
```

### Using COALESCE

Provide default values:

```yaml
- name: total_with_default
  kind: Expression
  sql: COALESCE(SUM(amount), 0)
```

### Filtering NULLs

Exclude NULL values:

```yaml
- name: non_null_count
  kind: Expression
  sql: COUNT(CASE WHEN value IS NOT NULL THEN 1 END)
```

## Formatters

### Currency

```yaml
- name: revenue
  kind: Sum
  sql: amount
  formatter: currency:USD
```

Display: $1,234.56

### Percentage

```yaml
- name: rate
  kind: Expression
  sql: ...
  formatter: percent
```

Display: 45.67%

### Number

```yaml
- name: count
  kind: Count
  formatter: number
```

Display: 1,234,567

## Hidden Measures

Hide measures used only for calculations:

```yaml
- name: _total_for_calc
  kind: Sum
  sql: amount
  hidden: true
```

## Combining Measures

Create derived measures using Expression:

```yaml
measures:
  - name: total_orders
    kind: Count

  - name: completed_orders
    kind: Expression
    sql: COUNT(CASE WHEN status = 'completed' THEN 1 END)

  - name: completion_rate
    kind: Expression
    sql: |
      COUNT(CASE WHEN status = 'completed' THEN 1 END)::FLOAT /
      NULLIF(COUNT(*), 0) * 100
```

## Best Practices

### Naming

- Use descriptive names: `total_revenue` not `sum1`
- Include unit if relevant: `revenue_usd`, `duration_minutes`
- Use prefixes for related measures: `order_count`, `order_value`

### Descriptions

- Explain what the measure represents
- Include calculation details for Expression
- Note any filters or conditions

### Performance

- Prefer built-in kinds over Expression when possible
- COUNT DISTINCT can be expensive on large datasets
- Consider approximate functions for large-scale analytics

### Testing

Before deploying:
1. Verify SQL syntax is valid
2. Check NULL handling
3. Test with sample data
4. Verify expected values
