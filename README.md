# Altertable Skills and Plugins

[![CI](https://github.com/altertable-ai/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/ci.yml)
[![Score Skills](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/score-skills.yml)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-8A2BE2)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-3776AB.svg)](https://www.python.org)

[Agent Skills](https://agentskills.io) for working with [Altertable](https://altertable.ai): explore catalogs, run DuckDB SQL, analyze product behavior, and build insights, dashboards, data apps, and tasks.

Skills are guidance, not access. Live work goes through the hosted Altertable MCP server, which needs an Altertable account. The Claude Code, Codex, and Cursor plugins register it; `npx skills add` does not.

## Install

Fastest: paste this into an agent with terminal access.

```text
Fetch https://altertable.ai/docs/agent-setup/prompt.md and follow the instructions.
```

Or by hand:

| Agent | Install |
| ----- | ------- |
| [Claude Code](https://altertable.ai/docs/agent-setup/claude-code) | `claude plugin marketplace add altertable-ai/skills`<br>`claude plugin install altertable@altertable-ai` |
| [Codex](https://altertable.ai/docs/agent-setup/codex) | `codex plugin marketplace add altertable-ai/skills`<br>`codex plugin add altertable@altertable-ai` |
| [Cursor](https://altertable.ai/docs/agent-setup/cursor) | `agent plugin marketplace add https://github.com/altertable-ai/skills`<br>then install **Altertable** from Customize → Plugins |
| [Claude](https://altertable.ai/docs/agent-setup/claude), [ChatGPT](https://altertable.ai/docs/agent-setup/chatgpt) | See the guide |
| [Other agents](https://altertable.ai/docs/agent-setup/other-agents) | `npx skills add altertable-ai/skills`<br>then add the MCP server `https://mcp.altertable.ai/mcp` |

Each guide covers updates and troubleshooting.

## Verify

Start a new session and ask:

```text
Use Altertable to list my available catalogs.
```

The first tool call opens a browser sign-in: pick the organization, the environment, and an access level (Read-only by default). Read-only explores and queries. Analyst also saves insights, dashboards, data apps, and knowledge. Full access also creates tasks and writes to the lakehouse.

## Use the skills

Ask in plain language:

- "Analyze the signup funnel from landing page to account creation."
- "Analyze web traffic for the last 30 days and call out meaningful changes."

`ask-altertable` delegates the question to the Altertable Agent; `query-altertable` runs DuckDB SQL you control. In Claude Code, call a skill with `/altertable:<skill>`.

## Available Skills

| Skill | Description |
| ----- | ----------- |
| [analyze-product-behavior](skills/analyze-product-behavior/) | Analyzes Altertable Product Analytics events, identities, web sessions, funnels, retention, segmentation, and saved segments |
| [ask-altertable](skills/ask-altertable/) | Delegates analytical questions and follow-up investigations to the Altertable Agent |
| [build-dashboards](skills/build-dashboards/) | Creates and updates persistent Altertable Dashboards composed of Insights, text, sections, variables, and grid positions |
| [build-data-app](skills/build-data-app/) | Creates, updates, and deletes Altertable-hosted data apps through MCP (beta) |
| [build-insights](skills/build-insights/) | Renders, creates, updates, and explains Altertable Insights |
| [build-local-data-app](skills/build-local-data-app/) | Builds and runs Altertable data apps locally with the CLI (beta) |
| [configure-tasks](skills/configure-tasks/) | Creates and updates Altertable Tasks that run SQL, code, or AI work on a schedule |
| [ingest-data](skills/ingest-data/) | Loads data into Altertable through the CLI, HTTP API, DataFrame tooling, object storage, or generated pipelines |
| [instrument-product-analytics](skills/instrument-product-analytics/) | Adds or changes Altertable Product Analytics instrumentation in application code |
| [investigate-opentelemetry](skills/investigate-opentelemetry/) | Investigates OpenTelemetry logs and traces in Altertable using SQL |
| [manage-knowledge](skills/manage-knowledge/) | Searches and maintains Altertable memories, knowledge entries, repository context, and semantic-model descriptions |
| [query-altertable](skills/query-altertable/) | Inspects Altertable catalogs and runs controlled DuckDB SQL across managed and external data |
| [query-with-chatgpt-data](skills/query-with-chatgpt-data/) | Use when ChatGPT Work's @Data agent, the ChatGPT Data agent, or a Codex workflow coordinating with @Data needs Altertable as a governed read-only source |
| [use-altertable](skills/use-altertable/) | Provides Altertable's foundational operating model, environment and catalog concepts, DuckDB conventions, and MCP-versus-CLI choices |

## Optional CLI

For terminal queries, ingestion, and CI, install the [Altertable CLI](https://altertable.ai/docs/developer-tooling/cli) separately.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). CI validates every skill and scores changed ones with an LLM judge (minimum 70/100).

## License

[MIT](LICENSE)
