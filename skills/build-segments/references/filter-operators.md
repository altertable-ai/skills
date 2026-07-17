# Filter Operators

Event property and user trait filters use `operator` and `values`. Use the serialized MCP values below.

| Purpose | Operators |
| --- | --- |
| Equality | `=`, `!=` |
| Comparison | `>`, `>=`, `<`, `<=` |
| Range | `between` |
| String | `starts_with`, `not_starts_with`, `ends_with`, `not_ends_with`, `contains`, `not_contains` |
| List | `in`, `not_in` |
| Null | `is_null`, `is_not_null` |
| IP range | `ip_matches`, `ip_not_matches` |

## Event Property

```yaml
property_filters:
  - property: country
    operator: in
    values: [FR, DE]
```

## User Trait

```yaml
user_trait_filters:
  - trait: plan
    operator: "="
    values: [enterprise]
```

## Numeric Range

```yaml
property_filters:
  - property: amount
    operator: ">="
    values: [100]
  - property: amount
    operator: "<="
    values: [500]
```

## Date or Timestamp Range

`between` takes one range object inside `values`. It does not take two scalar entries.

```yaml
property_filters:
  - property: occurred_at
    operator: between
    values:
      - from: "2026-07-01T00:00:00Z"
        to: "2026-08-01T00:00:00Z"
```

Filters must use a `values` array, including when matching one value. Read the live MCP schema before using operators not listed here.
