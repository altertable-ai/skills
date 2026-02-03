# MCP Servers Reference

Guide to Model Context Protocol server integration.

## MCP Overview

### What is MCP

Model Context Protocol is a standard for:
- AI agent tool discovery
- Context sharing between systems
- Capability extension
- Standardized communication

### MCP Components

| Component | Description |
|-----------|-------------|
| Server | Provides tools and context |
| Client | Consumes tools (agents) |
| Tools | Executable capabilities |
| Resources | Readable context |
| Prompts | Pre-defined prompts |

## Server Configuration

### Basic Configuration

```yaml
mcp_server:
  name: server_name
  type: http  # or stdio
  url: https://mcp.example.com
  transport: streamable-http
```

### Authentication

```yaml
mcp_server:
  name: authenticated_server
  url: https://mcp.example.com
  auth:
    type: bearer
    token: ${MCP_TOKEN}
  headers:
    X-Custom-Header: value
```

### Connection Options

| Option | Description |
|--------|-------------|
| timeout | Request timeout |
| retry_count | Number of retries |
| keepalive | Connection persistence |
| ssl_verify | Certificate validation |

## Available MCP Servers

### Amplitude MCP

Analytics platform integration:

**Tools:**
| Tool | Description |
|------|-------------|
| query_events | Query event data |
| get_cohort | Retrieve cohort |
| run_funnel | Funnel analysis |
| get_chart | Chart data |

**Configuration:**
```yaml
mcp_server:
  name: amplitude
  url: https://mcp.amplitude.com
  auth:
    type: bearer
    token: ${AMPLITUDE_MCP_TOKEN}
```

### Omni MCP

BI platform integration:

**Tools:**
| Tool | Description |
|------|-------------|
| query_metric | Get metric values |
| list_dashboards | Find dashboards |
| run_query | Execute query |
| get_schema | Explore schema |

**Configuration:**
```yaml
mcp_server:
  name: omni
  url: https://mcp.omni.co
  auth:
    type: api_key
    key: ${OMNI_API_KEY}
```

### Custom MCP Servers

Build your own:

**Requirements:**
- Implement MCP protocol
- Define tools schema
- Handle authentication
- Return structured responses

## Tool Discovery

### Listing Tools

When server connects:
1. Client requests tool list
2. Server returns available tools
3. Tools become available to agents

### Tool Schema

```yaml
tool:
  name: query_events
  description: Query events from Amplitude
  parameters:
    event_type:
      type: string
      required: true
    time_range:
      type: string
      default: last_7_days
    filters:
      type: object
      required: false
```

## Using MCP Tools

### Invocation

Agents can call MCP tools:
```yaml
tool_call:
  server: amplitude
  tool: query_events
  parameters:
    event_type: purchase_completed
    time_range: last_30_days
```

### Response Handling

Responses are structured:
```yaml
response:
  success: true
  data:
    events: [...]
    total_count: 1500
  metadata:
    query_time_ms: 245
```

### Error Handling

```yaml
error_response:
  success: false
  error:
    code: RATE_LIMITED
    message: Too many requests
    retry_after: 60
```

## Resource Access

### What are Resources

Resources provide read-only context:
- Documentation
- Data schemas
- Configuration
- Reference material

### Accessing Resources

```yaml
resource:
  server: amplitude
  uri: amplitude://schemas/events
```

## Server Management

### Health Checks

Monitor server health:
- Connection status
- Response time
- Error rate
- Available tools

### Reconnection

Handle disconnections:
- Automatic reconnect
- Backoff strategy
- Notification on failure

### Version Management

Handle server updates:
- Check compatibility
- Update tool schemas
- Handle deprecations

## Security Considerations

### Credential Storage

- Use secrets management
- Environment variables
- Never hardcode tokens
- Rotate regularly

### Network Security

- HTTPS only
- Certificate validation
- IP restrictions if possible
- Audit connections

### Access Control

- Principle of least privilege
- Audit tool usage
- Monitor for abuse
- Regular access review

## Best Practices

### Configuration

- Use environment variables
- Document server purpose
- Set appropriate timeouts
- Configure retries

### Reliability

- Monitor connection health
- Handle failures gracefully
- Log all interactions
- Alert on issues

### Performance

- Cache tool lists
- Batch requests where possible
- Set reasonable timeouts
- Monitor latency

## Troubleshooting

### Connection Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Timeout | Server slow | Increase timeout |
| Auth failed | Bad token | Check credentials |
| SSL error | Cert issue | Verify certificates |
| Not found | Wrong URL | Check server URL |

### Tool Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Tool not found | Not available | Check tool list |
| Invalid params | Schema mismatch | Check schema |
| Error response | Server error | Check server logs |
