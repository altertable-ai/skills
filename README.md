# Altertable Skills and Plugins

[![CI](https://github.com/altertable-ai/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/ci.yml)
[![Score Skills](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-19-green)](https://github.com/altertable-ai/skills)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg)](https://www.python.org)

This repository is the source of truth for [Altertable](https://altertable.ai) [Agent Skills](https://agentskills.io): portable, version-controlled packages of instructions, scripts, and references.

It is also the marketplace Claude Code, Codex, and Cursor install from. Those plugins ship the same skills plus the hosted MCP configuration. Other agents can install the skills alone with `npx skills add`.

## What are Agent Skills?

Agent Skills are an [open standard](https://agentskills.io/specification) for giving AI agents specialized capabilities. Each skill is a self-contained folder with a `SKILL.md` file containing instructions that agents load on demand. Build once, use across any compatible platform.

## Quick Start with `/altertable:ask`

Don't know which skill to use? Just type:

```
/altertable:ask <your question>
```

The `/altertable:ask` command routes your query to the best skill automatically. Examples:

- `/altertable:ask show me my web traffic` -> `analyze-web-traffic`
- `/altertable:ask what tables do I have?` -> `explore-data`
- `/altertable:ask analyze my signup funnel` -> `analyze-funnels`
- `/altertable:ask what is Altertable?` -> `understand-platform`

## Available Skills

| Skill | Description |
| ----- | ----------- |
| [analyze-funnels](skills/analyze-funnels/) | Builds conversion funnels over ordered steps |
| [analyze-insights](skills/analyze-insights/) | Explains what an existing insight or chart shows |
| [analyze-web-traffic](skills/analyze-web-traffic/) | Analyzes website traffic (pageviews, sessions, referrers, landing pages) |
| [ask](skills/ask/) | Routes user queries to the best-fit Altertable skill |
| [build-segments](skills/build-segments/) | Compares event metrics across cohorts using filters, breakdowns, and dimensions |
| [configure-tasks](skills/configure-tasks/) | Schedules recurring AI tasks over insights and dashboards |
| [create-discoveries](skills/create-discoveries/) | Reports a change, anomaly, root cause, recommendation, or warning to users |
| [create-insights](skills/create-insights/) | Drafts, renders, and saves insights of every type (SQL, semantic, segmentation, funnel, retention) |
| [decide-actions](skills/decide-actions/) | Decision matrices for picking insight types (funnel, retention, semantic, segmentation, SQL), task types, and discovery actions |
| [evaluate-skills](skills/evaluate-skills/) | Evaluates and authors agent skills against the Agent Skills spec |
| [explore-data](skills/explore-data/) | Inspects catalogs, schemas, tables, columns, semantic models, measures, and dimensions |
| [forecast-timeseries](skills/forecast-timeseries/) | Runs on-demand statistics over a time series to spot outliers and project values |
| [instrument-product-analytics](skills/instrument-product-analytics/) | Adds Altertable product analytics to an application (event tracking, user identification, traits, consent, session reset, aliasing) |
| [manage-discoveries](skills/manage-discoveries/) | Reviews, approves, and rejects existing discoveries |
| [query-lakehouse](skills/query-lakehouse/) | Writes, validates, optimizes, and runs DuckDB SQL against the Altertable lakehouse |
| [query-product-events](skills/query-product-events/) | Queries product events and identities with SQL (event counts, properties, user activity, traits) |
| [query-with-chatgpt-data](skills/query-with-chatgpt-data/) | Use when ChatGPT Work's @Data agent, the ChatGPT Data agent, or a Codex workflow coordinating with @Data needs to inspect or query Altertable |
| [understand-platform](skills/understand-platform/) | Explains Altertable concepts and architecture |
| [use-memory](skills/use-memory/) | Stores and recalls agent memories and org knowledge between sessions |

## Install the marketplace plugin

Claude Code, Codex, and Cursor load this repo as a marketplace. The plugin they install embeds the skills in this repository and the Altertable MCP server.

The repository, marketplace, and plugin have separate identifiers:

- Repository and marketplace source: `altertable-ai/skills`
- Marketplace identifier: `altertable-ai`
- Plugin identifier: `altertable`
- Qualified plugin ID (`plugin@marketplace`): `altertable@altertable-ai`

Codex:

```bash
codex plugin marketplace add altertable-ai/skills
codex plugin add altertable@altertable-ai
```

Claude Code:

```bash
claude plugin marketplace add altertable-ai/skills
claude plugin install altertable@altertable-ai
```

Cursor:

```bash
agent plugin marketplace add https://github.com/altertable-ai/skills
```

Then install **Altertable** from Customize → Plugins, or from `/plugin` in the Agent CLI.

Other compatible agents can install the portable skills without a native plugin:

```bash
npx skills add altertable-ai/skills
```

## Getting Started

```bash
git clone https://github.com/altertable-ai/skills.git
cd skills
uv sync
uv run pre-commit install
```

### Validate a skill

```bash
uv run skills validate ./skills/skill-name
```

### Score a skill

Every skill is scored by an LLM judge against the Agent Skills spec (threshold: 70/100):

```bash
uv run python scripts/score-skills.py ./skills/skill-name --verbose
```

### Run tests

```bash
uv run pytest scripts/tests/ -v
```

## Creating a New Skill

```bash
cp -r templates/SKILL_TEMPLATE skills/my-new-skill
```

Each skill follows the [Agent Skills Specification](https://agentskills.io/specification):

```
skills/
  skill-name/
    SKILL.md          # Required: metadata + instructions
    references/       # Optional: detailed documentation
    scripts/          # Optional: executable code
    assets/           # Optional: templates, resources
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## Compatibility

Skills follow the open [Agent Skills](https://agentskills.io) standard and work across 30+ compatible platforms:

**Claude Code** | **Cursor** | **VS Code** | **Gemini CLI** | **OpenAI Codex** | **GitHub Copilot** | **Goose** | **Roo Code** | **OpenHands** | **and more**

## Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Altertable](https://altertable.ai)
- [Anthropic Skills Examples](https://github.com/anthropics/skills)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
