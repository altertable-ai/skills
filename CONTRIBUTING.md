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

| Constraint | Limit |
|------------|-------|
| SKILL.md body | <500 lines |
| Reference depth | 1 level only |

#### Recommended Sections

1. **Quick Start** - Immediate, actionable example
2. **When to Use This Skill** - Trigger conditions
3. **Common Pitfalls** - 5-10 mistakes to avoid
4. **References** - Links to `references/` files

### 5. Reference Files

Place detailed content in `references/`:

```markdown
## References
- [Topic details](references/topic.md)
```

Keep references **one level deep** (no nested directories).

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

1. Tag the tip of `main` as `vMAJOR.MINOR.PATCH` and push the tag. No manual version bump is needed.
2. Wait for the `Release version` workflow to pass. It updates every manifest version from the tag, syncs `AGENTS.md`, validates every packaged skill, the repository tests, and strict Claude plugin schemas, then commits the release to `main` and moves the tag onto that commit.
3. Run `git fetch --tags --force` locally to pick up the moved tag.
4. Publish the GitHub release from the validated tag.

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
