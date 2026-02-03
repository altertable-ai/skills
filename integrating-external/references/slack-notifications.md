# Slack Notifications Reference

Guide to Slack integration and notifications.

## Slack Setup

### Prerequisites

1. Slack workspace admin access
2. Ability to create Slack apps
3. OAuth permissions granted

### Creating Slack App

1. Go to api.slack.com/apps
2. Create new app
3. Configure OAuth scopes
4. Install to workspace
5. Get OAuth token

### Required Scopes

| Scope | Purpose |
|-------|---------|
| chat:write | Post messages |
| channels:read | List channels |
| users:read | Resolve users |
| files:write | Upload files |

## Configuration

### Basic Setup

```yaml
slack_integration:
  workspace_id: T12345678
  oauth_token: ${SLACK_TOKEN}
  default_channel: "#analytics-alerts"
```

### Channel Configuration

```yaml
channels:
  - name: "#critical-alerts"
    types:
      - critical_discovery
      - system_alert
    mention_on_alert: true

  - name: "#daily-insights"
    types:
      - daily_summary
      - weekly_report
    schedule: "09:00 UTC"
```

## Message Types

### Discovery Notifications

When discoveries are approved:

```yaml
notification:
  type: discovery
  channel: "#analytics"
  content:
    headline: "Revenue dropped 15%"
    details: "Day-over-day comparison shows..."
    chart_url: "https://..."
    actions:
      - label: "View Details"
        url: "https://app.altertable.ai/..."
```

### Alert Notifications

For time-sensitive alerts:

```yaml
notification:
  type: alert
  channel: "#alerts"
  urgency: high
  content:
    title: "Payment Error Spike"
    message: "Error rate exceeded threshold"
    metrics:
      current: "5.2%"
      threshold: "2%"
```

### Summary Notifications

Periodic summaries:

```yaml
notification:
  type: summary
  channel: "#insights"
  content:
    title: "Daily Analytics Summary"
    sections:
      - header: "Key Metrics"
        items: [...]
      - header: "Notable Changes"
        items: [...]
```

## Message Formatting

### Text Formatting

```
*bold* text
_italic_ text
~strikethrough~
`code`
```code block```
>quote
```

### Rich Blocks

```yaml
blocks:
  - type: header
    text: "Daily Report"

  - type: section
    text: "Key metrics for today"

  - type: divider

  - type: section
    fields:
      - type: mrkdwn
        text: "*Revenue:*\n$125,000"
      - type: mrkdwn
        text: "*Users:*\n15,432"
```

### Attachments

```yaml
attachments:
  - color: "#36a64f"
    title: "Revenue Up"
    text: "15% increase day-over-day"
    fields:
      - title: "Current"
        value: "$125,000"
        short: true
      - title: "Previous"
        value: "$108,695"
        short: true
```

## Interactive Components

### Buttons

```yaml
actions:
  - type: button
    text: "View Details"
    url: "https://..."
    style: primary

  - type: button
    text: "Dismiss"
    action_id: dismiss_alert
```

### Menus

```yaml
accessory:
  type: static_select
  placeholder: "Select action"
  options:
    - text: "Investigate"
      value: "investigate"
    - text: "Ignore"
      value: "ignore"
```

## Notification Rules

### Routing Rules

Route by type:
```yaml
rules:
  - match:
      type: critical
    channel: "#urgent-alerts"
    mention: "@channel"

  - match:
      type: insight
      topic: revenue
    channel: "#revenue-team"
```

### Timing Rules

Control delivery timing:
```yaml
timing:
  business_hours_only: true
  timezone: "America/New_York"
  start_hour: 9
  end_hour: 18

  outside_hours:
    action: queue
    deliver_at: next_business_hour
```

### Rate Limiting

Prevent alert fatigue:
```yaml
rate_limits:
  per_channel:
    max: 10
    period: 1_hour

  per_user:
    max: 5
    period: 1_hour

  overflow:
    action: batch
    summary_interval: 30_minutes
```

## Thread Management

### Threading Strategy

```yaml
threading:
  group_by: discovery_source
  reply_window: 24_hours

  new_thread_when:
    - new_topic
    - priority_change
    - after_24_hours
```

### Thread Updates

```yaml
thread_update:
  parent_ts: "1234567890.123456"
  reply:
    text: "Update: Issue resolved"
    type: status_update
```

## User Mentions

### Mention Types

| Type | Syntax | Use |
|------|--------|-----|
| User | <@U12345> | Direct mention |
| Channel | <!channel> | All channel |
| Here | <!here> | Active members |
| Group | <!subteam^S123> | User group |

### Dynamic Mentions

```yaml
mentions:
  on_critical: "@oncall-team"
  on_revenue: "@revenue-lead"
  default: null
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| channel_not_found | Bad channel | Verify channel name |
| not_in_channel | Bot not added | Add bot to channel |
| rate_limited | Too many messages | Implement backoff |
| invalid_blocks | Bad formatting | Check block syntax |

### Retry Strategy

```yaml
retry:
  max_attempts: 3
  backoff: exponential
  initial_delay: 1_second
  max_delay: 30_seconds
```

## Best Practices

### Message Design

- Keep messages concise
- Use formatting sparingly
- Include actionable info
- Link to more details

### Channel Organization

- Separate by urgency
- Group by topic
- Limit noise in channels
- Use threads for updates

### Alert Management

- Set appropriate thresholds
- Batch related alerts
- Include context
- Make actionable
