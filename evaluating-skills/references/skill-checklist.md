# Skill Evaluation Checklist

Use this detailed checklist when reviewing skills for quality and compliance.

## Frontmatter Validation

### Name Field
| Criterion | Valid | Invalid |
|-----------|-------|---------|
| Format | `analyzing-data` | `data-analysis`, `AnalyzingData` |
| Case | lowercase only | `Analyzing-Data` |
| Separator | hyphens | `analyzing_data`, `analyzingdata` |
| Form | gerund (verb-ing) | noun or adjective |
| Length | ≤ 64 characters | > 64 characters |
| Directory match | name = folder name | name ≠ folder name |

### Description Field
| Criterion | Check |
|-----------|-------|
| Person | Third person ("Analyzes...") |
| Trigger keywords | Contains words that activate the skill |
| Purpose | Explains what the skill does |
| When to use | Explains activation conditions |
| Length | ≤ 1024 characters |

### Compatibility Field
Valid values:
- `Cursor`
- `VS Code`
- `Claude Code`
- `Altertable`

## Structure Validation

### File Organization
```
skill-name/
├── SKILL.md           ✓ Required
└── references/        ○ Optional
    ├── file-1.md     ✓ Allowed
    ├── file-2.md     ✓ Allowed
    └── nested/       ✗ Not allowed
```

### Size Constraints
| Element | Limit |
|---------|-------|
| SKILL.md body | < 500 lines |
| Total skill tokens | < 5000 tokens |
| Reference depth | 1 level only |

### Required Sections
- [ ] Quick Start (first content section)
- [ ] When to Use This Skill

### Recommended Sections
- [ ] Core Concepts or Core Workflow
- [ ] Examples (with code blocks)
- [ ] Common Pitfalls
- [ ] References (if references/ exists)

## Content Quality Scoring

### Clarity (0-10)
| Score | Criteria |
|-------|----------|
| 9-10 | Crystal clear, no ambiguity |
| 7-8 | Clear with minor improvements possible |
| 5-6 | Understandable but requires re-reading |
| 3-4 | Confusing in places |
| 0-2 | Difficult to understand |

### Actionability (0-10)
| Score | Criteria |
|-------|----------|
| 9-10 | Can immediately apply knowledge |
| 7-8 | Actionable with minor gaps |
| 5-6 | Requires additional context |
| 3-4 | More conceptual than practical |
| 0-2 | Not actionable |

### Completeness (0-10)
| Score | Criteria |
|-------|----------|
| 9-10 | Comprehensive coverage |
| 7-8 | Covers most use cases |
| 5-6 | Covers common cases |
| 3-4 | Missing important scenarios |
| 0-2 | Incomplete |

### Examples (0-10)
| Score | Criteria |
|-------|----------|
| 9-10 | Concrete, diverse, realistic |
| 7-8 | Good examples with minor gaps |
| 5-6 | Basic examples present |
| 3-4 | Examples too abstract |
| 0-2 | No meaningful examples |

## Formatting Checks

### Text Formatting
- [ ] Paragraphs ≤ 5 lines
- [ ] Headers for organization
- [ ] Bold for emphasis (not ALL CAPS)
- [ ] Bullet points for lists
- [ ] Tables for comparisons

### Code Formatting
- [ ] Fenced code blocks (```)
- [ ] Language hints (```sql, ```python)
- [ ] Realistic, working examples
- [ ] Comments for complex code

### Visual Elements
- [ ] ASCII diagrams for workflows
- [ ] Tables for structured data
- [ ] Decision trees for choices

## Anti-Pattern Detection

### Description Anti-Patterns
| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "I help you..." | First person | "Helps users..." |
| "This skill..." | Self-referential | Direct description |
| No keywords | Can't be found | Add trigger words |
| Too vague | Unclear purpose | Be specific |

### Content Anti-Patterns
| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Wall of text | Hard to scan | Break into sections |
| No examples | Abstract | Add concrete cases |
| Nested refs | Violates spec | Flatten structure |
| > 500 lines | Too long | Move to references |

### Naming Anti-Patterns
| Anti-Pattern | Correct Form |
|--------------|--------------|
| `data-analyzer` | `analyzing-data` |
| `report_creator` | `creating-reports` |
| `UserManagement` | `managing-users` |
| `skill` | `specific-action-skill` |

## Quick Evaluation Template

```markdown
## Skill Evaluation: [skill-name]

### Frontmatter: [PASS/FAIL]
- Name format: [✓/✗]
- Description quality: [✓/✗]
- Compatibility: [✓/✗]

### Structure: [PASS/FAIL]
- Size constraints: [✓/✗]
- Required sections: [✓/✗]
- Reference organization: [✓/✗]

### Content Quality: [X/40]
- Clarity: [X/10]
- Actionability: [X/10]
- Completeness: [X/10]
- Examples: [X/10]

### Issues Found:
1. [Issue description]
2. [Issue description]

### Recommendations:
1. [Improvement suggestion]
2. [Improvement suggestion]

### Overall: [PASS/NEEDS WORK/FAIL]
```
