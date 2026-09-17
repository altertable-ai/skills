---
name: investigate-opentelemetry
compatibility: Requires Altertable MCP server
description: "Investigates OpenTelemetry logs and traces in Altertable using SQL. Use when analysis involves observability data, including debugging, trace correlation, or joins with business data."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Investigate OpenTelemetry Logs and Traces

Use SQL to investigate logs and traces.

## Tables

Logs:

```sql
opentelemetry.main.logs
```

Traces:

```sql
opentelemetry.main.spans
```

## Narrow the Query

Start with the smallest useful query: time range, environment, service or deployment, then error/trace filters.

## Filter Attributes

Resource attributes are stored in `resource_attributes` VARIANT. Span/log attributes are stored in `attributes` VARIANT.

Use `variant_extract` for filters:

```sql
variant_extract(resource_attributes, 'env') = 'production'
variant_extract(resource_attributes, 'k8s.pod.name') ILIKE 'api-%'
variant_extract(attributes, 'http.method') = 'POST'
variant_extract(attributes, 'http.route') = '/graphql'
```

For numeric attributes, cast before comparing:

```sql
TRY_CAST(variant_extract(attributes, 'http.status_code') AS INTEGER) >= 500
```

## Search Messages

Use the `@@` operator for full text search on indexed columns instead of `LIKE`/`ILIKE`. Only the `message` column is indexed for full text search:

```sql
message @@ 'timeout'
message @@ 'connection refused'
message @@ 'error'
```

## Filter by Time

Use `timestamp` for log time filters:

```sql
SELECT *
FROM opentelemetry.main.logs
WHERE timestamp >= now() - INTERVAL '1 hour'
  AND variant_extract(resource_attributes, 'env') = 'production'
  AND service_name = 'api'
ORDER BY timestamp DESC
LIMIT 500;
```

Use `start_time` for trace time filters:

```sql
SELECT *
FROM opentelemetry.main.spans
WHERE start_time >= now() - INTERVAL '1 hour'
  AND variant_extract(resource_attributes, 'env') = 'production'
  AND service_name = 'api'
ORDER BY start_time DESC
LIMIT 100;
```

## Pivot by Trace ID

Pivot by `trace_id` when available:

```sql
SELECT *
FROM opentelemetry.main.spans
WHERE trace_id = '<trace-id>'
ORDER BY start_time ASC;
```

```sql
SELECT *
FROM opentelemetry.main.logs
WHERE trace_id = '<trace-id>'
ORDER BY timestamp ASC;
```
