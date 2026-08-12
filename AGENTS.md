# AGENTS.md

Guidance for AI coding agents working with this repository.

## Repository Overview

A collection of skills for AI agents following the [Agent Skills Specification](https://agentskills.io/specification).

## Structure

```
skills/
  {skill-name}/
    SKILL.md
    references/
      {topic}.md

scripts/
  score-skills.py
  scorer/
  tests/
```

## Creating a New Skill

### Naming Convention

Use an imperative verb, lowercase, and hyphens only:
- `analyze-data` ✓
- `analyzing-data` ✗

### SKILL.md Format

```markdown
---
name: {skill-name}
description: {Third-person description with trigger keywords}
---

# {Skill Title}

## Quick Start
{Immediate actionable example}

## When to Use This Skill
{Bullet points with trigger conditions}

## Common Pitfalls
{5-10 mistakes to avoid}

## References
{Links to references/ files}
```

### Best Practices

- Keep SKILL.md under 500 lines
- Move details to references/
- Third-person descriptions ("Analyzes..." not "I help you...")
- Include trigger keywords
- References one level deep only

## Commands

- `/altertable:ask <query>` -- routes user queries to the best skill (see `skills/ask/SKILL.md`)

## Available Skills

<available_skills>
  <skill>
    <name>analyze-funnels</name>
    <description>Builds conversion funnels over ordered steps. Use for user journeys, drop-off, onboarding, checkout, or multi-step flows. Returns a funnel insight.</description>
  </skill>
  <skill>
    <name>analyze-insights</name>
    <description>Explains what an existing insight or chart shows. Use when asked what a visualization or graph means, or to read out its outliers. Does not run a query.</description>
  </skill>
  <skill>
    <name>analyze-web-traffic</name>
    <description>Analyzes website traffic (pageviews, sessions, referrers, landing pages). Use for site visits, traffic sources, bounce, or visitor behavior.</description>
  </skill>
  <skill>
    <name>ask</name>
    <description>Routes user queries to the best-fit Altertable skill. Use when unsure which Altertable skill applies to a request.</description>
  </skill>
  <skill>
    <name>build-segments</name>
    <description>Compares event metrics across cohorts using filters, breakdowns, and dimensions. Use to define an audience or compare groups such as free versus paid. Returns a segmentation insight.</description>
  </skill>
  <skill>
    <name>configure-tasks</name>
    <description>Schedules recurring AI tasks over insights and dashboards. Use for alerts, cron-style monitoring, or anomaly and forecast checks that run on their own.</description>
  </skill>
  <skill>
    <name>create-discoveries</name>
    <description>Reports a change, anomaly, root cause, recommendation, or warning to users. Use when analysis produces something worth telling someone. Returns a discovery that enters review.</description>
  </skill>
  <skill>
    <name>create-insights</name>
    <description>Drafts, renders, and saves insights of every type (SQL, semantic, segmentation, funnel, retention). Use to build, preview, or share a visualization. Returns a saved insight.</description>
  </skill>
  <skill>
    <name>decide-actions</name>
    <description>Decision matrices for picking insight types (funnel, retention, semantic, segmentation, SQL), task types, and discovery actions. Use when choosing types or whether to create, update, or skip discoveries.</description>
  </skill>
  <skill>
    <name>evaluate-skills</name>
    <description>Evaluates and authors agent skills against the Agent Skills spec. Use when reviewing, writing, or refactoring a SKILL.md, or asking about structure, frontmatter, or naming.</description>
  </skill>
  <skill>
    <name>explore-data</name>
    <description>Inspects catalogs, schemas, tables, columns, semantic models, measures, and dimensions. Use to find what data exists or a table&#x27;s columns. Reads metadata, runs no query.</description>
  </skill>
  <skill>
    <name>forecast-timeseries</name>
    <description>Runs on-demand statistics over a time series to spot outliers and project values. Use for whether a spike is normal, or what a metric reaches next week.</description>
  </skill>
  <skill>
    <name>instrument-product-analytics</name>
    <description>Adds Altertable product analytics to an application (event tracking, user identification, traits, consent, session reset, aliasing). Use when writing instrumentation code.</description>
  </skill>
  <skill>
    <name>manage-discoveries</name>
    <description>Reviews, approves, and rejects existing discoveries. Use for the approval queue, discovery states, or user feedback on a discovery.</description>
  </skill>
  <skill>
    <name>query-lakehouse</name>
    <description>Writes, validates, optimizes, and runs DuckDB SQL against the Altertable lakehouse. Use when answering a question requires executing a query, joining tables, or aggregating metrics.</description>
  </skill>
  <skill>
    <name>query-product-events</name>
    <description>Queries product events and identities with SQL (event counts, properties, user activity, traits). Use to answer a question about tracked behavior or confirm new tracking arrives.</description>
  </skill>
  <skill>
    <name>understand-platform</name>
    <description>Explains Altertable concepts and architecture. Use for what Altertable is, or how agents, discoveries, insights, memories, and dashboards relate. Concepts only.</description>
  </skill>
  <skill>
    <name>use-memory</name>
    <description>Stores and recalls agent memories and org knowledge between sessions. Use to remember a definition, threshold, or convention, or recall earlier context. Not user-facing.</description>
  </skill>
</available_skills>

## Scoring development

```bash
uv sync
uv run pre-commit install
uv run pytest scripts/tests/
uv run skills validate ./skills/skill-name
```
