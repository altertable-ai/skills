---
name: analyze-product-behavior
compatibility: Requires Altertable MCP server and an enabled Product Analytics catalog
description: "Analyzes Altertable Product Analytics events, identities, web sessions, funnels, retention, segmentation, and saved segments. Use for product behavior, conversion, cohorts, event delivery, or identity-aware analysis."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Analyze Product Behavior

Altertable stores Product Analytics beside operational, billing, support, and warehouse data, so product behavior can be analyzed alone or joined across catalogs.

## Establish the Data Model

1. Verify that the Product Analytics catalog is enabled in the intended environment.
2. Inspect its current tables, fields, and semantic definitions rather than assuming them.
3. Use `list_events` for actual event names and recent volume, and `list_user_traits` for available identity attributes.

The built-in catalog commonly contains:

| Table or view | Use |
| --- | --- |
| `product_analytics.main.events` | Raw `/track` payloads and delivery verification |
| `product_analytics.main.identities` | Raw `/identify` payloads |
| `product_analytics.analytics.events` | Identity-resolved behavioral analysis |
| `product_analytics.analytics.identities` | Identity-resolved user profiles |
| `product_analytics.analytics.web_sessions` | Aggregated web sessions |
| `product_analytics.analytics.web_pageviews` | Page-level web analysis |

Inspect the environment because enabled views and columns can evolve. Use raw tables to verify ingestion and resolved views for person-level analysis unless the question explicitly needs raw identity semantics.

Some `properties` keys start with `$`, such as `$utm_source`. DuckDB reads `$` as the JSONPath root, so `properties->>'$utm_source'` fails with `JSON path error near 'utm_source'`. For UTM, referrer, and device breakdowns, use inspected `web_pageviews` columns. When the value lives only in `properties`, quote the key: `json_extract_string(properties, '$."$utm_source"')`. Quote any key that contains `.` or `[` the same way.

Treat `distinct_id`, `anonymous_id`, `session_id`, and `device_id` as opaque text. Their values are not always UUIDs, so do not cast them to `UUID`.

## Web, Funnel, and Segment Semantics

- Use `web_sessions` for session-level volume and engagement, and `web_pageviews` for page-level paths, landing or exit pages, referrers, UTM attribution, and device or geography breakdowns. Inspect the current columns instead of assuming a session timeout or attribution rule.
- A funnel needs at least two sequential events. Make its conversion window, user filters, ordering, counting entity, and date range explicit; report step counts, conversion, drop-off, and step timing without importing industry benchmarks. Disclose sampled or approximate results.
- A reusable Segment is an audience definition. Read the live schema for filter operators and property paths.
- For retention, make the starting event, the return event, “return on” versus “return on or after”, and calendar versus rolling windows explicit.

For open-ended questions, prefer the `ask-altertable` fast path. For exact control, run DuckDB SQL with `query-altertable`. Use `build-data-app` when the user requests a reusable, persisted view of the analysis.

## Behavior-Oriented SQL

Altertable augments DuckDB with behavior-oriented SQL features. Use them when sequence, session, or path semantics would make an investigation more accurate or reveal behavior hidden by ordinary aggregates. Before writing or reviewing a query with one of these features, read its linked reference for the inlined syntax, semantics, output modes, and constraints:

- [`MATCH_RECOGNIZE`](references/match-recognize.md) matches ordered row patterns with a regular-expression-like pattern for funnels, state transitions, journeys, and anomaly shapes. Use it when the sequence to detect is known in advance and needs explicit row roles, alternatives, repetition, and filler events. Partition by the investigated entity, order deterministically with a stable tie-breaker, and bound conversion windows explicitly.
- [`SESSIONIZE`](references/sessionize.md) groups ordered events into sessions using an inactivity gap without requiring a lag, cumulative sum, and grouping pipeline. It compares each event with the preceding event, so a session can outlast the gap while consecutive events remain close enough. Choose row-preserving output or one row per session with measures according to whether downstream analysis needs individual events or session summaries; use it to reconstruct visits or workflows and to distinguish event-level from session-level behavior.
- [`JOURNEYS`](references/journeys.md) discovers the paths people take before, after, or between events without defining the path in advance. It aggregates identical paths rather than returning one row per person and reports conversion, truncation, frequency, and duration. Use it to expose detours, loops, unexpected steps, and where successful and failed paths diverge; set the counting mode, time window, and maximum retained steps explicitly.

## Accuracy Rules

- State whether a result counts events, sessions, anonymous IDs, or resolved people.
- Make the environment, date range, timezone, and interval explicit.
- Inspect property shape before casting values stored in JSON.
- Check unknown identity rates, duplicated retries, and ingestion gaps before interpreting a sudden change as behavior.
- Hold event definitions, filters, timeframe, and calculation mode constant when comparing cohorts.
- Sampling and approximate distinct counts trade exactness for speed; disclose either when enabled.
- Do not use generic industry benchmarks as evidence for a user's product.

When validating new instrumentation, confirm the exact event name, expected properties, environment, and identity context without returning sensitive values.
