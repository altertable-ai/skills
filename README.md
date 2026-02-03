# Skills

A collection of skills for AI agents.

## Installation

```bash
npx skills add altertable/skills
```

## General Skills

| Skill | Description |
|-------|-------------|
| `evaluating-skills` | Evaluate and review skill quality |

## Altertable Skills

| Skill | Description |
|-------|-------------|
| `exploring-data` | Explore data connections and schemas |
| `querying-lakehouse` | Write and execute DuckDB SQL queries |
| `modeling-semantics` | Create semantic models with dimensions and measures |
| `creating-insights` | Create discoveries with insights |
| `deciding-actions` | Decision matrices for insight types and duplicate prevention |
| `analyzing-charts` | Interpret chart data for patterns and anomalies |
| `analyzing-web-traffic` | Analyze web analytics and traffic trends |
| `building-segments` | Create user segments and cohorts |
| `analyzing-funnels` | Analyze conversion funnels |
| `configuring-watchers` | Set up monitoring agents |
| `managing-discoveries` | Handle discovery approval workflow |
| `using-memory` | Store and retrieve agent memories |
| `understanding-platform` | Understand Altertable platform concepts |
| `tracking-events` | Work with product analytics events |
| `integrating-external` | Connect to external MCP servers |

## Skill Format

```yaml
---
name: skill-name
description: Third-person description with trigger keywords. Use when...
---

# Skill Title

## Quick Start
...
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Sources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
