# Filter Operators Reference

Complete guide to segment filter operators.

## Operator Categories

### Equality

#### Eq (Equals)

Exact match comparison.

```yaml
- dimension: status
  operator: Eq
  value: "active"
```

**Behavior**:
- Case-sensitive for strings
- NULL does not equal anything
- Type must match

#### Ne (Not Equals)

Inverse of Eq.

```yaml
- dimension: status
  operator: Ne
  value: "cancelled"
```

**Behavior**:
- Excludes exact matches
- NULL does not match (use IsNotNull)
- Includes all other values

### Comparison

#### Gt (Greater Than)

Strictly greater than value.

```yaml
- dimension: purchase_count
  operator: Gt
  value: 5
```

**Behavior**:
- Numeric comparison
- Excludes equal value
- NULL is excluded

#### Gte (Greater Than or Equal)

Greater than or equal to value.

```yaml
- dimension: purchase_count
  operator: Gte
  value: 5
```

**Behavior**:
- Includes equal value
- Common for "at least" criteria

#### Lt (Less Than)

Strictly less than value.

```yaml
- dimension: days_inactive
  operator: Lt
  value: 30
```

#### Lte (Less Than or Equal)

Less than or equal to value.

```yaml
- dimension: days_inactive
  operator: Lte
  value: 30
```

### String Matching

#### StartsWith

String begins with prefix.

```yaml
- dimension: page_path
  operator: StartsWith
  value: "/products/"
```

**Behavior**:
- Case-sensitive
- Matches from beginning
- Empty string matches all

#### NotStartsWith

String does not begin with prefix.

```yaml
- dimension: email
  operator: NotStartsWith
  value: "test"
```

#### EndsWith

String ends with suffix.

```yaml
- dimension: email
  operator: EndsWith
  value: "@company.com"
```

**Behavior**:
- Case-sensitive
- Matches at end
- Common for domain filtering

#### NotEndsWith

String does not end with suffix.

```yaml
- dimension: email
  operator: NotEndsWith
  value: "@test.com"
```

#### Contains

String contains substring anywhere.

```yaml
- dimension: name
  operator: Contains
  value: "smith"
```

**Behavior**:
- Case-sensitive
- Matches anywhere in string
- Empty string matches all

#### NotContains

String does not contain substring.

```yaml
- dimension: email
  operator: NotContains
  value: "spam"
```

### List Operations

#### In

Value is in provided list.

```yaml
- dimension: country
  operator: In
  values: ["US", "CA", "UK", "AU"]
```

**Behavior**:
- Matches any value in list
- Case-sensitive for strings
- Efficient for multiple values

#### NotIn

Value is not in provided list.

```yaml
- dimension: status
  operator: NotIn
  values: ["test", "deleted", "banned"]
```

### Null Handling

#### IsNull

Value is null or empty.

```yaml
- dimension: phone
  operator: IsNull
```

**Behavior**:
- Matches NULL values
- May match empty strings (depends on implementation)
- No value parameter needed

#### IsNotNull

Value exists (not null).

```yaml
- dimension: phone
  operator: IsNotNull
```

**Behavior**:
- Matches any non-null value
- Common for "has X" criteria

### IP Address

#### IpMatches

IP address matches CIDR range.

```yaml
- dimension: ip_address
  operator: IpMatches
  value: "10.0.0.0/8"
```

**Behavior**:
- CIDR notation required
- Supports IPv4 and IPv6
- Common for internal user exclusion

#### IpNotMatches

IP address does not match CIDR range.

```yaml
- dimension: ip_address
  operator: IpNotMatches
  value: "192.168.0.0/16"
```

## Combining Filters

### AND Logic

All filters must be true:

```yaml
filters:
  - dimension: status
    operator: Eq
    value: "active"
  - dimension: tier
    operator: Eq
    value: "premium"
  # Both conditions must be true
```

### Implicit AND

Multiple filters are always ANDed:

```yaml
filters:
  - dimension: country
    operator: Eq
    value: "US"
  - dimension: age
    operator: Gte
    value: 21
  # country = US AND age >= 21
```

## Type Considerations

### String Filters

- Use Eq, Ne for exact match
- Use Contains, StartsWith, EndsWith for partial
- Case-sensitive by default

### Numeric Filters

- Use Gt, Gte, Lt, Lte for ranges
- Use Eq for exact values
- Use In for discrete values

### Date Filters

- Use Gte, Lte for date ranges
- Format: ISO 8601 or relative
- Consider timezone

### Boolean Filters

- Use Eq with true/false
- Avoid string comparisons

## Common Patterns

### Date Range

```yaml
filters:
  - dimension: created_at
    operator: Gte
    value: "2024-01-01"
  - dimension: created_at
    operator: Lt
    value: "2024-02-01"
```

### Exclude Internal

```yaml
filters:
  - dimension: email
    operator: NotEndsWith
    value: "@company.com"
  - dimension: ip_address
    operator: IpNotMatches
    value: "10.0.0.0/8"
```

### Value Exists

```yaml
filters:
  - dimension: purchase_date
    operator: IsNotNull
```

### Multi-Value Match

```yaml
filters:
  - dimension: plan
    operator: In
    values: ["starter", "pro", "enterprise"]
```
