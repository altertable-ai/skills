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

Spans and logs are wide: `attributes`, `resource_attributes`, and the span `events` and `links` hold large VARIANT payloads. Never `SELECT *` from them. Select only the columns the question needs, and extract single attributes with `variant_extract`.

## Aggregate First

Count, rate, and rank in SQL over the whole window before reading any rows. A few rows of a busy service rarely contain the incident:

```sql
SELECT
  service_name,
  date_trunc('minute', start_time) AS minute,
  count(*) AS spans,
  count(*) FILTER (WHERE status_code = 'STATUS_CODE_ERROR') AS errors,
  quantile_cont(duration_ns / 1e6, 0.95) AS p95_ms
FROM opentelemetry.main.spans
WHERE start_time >= now() - INTERVAL '1 hour'
  AND variant_extract(resource_attributes, 'env') = 'production'
GROUP BY ALL
ORDER BY errors DESC, minute
LIMIT 50;
```

Then fetch a few example rows or trace IDs from the windows the aggregate points to.

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
SELECT timestamp, severity_text, trace_id, message
FROM opentelemetry.main.logs
WHERE timestamp >= now() - INTERVAL '1 hour'
  AND variant_extract(resource_attributes, 'env') = 'production'
  AND service_name = 'api'
  AND severity_number >= 17
ORDER BY timestamp DESC
LIMIT 20;
```

Use `start_time` for trace time filters:

```sql
SELECT start_time, trace_id, span_id, name, status_code, duration_ns / 1e6 AS duration_ms
FROM opentelemetry.main.spans
WHERE start_time >= now() - INTERVAL '1 hour'
  AND variant_extract(resource_attributes, 'env') = 'production'
  AND service_name = 'api'
  AND status_code = 'STATUS_CODE_ERROR'
ORDER BY start_time DESC
LIMIT 20;
```

## Pivot by Trace ID

Pivot by `trace_id` when available:

```sql
SELECT start_time, span_id, parent_span_id, service_name, name, status_code, status_message, duration_ns / 1e6 AS duration_ms
FROM opentelemetry.main.spans
WHERE trace_id = '<trace-id>'
ORDER BY start_time ASC;
```

```sql
SELECT timestamp, span_id, service_name, severity_text, message
FROM opentelemetry.main.logs
WHERE trace_id = '<trace-id>'
ORDER BY timestamp ASC;
```
