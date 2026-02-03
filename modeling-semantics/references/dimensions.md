# Dimensions Reference

Complete guide to defining dimensions in semantic sources.

## Dimension Definition

```yaml
dimensions:
  - name: dimension_name      # Required: unique identifier
    type: String              # Required: data type
    sql: column_expression    # Optional: defaults to name
    description: "..."        # Optional: human-readable description
    hidden: false             # Optional: hide from UI
    formatter: "..."          # Optional: display format
```

## Data Types

### String

Text and categorical values.

```yaml
- name: country
  type: String
  sql: country_code
  description: ISO country code
```

Use for:
- Categories (status, type, category)
- Names (product_name, user_name)
- Codes (country_code, currency)
- Any text-based grouping

### Integer

Whole numbers.

```yaml
- name: age
  type: Integer
  sql: EXTRACT(YEAR FROM AGE(birth_date))
  description: User age in years
```

Use for:
- Ages, counts, quantities
- Years (when not using Date type)
- Numeric categories (rating 1-5)

### Float

Decimal numbers.

```yaml
- name: score
  type: Float
  sql: quality_score
  description: Quality score (0-100)
```

Use for:
- Scores, ratings
- Percentages
- Any continuous numeric value for grouping

### Boolean

True/false values.

```yaml
- name: is_premium
  type: Boolean
  sql: subscription_tier = 'premium'
  description: Whether user has premium subscription
```

Use for:
- Flags (is_active, has_subscription)
- Binary categories
- Computed boolean conditions

### Timestamp

Date and time values with breakdown support.

```yaml
- name: created_at
  type: Timestamp
  sql: created_at
  description: When the record was created
```

Supports breakdowns: Hour, Day, Week, Month, Quarter, Year

Use for:
- Event timestamps
- Created/updated times
- Any time-series analysis

### Date

Date-only values.

```yaml
- name: order_date
  type: Date
  sql: DATE(order_timestamp)
  description: Date of the order
```

Use for:
- Calendar dates without time
- Birth dates, expiration dates
- When time component is not needed

### UUID

Unique identifiers.

```yaml
- name: user_id
  type: UUID
  sql: user_id
  description: Unique user identifier
```

Use for:
- Primary keys
- Foreign keys
- Any unique identifier

### JSON

Semi-structured data.

```yaml
- name: properties
  type: JSON
  sql: event_properties
  description: Event-specific properties
```

Use for:
- Flexible schemas
- Nested data
- Properties bags

## Timestamp Breakdowns

When a dimension has type `Timestamp`, users can group by time periods:

| Breakdown | Groups By | Example Output |
|-----------|-----------|----------------|
| Hour | Hour of day | 0, 1, 2, ..., 23 |
| Day | Calendar day | 2024-03-15 |
| Week | Week start (Monday) | 2024-03-11 |
| Month | Calendar month | 2024-03-01 |
| Quarter | Quarter | 2024-01-01 |
| Year | Year | 2024-01-01 |

## SQL Expressions

The `sql` field can contain any valid SQL expression:

### Direct Column Reference

```yaml
- name: status
  type: String
  sql: status
```

### Computed Expression

```yaml
- name: full_name
  type: String
  sql: first_name || ' ' || last_name
```

### Conditional Logic

```yaml
- name: user_tier
  type: String
  sql: |
    CASE
      WHEN total_spend >= 10000 THEN 'Platinum'
      WHEN total_spend >= 5000 THEN 'Gold'
      WHEN total_spend >= 1000 THEN 'Silver'
      ELSE 'Bronze'
    END
```

### JSON Extraction

```yaml
- name: utm_source
  type: String
  sql: properties->>'utm_source'
```

### Date Manipulation

```yaml
- name: signup_month
  type: Date
  sql: DATE_TRUNC('month', created_at)
```

## Formatters

Formatters control how values display in the UI:

```yaml
- name: revenue_usd
  type: Float
  formatter: currency:USD
```

Common formatters:
- `currency:USD` - Format as US dollars
- `currency:EUR` - Format as Euros
- `percent` - Format as percentage
- `number` - Format with thousand separators

## Hidden Dimensions

Hide dimensions that are only used internally:

```yaml
- name: internal_id
  type: UUID
  hidden: true
```

Hidden dimensions:
- Still available for joins and relations
- Not shown in UI dimension selectors
- Useful for technical fields

## Best Practices

### Naming

- Use snake_case: `user_id`, `created_at`
- Be descriptive: `order_status` not `status`
- Avoid abbreviations: `customer_id` not `cust_id`

### Descriptions

Always add descriptions:
- What the dimension represents
- Valid values (for categories)
- Business context

### SQL Expressions

- Use explicit column references
- Handle NULL values appropriately
- Test expressions before deploying

### Type Selection

- Use `Timestamp` for time-series, `Date` for calendar dates
- Use `String` for categories, even if they look like numbers
- Use `Boolean` for binary flags, not `String` with 'yes'/'no'
