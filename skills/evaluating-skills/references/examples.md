# Skill Patterns & Examples

Patterns extracted from well-designed skills in this repository.

## Frontmatter Examples

### Good Descriptions

**Exploratory Skill:**
```yaml
description: "Explores available data connections and their structure. Use when
discovering what data exists, understanding table schemas, or finding available
fields for analysis."
```

**Procedural Skill:**
```yaml
description: "Writes and executes SQL queries against the DuckDB Lakehouse. Use
when analyzing data, building reports, aggregating metrics, or exploring tables."
```

**Analytical Skill:**
```yaml
description: "Analyzes chart visualizations to extract meaningful insights. Use
when interpreting dashboards, identifying trends, spotting anomalies, or
explaining patterns to stakeholders."
```

**Decision Skill:**
```yaml
description: "Determines the appropriate action based on user intent and context.
Use when routing requests, selecting tools, or choosing between multiple
valid approaches."
```

### Bad Descriptions (Don't Do This)

```yaml
# First person
description: "I help you analyze data and create reports."

# Too vague
description: "Works with data."

# No trigger keywords
description: "A skill for working with things."

# Self-referential
description: "This skill is used for analyzing charts."
```

## Quick Start Patterns

### Numbered Steps (Procedural)
```markdown
## Quick Start

1. Identify the data source connection
2. Write your SQL query using DuckDB syntax
3. Execute and review results
```

### Decision Tree (Framework)
```markdown
## Quick Start

User request → Check keywords → Match to skill → Execute

- Data question? → exploring-data
- Need query? → querying-lakehouse
- Chart output? → analyzing-insights
```

### Code Example (Technical)
```markdown
## Quick Start

```sql
SELECT customer_name, SUM(revenue)
FROM sales
WHERE date >= '2024-01-01'
GROUP BY customer_name
ORDER BY SUM(revenue) DESC
LIMIT 10;
```
```

## When to Use Section Patterns

### Bullet List with Keywords
```markdown
## When to Use This Skill

- User asks "what data do I have?"
- User wants to understand table structure
- User needs to find available fields
- Keywords: "schema", "tables", "columns", "connections", "data source"
```

### Scenario-Based
```markdown
## When to Use This Skill

- **Data exploration**: Finding available tables and fields
- **Schema questions**: Understanding column types and relationships
- **Connection discovery**: Listing available data sources
- **Field lookup**: Finding specific columns across tables
```

## Workflow Diagrams

### Simple Flow
```
Request → Parse → Execute → Return
```

### Branching Flow
```
Request
    ├── Type A → Process A → Result
    ├── Type B → Process B → Result
    └── Unknown → Clarify → Restart
```

### State Machine
```
┌─────────┐    ┌──────────┐    ┌──────────┐
│ Pending │───→│ Running  │───→│ Complete │
└─────────┘    └──────────┘    └──────────┘
     │              │
     └──────────────┴───→ [Failed]
```

## Table Patterns

### Comparison Table
```markdown
| Approach | Pros | Cons | Use When |
|----------|------|------|----------|
| Option A | Fast, simple | Limited | Quick tasks |
| Option B | Flexible | Complex | Advanced needs |
| Option C | Comprehensive | Slow | Full analysis |
```

### Reference Table
```markdown
| Function | Syntax | Example |
|----------|--------|---------|
| `SUM` | `SUM(column)` | `SUM(revenue)` |
| `AVG` | `AVG(column)` | `AVG(price)` |
| `COUNT` | `COUNT(*)` | `COUNT(DISTINCT id)` |
```

### Decision Matrix
```markdown
| Signal | Weight | Skill Match |
|--------|--------|-------------|
| "chart" in query | High | analyzing-insights |
| "SQL" in query | High | querying-lakehouse |
| "what data" | Medium | exploring-data |
```

## Common Pitfalls Patterns

### Numbered List with Explanations
```markdown
## Common Pitfalls

1. **Using SELECT * in production** - Always specify columns for performance
2. **Missing WHERE clause on updates** - Can affect all rows unintentionally
3. **Not handling NULL values** - Use COALESCE or explicit NULL checks
```

### Do/Don't Format
```markdown
## Common Pitfalls

| Don't | Do | Why |
|-------|-----|-----|
| `SELECT *` | `SELECT col1, col2` | Performance |
| Nested subqueries | CTEs or JOINs | Readability |
| String concatenation | Parameterized queries | Security |
```

## Reference File Organization

### Technical Reference
```
references/
├── functions.md        # Function signatures and examples
├── operators.md        # Operator reference table
└── patterns.md         # Common code patterns
```

### Conceptual Reference
```
references/
├── terminology.md      # Glossary of terms
├── concepts.md         # Detailed explanations
└── examples.md         # Extended examples
```

### Procedural Reference
```
references/
├── step-by-step.md     # Detailed procedures
├── troubleshooting.md  # Common issues and fixes
└── advanced.md         # Advanced techniques
```

## Complete Skill Template

```markdown
---
name: doing-something
compatibility: Cursor, VS Code, Claude Code, Altertable
description: "Does something specific for a clear purpose. Use when users need
to accomplish X, work with Y, or ask about Z."
---

# Doing Something

## Quick Start

1. First step
2. Second step
3. Third step

## When to Use This Skill

- User asks about X
- User needs to do Y
- User mentions keywords: "keyword1", "keyword2"

## Core Concepts

Explain the fundamental ideas needed to understand this skill.

### Concept 1

Brief explanation with example.

### Concept 2

Brief explanation with example.

## Workflow

```
Step 1 → Step 2 → Step 3 → Result
```

Explain the workflow in detail.

## Examples

### Basic Example

```code
example code here
```

### Advanced Example

```code
more complex example
```

## Common Pitfalls

1. **Pitfall 1** - Explanation and how to avoid
2. **Pitfall 2** - Explanation and how to avoid
3. **Pitfall 3** - Explanation and how to avoid

## References

- [detailed-topic.md](references/detailed-topic.md) - Extended coverage of topic
- [examples.md](references/examples.md) - More examples
```
