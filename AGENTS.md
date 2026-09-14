# AGENTS.md

Guidance for agents maintaining Altertable's portable Agent Skills and marketplace plugin metadata.

## Sources of Truth

- Use [Altertable's complete agent documentation](https://altertable.ai/docs/llms-full.txt) for current product concepts and public behavior.
- For MCP arguments and enums, prefer the live tool schema and `search_docs` over copied parameter lists.
- Treat explicit product corrections from the maintainers as authoritative when published documentation is lagging a release.
- Follow the [Agent Skills Specification](https://agentskills.io/specification) for package structure and frontmatter.

Do not preserve an obsolete product concept merely because an older skill or documentation page still mentions it.

## Repository Map

```text
skills/{skill-name}/SKILL.md       Shipped skill entry points
skills/{skill-name}/references/   Optional conditional detail
templates/SKILL_TEMPLATE/         Starting point for a new skill
.claude-plugin/                   Claude plugin metadata
.codex-plugin/plugin.json         Codex plugin metadata
.cursor-plugin/                   Cursor plugin metadata
scripts/sync-agents-md.py         Regenerates skill inventories
scripts/scorer/                   LLM quality scorer
scripts/tests/                    Repository and portfolio checks
```

## Portfolio Principles

- Assume the agent already understands analytics, SQL, APIs, and software engineering. Teach the non-obvious Altertable behavior that changes execution.
- Organize skills around durable platform workflows, not generic analytical techniques or a catalog of every tool.
- Keep `SKILL.md` concise; target fewer than 180 lines. Add a focused reference only when conditional detail warrants loading it separately.
- Distinguish read-only analysis, previews, and persistent writes. Authentication never implies permission for an unrequested mutation.
- Use imperative lowercase names with hyphens. Write third-person descriptions with discriminating trigger language.
- Treat [use-altertable](skills/use-altertable/SKILL.md) as the shared platform brief and [ask-altertable](skills/ask-altertable/SKILL.md) as the fast path for delegated analytical questions.
- Tasks produce Findings delivered through Notifications. Do not reintroduce retired feature terminology or workflows.

There is no mandatory body outline. Start from [the template](templates/SKILL_TEMPLATE/SKILL.md), then retain only the sections useful to that workflow.

## Updating the Repository

1. Read the affected skill, nearby tests, and current Altertable documentation.
2. Add or update a behavior-level portfolio test and observe it fail before changing shipped content.
3. Make the smallest coherent skill and metadata changes.
4. When skill names or descriptions change, run `uv run python scripts/sync-agents-md.py`. The Available Skills sections below and in `README.md` are generated from skill frontmatter; do not edit those inventories manually.
5. If the portfolio's advertised scope changes, keep `.claude-plugin`, `.codex-plugin/plugin.json`, and `.cursor-plugin` descriptions aligned.
6. Run the complete validation commands before committing.

The marketplace plugin provides skills and hosted MCP access; it does not install the Altertable CLI. The CLI is optional and installed separately for terminal, CI, ingestion, or structured-output workflows. Link to the [CLI guide](https://altertable.ai/docs/developer-tooling/cli) for setup and the [CLI repository](https://github.com/altertable-ai/altertable-cli) for releases and its command contract. Do not run an installer unless the user explicitly asks.

## Useful Commands

- `/altertable:ask-altertable <query>` delegates questions to the Altertable Agent.

```bash
uv sync
uv run python scripts/sync-agents-md.py
uv run pytest scripts/tests/
uv run skills validate ./skills/skill-name
uv run python scripts/score-skills.py skills --scan_all --validate_only
uv run pre-commit run --all-files
```

## Available Skills

<available_skills>
  <skill>
    <name>analyze-product-behavior</name>
    <description>Analyzes Altertable Product Analytics events, identities, web sessions, funnels, retention, segmentation, and saved segments. Use for product behavior, conversion, cohorts, event delivery, or identity-aware analysis.</description>
  </skill>
  <skill>
    <name>ask-altertable</name>
    <description>Delegates analytical questions and follow-up investigations to the Altertable Agent. Use as the default fast path for questions about connected data, metrics, changes, causes, or recommendations when exact SQL control is unnecessary.</description>
  </skill>
  <skill>
    <name>build-dashboards</name>
    <description>Creates and updates persistent Altertable Dashboards composed of Insights, text, sections, variables, and grid positions. Use only when the user requests an Altertable-hosted dashboard or changes to an existing Altertable Dashboard; do not use for generic or client-native dashboards, reports, or visualizations.</description>
  </skill>
  <skill>
    <name>build-insights</name>
    <description>Renders, creates, updates, and explains existing Altertable Insights. Use when the user wants a reusable SQL, semantic, funnel, retention, or segmentation analysis, or needs to understand a saved chart rather than run an unrelated one-off query.</description>
  </skill>
  <skill>
    <name>configure-tasks</name>
    <description>Creates and updates Altertable Tasks that run SQL, code, or AI work on a schedule. Use for recurring analysis, anomaly checks, forecasts, monitoring, or Findings delivered through Notifications.</description>
  </skill>
  <skill>
    <name>ingest-data</name>
    <description>Loads data into Altertable through the CLI, HTTP API, DataFrame tooling, object storage, or generated pipelines. Use for file upload, append, upsert, overwrite, bucket synchronization, or deciding between ingestion and an external catalog.</description>
  </skill>
  <skill>
    <name>instrument-product-analytics</name>
    <description>Adds or changes Altertable Product Analytics instrumentation in application code. Use for SDK setup, event tracking, user identification, traits, consent, session reset, page or screen tracking, and identity aliasing.</description>
  </skill>
  <skill>
    <name>manage-knowledge</name>
    <description>Searches and maintains Altertable memories, knowledge entries, repository context, and semantic-model descriptions. Use when reusable business context, definitions, preferences, or model documentation should guide future agent work.</description>
  </skill>
  <skill>
    <name>query-lakehouse</name>
    <description>Inspects Altertable catalogs and runs controlled DuckDB SQL across managed and external data. Use for exact queries, raw results, schema inspection, federated joins, query validation, plans, or optimization.</description>
  </skill>
  <skill>
    <name>query-with-chatgpt-data</name>
    <description>Use when ChatGPT Work&#x27;s @Data agent, the ChatGPT Data agent, or a Codex workflow coordinating with @Data needs Altertable as a governed read-only source. Do not use for ordinary Altertable analysis.</description>
  </skill>
  <skill>
    <name>use-altertable</name>
    <description>Provides Altertable&#x27;s foundational operating model, environment and catalog concepts, DuckDB conventions, and MCP-versus-CLI choices. Use for platform orientation, setup, tool selection, or any Altertable workflow needing shared context.</description>
  </skill>
</available_skills>
