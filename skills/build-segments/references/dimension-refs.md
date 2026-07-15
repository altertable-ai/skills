# Dimension References

How to reference dimensions in segment filters.

## Basic Reference

### Direct Dimension

Reference a dimension from a source:

```yaml
filters:
  - dimension: status
    operator: Eq
    value: "active"
```

The dimension name must match exactly.

### Source-Qualified Reference

When dimension could be ambiguous:

```yaml
filters:
  - source: users
    dimension: status
    operator: Eq
    value: "active"
```

## Dimension Types

### String Dimensions

Text values for categorical data.

**Operators**: Eq, Ne, Contains, StartsWith, EndsWith, In, NotIn

```yaml
- dimension: country
  operator: In
  values: ["US", "CA"]
```

### Integer Dimensions

Whole numbers.

**Operators**: Eq, Ne, Gt, Gte, Lt, Lte, In, NotIn

```yaml
- dimension: age
  operator: Gte
  value: 18
```

### Float Dimensions

Decimal numbers.

**Operators**: Eq, Ne, Gt, Gte, Lt, Lte

```yaml
- dimension: score
  operator: Gte
  value: 0.5
```

### Boolean Dimensions

True/false values.

**Operators**: Eq, Ne

```yaml
- dimension: is_verified
  operator: Eq
  value: true
```

### Timestamp Dimensions

Date and time values.

**Operators**: Eq, Ne, Gt, Gte, Lt, Lte

```yaml
- dimension: created_at
  operator: Gte
  value: "2024-01-01T00:00:00Z"
```

### Date Dimensions

Date-only values.

**Operators**: Eq, Ne, Gt, Gte, Lt, Lte

```yaml
- dimension: birth_date
  operator: Lt
  value: "2000-01-01"
```

### UUID Dimensions

Unique identifiers.

**Operators**: Eq, Ne, In, NotIn

```yaml
- dimension: user_id
  operator: In
  values: ["uuid-1", "uuid-2"]
```

### JSON Dimensions

Semi-structured data.

Access nested values with arrow notation:

```yaml
- dimension: properties->>'plan'
  operator: Eq
  value: "premium"
```

## Related Dimensions

### Via Relations

Reference dimensions from related sources:

```yaml
filters:
  - source: identities
    dimension: country
    operator: Eq
    value: "US"
```

This joins through defined relations.

### Join Path

The system automatically finds the shortest join path between sources.

Example:
- Segment on `events`
- Filter by `identities.country`
- Joins via `events.user_id -> identities.id`

## Computed Dimensions

### Expression-Based

Some dimensions are computed from SQL:

```yaml
# Dimension defined as:
# sql: CASE WHEN total_spend >= 1000 THEN 'high' ELSE 'low' END

filters:
  - dimension: spend_tier
    operator: Eq
    value: "high"
```

### Breakdown Dimensions

Timestamp dimensions with breakdowns:

```yaml
- dimension: created_at
  breakdown: Month
  operator: Eq
  value: "2024-01"
```

Breakdowns: Hour, Day, Week, Month, Quarter, Year

## Common Patterns

### User Traits

```yaml
filters:
  - source: identities
    dimension: traits->>'plan'
    operator: Eq
    value: "enterprise"
```

### Event Properties

```yaml
filters:
  - source: events
    dimension: properties->>'utm_source'
    operator: Eq
    value: "google"
```

### Aggregated Metrics

When dimension represents aggregation:

```yaml
filters:
  - dimension: total_orders
    operator: Gte
    value: 5
```

## Best Practices

### Exact Names

- Use exact dimension names
- Check source definition
- Case-sensitive

### Type Matching

- String values in quotes
- Numbers without quotes
- Booleans as true/false

### NULL Awareness

- Some dimensions may be NULL
- Use IsNull/IsNotNull when relevant
- Equality doesn't match NULL

### Performance

- Filter on indexed dimensions first
- Avoid complex JSON paths
- Limit cardinality of In lists
