# Contributing to Skills

Guidelines for creating and modifying skills following the [Anthropic Agent Skills](https://agentskills.io) standard.

## Creating a New Skill

### 1. Directory Structure

```bash
mkdir -p skill-name/references
```

### 2. Naming Convention

Use **gerund form** (verb + -ing), lowercase, hyphens only:

- `analyzing-data` (correct)
- `analyze-data` (incorrect)
- `AnalyzeData` (incorrect)

### 3. SKILL.md Requirements

#### Frontmatter (Required)

```yaml
---
name: skill-name          # Must match directory name, max 64 chars
description: ...          # Max 1024 chars, third person, include trigger keywords
---
```

#### Description Guidelines

- Write in **third person**: "Analyzes data..." not "I can help you..."
- Include **trigger keywords** that help agents identify when to use the skill
- Describe both **what** the skill does and **when** to use it

**Good example:**
```yaml
description: Writes and executes SQL queries against the DuckDB Lakehouse. Use when analyzing data, building reports, aggregating metrics, or when the user asks about data in connections.
```

**Bad example:**
```yaml
description: Helps with queries.
```

### 4. Body Content Guidelines

| Constraint | Limit |
|------------|-------|
| SKILL.md body | <500 lines |
| Total skill tokens | <5000 tokens |
| Reference depth | 1 level only |

#### Recommended Sections

1. **Quick Start** - Immediate, actionable example
2. **When to Use This Skill** - Trigger conditions
3. **Procedure** - Step-by-step instructions
4. **Examples** - Concrete examples with code
5. **Common Pitfalls** - Mistakes to avoid
6. **Reference Files** - Links to detailed references

### 5. Reference Files

Place detailed content in `references/` to enable progressive disclosure:

```markdown
## Reference Files
- [DuckDB functions](references/duckdb-functions.md)
- [Query patterns](references/query-patterns.md)
```

**Rules:**
- Keep references **one level deep** (no nested references)
- Use descriptive filenames: `filter-operators.md` not `doc1.md`
- Add table of contents for files >100 lines

## Checklist Before Submitting

- [ ] Name uses gerund form (`analyzing-*`, `creating-*`)
- [ ] Description is in third person
- [ ] Description includes trigger keywords
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details are in separate reference files
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep

## Testing Skills

1. Check SKILL.md exists and has required frontmatter
2. Ask an agent a question that should trigger the skill
3. Verify it activates and behaves correctly

## Style Guide

### Code Examples

Use fenced code blocks with language hints:

````markdown
```sql
SELECT * FROM events WHERE timestamp > current_date - INTERVAL 7 DAY
```
````

### Terminology

Use consistent terms throughout:

| Preferred | Avoid |
|-----------|-------|
| "connection" | "data source", "database" |
| "semantic source" | "model", "semantic model" |
| "dimension" | "attribute", "field" |
| "measure" | "metric", "aggregate" |
| "discovery" | "finding", "insight" (when referring to the entity) |
| "watcher" | "agent", "monitor" |

### Formatting

- Use headers to organize content
- Keep paragraphs short (3-5 lines)
- Use bullet points for lists
- Use tables for structured data
- Use bold for emphasis, not ALL CAPS
