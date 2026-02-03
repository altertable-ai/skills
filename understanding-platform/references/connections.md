# Connections Reference

Guide to data source connections.

## Connection Types

### Databases

Direct database connections:

| Type | Description |
|------|-------------|
| PostgreSQL | Open-source relational |
| MySQL | Popular relational |
| SQL Server | Microsoft database |
| Oracle | Enterprise database |

### Data Warehouses

Cloud warehouse connections:

| Type | Description |
|------|-------------|
| Snowflake | Cloud data platform |
| BigQuery | Google's warehouse |
| Redshift | AWS warehouse |
| Databricks | Lakehouse platform |

### DuckDB Lakehouse

Built-in analytics engine:

| Feature | Description |
|---------|-------------|
| Local processing | In-memory analytics |
| File support | Parquet, CSV, JSON |
| SQL interface | Standard SQL |
| Fast queries | Columnar storage |

### Other Sources

| Type | Description |
|------|-------------|
| APIs | REST/GraphQL endpoints |
| Files | CSV, Parquet, JSON |
| Streams | Real-time data |

## Connection Properties

### Identity

| Property | Description |
|----------|-------------|
| `id` | Unique identifier |
| `name` | Display name |
| `slug` | URL-safe identifier |
| `type` | Connection type |

### Configuration

| Property | Description |
|----------|-------------|
| `host` | Server address |
| `port` | Server port |
| `database` | Database name |
| `schema` | Default schema |

### Credentials

| Property | Description |
|----------|-------------|
| `username` | Auth username |
| `password` | Auth password (encrypted) |
| `ssl` | SSL configuration |
| `ssh_tunnel` | Tunnel config |

## Connection Lifecycle

### Creation

```
Configure → Test → Save → Active
```

1. Enter connection details
2. Test connectivity
3. Save configuration
4. Connection becomes active

### Testing

Test checks:
- Network connectivity
- Authentication
- Permission access
- Query execution

### Maintenance

Regular maintenance:
- Credential rotation
- Performance monitoring
- Schema refresh
- Permission review

### Deactivation

When removing:
- Check dependencies
- Archive if needed
- Remove credentials
- Update references

## Schema Discovery

### Automatic Discovery

Connections can discover:
- Available schemas
- Tables in schemas
- Columns in tables
- Data types

### Schema Cache

Schema information is cached:
- Reduces query load
- Faster browsing
- Manual refresh available

### Refresh Frequency

| Type | Recommended |
|------|-------------|
| Production | Daily |
| Staging | On demand |
| Development | On demand |

## Query Execution

### Query Flow

```
User Query → Connection → Database → Results → User
```

### Query Limits

| Limit | Default |
|-------|---------|
| Timeout | 120 seconds |
| Row limit | 10,000 rows |
| Result size | 100 MB |

### Query Optimization

Tips:
- Use appropriate indexes
- Limit result sets
- Avoid SELECT *
- Use caching

## Security

### Credential Storage

- Encrypted at rest
- Never logged
- Access controlled
- Regular rotation

### Network Security

| Option | Description |
|--------|-------------|
| SSL/TLS | Encrypted connection |
| SSH Tunnel | Secure tunnel |
| IP Whitelist | Restrict access |
| VPC Peering | Private network |

### Permission Model

Connect with minimal permissions:
- Read-only when possible
- Specific schemas only
- No admin access
- Audit all queries

## Connection Patterns

### Read Replica

Use read replicas for:
- Heavy queries
- Analytics workloads
- No production impact

### Multiple Connections

Create separate connections for:
- Different purposes
- Different permissions
- Different environments
- Performance isolation

### Pooling

Connection pooling:
- Reuse connections
- Reduce overhead
- Better performance
- Resource management

## Monitoring

### Health Checks

Monitor connection health:
- Connectivity status
- Response time
- Error rate
- Query performance

### Alerts

Alert on:
- Connection failures
- High latency
- Authentication errors
- Quota exceeded

### Metrics

Track metrics:
- Queries per minute
- Average response time
- Error rate
- Data transferred

## Best Practices

### Configuration

- Use descriptive names
- Document purpose
- Set appropriate timeouts
- Configure SSL

### Security

- Rotate credentials regularly
- Use minimal permissions
- Enable audit logging
- Review access periodically

### Performance

- Monitor query patterns
- Optimize slow queries
- Use appropriate indexes
- Cache when possible

## Common Issues

### Connection Failures

| Issue | Solution |
|-------|----------|
| Timeout | Increase timeout, check network |
| Auth failed | Verify credentials |
| SSL error | Check SSL configuration |
| Network error | Verify firewall rules |

### Performance Issues

| Issue | Solution |
|-------|----------|
| Slow queries | Optimize query, add indexes |
| High load | Use read replica |
| Timeout | Increase limit, optimize query |
| Memory | Limit result sets |

### Schema Issues

| Issue | Solution |
|-------|----------|
| Missing tables | Refresh schema, check permissions |
| Wrong types | Verify schema, update model |
| Stale cache | Force refresh |
