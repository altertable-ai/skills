# Contributing to Skills

Guidelines for creating and modifying skills following the [Agent Skills Specification](https://agentskills.io).

## Creating a New Skill

### 1. Directory Structure

```bash
cp -r templates/SKILL_TEMPLATE skills/my-new-skill
```

### 2. Naming Convention

Use an imperative verb, lowercase, and hyphens only:

- `analyze-data` ✓
- `analyzing-data` ✗

### 3. SKILL.md Requirements

#### Frontmatter (Required)

```yaml
---
name: skill-name
description: Third-person description with trigger keywords
---
```

#### Description Guidelines

- Write in **third person**: "Analyzes data..." not "I can help you..."
- Include **trigger keywords** that help agents identify when to use the skill

### 4. Body Content

Assume a capable agent already understands general analytics, SQL, APIs, and software engineering. A skill earns its context budget by explaining the non-obvious Altertable details that change execution: object boundaries, required call order, permissions, defaults, side effects, and product-specific choices.

- Start with the outcome and the smallest platform-specific workflow.
- Prefer the live tool schema or `search_docs` for evolving arguments and behavior.
- Distinguish read-only operations, previews or drafts, and persistent writes.
- Keep the entry point concise; target fewer than 180 lines.
- Add sections only when they help the workflow. There is no mandatory body outline.
- Avoid generic tutorials, exhaustive parameter copies, and taxonomies a capable model can infer.

### 5. Reference Files

Place detailed content in `references/`:

```markdown
## References
- [Topic details](references/topic.md)
```

References are optional. Use them only for focused, conditional detail, state when the agent should read them, and keep them **one level deep** (no nested directories).

## Setup

```bash
git clone https://github.com/altertable-ai/skills.git
cd skills
uv sync
uv run pre-commit install
```

## Testing

```bash
uv run skills validate ./skills/skill-name
uv run pytest scripts/tests/ -v
```

## Scoring

Score a skill with the LLM judge (threshold: 70/100):

```bash
uv run python scripts/score-skills.py ./skills/skill-name --verbose
```

## Releasing

Release Please derives the next version from Conventional Commit PR titles and keeps a release PR current as changes land on `main`.

1. Review the generated release PR and wait for its checks to pass.
2. Merge the release PR when the release is ready.
3. Release Please updates every manifest version, creates the `vMAJOR.MINOR.PATCH` tag, and publishes the GitHub release.

Use `fix:` for patch releases, `feat:` for minor releases, and `!` for major releases. Squash PRs so their Conventional Commit titles become the commits on `main`.

## Style Guide

### Code Examples

Use fenced code blocks with language hints:

````markdown
```sql
SELECT * FROM events
```
````

### Formatting

- Use headers to organize content
- Keep paragraphs short
- Use bullet points for lists
- Use tables for structured data
