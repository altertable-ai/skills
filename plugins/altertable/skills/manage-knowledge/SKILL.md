---
name: manage-knowledge
compatibility: Requires Altertable MCP server; knowledge writes require read-write access
description: "Searches and maintains Altertable memories, knowledge entries, and repository context, and interviews users to capture business context. Use when reusable business context, definitions, or preferences should guide future agent work, when the user wants to write down business context or teach the agent about their data, or when the user asks to document or describe a table or its columns."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Manage Knowledge

Altertable has distinct context layers. Put information in the layer whose ownership and lifecycle match it.

| Context              | Use                                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| Semantic model       | Governed measures, dimensions and relations attached to data                                                  |
| Knowledge entry      | Durable knowledge material intentionally maintained by the organization                                       |
| Knowledge repository | Extracted knowledge material synchronized from a source git repository (incl. dbt, code, documentation, etc.) |
| Memory               | High-signal context learned from work that will save effort in later runs                                     |

## Recall Context

Use `search_memory` when prior preferences, metric caveats, entity history, or successful techniques are likely to matter. Each returned memory has its access count incremented, so do not search reflexively when past context cannot affect the task.

Memories are scoped by environment. Their usefulness is driven by importance, recency, and retrieval frequency; related memories may consolidate and stale memories may fade. Treat that as relevance behavior, not as a promise of a particular decay schedule.

## Create Memories

Use `create_memory` for a high-signal fact, decision, Finding, preference, caveat, or reusable technique that is likely to matter later. Skip routine outcomes and details easily recovered from the schema or data.

Attach the source and related entities when available so the memory can be retrieved in context. Follow the live schema for optional importance or scope fields; do not manufacture a scoring or decay policy in the skill.

## Maintain Knowledge Entries

`create_knowledge` and `update_knowledge` require explicit human intent. The title and content must be text the human supplied, text fetched verbatim from a source they explicitly identified, or a draft they approved unchanged (below).

Otherwise never summarize, synthesize, translate, reformat, or infer organization-wide knowledge for these tools. If scope, title, source, or exact content is unclear, ask before writing. Prefer a repository sync when the maintained source already lives in version control.

## Capture Business Context

Use this only when the user asks to write down or update business context or to teach the agent about their data, or accepts your offer to do so. Never start it unprompted.

1. Ground first. Call `get_catalog`, and `profile_columns` only for columns you are about to ask about. Every question names real tables or columns and the specific ambiguity found: two similar amount columns, several timestamps, test data.
2. Ask whenever you are unsure. Never guess. Use `ask_question` only when the catalog evidence gives real options to choose from. Otherwise ask plainly. Cover these topics, skipping any the catalog, semantic layer, or existing knowledge already answers:
   1. What the business does, and who uses these answers to decide what.
   2. The rules behind the key metrics: what counts as a sale or an active customer, and what each excludes.
   3. Known traps, as rules: test or internal accounts, duplicated sources, periods where the data is unreliable.
   4. Defaults: currency, timezone, fiscal calendar, and the date range when none is given.
   5. Internal terms and acronyms that never appear in the schema.
3. If the user does not know an answer, leave it out.
4. Do not ask which tables to prefer or avoid. Point the user to marking tables Verified or Excluded in the Catalog.

Then show the full draft, holding only what the user stated or confirmed, and use `ask_question` to ask whether to save it as environment knowledge. On approval, call `create_knowledge` with exactly that document, or `update_knowledge` with the full revised entry built from its current content, and share the returned `url` so they can review or edit it. If they ask for changes, revise it and ask again. A user who cannot add knowledge can pass the document to someone who can.

## Document a Table

Use this when the user asks to document or describe a table or its columns.

1. Read the table's current definition from the attached table or `get_catalog`. A table or column without a description is missing one. Never overwrite an existing description.
2. Gather evidence only for the columns you will describe: `profile_columns`, and `query_lakehouse` sparingly.
3. Ask the user when the meaning is unclear. Leave a column out rather than guess.
4. Write what the table or column means: grain (one row per ...), units, caveats, and the allowed values of a categorical column. Never row-level values (ids, amounts, names, free text) or personal data.
5. Propose, never write directly. When the `draft_table_descriptions` tool is available, call it with only the missing descriptions so the user reviews and applies them. Otherwise present them as a list the user can apply.
6. When the table's descriptions are managed in a dbt or LookML repository (the draft tool rejects it, or the user says so), write the YAML for the user to commit instead. Open a pull request only if a pull-request tool is available.

## Boundaries

- Do not store secrets or sensitive row values in any context layer.
- Do not duplicate a semantic definition as a memory.
- Do not record which tables to prefer or avoid as a memory or knowledge entry. Endorsement status on the table or catalog carries that into discovery for every agent.
- Do not turn one unverified query result into durable organizational context.
- Do not overwrite maintained knowledge to resolve a temporary contradiction; surface the conflict.
