# AGENTS.md

Guidance for AI coding agents working with this repository.

## Repository Overview

A collection of skills for AI agents following the [Agent Skills Specification](https://agentskills.io/specification).

## Structure

```
{skill-name}/
  SKILL.md
  references/
    {topic}.md

scripts/
  score-skills.py
  scorer/
  tests/
```

## Creating a New Skill

### Naming Convention

Use **gerund form** (verb + -ing), lowercase, hyphens only:
- `analyzing-data` ✓
- `analyze-data` ✗

### SKILL.md Format

```markdown
---
name: {skill-name}
description: {Third-person description with trigger keywords}
---

# {Skill Title}

## Quick Start
{Immediate actionable example}

## When to Use This Skill
{Bullet points with trigger conditions}

## Common Pitfalls
{5-10 mistakes to avoid}

## References
{Links to references/ files}
```

### Best Practices

- Keep SKILL.md under 500 lines
- Move details to references/
- Third-person descriptions ("Analyzes..." not "I help you...")
- Include trigger keywords
- References one level deep only

## Scoring development

```bash
uv sync
uv run pre-commit install
uv run pytest scripts/tests/
uv run skills validate ./skill-name
```
