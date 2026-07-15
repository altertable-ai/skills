# Product Event Query Patterns

## Raw vs Resolved Events

Start with `product_analytics.analytics.events` for behavioral analysis. It applies anonymous and alias identity resolution and exposes identity traits with events.

Use `product_analytics.main.events` when validating the payload that reached ingestion, checking a newly added property, or comparing raw and resolved identity behavior.

## Count Units

Name the counting unit in both SQL aliases and the explanation:

```sql
SELECT
  COUNT(*) AS event_count,
  COUNT(DISTINCT distinct_id) AS identity_count
FROM product_analytics.analytics.events
WHERE event = 'Purchase Completed';
```

An identity count is not necessarily a real-person count when users can remain anonymous or share devices.

## JSON Properties

`->>` extracts text. Cast values before aggregation:

```sql
SELECT
  AVG(TRY_CAST(properties->>'amount' AS DOUBLE)) AS average_amount
FROM product_analytics.analytics.events
WHERE event = 'Purchase Completed';
```

Use `TRY_CAST` while exploring inconsistent historical payloads. Surface failed casts as a data-quality finding instead of silently assuming zero.

## Validate New Instrumentation

Compare recent raw payload coverage before and after deployment:

```sql
SELECT
  date_trunc('hour', timestamp) AS hour,
  COUNT(*) AS events,
  COUNT(properties->>'new_property') AS populated
FROM product_analytics.main.events
WHERE event = 'Example Event'
  AND timestamp >= current_timestamp - INTERVAL '24 hours'
GROUP BY 1
ORDER BY 1;
```

If raw events exist but resolved events do not, inspect identity inputs and alias behavior. If neither exists, inspect environment, API credentials, consent, network delivery, and the instrumentation call.
