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

Use **gerund form** (verb + -ing), lowercase, hyphens only:
- `analyzing-data` ✓
- `analyze-data` ✗

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
    <name>analyzing-funnels</name>
    <description>Creates and analyzes conversion funnels. Use when analyzing user journeys, drop-off points, onboarding, checkout, or multi-step flows.</description>
  </skill>
  <skill>
    <name>analyzing-insights</name>
    <description>Interprets Insight data to identify patterns, anomalies, and trends. Use when analyzing visualizations, extracting findings, or explaining patterns in graphs.</description>
  </skill>
  <skill>
    <name>analyzing-web-traffic</name>
    <description>Analyzes web analytics traffic patterns and user behavior. Use when asked about pageviews, sessions, traffic sources, or website user behavior.</description>
  </skill>
  <skill>
    <name>ask</name>
    <description>Routes user queries to the best-fit Altertable skill. Use when unsure which Altertable skill applies to a request.</description>
  </skill>
  <skill>
    <name>building-segments</name>
    <description>Builds segmentation insights with filters, dimensions, and breakdowns. Use when segmenting users, comparing event metrics by properties, building cohorts, or defining audiences.</description>
  </skill>
  <skill>
    <name>configuring-tasks</name>
    <description>Configures scheduled AI tasks that analyze Insights and Dashboards. Use for anomaly detection, forecasting, alerts, or recurring automated monitoring.</description>
  </skill>
  <skill>
    <name>creating-insights</name>
    <description>Creates discoveries with insights through the approval workflow. Use when generating findings, creating visualizations, or saving and sharing analysis results.</description>
  </skill>
  <skill>
    <name>deciding-actions</name>
    <description>Decision matrices for picking insight types (funnel, retention, semantic, segmentation, SQL), task types, and discovery actions. Use when choosing types or whether to create, update, or skip discoveries.</description>
  </skill>
  <skill>
    <name>evaluating-skills</name>
    <description>Evaluates and creates agent skills following best practices. Use when reviewing, writing, or refactoring skills, or asking about skill structure, format, or specification.</description>
  </skill>
  <skill>
    <name>exploring-data</name>
    <description>Explores data connections and schemas. Use when asking about tables, columns, data types, data structure, or available sources before querying.</description>
  </skill>
  <skill>
    <name>forecasting-timeseries</name>
    <description>Analyzes time series for trends, anomalies, and forecasts. Use when detecting spikes or drops, predicting future values, or finding unusual patterns over time.</description>
  </skill>
  <skill>
    <name>managing-discoveries</name>
    <description>Manages the discovery approval workflow. Use when handling discovery reviews, approval states, user feedback, or discovery lifecycle.</description>
  </skill>
  <skill>
    <name>querying-lakehouse</name>
    <description>Writes and executes DuckDB SQL against the Altertable lakehouse. Use when analyzing data, aggregating metrics, building reports, or querying tables in connections.</description>
  </skill>
  <skill>
    <name>tracking-events</name>
    <description>Works with Altertable product analytics events, user identification, and aliasing. Use when tracking events, identifying users, managing traits, or resolving identities.</description>
  </skill>
  <skill>
    <name>understanding-platform</name>
    <description>Explains Altertable platform concepts and architecture. Use when asking what Altertable is or how agents, discoveries, memories, insights, and dashboards fit together.</description>
  </skill>
  <skill>
    <name>using-memory</name>
    <description>Stores and retrieves agent memories for context persistence. Use when saving findings, recalling past analysis, or searching for relevant context.</description>
  </skill>
</available_skills>

## Scoring development

```bash
uv sync
uv run pre-commit install
uv run pytest scripts/tests/
uv run skills validate ./skills/skill-name
```
