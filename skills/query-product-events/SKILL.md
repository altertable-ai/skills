---
name: query-product-events
compatibility: Requires Altertable MCP server
description: "Queries product events and identities with SQL (event counts, properties, user activity, traits). Use to answer a question about tracked behavior or confirm new tracking arrives."
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Query Product Events

Use this skill with the Altertable MCP server.

## Quick Start

1. Call `initialize` before any other Altertable MCP tool.
2. Use `list_catalogs`, then inspect the `product_analytics` catalog with `get_catalog`. Do not assume schemas, views, or columns.
3. Choose the identity-resolved event view for user-level analysis and the raw ingestion table only when inspecting payload delivery.
4. Validate SQL with `validate_sql`, then execute it with `query_lakehouse`.
5. State the time range, environment, identity semantics, and any data-quality limitations with the result.

Read the canonical [Product Analytics overview](https://altertable.ai/docs/product-analytics.md) and [query guide](https://altertable.ai/docs/product-analytics/query-data.md) for the current data model and supported analysis paths.

## When to Use This Skill

- Counting or listing tracked product events
- Inspecting event properties or recent user activity
- Joining events to resolved identities or traits
- Investigating whether new instrumentation is arriving
- Analyzing product behavior with SQL
- Comparing event activity across time, environment, plan, or another dimension

Use `instrument-product-analytics` when the task changes application code or sends new events. Prefer:

- `analyze-funnels` for ordered conversion and drop-off
- `analyze-web-traffic` for pageviews, sessions, referrers, UTM, device, or country
- `build-segments` for defining or comparing cohorts
- `query-lakehouse` for generic or cross-catalog SQL

## Query Workflow

### 1. Establish Context

Call `initialize` first. Confirm the organization and environment before inspecting data.

Clarify:

- the event or behavior being measured
- the requested time range and timezone
- whether the metric counts events, sessions, or distinct people
- which environment is in scope
- whether anonymous and aliased identities should be resolved

### 2. Discover the Current Schema

Use `list_catalogs` and `get_catalog` to discover the actual `product_analytics` schemas, tables, views, columns, and semantic definitions.

Do not copy a table path from an old query without checking it. Product Analytics commonly exposes both raw ingestion data and identity-resolved analytical views; choose based on the question rather than convenience.

When a field is stored in event properties, inspect its observed shape before casting or aggregating it.

### 3. Build a Bounded Query

- Fully qualify tables as `catalog.schema.table`.
- Add an explicit time filter.
- Use `LIMIT` while inspecting rows or property shapes.
- Use deterministic `ORDER BY` when results may be paginated.
- Define whether counts are raw events or distinct resolved users.
- Guard casts and ratios against malformed values, nulls, and division by zero.

Validate with `validate_sql`. Use `explain_sql` before a complex or expensive query, then run `query_lakehouse`.

### 4. Check the Result

Before drawing a conclusion:

- compare the result with total volume or a nearby time range
- check null and unknown identity rates when analyzing users
- look for duplicated retries or abrupt ingestion gaps
- distinguish missing events from genuine zero activity
- mention incomplete recent data if ingestion may still be processing

When validating new instrumentation, confirm the event name, environment, expected properties, and identity context. Do not expose a user's sensitive properties in the response.

### 5. Present the Answer

Report:

- the metric and unit
- exact time range and timezone
- event-count versus distinct-user semantics
- filters and environment
- important data-quality caveats

Offer SQL or a rendered insight when useful, but do not save an insight unless the user asks.

## Common Pitfalls

1. Querying before `initialize`
2. Assuming a table or column name instead of inspecting the catalog
3. Mixing raw and identity-resolved events in one metric
4. Treating event count as user count
5. Omitting the time range or environment
6. Casting arbitrary property values without checking their shape
7. Interpreting an ingestion outage as a behavioral drop
8. Returning sensitive traits or event properties unnecessarily
