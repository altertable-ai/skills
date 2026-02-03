# Event Definitions Reference

Comprehensive guide to event design and management.

## Event Taxonomy

### Tier 1: Core Events

High-priority, always track:

| Event | Description |
|-------|-------------|
| user_signed_up | Account creation |
| user_logged_in | Authentication |
| purchase_completed | Revenue event |
| subscription_started | Monetization |

### Tier 2: Engagement Events

Track for behavior analysis:

| Event | Description |
|-------|-------------|
| page_viewed | Navigation |
| feature_used | Activation |
| search_performed | Intent |
| content_consumed | Engagement |

### Tier 3: Detail Events

Track for deep analysis:

| Event | Description |
|-------|-------------|
| button_clicked | Micro-interactions |
| form_field_changed | Form analytics |
| tooltip_shown | UX analytics |
| error_encountered | Technical tracking |

## Event Naming

### Convention

```
{noun}_{past_tense_verb}
```

Examples:
- `order_placed`
- `email_sent`
- `report_generated`
- `notification_dismissed`

### Naming Rules

| Rule | Good | Bad |
|------|------|-----|
| Use past tense | `clicked` | `click` |
| Use underscores | `page_viewed` | `pageViewed` |
| Be specific | `signup_completed` | `done` |
| Avoid abbreviations | `notification` | `notif` |

### Naming Hierarchy

```
Category
├── Object
│   └── Action
```

Examples:
```
ecommerce
├── cart
│   ├── cart_viewed
│   ├── cart_updated
│   └── cart_cleared
├── checkout
│   ├── checkout_started
│   ├── checkout_completed
│   └── checkout_abandoned
```

## Standard Events

### Page Events

```yaml
page_viewed:
  properties:
    page_name: string
    page_path: string
    referrer: string
    title: string
```

### Click Events

```yaml
element_clicked:
  properties:
    element_name: string
    element_type: string
    page_name: string
    position: object
```

### Form Events

```yaml
form_submitted:
  properties:
    form_name: string
    form_type: string
    fields_count: number
    success: boolean
```

### Commerce Events

```yaml
product_viewed:
  properties:
    product_id: string
    product_name: string
    category: string
    price: number

cart_updated:
  properties:
    cart_id: string
    products: array
    total_value: number
    action: enum[add, remove, update]

purchase_completed:
  properties:
    order_id: string
    products: array
    total: number
    currency: string
    payment_method: string
```

## Event Properties

### Required Properties

Every event should have:

| Property | Type | Description |
|----------|------|-------------|
| timestamp | datetime | When event occurred |
| user_id | string | User identifier |
| event_id | string | Unique event ID |

### Context Properties

Automatically captured:

| Property | Type | Description |
|----------|------|-------------|
| session_id | string | Session identifier |
| device_type | string | mobile/desktop/tablet |
| browser | string | User agent |
| ip_address | string | Client IP |
| locale | string | User locale |

### Custom Properties

Event-specific context:

| Property | Type | Description |
|----------|------|-------------|
| (varies) | any | Event-specific data |

## Property Guidelines

### Type Consistency

| Type | Use For | Example |
|------|---------|---------|
| string | Identifiers, names | `"product_123"` |
| number | Counts, amounts | `99.99` |
| boolean | Flags | `true` |
| datetime | Timestamps | `"2024-01-15T10:30:00Z"` |
| array | Lists | `["tag1", "tag2"]` |
| object | Nested data | `{"key": "value"}` |

### Property Naming

| Rule | Good | Bad |
|------|------|-----|
| snake_case | `user_name` | `userName` |
| Descriptive | `total_price_usd` | `tp` |
| Consistent | always `user_id` | `uid`/`userId`/`user_id` |

## Event Validation

### Schema Validation

Validate on ingestion:
- Required properties present
- Types match schema
- Values within range
- Enums are valid

### Quality Checks

Monitor for:
- Missing required fields
- Invalid types
- Unusual volumes
- Duplicate events

## Event Documentation

### Event Spec Template

```markdown
## event_name

**Description**: What this event represents

**When to Send**: Trigger conditions

**Properties**:
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| prop_name | type | yes/no | Description |

**Example**:
\`\`\`json
{
  "event": "event_name",
  "properties": { ... }
}
\`\`\`
```

## Event Versioning

### When to Version

- Property added
- Property removed
- Type changed
- Meaning changed

### Versioning Strategy

Option 1: New event name
```
order_completed_v2
```

Option 2: Version property
```yaml
event: order_completed
properties:
  schema_version: 2
```
