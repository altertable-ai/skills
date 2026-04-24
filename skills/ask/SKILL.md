---
name: ask
description: Routes the user's query to the best-fit Altertable skill. Use when an AI agent needs to decide which Altertable skill to invoke for a user request.
metadata:
  author: altertable-ai
---

# Altertable Ask

Central entry point for Altertable skills. Every Altertable task starts here. Match the user query to the best available skill and hand off.

## Procedure

1. Read the user's query.
2. Match the query against the routing table below, then apply the rules.
3. Invoke the matched skill via the Skill tool, passing the original query through so the matched skill has full context.
4. If no skill matches with confidence, invoke `understanding-platform` to orient the user.

## Routing Table

| Skill | When to route |
|-------|---------------|
| `exploring-data` | Discover what data exists: connections, schemas, tables, columns, semantic models |
| `querying-lakehouse` | Run an ad-hoc SQL query against the lakehouse to answer a specific question |
| `analyzing-funnels` | Build or analyze a step-by-step conversion flow (drop-off between ordered events) |
| `analyzing-web-traffic` | Web analytics: pageviews, sessions, traffic sources, UTM, device, country breakdowns |
| `analyzing-insights` | Interpret an existing chart or visualization the user is looking at |
| `building-segments` | Define or compare user cohorts by properties (not step-based) |
| `forecasting-timeseries` | Project future metric values or detect whether a change is within normal range |
| `tracking-events` | Work with tracked product analytics events, identities, or traits (querying or advising on instrumentation) |
| `creating-insights` | Create a new chart or discovery that will be saved and visible to users |
| `deciding-actions` | Decide which insight or task type to use, or whether to create / update / skip a discovery |
| `managing-discoveries` | Review, approve, or reject existing discoveries and process user feedback on them |
| `configuring-tasks` | Set up a scheduled AI task (anomaly detection, forecast, monitor) that runs on a cron |
| `using-memory` | Persist or retrieve agent-side context across runs (not user-visible findings; that is `creating-insights`) |
| `evaluating-skills` | Review or author agent skills themselves (skill structure, spec, quality) |
| `understanding-platform` | Explain Altertable concepts, architecture, or how agents work |

When a skill is added, renamed, or removed from this repository, update this table in the same change.

## Routing Rules

1. **Single best match**: pick one skill. Do not fan out.
2. **Prefer the narrower skill**: when two skills could match, prefer the more specific one.
3. **Data-first when intent is vague**: if the user wants to analyze data but does not specify how, start with `exploring-data`.
4. **Fallback for unknown queries**: if nothing matches with confidence, route to `understanding-platform`.
5. **Pass context through**: hand the original query to the matched skill.
6. **Never invent a skill**: only invoke skills that are actually installed.
