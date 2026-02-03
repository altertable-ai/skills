# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, Copilot, etc.) when working with code in this repository.

## Repository Overview

A collection of skills for AI agents. Skills are packaged instructions that extend agent capabilities.

## Structure

```
{skill-name}/             # Gerund form (verb-ing), kebab-case
  SKILL.md                # Required: skill definition (<500 lines)
  references/             # Optional: supporting documentation
    {topic}.md            # One level deep only
```

## Creating a New Skill

### Naming Convention

Use **gerund form** (verb + -ing), lowercase, hyphens only:
- `analyzing-data` ✓
- `analyze-data` ✗
- `data-analyzer` ✗

### SKILL.md Format

```markdown
---
name: {skill-name}
description: {Third-person description with trigger keywords. Use when...}
---

# {Skill Title}

## Quick Start
{Immediate, actionable example}

## When to Use This Skill
{Bullet points with trigger conditions}

## {Core Content}
{Concepts, workflows, examples}

## Common Pitfalls
{5-10 mistakes to avoid}

## References
{Links to references/ files}
```

### Best Practices

- **Keep SKILL.md under 500 lines** — move details to references/
- **Write specific descriptions** — helps agents know when to activate
- **Use progressive disclosure** — reference files load only when needed
- **References one level deep** — no nested folders in references/
- **Third-person descriptions** — "Analyzes..." not "I help you..."
- **Include trigger keywords** — helps agent routing

## Installation

```bash
npx skills add altertable/skills
```
