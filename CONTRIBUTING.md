# Contributing to Skills

Guidelines for creating and modifying skills following the [Agent Skills Specification](https://agentskills.io).

## Creating a New Skill

### 1. Directory Structure

```bash
cp -r skills/SKILL_TEMPLATE skills/my-new-skill
```

### 2. Naming Convention

Use **gerund form** (verb + -ing), lowercase, hyphens only:

- `analyzing-data` ✓
- `analyze-data` ✗

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
