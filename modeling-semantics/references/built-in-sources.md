# Built-in Sources Reference

Pre-defined semantic sources available in every Altertable organization.

## Events Source

Product analytics events from the `altertable` connection.

### Purpose

Tracks user interactions and system events across applications.

### Key Dimensions

| Dimension | Type | Description |
|-----------|------|-------------|
| `event` | String | Type of event (e.g., page_view, click, purchase) |
| `timestamp` | Timestamp | When the event occurred |
| `user_id` | UUID | User who triggered the event |
| `distinct_id` | String | Anonymous identifier before identification |
| `properties` | JSON | Event-specific properties |

### Key Measures

| Measure | Kind | Description |
|---------|------|-------------|
| `event_count` | Count | Total number of events |
| `unique_users` | CountDistinct | Unique users (by user_id) |

### Relations

- `identities` via `user_id` - User identity information

### Common Use Cases

- Event funnel analysis
- User activity tracking
- Feature usage metrics
- Conversion tracking

### Example Queries

Count events by type:
- Dimension: `event`
- Measure: `event_count`

Daily active users:
- Dimension: `timestamp` (Day breakdown)
- Measure: `unique_users`

## Identities Source

User identity information from the `altertable` connection.

### Purpose

Stores user profile information and traits.

### Key Dimensions

| Dimension | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Unique user identifier |
| `email` | String | User email address |
| `created_at` | Timestamp | When user was first seen |
| `traits` | JSON | User traits and properties |

### Key Measures

| Measure | Kind | Description |
|---------|------|-------------|
| `user_count` | Count | Total number of users |

### Common Use Cases

- User segmentation
- Demographic analysis
- User growth metrics

### Example Queries

Users by signup month:
- Dimension: `created_at` (Month breakdown)
- Measure: `user_count`

## Pageviews Source

Web page view events from the `altertable` connection.

### Purpose

Tracks page visits with URL and referrer information.

### Key Dimensions

| Dimension | Type | Description |
|-----------|------|-------------|
| `timestamp` | Timestamp | When page was viewed |
| `user_id` | UUID | User who viewed the page |
| `page_url` | String | URL of the page |
| `page_path` | String | Path portion of URL |
| `referrer` | String | Referring URL |
| `referrer_host` | String | Referring domain |
| `device_type` | String | Mobile, desktop, tablet |
| `browser` | String | Browser name |
| `os` | String | Operating system |

### Key Measures

| Measure | Kind | Description |
|---------|------|-------------|
| `pageview_count` | Count | Total page views |
| `unique_visitors` | CountDistinct | Unique visitors |

### Relations

- `identities` via `user_id` - User identity information
- `sessions` via `session_id` - Session information

### Common Use Cases

- Page popularity analysis
- Traffic source analysis
- Device/browser analytics
- User journey analysis

### Example Queries

Top pages by views:
- Dimension: `page_path`
- Measure: `pageview_count`
- Sort: descending

Traffic by device:
- Dimension: `device_type`
- Measure: `unique_visitors`

## Sessions Source

Web session aggregations from the `altertable` connection.

### Purpose

Session-level metrics aggregated from pageviews.

### Key Dimensions

| Dimension | Type | Description |
|-----------|------|-------------|
| `session_id` | UUID | Unique session identifier |
| `user_id` | UUID | User for this session |
| `started_at` | Timestamp | Session start time |
| `ended_at` | Timestamp | Session end time |
| `entry_page` | String | First page of session |
| `exit_page` | String | Last page of session |
| `referrer_host` | String | Traffic source |
| `device_type` | String | Device used |
| `country` | String | User location |

### Key Measures

| Measure | Kind | Description |
|---------|------|-------------|
| `session_count` | Count | Total sessions |
| `total_pageviews` | Sum | Total pageviews in sessions |
| `avg_session_duration` | Average | Average session length |
| `bounce_rate` | Expression | Single-page session rate |

### Relations

- `identities` via `user_id` - User identity information

### Common Use Cases

- Session analytics
- Bounce rate analysis
- Traffic source performance
- User engagement metrics

### Example Queries

Sessions by source:
- Dimension: `referrer_host`
- Measure: `session_count`

Bounce rate by page:
- Dimension: `entry_page`
- Measure: `bounce_rate`

## Identity Overrides Source

Identity resolution rules from the `altertable` connection.

### Purpose

Maps anonymous identifiers to known user identities.

### Key Dimensions

| Dimension | Type | Description |
|-----------|------|-------------|
| `distinct_id` | String | Anonymous identifier |
| `user_id` | UUID | Resolved user identity |
| `created_at` | Timestamp | When mapping was created |

### Common Use Cases

- Identity resolution debugging
- User journey reconstruction
- Anonymous to known user mapping

## Using Built-in Sources

### In Queries

Reference built-in sources like any other source:
- Select dimensions and measures
- Apply filters
- Join with other sources via relations

### Extending with Custom Sources

Create custom sources that relate to built-in sources:

```yaml
# Custom orders source
relations:
  - source: identities
    foreign_key: user_id
```

This allows querying orders with user identity dimensions.

### Filtering Built-in Sources

Common filters for events:
- `timestamp` >= last 30 days
- `event` = specific event
- `properties->>'key'` = value

### Combining Sources

Query across sources using relations:
- Events with identity traits
- Pageviews with session metrics
- Sessions with user properties
