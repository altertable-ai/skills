# Altertable Skills

[![CI](https://github.com/altertable-ai/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/ci.yml)
[![Score Skills](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-16-green)](https://github.com/altertable-ai/skills)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg)](https://www.python.org)

A collection of [Agent Skills](https://agentskills.io) for [Altertable](https://altertable.ai) AI agents. Skills are portable, version-controlled packages of instructions, scripts, and references that give agents new capabilities.

## What are Agent Skills?

Agent Skills are an [open standard](https://agentskills.io/specification) for giving AI agents specialized capabilities. Each skill is a self-contained folder with a `SKILL.md` file containing instructions that agents load on demand. Build once, use across any compatible platform.

## Available Skills

| Skill | Description |
|-------|-------------|
| [analyzing-insights](analyzing-insights/) | Interprets chart data to identify patterns, anomalies, and trends |
| [analyzing-funnels](analyzing-funnels/) | Creates and analyzes conversion funnels to understand user journeys |
| [analyzing-web-traffic](analyzing-web-traffic/) | Analyzes web analytics data to identify traffic patterns |
| [building-segments](building-segments/) | Creates user segments and cohorts using filters and dimensions |
| [configuring-watchers](configuring-watchers/) | Configures monitoring agents with intervals and targets |
| [creating-insights](creating-insights/) | Creates discoveries with insights through the approval workflow |
| [deciding-actions](deciding-actions/) | Decision matrices for choosing insight types and discovery actions |
| [evaluating-skills](evaluating-skills/) | Evaluates and creates agent skills following best practices |
| [exploring-data](exploring-data/) | Explores data connections and schemas |
| [forecasting-timeseries](forecasting-timeseries/) | Analyzes time series data for trends, anomalies, and forecasts |
| [managing-discoveries](managing-discoveries/) | Manages the discovery approval workflow and user feedback |
| [modeling-semantics](modeling-semantics/) | Creates and maintains semantic models with dimensions and measures |
| [querying-lakehouse](querying-lakehouse/) | Writes and executes SQL queries against the DuckDB Lakehouse |
| [tracking-events](tracking-events/) | Works with product analytics events and user identification |
| [understanding-platform](understanding-platform/) | Explains platform concepts and architecture |
| [using-memory](using-memory/) | Stores and retrieves agent memories for learning and context |

## Getting Started

```bash
git clone https://github.com/altertable-ai/skills.git
cd skills
uv sync
uv run pre-commit install
```

### Validate a skill

```bash
uv run skills validate ./skill-name
```

### Score a skill

Every skill is scored by an LLM judge against the Agent Skills spec (threshold: 70/100):

```bash
uv run python scripts/score-skills.py ./skill-name --verbose
```

### Run tests

```bash
uv run pytest scripts/tests/ -v
```

## Creating a New Skill

```bash
cp -r SKILL_TEMPLATE my-new-skill
```

Each skill follows the [Agent Skills Specification](https://agentskills.io/specification):

```
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
