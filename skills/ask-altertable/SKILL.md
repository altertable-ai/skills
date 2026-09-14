---
name: ask-altertable
compatibility: Requires Altertable MCP server
description: "Delegates analytical questions and follow-up investigations to the Altertable Agent. Use as the default fast path for questions about connected data, metrics, changes, causes, or recommendations when exact SQL control is unnecessary."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Ask the Altertable Agent

Use the Altertable Agent as the default fast path for analytical questions. It can inspect the governed environment, use semantic models and knowledge, run queries, and return a completed answer without the calling agent coordinating each operation itself.

## Workflow

1. Call `ask` with the user's original question and all constraints that affect the answer.
2. Return the answer, assumptions, and relevant evidence without repeating the investigation through direct tools.
3. For a follow-up, pass the returned `chat_id` so the Altertable Agent continues the same investigation. Omit it only for a genuinely separate question.

Do not inspect catalogs or pre-write SQL before `ask` merely to help it. Delegation is valuable because the Altertable Agent performs that work internally.

## Use Direct Tools Instead When

- The user requests exact SQL, raw rows, a query plan, or reproducible query evidence.
- The task requires a precisely controlled create or update operation.
- The caller must return Altertable data to another analysis system rather than an interpreted answer.
- The request concerns ingestion, application instrumentation, or another operation outside analytical Q&A.

When a request combines analysis with persistence, use `ask` for the analysis and perform the write only when the user explicitly requested it and the connection has read-write access.

## Guardrails

- Preserve the user's timeframe, timezone, metric definition, and requested scope in the delegated prompt.
- Do not start a new chat for every follow-up; continuity is the purpose of `chat_id`.
- Do not present the Altertable Agent's assumptions as established facts.
- If `ask` reports missing context or ambiguous data, surface that limitation or continue the same chat with the necessary clarification.
- Use `search_docs` when the question is about Altertable itself rather than the user's data.
