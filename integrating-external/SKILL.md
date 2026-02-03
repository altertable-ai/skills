---
name: integrating-external
compatibility: Altertable
description: Connects to external MCP servers and services for extended capabilities. Use when integrating with Amplitude, Omni, Slack, or other external tools, or when configuring notifications and external data sources.
---

# Integrating External

## Quick Start

External integrations enable:
1. Connecting to third-party data sources
2. Sending notifications to external systems
3. Extending agent capabilities
4. Syncing with external platforms

## When to Use This Skill

- Connecting to external MCP servers
- Configuring Slack notifications
- Integrating with Amplitude
- Connecting to Omni
- Setting up webhooks
- Managing external data sources

## Integration Types

### MCP Servers

External Model Context Protocol servers:
- Amplitude MCP
- Omni MCP
- Custom MCP servers

### Notification Channels

Output destinations:
- Slack
- Email
- Webhooks
- Custom endpoints

### Data Connectors

External data sources:
- Third-party APIs
- External databases
- SaaS platforms

## MCP Integration

### What is MCP

Model Context Protocol enables:
- Tool discovery
- Context sharing
- Capability extension
- Standardized communication

### Adding MCP Server

```yaml
mcp_server:
  name: amplitude
  url: https://mcp.amplitude.com
  api_key: ${AMPLITUDE_API_KEY}
  capabilities:
    - query_events
    - get_cohorts
    - export_data
```

### Using MCP Tools

Once connected:
- Tools appear in agent context
- Can be invoked by agents
- Results flow back to analysis

## Slack Integration

### Setup

Configure Slack connection:
- Create Slack app
- Set up OAuth
- Configure permissions
- Connect workspace

### Notification Types

| Type | Use Case |
|------|----------|
| Discovery alerts | New findings |
| Watcher notifications | Automated monitoring |
| Direct messages | Personal alerts |
| Channel posts | Team updates |

### Message Formatting

Slack messages can include:
- Rich text formatting
- Charts and images
- Interactive buttons
- Thread replies

### Channel Configuration

```yaml
slack_channel:
  name: "#analytics-alerts"
  notification_types:
    - critical_discoveries
    - daily_summaries
  format: rich
  mention_on_critical: true
```

## External Data Sources

### API Integration

Connect to external APIs:
- REST endpoints
- GraphQL APIs
- Webhook receivers

### Configuration

```yaml
external_source:
  name: external_api
  type: rest
  base_url: https://api.example.com
  auth:
    type: bearer
    token: ${API_TOKEN}
  endpoints:
    - path: /metrics
      method: GET
    - path: /events
      method: POST
```

### Data Sync

Options for syncing:
- Real-time (webhooks)
- Scheduled (polling)
- On-demand (manual)

## Amplitude Integration

### Capabilities

With Amplitude MCP:
- Query event data
- Access cohorts
- Run analyses
- Export reports

### Common Operations

| Operation | Description |
|-----------|-------------|
| Query events | Fetch event data |
| Get cohort | Retrieve user segment |
| Run funnel | Analyze conversion |
| Get retention | Analyze retention |

### Example Usage

```yaml
amplitude_query:
  event_type: "purchase_completed"
  time_range: "last_30_days"
  group_by: "product_category"
  metrics:
    - total_events
    - unique_users
```

## Omni Integration

### Capabilities

With Omni MCP:
- Query metrics
- Access dashboards
- Run reports
- Get dimensions

### Common Operations

| Operation | Description |
|-----------|-------------|
| Query metric | Get metric values |
| List dashboards | Find dashboards |
| Get report | Run saved report |
| Explore data | Ad-hoc analysis |

## Webhook Configuration

### Incoming Webhooks

Receive data from external systems:
- Event notifications
- Data updates
- Trigger signals

### Outgoing Webhooks

Send data to external systems:
- Discovery alerts
- Status updates
- Data exports

### Webhook Security

- Signature verification
- IP whitelisting
- Token authentication
- HTTPS required

## Integration Patterns

### Data Enrichment

```
Internal Data → Query External → Combine → Analysis
```

### Cross-Platform Analysis

```
Amplitude Events + Internal Data → Unified Analysis
```

### Alert Distribution

```
Discovery → Slack + Email + Webhook
```

### Scheduled Sync

```
Every Hour: External API → Internal Storage → Analysis
```

## Authentication Methods

### API Key

Simple key-based auth:
```yaml
auth:
  type: api_key
  header: X-API-Key
  value: ${API_KEY}
```

### OAuth 2.0

Token-based auth:
```yaml
auth:
  type: oauth2
  client_id: ${CLIENT_ID}
  client_secret: ${CLIENT_SECRET}
  token_url: https://auth.example.com/token
```

### Bearer Token

JWT or similar:
```yaml
auth:
  type: bearer
  token: ${BEARER_TOKEN}
```

## Error Handling

### Retry Logic

For transient failures:
- Exponential backoff
- Max retry limits
- Circuit breakers

### Fallback Behavior

When integration fails:
- Log error
- Alert admin
- Use cached data
- Graceful degradation

## Best Practices

### Security

- Store credentials securely
- Use environment variables
- Rotate tokens regularly
- Audit access logs

### Reliability

- Implement retry logic
- Monitor integration health
- Set appropriate timeouts
- Handle rate limits

### Performance

- Cache where appropriate
- Batch requests
- Use async operations
- Monitor latency

## Common Pitfalls

- Hardcoded credentials
- Missing error handling
- Ignoring rate limits
- No retry logic
- Missing monitoring
- Over-reliance on external

## Reference Files

- [MCP servers](references/mcp-servers.md)
- [Slack notifications](references/slack-notifications.md)
