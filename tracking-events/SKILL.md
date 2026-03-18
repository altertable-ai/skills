---
name: tracking-events
compatibility: Requires Altertable MCP server
description: Works with product analytics events and user identities. Use when analyzing user behavior, event tracking, understanding event schemas, identity resolution, or user trait management.
metadata:
  author: altertable-ai
---

# Tracking Events

## Quick Start

Product analytics involves:
1. Tracking user events (actions)
2. Capturing user properties (traits)
3. Resolving user identities
4. Analyzing behavioral patterns

## When to Use This Skill

- Analyzing user behavior
- Understanding event schemas
- Working with user traits
- Resolving user identities
- Building behavioral segments
- Creating event-based funnels

## Event Fundamentals

### What is an Event

An event represents an action:
- User action (clicked, viewed, purchased)
- System event (loaded, errored, completed)
- Business event (subscribed, churned, renewed)

### Event Structure

```yaml
event:
  name: "button_clicked"
  timestamp: "2024-01-15T10:30:00Z"
  user_id: "user_123"
  properties:
    button_name: "signup"
    page: "/home"
    device: "mobile"
```

### Core Components

| Component | Description |
|-----------|-------------|
| `name` | Event identifier |
| `timestamp` | When it occurred |
| `user_id` | Who did it |
| `properties` | Additional context |

## Common Event Types

### Engagement Events

| Event | Purpose |
|-------|---------|
| page_viewed | Track navigation |
| button_clicked | Track interactions |
| form_submitted | Track conversions |
| search_performed | Track intent |

### Commerce Events

| Event | Purpose |
|-------|---------|
| product_viewed | Track interest |
| cart_updated | Track intent |
| checkout_started | Track funnel |
| purchase_completed | Track conversion |

### Lifecycle Events

| Event | Purpose |
|-------|---------|
| account_created | Track acquisition |
| onboarding_completed | Track activation |
| feature_used | Track engagement |
| subscription_changed | Track monetization |

## Event Properties

### Standard Properties

Always capture:
- `timestamp` - When
- `user_id` - Who
- `session_id` - Context
- `device_type` - How

### Custom Properties

Add context-specific:
- Event-specific details
- Business context
- Technical metadata
- Attribution data

### Property Types

| Type | Example |
|------|---------|
| String | `"homepage"` |
| Number | `99.99` |
| Boolean | `true` |
| Date | `"2024-01-15"` |
| Array | `["tag1", "tag2"]` |
| Object | `{"nested": "value"}` |

## User Identities

### Identity Concept

Users have multiple identifiers:
- Anonymous IDs (before login)
- User IDs (after login)
- External IDs (third-party)
- Device IDs (per device)

### Identity Resolution

Linking identities together:

```
anonymous_123 ─┐
               ├─→ user_456 (resolved identity)
device_789 ────┘
```

### Identity Methods

| Method | When to Use |
|--------|-------------|
| identify | Associate user ID |
| alias | Link two identities |
| merge | Combine profiles |

## User Traits

### What are Traits

Persistent user attributes:
- Demographics
- Preferences
- Computed properties
- Business attributes

### Trait Structure

```yaml
user:
  id: "user_123"
  traits:
    email: "user@example.com"
    plan: "premium"
    signup_date: "2024-01-01"
    lifetime_value: 599.99
```

### Trait Categories

| Category | Examples |
|----------|----------|
| Demographic | name, email, location |
| Behavioral | last_active, purchase_count |
| Business | plan, mrr, account_type |
| Computed | lifetime_value, engagement_score |

## Event Analysis

### Volume Analysis

Track event counts:
- Events per day
- Events per user
- Event distribution

### Sequence Analysis

Track event orders:
- Common paths
- Drop-off points
- Success patterns

### Cohort Analysis

Compare groups by:
- Signup date
- First action
- User segment

## Event Schema Management

### Schema Design

Good event schemas:
- Consistent naming
- Clear properties
- Documented purpose
- Appropriate granularity

### Naming Conventions

```
{object}_{action}
```

Examples:
- `page_viewed`
- `button_clicked`
- `order_completed`
- `subscription_started`

### Schema Evolution

When changing events:
- Document changes
- Consider backwards compatibility
- Migrate gradually
- Update consumers

## Best Practices

### Event Design

- Be consistent
- Be specific enough
- Don't over-track
- Document everything

### Identity Management

- Identify early
- Link all touchpoints
- Handle anonymous users
- Clean up duplicates

### Property Management

- Use consistent types
- Validate on ingestion
- Don't store PII unnecessarily
- Use enums where appropriate

## Common Patterns

### Funnel Tracking

Track conversion funnel:
```
page_viewed (landing)
  → signup_started
    → signup_completed
      → onboarding_started
        → onboarding_completed
```

### Feature Adoption

Track feature usage:
```
feature_viewed
  → feature_tried
    → feature_used_regularly
```

### Engagement Scoring

Combine events for score:
```
Daily active: page_viewed (today)
Feature usage: feature_used (count)
Social: invite_sent, share_clicked
```

## Common Pitfalls

- Inconsistent event naming
- Missing user identification
- Over-tracking (too many events)
- Under-tracking (missing context)
- Not handling anonymous users
- Storing sensitive data in events

## Reference Files

- [Event definitions](references/event-definitions.md)
- [User traits](references/user-traits.md)
- [Identity resolution](references/identity-resolution.md)
