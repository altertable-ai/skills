---
name: evaluating-skills
compatibility: Cursor, VS Code, Claude Code, Altertable
description: "Evaluates and creates agent skills following best practices. Use when reviewing skill quality, writing new skills, refactoring existing skills, or when the user asks about skill structure, format, or specification."
---

# Evaluating & Creating Skills

## Quick Start

1. **Creating**: Use gerund name → write frontmatter → structure SKILL.md → add references
2. **Evaluating**: Check frontmatter → verify structure → assess content quality → validate constraints

## When to Use This Skill

- User wants to create a new skill
- User asks to review or evaluate an existing skill
- User needs help with skill format or structure
- User asks about skill best practices
- User wants to refactor or improve a skill
- Keywords: "skill", "SKILL.md", "create skill", "evaluate skill", "skill quality"

## Skill Anatomy

```
skill-name/                    # Gerund form (verb-ing)
├── SKILL.md                   # Main documentation (<500 lines)
└── references/                # Optional detailed references
    ├── topic-1.md            # One level deep only
    └── topic-2.md
```

### Frontmatter (Required)

```yaml
---
name: skill-name                    # Gerund, lowercase, hyphens, max 64 chars
compatibility: Cursor, VS Code, Claude Code, Altertable
description: "Third person description with trigger keywords. Max 1024 chars."
---
```

**Description Rules:**
- Third person: "Analyzes data..." not "I help you..."
- Include trigger keywords for agent activation
- Describe what AND when to use

## Recommended Section Order

| Section | Purpose | Guidelines |
|---------|---------|------------|
| Quick Start | Immediate value | 2-5 lines, actionable |
| When to Use | Activation triggers | Bullet points, keywords |
| Core Concepts | Mental models | Build understanding |
| Workflow/Procedures | Step-by-step | Progressive complexity |
| Examples | Concrete patterns | Code blocks, scenarios |
| Common Pitfalls | Mistakes to avoid | 5-10 items |
| References | Deep dives | Link to references/ |

## Skill Types & Patterns

### Exploratory Skills
Explain concepts, provide reference material, build mental models.
- Lead with fundamentals
- Include terminology glossary
- Show common patterns

### Procedural Skills
Step-by-step guides for completing tasks.
- Start with quick start
- Show code examples early
- Progress simple → complex

### Decision/Framework Skills
Help make choices between options.
- Lead with decision trees (ASCII)
- Provide decision matrices
- Include keyword signals

### Analytical Skills
Interpret data or outputs.
- Explain interpretation frameworks
- Pattern recognition guidance
- Good vs bad examples

## Evaluation Checklist

### Frontmatter
- [ ] Name uses gerund form (verb-ing)
- [ ] Name is lowercase with hyphens only
- [ ] Name matches directory name
- [ ] Description is third person
- [ ] Description includes trigger keywords
- [ ] Description < 1024 characters

### Structure
- [ ] SKILL.md body < 500 lines
- [ ] Total skill < 5000 tokens
- [ ] References one level deep only
- [ ] Has Quick Start section
- [ ] Has When to Use section

### Content Quality
- [ ] Paragraphs 3-5 lines max
- [ ] Uses headers for organization
- [ ] Code in fenced blocks with language
- [ ] Tables for comparisons
- [ ] Concrete examples (not abstract)
- [ ] No time-sensitive information
- [ ] Consistent terminology

### Common Pitfalls
- [ ] Includes pitfalls section
- [ ] 5-10 specific mistakes
- [ ] Explains why they're wrong

## Creating a New Skill

### Step 1: Choose the Name

```
Good: analyzing-data, creating-reports, managing-users
Bad:  data-analysis, report-creator, user-management
```

Use gerund form (verb + -ing). The action should be clear.

### Step 2: Write the Description

Template:
```
"{Verb}s {what} for {purpose}. Use when {trigger conditions}."
```

Example:
```
"Analyzes chart visualizations to extract insights. Use when interpreting
dashboards, identifying trends, or explaining data patterns to stakeholders."
```

### Step 3: Structure Content

1. Start with Quick Start (2-5 actionable lines)
2. Add When to Use (bullet list of triggers)
3. Write core content (concepts, workflows, examples)
4. Add Common Pitfalls
5. Move detailed content to references/

### Step 4: Validate

Run through the evaluation checklist above.

## Common Pitfalls

1. **First-person descriptions** - Use "Analyzes..." not "I analyze..."
2. **Missing trigger keywords** - Agents can't find the skill
3. **Too long SKILL.md** - Move details to references/
4. **Nested reference folders** - Only one level allowed
5. **Abstract examples** - Use concrete, real scenarios
6. **Noun-form names** - Use "analyzing-data" not "data-analyzer"
7. **No Quick Start** - Users abandon without immediate value
8. **Inconsistent terminology** - Pick terms and stick with them
9. **Missing pitfalls section** - Helps users avoid mistakes
10. **Time-sensitive content** - Skills should be evergreen

## References

- [skill-checklist.md](references/skill-checklist.md) - Detailed evaluation checklist
- [examples.md](references/examples.md) - Patterns from well-designed skills
