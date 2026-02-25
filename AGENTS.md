# AGENTS.md

Guidance for AI coding agents working with this repository.

## Repository Overview

A collection of skills for AI agents following the [Agent Skills Specification](https://agentskills.io/specification).

## Structure

```
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

## Available Skills

<available_skills>
  <skill>
    <name>analyzing-charts</name>
    <description>Interprets chart data to identify patterns, anomalies, and trends. Use when analyzing visualizations, extracting insights from charts, explaining what data shows, or when asked about patterns in graphs.</description>
  </skill>
  <skill>
    <name>analyzing-funnels</name>
    <description>Creates and analyzes conversion funnels to understand user journeys and drop-off points. Use when analyzing conversion, onboarding, checkout flows, or multi-step processes.</description>
  </skill>
  <skill>
    <name>analyzing-web-traffic</name>
    <description>Analyzes web analytics data to identify traffic patterns and user behavior trends. Use when asked about pageviews, sessions, web metrics, traffic sources, or user behavior on websites.</description>
  </skill>
  <skill>
    <name>building-segments</name>
    <description>Creates user segments and cohorts using filters and dimensions. Use when segmenting users, building cohorts, filtering populations, defining audiences, or when asked about user groups.</description>
  </skill>
  <skill>
    <name>configuring-watchers</name>
    <description>Configures monitoring agents (watchers) with intervals and targets. Use when setting up automated monitoring, scheduled analysis, alerts, or autonomous data observation.</description>
  </skill>
  <skill>
    <name>creating-insights</name>
    <description>Creates discoveries with insights that flow through the approval workflow. Use when generating findings, creating visualizations, surfacing patterns, or when the user asks to save or share analysis results.</description>
  </skill>
  <skill>
    <name>deciding-actions</name>
    <description>Decision matrices for choosing insight types, discovery actions, and avoiding duplicates. Use when deciding between funnel, retention, semantic, segmentation, or SQL insights, or when determining whether to create, update, or skip discoveries.</description>
  </skill>
  <skill>
    <name>evaluating-skills</name>
    <description>Evaluates and creates agent skills following best practices. Use when reviewing skill quality, writing new skills, refactoring existing skills, or when the user asks about skill structure, format, or specification.</description>
  </skill>
  <skill>
    <name>exploring-data</name>
    <description>Explores data connections and schemas to understand available tables, columns, and data types. Use when the user asks about data structure, available tables, what data exists, or wants to understand their data sources before querying.</description>
  </skill>
  <skill>
    <name>forecasting-timeseries</name>
    <description>Analyzes time series data for trends, anomalies, and forecasts. Use when detecting spikes or drops, predicting future values, identifying anomalies in metrics over time, or when the user asks about forecasting, projections, or unusual patterns in hourly/daily/weekly/monthly data.</description>
  </skill>
  <skill>
    <name>integrating-external</name>
    <description>Connects to external MCP servers and services for extended capabilities. Use when integrating with Amplitude, Omni, Slack, or other external tools, or when configuring notifications and external data sources.</description>
  </skill>
  <skill>
    <name>managing-discoveries</name>
    <description>Manages the discovery approval workflow and user feedback processing. Use when handling discovery reviews, understanding approval states, processing user feedback, or managing discovery lifecycle.</description>
  </skill>
  <skill>
    <name>modeling-semantics</name>
    <description>Creates and maintains semantic models with dimensions, measures, and relations. Use when defining business metrics, creating reusable data models, setting up the semantic layer, or when users ask about dimensions and measures.</description>
  </skill>
  <skill>
    <name>querying-lakehouse</name>
    <description>Writes and executes SQL queries against the DuckDB Lakehouse. Use when analyzing data, building reports, aggregating metrics, exploring tables, or when the user asks about data in connections.</description>
  </skill>
  <skill>
    <name>tracking-events</name>
    <description>Works with product analytics events and user identities. Use when analyzing user behavior, event tracking, understanding event schemas, identity resolution, or user trait management.</description>
  </skill>
  <skill>
    <name>understanding-platform</name>
    <description>Explains Altertable platform concepts and architecture. Use when user asks about organizations, environments, connections, versioning, or how the platform works.</description>
  </skill>
  <skill>
    <name>using-memory</name>
    <description>Stores and retrieves agent memories for learning and context persistence. Use when saving findings, recalling past analysis, building knowledge, or searching for relevant context.</description>
  </skill>
</available_skills>

## Scoring development

```bash
uv sync
uv run pre-commit install
uv run pytest scripts/tests/
uv run skills validate ./skill-name
```
