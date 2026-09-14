---
name: <lowercase-hyphenated-name>
description: "<what specialized capability this provides and when it should activate>"
# Add compatibility only when the workflow has concrete environment requirements.
# compatibility: Requires Altertable MCP server
metadata:
  author: Altertable
# Add metadata.requires only when the skill depends on a packaged runtime.
#   requires: "altertable-mcp"
---

# Your Skill Title

State the outcome and the non-obvious Altertable context that changes how an agent should perform this workflow. Do not explain generic analytics, SQL, charts, HTTP, or other concepts a capable model already knows.

## Workflow

Do not repeat shared MCP bootstrap from `use-altertable`. Start with the first decision or action specific to this workflow.

1. Start with the smallest platform-specific action that advances this workflow.
2. Use the live tool schema or `search_docs` for evolving arguments and product behavior.
3. Validate the observable result before reporting completion.

Keep fixed sequences only where order affects correctness, permissions, or side effects.

## Altertable Rules

- Record platform invariants, object boundaries, defaults, and gotchas that are easy to infer incorrectly.
- Distinguish read-only analysis, drafts, and persistent writes.
- Require explicit user intent before creating or updating persistent resources.
- Prefer live schemas and documentation over copied parameter catalogs.

## Boundaries

Explain the nearest workflows this skill does not own so its description and instructions do not attract unrelated requests.

## References

Add a focused reference only when it is needed conditionally. State exactly when the agent should read it; otherwise omit this section and the `references/` directory.
