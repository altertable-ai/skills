---
name: building-segments
compatibility: Requires Altertable MCP server
description: Creates user segments and cohorts using filters and dimensions. Use when segmenting users, building cohorts, filtering populations, defining audiences, or when asked about user groups.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Building Segments

## Quick Start

A segment defines a subset of users based on:
1. **Primary dimension**: How to group users
2. **Filters**: Criteria that define the segment
3. **Time range**: When to evaluate

## When to Use This Skill

- Defining user cohorts for analysis
- Creating audiences for targeting
- Comparing user groups
- Building behavioral segments
- Filtering populations for insights

## Segment Structure

```yaml
segment:
  name: segment-name
  description: Human-readable description
  primary_dimension_ref:
    source: source-slug
    name: dimension-name
  filters:
    - dimension: dimension-name
      operator: Eq
      value: "value"
```

## Filter Operators

### Equality Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `Eq` | Equals | status = 'active' |
| `Ne` | Not equals | status != 'churned' |

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `Gt` | Greater than | purchases > 5 |
| `Gte` | Greater or equal | purchases >= 5 |
| `Lt` | Less than | days_inactive < 30 |
| `Lte` | Less or equal | days_inactive <= 30 |

### String Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `StartsWith` | Begins with | email starts with 'john' |
| `NotStartsWith` | Doesn't begin with | email not starts with 'test' |
| `EndsWith` | Ends with | email ends with '@company.com' |
| `NotEndsWith` | Doesn't end with | email not ends with '@test.com' |
| `Contains` | Contains substring | name contains 'smith' |
| `NotContains` | Doesn't contain | name not contains 'test' |

### List Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `In` | In list | country in ['US', 'CA'] |
| `NotIn` | Not in list | status not in ['test', 'deleted'] |

### Null Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `IsNull` | Is null/empty | email is null |
| `IsNotNull` | Has value | last_purchase is not null |

### IP Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `IpMatches` | IP in CIDR range | ip matches '10.0.0.0/8' |
| `IpNotMatches` | IP not in range | ip not matches '192.168.0.0/16' |

## Common Segment Patterns

### Active Users

```yaml
filters:
  - dimension: last_activity_date
    operator: Gte
    value: "${30_days_ago}"
  - dimension: status
    operator: Eq
    value: "active"
```

### Premium Subscribers

```yaml
filters:
  - dimension: subscription_tier
    operator: In
    values: ["premium", "enterprise"]
  - dimension: subscription_status
    operator: Eq
    value: "active"
```

### High-Value Customers

```yaml
filters:
  - dimension: total_purchases
    operator: Gte
    value: 10
  - dimension: total_spend
    operator: Gte
    value: 1000
```

### New Users (Last 7 Days)

```yaml
filters:
  - dimension: created_at
    operator: Gte
    value: "${7_days_ago}"
```

### Churned Users

```yaml
filters:
  - dimension: last_activity_date
    operator: Lt
    value: "${90_days_ago}"
  - dimension: status
    operator: Ne
    value: "cancelled"
```

### Internal Users (Exclude)

```yaml
filters:
  - dimension: email
    operator: NotContains
    value: "@company.com"
  - dimension: is_internal
    operator: Ne
    value: true
```

## Workflow

### Step 1: Define Objective

What question are you answering?
- Who are my most valuable users?
- Which users are at risk of churning?
- Who should receive this campaign?

### Step 2: Identify Criteria

What defines this segment?
- Behavioral attributes (actions taken)
- Demographic attributes (traits)
- Temporal attributes (when)

### Step 3: Build Filters

Translate criteria to filters:
- Choose appropriate operators
- Set correct values
- Combine with AND logic

### Step 4: Validate

Check the segment:
- Is the size reasonable?
- Are edge cases handled?
- Does it match expectations?

### Step 5: Document

Record the definition:
- Clear name
- Detailed description
- Business context

## Advanced Patterns

### Multi-Condition Segments

All conditions must be true (AND logic):

```yaml
filters:
  # Must be premium
  - dimension: tier
    operator: Eq
    value: "premium"
  # AND active
  - dimension: status
    operator: Eq
    value: "active"
  # AND purchased recently
  - dimension: last_purchase_date
    operator: Gte
    value: "${30_days_ago}"
```

### Exclusion Segments

Define who NOT to include:

```yaml
filters:
  # Exclude test accounts
  - dimension: email
    operator: NotEndsWith
    value: "@test.com"
  # Exclude employees
  - dimension: is_employee
    operator: Ne
    value: true
  # Exclude unverified
  - dimension: email_verified
    operator: Eq
    value: true
```

### Behavioral Segments

Based on user actions:

```yaml
filters:
  # Completed onboarding
  - dimension: onboarding_completed
    operator: Eq
    value: true
  # Made a purchase
  - dimension: purchase_count
    operator: Gte
    value: 1
```

## Best Practices

### Clear Naming

- Use descriptive names
- Include key criteria
- Avoid ambiguity

Good: `premium-active-users`
Bad: `segment-1`

### Document Thoroughly

- Explain business purpose
- List all criteria
- Note edge cases

### Test Incrementally

- Start with one filter
- Add filters one at a time
- Verify at each step

### Consider Edge Cases

- NULL values
- Boundary conditions
- Data quality issues

## Common Pitfalls

- Using wrong operator (Eq vs Contains)
- Forgetting NULL handling
- Overly complex filters
- Not testing segment size
- Missing exclusion criteria
- Ambiguous segment definitions

## Reference Files

- [Filter operators](references/filter-operators.md)
- [Dimension references](references/dimension-refs.md)
- [Cohort patterns](references/cohort-patterns.md)
