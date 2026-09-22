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

## Web, Funnel, and Segment Semantics

- Use `web_sessions` for session-level volume and engagement, and `web_pageviews` for page-level paths, landing or exit pages, referrers, UTM attribution, and device or geography breakdowns. Inspect the current columns instead of assuming a session timeout or attribution rule.
- A funnel needs at least two sequential events. Make its conversion window, user filters, ordering, counting entity, and date range explicit; report step counts, conversion, drop-off, and step timing without importing industry benchmarks. Disclose sampled or approximate results.
- A reusable Segment is an audience definition; a Segmentation Insight compares event metrics over time and is not the same object. Read the live schema for filter operators and property paths.

## Choose the Altertable Analysis

- Use a funnel insight for ordered event progression and drop-off.
- Use a retention insight for return behavior after a starting event, including its “return on” versus “return on or after” and calendar versus rolling-window choices.
- Prefer a segmentation insight for event metrics over time compared across properties, identity attributes, or behavioral cohorts.
- Use native breakdowns when the required grouping values are stored on events or identities. Use a semantic or SQL insight when the analysis requires derived dimensions or aggregates unavailable in segmentation.
- Use direct DuckDB SQL when the analysis requires cross-catalog joins or logic unavailable in the builders.

For open-ended questions, prefer the `ask-altertable` fast path. For a controlled preview on a user-facing surface, call `render_insight` with a `definition`, including the timeframe its kind requires. Use `execute_insight` with that same `definition` when the caller cannot or should not attach the Insight Viewer, such as a subagent. A `definition` does not persist an Insight. Use `build-insights` when the user requests a reusable persisted analysis.

## Behavior-Oriented SQL

Altertable augments DuckDB with behavior-oriented SQL features. Use them when sequence, session, or path semantics would make an investigation more accurate or reveal behavior hidden by ordinary aggregates. Before writing or reviewing a query with one of these features, read its linked reference for the inlined syntax, semantics, output modes, and constraints:

- [`MATCH_RECOGNIZE`](references/match-recognize.md) matches ordered row patterns with a regular-expression-like pattern for funnels, state transitions, journeys, and anomaly shapes. Use it when the sequence to detect is known in advance and needs explicit row roles, alternatives, repetition, and filler events. Partition by the investigated entity, order deterministically with a stable tie-breaker, and bound conversion windows explicitly.
- [`SESSIONIZE`](references/sessionize.md) groups ordered events into sessions using an inactivity gap without requiring a lag, cumulative sum, and grouping pipeline. It compares each event with the preceding event, so a session can outlast the gap while consecutive events remain close enough. Choose row-preserving output or one row per session with measures according to whether downstream analysis needs individual events or session summaries; use it to reconstruct visits or workflows and to distinguish event-level from session-level behavior.
- [`JOURNEYS`](references/journeys.md) discovers the paths people take before, after, or between events without defining the path in advance. It aggregates identical paths rather than returning one row per person and reports conversion, truncation, frequency, and duration. Use it to expose detours, loops, unexpected steps, and where successful and failed paths diverge; set the counting mode, time window, and maximum retained steps explicitly.

## Native Cohort and Identity Filters

Check these primitives before writing a join or self-join for product-event analysis. Use the live schema for the full definition and inspect actual event names, property values, dimensions, and relations.

- **Related-model attributes:** use `segmented_by.filters[].dimension_filter` with a `dimension_ref` for the related model's dimension. The engine resolves supported joins through the declared relation; an attribute living outside the events table is not itself a reason to choose SQL. Confirm the dimension and relation exist first.
- **Behavioral cohort membership:** use `filters[].performed_event_filter` to include or exclude identities based on event performance. To compare complementary cohorts, use two separate `segmented_by` entries with distinct keys and identical membership conditions, setting `including: true` for one and `including: false` for the other. Filtering the events being measured does not filter identities by their event history.
- **Cohort scope:** set the performed-event filter's `period` to the intended membership window. Without it, membership considers all available history, not just the chart's date range. Membership is identity-based; it does not enforce ordered or same-session conversion. Use a funnel for ordered progression and select the appropriate counting entity. Treat identity attributes and event performance as distinct conditions.

### Breakdown Boundary

Segmentation `breakdowns` group by stored values of an event `property` or identity `trait`; they do not accept arbitrary semantic dimensions or transformation expressions. Filtering on a semantic dimension does not make that dimension available as a segmentation breakdown.

If the needed grouping and measure are exposed together by a semantic model, use a Semantic Insight. Choose SQL only when the required capability is unavailable in native definitions, such as derived grouping, cross-catalog joins, or custom aggregation logic. Do not turn one widget's requirement into a SQL default for the whole dashboard.

## Accuracy Rules

- State whether a result counts events, sessions, anonymous IDs, or resolved people.
- Make the environment, date range, timezone, and interval explicit.
- Inspect property shape before casting values stored in JSON.
- Check unknown identity rates, duplicated retries, and ingestion gaps before interpreting a sudden change as behavior.
- Hold event definitions, filters, timeframe, and calculation mode constant when comparing cohorts.
- Sampling and approximate distinct counts trade exactness for speed; disclose either when enabled.
- Do not use generic industry benchmarks as evidence for a user's product.

When validating new instrumentation, confirm the exact event name, expected properties, environment, and identity context without returning sensitive values.
