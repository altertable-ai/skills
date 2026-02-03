# User Traits Reference

Guide to user properties and traits management.

## Trait Categories

### Identity Traits

Core identification:

| Trait | Type | Description |
|-------|------|-------------|
| user_id | string | Primary identifier |
| email | string | Email address |
| phone | string | Phone number |
| external_id | string | Third-party ID |

### Demographic Traits

User attributes:

| Trait | Type | Description |
|-------|------|-------------|
| first_name | string | First name |
| last_name | string | Last name |
| age | number | User age |
| gender | string | Gender |
| location | object | Geographic location |
| timezone | string | User timezone |

### Business Traits

Account attributes:

| Trait | Type | Description |
|-------|------|-------------|
| plan | string | Subscription plan |
| company | string | Company name |
| role | string | Job role |
| industry | string | Industry |
| company_size | string | Company size bracket |

### Behavioral Traits

Computed from events:

| Trait | Type | Description |
|-------|------|-------------|
| first_seen | datetime | First activity |
| last_seen | datetime | Last activity |
| session_count | number | Total sessions |
| event_count | number | Total events |
| purchase_count | number | Total purchases |

### Computed Traits

Derived metrics:

| Trait | Type | Description |
|-------|------|-------------|
| lifetime_value | number | Total revenue |
| engagement_score | number | Activity metric |
| churn_risk | number | Churn probability |
| nps_score | number | Net promoter score |

## Trait Lifecycle

### Creation

When traits are set:
- User registration
- Profile update
- Computed from events
- Imported from external

### Update

When traits change:
- User edits profile
- Computed trait recalculated
- Integration sync
- Manual update

### Deletion

When traits are removed:
- User request (GDPR)
- Data cleanup
- Account deletion

## Trait Operations

### Set Trait

```yaml
operation: identify
user_id: user_123
traits:
  plan: premium
  company: Acme Inc
```

### Update Trait

```yaml
operation: identify
user_id: user_123
traits:
  plan: enterprise  # overwrites previous
```

### Increment Trait

```yaml
operation: increment
user_id: user_123
trait: login_count
value: 1
```

### Append to Trait

```yaml
operation: append
user_id: user_123
trait: tags
value: "power_user"
```

## Standard Trait Schema

### Recommended Traits

```yaml
user:
  # Identity
  user_id: string (required)
  email: string
  phone: string

  # Profile
  first_name: string
  last_name: string
  avatar_url: string

  # Account
  created_at: datetime
  plan: string
  status: string

  # Business
  company: string
  role: string

  # Behavior
  first_seen: datetime
  last_seen: datetime
  session_count: number

  # Computed
  lifetime_value: number
  engagement_score: number
```

## Trait Naming

### Convention

```
{category}_{attribute}
```

Or just:
```
{attribute}
```

Examples:
- `email`
- `first_name`
- `subscription_plan`
- `last_purchase_date`

### Rules

| Rule | Good | Bad |
|------|------|-----|
| snake_case | `first_name` | `firstName` |
| Lowercase | `email` | `Email` |
| Descriptive | `subscription_end_date` | `sub_end` |

## Computed Traits

### Aggregation Based

```yaml
trait: total_purchases
computation: count
source: purchase_completed
filter: last_365_days
```

### Formula Based

```yaml
trait: engagement_score
formula: |
  (page_views * 1) +
  (feature_uses * 5) +
  (shares * 10)
```

### Time Based

```yaml
trait: days_since_last_active
computation: days_since
source: last_seen
```

## Trait Segmentation

### Using Traits for Segments

```yaml
segment:
  name: power_users
  filters:
    - trait: session_count
      operator: Gte
      value: 100
    - trait: purchase_count
      operator: Gte
      value: 5
```

### Trait-Based Targeting

| Segment | Trait Criteria |
|---------|---------------|
| High value | lifetime_value > 1000 |
| At risk | last_seen > 30 days ago |
| New users | created_at < 7 days ago |
| Engaged | engagement_score > 80 |

## Privacy Considerations

### PII Traits

Handle carefully:
- email
- phone
- full_name
- address
- ip_address

### Best Practices

- Encrypt at rest
- Limit access
- Support deletion
- Audit access
- Minimize collection

### GDPR Compliance

- Right to access
- Right to deletion
- Right to portability
- Right to correction

## Trait Validation

### Type Validation

| Trait | Expected | Validate |
|-------|----------|----------|
| email | string | Email format |
| age | number | 0-150 range |
| plan | string | Enum values |
| created_at | datetime | Valid ISO date |

### Quality Checks

Monitor for:
- Missing required traits
- Invalid formats
- Suspicious values
- Stale data
