# Altertable Skills and Plugins

[![CI](https://github.com/altertable-ai/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/ci.yml)
[![Score Skills](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-green)](https://github.com/altertable-ai/skills)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg)](https://www.python.org)

This repository is the source of truth for [Altertable](https://altertable.ai) [Agent Skills](https://agentskills.io): portable, version-controlled packages of instructions, scripts, and references.

It is also the marketplace Claude Code, Codex, and Cursor install from. Those plugins ship the same skills plus the hosted MCP configuration. Other agents can install the skills alone with `npx skills add`.

## What are Agent Skills?

Agent Skills are an [open standard](https://agentskills.io/specification) for giving AI agents specialized capabilities. Each skill is a self-contained folder with a `SKILL.md` file containing instructions that agents load on demand. Build once, use across any compatible platform.

## Available Skills

| Skill | Description |
| ----- | ----------- |
| [analyze-product-behavior](skills/analyze-product-behavior/) | Analyzes Altertable Product Analytics events, identities, web sessions, funnels, retention, segmentation, and saved segments |
| [ask](skills/ask/) | Delegates analytical questions and follow-up investigations to the Altertable Agent |
| [build-dashboards](skills/build-dashboards/) | Drafts, creates, and updates Altertable Dashboards composed of Insights, text, sections, variables, and grid positions |
| [build-insights](skills/build-insights/) | Renders, drafts, creates, updates, and explains existing Altertable Insights |
| [configure-tasks](skills/configure-tasks/) | Drafts, creates, and updates Altertable Tasks that run SQL, code, or AI work on a schedule |
| [ingest-data](skills/ingest-data/) | Loads data into Altertable through the CLI, HTTP API, DataFrame tooling, object storage, or generated pipelines |
| [instrument-product-analytics](skills/instrument-product-analytics/) | Adds or changes Altertable Product Analytics instrumentation in application code |
| [manage-knowledge](skills/manage-knowledge/) | Searches and maintains Altertable memories, knowledge entries, repository context, and semantic-model descriptions |
| [query-lakehouse](skills/query-lakehouse/) | Inspects Altertable catalogs and runs controlled DuckDB SQL across managed and external data |
| [query-with-chatgpt-data](skills/query-with-chatgpt-data/) | Use when ChatGPT Work's @Data agent, the ChatGPT Data agent, or a Codex workflow coordinating with @Data needs Altertable as a governed read-only source |
| [use-altertable](skills/use-altertable/) | Provides Altertable's foundational operating model, environment and catalog concepts, DuckDB conventions, and MCP-versus-CLI choices |

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

## Optional Altertable CLI

The marketplace plugin provides the skills and hosted MCP connection; it does not install the CLI. Install the CLI separately when you need terminal queries, ingestion, CI, or script-friendly output:

```bash
curl -fsSL https://install.altertable.ai | sh
```

See the [CLI guide](https://altertable.ai/docs/developer-tooling/cli) for setup and authentication, or the [CLI repository](https://github.com/altertable-ai/altertable-cli) for releases and the complete command reference.

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
