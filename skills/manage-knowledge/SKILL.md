---
name: manage-knowledge
compatibility: Requires Altertable MCP server; knowledge and semantic-model writes require read-write access
description: "Searches and maintains Altertable memories, knowledge entries, repository context, and semantic-model descriptions. Use when reusable business context, definitions, preferences, or model documentation should guide future agent work."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Manage Knowledge

Altertable has distinct context layers. Put information in the layer whose ownership and lifecycle match it.

| Context | Use |
| --- | --- |
| Semantic model | Governed measures, dimensions, timestamps, filters, and relations attached to data |
| Knowledge entry | Durable source material intentionally maintained by the organization |
| Knowledge repository | Files and dbt metadata synchronized from a source repository |
| Memory | High-signal context learned from work that will save effort in later runs |

## Recall Context

Call `initialize` first and apply the returned knowledge context. Use `search_memory` when prior preferences, metric caveats, entity history, or successful techniques are likely to matter. Each returned memory has its access count incremented, so do not search reflexively when past context cannot affect the task.

Use `list_knowledge_repositories` and `search_entities` when maintained documentation or repository material may contain the source of truth. Read the selected entity resource rather than relying on a search snippet.

## Create Memories

Use `create_memory` for a high-signal fact, decision, Finding, preference, caveat, or reusable technique that is likely to matter later. Skip routine outcomes and details easily recovered from the schema or data.

Set `source_slug` and related entities when available so the memory can be retrieved in context. Follow the live schema for optional importance or scope fields; do not manufacture a scoring or decay policy in the skill.

## Maintain Knowledge Entries

`create_knowledge` and `update_knowledge` require explicit human intent. The title and content must be text the human supplied or text fetched verbatim from a source they explicitly identified.

Never summarize, synthesize, translate, reformat, or infer organization-wide knowledge for these tools. If scope, title, source, or exact content is unclear, ask before writing. Prefer a repository sync when the maintained source already lives in version control.

## Document Semantic Models

Use `document_semantic_model` for a table-level natural-language description and `document_semantic_model_dimension` for a specific dimension. Retrieve the catalog first and pass the exact catalog, schema, table, and projection names.

Descriptions should state business meaning, grain, ownership, and known caveats. Do not encode a governed calculation only in prose when it belongs in a measure, dimension, filter, or relation definition.

## Boundaries

- Do not store secrets or sensitive row values in any context layer.
- Do not duplicate a semantic definition as a memory.
- Do not turn one unverified query result into durable organizational context.
- Do not overwrite maintained knowledge to resolve a temporary contradiction; surface the conflict.
