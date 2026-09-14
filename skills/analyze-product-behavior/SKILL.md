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
- Use a segmentation insight for event metrics over time with event, user, or session-property breakdowns.
- Use `draft_segment` when the user is iterating on a reusable segment object; a segment is not the same object as a segmentation insight.
- Query `web_sessions` and `web_pageviews` for source, UTM, landing-page, device, and session questions.
- Use direct DuckDB SQL when the analysis requires cross-catalog joins or logic unavailable in the builders.

For open-ended questions, prefer the `ask-altertable` fast path. For a controlled preview, call `render_insight` with the definition and timeframe required by its live schema. Use `draft_insight` for UI iteration and `build-insights` for persistence.

## Accuracy Rules

- State whether a result counts events, sessions, anonymous IDs, or resolved people.
- Make the environment, date range, timezone, and interval explicit.
- Inspect property shape before casting values stored in JSON.
- Check unknown identity rates, duplicated retries, and ingestion gaps before interpreting a sudden change as behavior.
- Hold event definitions, filters, timeframe, and calculation mode constant when comparing cohorts.
- Sampling and approximate distinct counts trade exactness for speed; disclose either when enabled.
- Do not use generic industry benchmarks as evidence for a user's product.

When validating new instrumentation, confirm the exact event name, expected properties, environment, and identity context without returning sensitive values.
