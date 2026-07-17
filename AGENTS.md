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

- Codex: `$altertable:ask <query>`; Claude Code: `/altertable:ask <query>` (see `skills/ask/SKILL.md`)

## Available Skills

<available_skills>
  <skill>
    <name>analyze-funnels</name>
    <description>Creates and analyzes conversion funnels. Use when analyzing user journeys, drop-off points, onboarding, checkout, or multi-step flows.</description>
  </skill>
  <skill>
    <name>analyze-insights</name>
    <description>Interprets Insight data to identify patterns, anomalies, and trends. Use when analyzing visualizations, extracting findings, or explaining patterns in graphs.</description>
  </skill>
  <skill>
    <name>analyze-web-traffic</name>
    <description>Analyzes web analytics traffic patterns and user behavior. Use when asked about pageviews, sessions, traffic sources, or website user behavior.</description>
  </skill>
  <skill>
    <name>ask</name>
    <description>Routes user queries to the best-fit Altertable skill. Use when unsure which Altertable skill applies to a request.</description>
  </skill>
  <skill>
    <name>build-segments</name>
    <description>Builds segmentation insights with filters and breakdowns. Use when comparing aggregate event metrics by properties or user traits.</description>
  </skill>
  <skill>
    <name>configure-tasks</name>
    <description>Configures scheduled AI tasks that analyze Insights and Dashboards. Use for anomaly detection, forecasting, alerts, or recurring automated monitoring.</description>
  </skill>
  <skill>
    <name>create-discoveries</name>
    <description>Creates Altertable discoveries from meaningful findings. Use when analysis finds a change, anomaly, root cause, recommendation, warning, or contextual finding that should notify users and enter review.</description>
  </skill>
  <skill>
    <name>create-insights</name>
    <description>Creates, drafts, renders, and saves Altertable insights. Use when generating findings, creating visualizations, or saving and sharing analysis results.</description>
  </skill>
  <skill>
    <name>decide-actions</name>
    <description>Decision matrices for picking insight types (funnel, retention, semantic, segmentation, SQL), task types, and discovery actions. Use when choosing types or whether to create or skip discoveries.</description>
  </skill>
  <skill>
    <name>evaluate-skills</name>
    <description>Evaluates and creates agent skills following best practices. Use when reviewing, writing, or refactoring skills, or asking about skill structure, format, or specification.</description>
  </skill>
  <skill>
    <name>explore-data</name>
    <description>Explores Altertable catalogs, schemas, semantic models, tables, and columns. Use when asking about available data, data structure, connections, or sources before querying.</description>
  </skill>
  <skill>
    <name>forecast-timeseries</name>
    <description>Analyzes time series for trends, anomalies, and forecasts. Use when detecting spikes or drops, predicting future values, or finding unusual patterns over time.</description>
  </skill>
  <skill>
    <name>manage-discoveries</name>
    <description>Manages the discovery approval workflow. Use when handling discovery reviews, approval states, user feedback, or discovery lifecycle.</description>
  </skill>
  <skill>
    <name>query-lakehouse</name>
    <description>Writes, validates, optimizes, and executes DuckDB SQL against the Altertable lakehouse. Use when analyzing data, aggregating metrics, building reports, or querying catalogs and external connections.</description>
  </skill>
  <skill>
    <name>track-events</name>
    <description>Works with Altertable product analytics events, user identification, and aliasing. Use when tracking events, identifying users, managing traits, or resolving identities.</description>
  </skill>
  <skill>
    <name>understand-platform</name>
    <description>Explains Altertable platform concepts and architecture. Use when asking what Altertable is or how agents, discoveries, memories, insights, and dashboards fit together.</description>
  </skill>
  <skill>
    <name>use-memory</name>
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
