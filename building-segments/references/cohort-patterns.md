# Cohort Patterns Reference

Common segment patterns for user cohorts.

## Lifecycle Cohorts

### New Users

Users who signed up recently.

```yaml
name: new-users-7d
description: Users who signed up in the last 7 days
filters:
  - dimension: created_at
    operator: Gte
    value: "${7_days_ago}"
```

### Activated Users

Users who completed onboarding.

```yaml
name: activated-users
description: Users who completed onboarding
filters:
  - dimension: onboarding_completed_at
    operator: IsNotNull
```

### Active Users

Users with recent activity.

```yaml
name: active-users-30d
description: Users active in last 30 days
filters:
  - dimension: last_activity_at
    operator: Gte
    value: "${30_days_ago}"
```

### Dormant Users

Users with no recent activity.

```yaml
name: dormant-users
description: Users inactive for 30-90 days
filters:
  - dimension: last_activity_at
    operator: Lt
    value: "${30_days_ago}"
  - dimension: last_activity_at
    operator: Gte
    value: "${90_days_ago}"
```

### Churned Users

Users who stopped using the product.

```yaml
name: churned-users
description: Users inactive for 90+ days
filters:
  - dimension: last_activity_at
    operator: Lt
    value: "${90_days_ago}"
  - dimension: status
    operator: Ne
    value: "cancelled"
```

## Value Cohorts

### High-Value Customers

Top spenders.

```yaml
name: high-value-customers
description: Customers with $1000+ lifetime spend
filters:
  - dimension: total_spend
    operator: Gte
    value: 1000
```

### Power Users

Heavy product users.

```yaml
name: power-users
description: Users with 100+ sessions
filters:
  - dimension: total_sessions
    operator: Gte
    value: 100
  - dimension: last_activity_at
    operator: Gte
    value: "${30_days_ago}"
```

### Frequent Purchasers

Multiple purchase users.

```yaml
name: frequent-purchasers
description: Users with 5+ purchases
filters:
  - dimension: purchase_count
    operator: Gte
    value: 5
```

## Subscription Cohorts

### Free Users

Non-paying users.

```yaml
name: free-users
description: Users on free plan
filters:
  - dimension: subscription_tier
    operator: Eq
    value: "free"
```

### Trial Users

Users in trial period.

```yaml
name: trial-users
description: Users in active trial
filters:
  - dimension: subscription_status
    operator: Eq
    value: "trial"
  - dimension: trial_end_date
    operator: Gte
    value: "${today}"
```

### Paid Subscribers

Active paying users.

```yaml
name: paid-subscribers
description: Active paid subscribers
filters:
  - dimension: subscription_status
    operator: Eq
    value: "active"
  - dimension: subscription_tier
    operator: NotIn
    values: ["free", "trial"]
```

### Enterprise Customers

Large account customers.

```yaml
name: enterprise-customers
description: Enterprise tier customers
filters:
  - dimension: subscription_tier
    operator: Eq
    value: "enterprise"
  - dimension: subscription_status
    operator: Eq
    value: "active"
```

## Behavioral Cohorts

### Feature Adopters

Users who used specific feature.

```yaml
name: feature-x-users
description: Users who used Feature X
filters:
  - dimension: has_used_feature_x
    operator: Eq
    value: true
```

### Mobile Users

Users primarily on mobile.

```yaml
name: mobile-users
description: Users with 50%+ mobile sessions
filters:
  - dimension: mobile_session_pct
    operator: Gte
    value: 50
```

### Engaged Users

Users with high engagement.

```yaml
name: engaged-users
description: Users with engagement score >= 7
filters:
  - dimension: engagement_score
    operator: Gte
    value: 7
```

## Demographic Cohorts

### Geographic Segments

By location.

```yaml
name: us-users
description: Users in United States
filters:
  - source: identities
    dimension: country
    operator: Eq
    value: "US"
```

### Enterprise Domains

Business email users.

```yaml
name: enterprise-domains
description: Users with business emails
filters:
  - dimension: email
    operator: NotEndsWith
    value: "@gmail.com"
  - dimension: email
    operator: NotEndsWith
    value: "@yahoo.com"
  - dimension: email
    operator: NotEndsWith
    value: "@hotmail.com"
```

## Risk Cohorts

### At-Risk Users

Users showing churn signals.

```yaml
name: at-risk-users
description: Active users with declining engagement
filters:
  - dimension: engagement_trend
    operator: Eq
    value: "declining"
  - dimension: subscription_status
    operator: Eq
    value: "active"
```

### Payment Issues

Users with billing problems.

```yaml
name: payment-issues
description: Users with failed payments
filters:
  - dimension: last_payment_status
    operator: Eq
    value: "failed"
```

## Exclusion Patterns

### Internal Users

```yaml
name: exclude-internal
description: Exclude company employees
filters:
  - dimension: email
    operator: NotEndsWith
    value: "@company.com"
  - dimension: is_employee
    operator: Ne
    value: true
```

### Test Accounts

```yaml
name: exclude-test
description: Exclude test accounts
filters:
  - dimension: email
    operator: NotContains
    value: "test"
  - dimension: name
    operator: NotContains
    value: "test"
```

## Combining Cohorts

### Premium Active Users

```yaml
name: premium-active-users
filters:
  # Premium
  - dimension: subscription_tier
    operator: In
    values: ["premium", "enterprise"]
  # Active
  - dimension: subscription_status
    operator: Eq
    value: "active"
  # Recent activity
  - dimension: last_activity_at
    operator: Gte
    value: "${7_days_ago}"
```

### High-Value At-Risk

```yaml
name: high-value-at-risk
filters:
  # High value
  - dimension: total_spend
    operator: Gte
    value: 500
  # At risk (declining)
  - dimension: activity_trend
    operator: Eq
    value: "declining"
```
