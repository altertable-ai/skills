---
name: query-product-events
compatibility: Requires Altertable MCP server
description: Queries Altertable product analytics events and identity tables with DuckDB SQL. Use when inspecting tracked events, event properties, identities, traits, aliases, event counts, or raw product behavior already stored in Altertable.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Query Product Events

Query the built-in `product_analytics` catalog for event and identity questions. Prefer resolved analytics tables unless the user explicitly needs the raw ingestion payload.

## Quick Start

1. Call `initialize` before other Altertable MCP tools.
2. Confirm table shape with `get_catalog` when columns or property types are unclear.
3. Choose raw or identity-resolved tables deliberately.
4. Validate SQL, execute it with `query_lakehouse`, and explain the result in product terms.

## Choose the Right Table

| Table | Use it for |
|-------|------------|
| `product_analytics.main.events` | Raw `/track` payloads and ingestion debugging |
| `product_analytics.analytics.events` | Event analysis with anonymous and aliased identity resolution |
| `product_analytics.analytics.identities` | Current identity traits and profile state |
| `product_analytics.analytics.web_pageviews` | Page-level web behavior; route broader analysis to `analyze-web-traffic` |
| `product_analytics.analytics.web_sessions` | Session and acquisition metrics; route broader analysis to `analyze-web-traffic` |

## Common Queries

### Event Counts by Type

```sql
SELECT
  event,
  properties->>'currency' AS currency,
  COUNT(*) AS total
FROM product_analytics.analytics.events
WHERE timestamp >= current_date - INTERVAL '30 days'
GROUP BY ALL
ORDER BY total DESC;
```

### Events for a User

```sql
SELECT
  event,
  properties,
  timestamp,
  identity_traits->>'email' AS email,
  identity_traits->>'plan' AS plan
FROM product_analytics.analytics.events
WHERE distinct_id = 'u_01jza857w4f23s1hf2s61befmw'
ORDER BY timestamp DESC;
```

### Current Identity Traits

```sql
SELECT
  distinct_id,
  traits->>'email' AS email,
  traits->>'plan' AS plan,
  updated_at
FROM product_analytics.analytics.identities
ORDER BY updated_at DESC;
```

### Inspect Property Coverage

```sql
SELECT
  event,
  COUNT(*) AS events,
  COUNT(properties->>'plan') AS with_plan,
  COUNT(properties->>'plan')::DOUBLE / COUNT(*) AS plan_coverage
FROM product_analytics.analytics.events
WHERE timestamp >= current_date - INTERVAL '7 days'
GROUP BY event
ORDER BY events DESC;
```

## Query Workflow

1. Establish the event names, time range, environment, and identity semantics needed.
2. Use `analytics.events` by default; use `main.events` only for payload-level diagnostics.
3. Extract JSON properties with `->>` and cast before numeric or date calculations.
4. Filter time and environment early to reduce scanned data.
5. Add deterministic ordering whenever results may be paginated.
6. Validate the query before execution and inspect unexpected nulls or duplicates.
7. State whether counts represent events, unique identities, sessions, or another unit.

## Boundaries and Collision Rules

- Use `instrument-product-analytics` when the user wants to add, fix, or review SDK/API tracking code.
- Use `analyze-funnels` for ordered multi-step conversion, completion, and drop-off questions.
- Use `analyze-web-traffic` for pageviews, sessions, referrers, UTM dimensions, bounce, and acquisition.
- Use `build-segments` when the output is a reusable cohort or audience definition rather than query results.
- Use `query-lakehouse` for cross-catalog joins, non-product data, or general DuckDB work. Keep this skill when product event or identity semantics are central.

## Common Pitfalls

- **Using raw events by default**: aliases and anonymous identities may not be resolved.
- **Confusing events with users**: use `COUNT(*)` for events and a documented identity key for unique people.
- **Comparing unbounded periods**: always apply a clear time range and equal comparison windows.
- **Treating JSON as typed data**: extract and cast properties before arithmetic or chronological comparisons.
- **Ignoring environment**: development and production events can distort the same metric.
- **Inferring instrumentation bugs too quickly**: compare raw and resolved tables before concluding data was dropped.
- **Rebuilding specialized analysis manually**: route funnels and web traffic to their narrower skills.

## References

- [Product event query patterns](references/query-patterns.md) - Read for identity semantics, JSON extraction, validation, and debugging patterns.
