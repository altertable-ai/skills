---
name: ask
description: Routes user queries to the best Altertable skill. Invoke with /altertable:ask <query> when unsure which skill to use.
metadata:
  author: altertable-ai
---

# Altertable

Entry point for all Altertable skills. Match the user's query to the best skill and invoke it.

1. Read the user's query: `$ARGUMENTS`
2. Match it against the routing table below
3. Invoke the best matching skill using the Skill tool
4. If no clear match, invoke `understanding-platform` to orient the user

## Routing Table

| Skill | When to route |
|-------|---------------|
| `exploring-data` | Asks about tables, columns, schemas, data sources, what data is available |
| `querying-lakehouse` | Wants to run SQL, query data, build reports, aggregate metrics, analyze data in connections |
| `analyzing-funnels` | Asks about conversion rates, user journeys, drop-off, step progression, onboarding flows |
| `analyzing-web-traffic` | Asks about pageviews, sessions, traffic sources, web metrics, user behavior on websites |
| `analyzing-insights` | Wants to interpret charts, understand patterns in visualizations, explain what data shows |
| `building-segments` | Wants to segment users, compare cohorts, filter by properties, build audiences |
| `forecasting-timeseries` | Asks about trends, anomalies, predictions, spikes, drops, forecasting, projections |
| `tracking-events` | Asks about event tracking, user identification, aliasing, traits, analytics instrumentation |
| `creating-insights` | Wants to save findings, create visualizations, surface patterns, share analysis results |
| `deciding-actions` | Unsure which insight type to use, choosing between funnel/retention/semantic/SQL/segmentation |
| `managing-discoveries` | Asks about discovery approval, review workflow, user feedback, discovery lifecycle |
| `configuring-watchers` | Wants to set up monitoring, scheduled analysis, alerts, autonomous data observation |
| `using-memory` | Wants to save findings, recall past analysis, build knowledge, search for context |
| `evaluating-skills` | Asks about skill quality, writing new skills, skill structure or specification |
| `understanding-platform` | Asks what Altertable is, how agents work, platform concepts, architecture overview |

## Routing Rules

1. **Single best match**: Pick the one skill that best fits the query. Do not invoke multiple skills.
2. **Ambiguous queries**: If the query could match multiple skills, prefer the more specific one (e.g., `analyzing-funnels` over `querying-lakehouse` for "conversion funnel").
3. **Data-first queries**: If the user wants to analyze data but doesn't specify how, start with `exploring-data` to understand what's available.
4. **Unknown queries**: If the query doesn't match any skill, invoke `understanding-platform` to explain what Altertable can do.
5. **Pass arguments through**: When invoking the matched skill, pass the original `$ARGUMENTS` so the skill has the full user context.
