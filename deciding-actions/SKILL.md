---
name: deciding-actions
compatibility: Cursor, VS Code, Claude Code, Altertable
description: Decision matrices for choosing insight types, discovery actions, and avoiding duplicates. Use when deciding between funnel vs semantic vs SQL analysis, or when determining whether to create new vs update vs skip discoveries.
---

# Deciding Actions

## Quick Start

This skill provides decision frameworks for:
1. Choosing the right insight type
2. Deciding discovery actions (new/update/skip)
3. Avoiding duplicate discoveries
4. Selecting analysis approaches

## When to Use This Skill

- Choosing between funnel, semantic, or SQL insights
- Deciding whether to create a new discovery
- Checking for duplicate discoveries
- Selecting the right analysis method
- Planning discovery workflow

## Insight Type Decision Matrix

### Quick Decision Tree

```
User Question
│
├─ About conversion/steps/flow?
│   └─ → FUNNEL INSIGHT
│
├─ About metrics/dimensions/trends?
│   └─ → SEMANTIC INSIGHT
│
├─ Complex/custom/joins needed?
│   └─ → SQL INSIGHT
│
├─ About segments/cohorts?
│   └─ → SEGMENTATION INSIGHT
│
└─ Just informing/acknowledging?
    └─ → FYI DISCOVERY
```

### Detailed Decision Matrix

| Signal | Funnel | Semantic | SQL | Segmentation | FYI |
|--------|--------|----------|-----|--------------|-----|
| "conversion rate" | ✓✓✓ | | | | |
| "drop-off" | ✓✓✓ | | | | |
| "steps to purchase" | ✓✓✓ | | | | |
| "user journey" | ✓✓✓ | | | | |
| "how many" | | ✓✓✓ | | | |
| "trend over time" | | ✓✓✓ | | | |
| "breakdown by" | | ✓✓✓ | | | |
| "compare periods" | | ✓✓✓ | | | |
| "join tables" | | | ✓✓✓ | | |
| "custom calculation" | | | ✓✓✓ | | |
| "raw data" | | | ✓✓✓ | | |
| "complex query" | | | ✓✓✓ | | |
| "users who" | | | | ✓✓✓ | |
| "cohort of" | | | | ✓✓✓ | |
| "segment where" | | | | ✓✓✓ | |
| "acknowledge" | | | | | ✓✓✓ |
| "got it" | | | | | ✓✓✓ |
| "thanks" | | | | | ✓✓✓ |

### When to Use Each Type

#### Use FUNNEL INSIGHT When

- User asks about conversion rates
- Question involves sequential steps
- Analyzing user journey/flow
- Finding where users drop off
- Measuring completion rates

**Keywords**: conversion, funnel, steps, journey, drop-off, flow, complete, abandon

#### Use SEMANTIC INSIGHT When

- User asks about metrics/KPIs
- Question involves trends over time
- Needs breakdown by dimension
- Standard analytics questions
- Comparing time periods

**Keywords**: how many, trend, breakdown, compare, metric, daily, weekly, growth

#### Use SQL INSIGHT When

- Semantic model doesn't have needed data
- Complex joins required
- Custom calculations needed
- Raw data exploration
- Ad-hoc analysis

**Keywords**: join, custom, raw, specific table, complex, calculate

#### Use SEGMENTATION INSIGHT When

- Defining user groups
- Building cohorts
- Targeting specific users
- Behavioral segmentation

**Keywords**: users who, segment, cohort, group of, target

#### Use FYI DISCOVERY When

- Acknowledging user input
- No analysis needed
- Informational response
- Status update
- Simple confirmation

**Keywords**: thanks, got it, understood, noted, will do

## Discovery Action Decision Matrix

### Create vs Update vs Skip

```
Is this finding new?
│
├─ YES: Does similar discovery exist?
│   │
│   ├─ NO → CREATE NEW
│   │
│   └─ YES: Is new info significantly different?
│       │
│       ├─ YES → CREATE NEW (with reference to previous)
│       │
│       └─ NO → SKIP (already covered)
│
└─ NO: Is it a follow-up to previous?
    │
    ├─ YES → CREATE NEW (as follow-up)
    │
    └─ NO → SKIP (redundant)
```

### Duplicate Detection Checklist

Before creating a discovery, check:

| Check | Action if True |
|-------|----------------|
| Same metric, same time range, same finding? | SKIP |
| Same insight within last 24 hours? | SKIP |
| Same topic, minor variation? | SKIP |
| Contradicts recent discovery? | CREATE (with explanation) |
| Adds significant new context? | CREATE |
| User explicitly asked again? | CREATE |

### Discovery Freshness Rules

| Discovery Age | Same Topic Action |
|---------------|-------------------|
| < 1 hour | Always skip unless contradicts |
| 1-24 hours | Skip unless significant new info |
| 1-7 days | Create if adds value |
| > 7 days | Treat as fresh topic |

## Semantic Model Check

### Before SQL, Check Semantic

```
Need data?
│
├─ Check semantic model first
│   │
│   ├─ Dimension/measure exists? → Use SEMANTIC
│   │
│   └─ Not available?
│       │
│       ├─ Can be added to model? → Consider adding, then SEMANTIC
│       │
│       └─ One-off need? → Use SQL
```

### Semantic vs SQL Decision

| Factor | Prefer Semantic | Prefer SQL |
|--------|----------------|------------|
| Reusability | ✓ | |
| Consistency | ✓ | |
| Performance | ✓ | |
| Flexibility | | ✓ |
| Complex joins | | ✓ |
| One-off analysis | | ✓ |
| Standard metrics | ✓ | |
| Custom calculations | | ✓ |

## Analysis Approach Selection

### Question Type → Approach

| Question Pattern | Primary Approach | Fallback |
|------------------|------------------|----------|
| "Why did X happen?" | Semantic breakdown | SQL drill-down |
| "How is X performing?" | Semantic trend | Dashboard |
| "Who are the users that..." | Segmentation | SQL filter |
| "What's the conversion..." | Funnel | SQL with steps |
| "Compare A vs B" | Semantic comparison | SQL union |
| "Predict/forecast" | Not supported | Explain limitation |

### Complexity Assessment

| Complexity | Approach | Notes |
|------------|----------|-------|
| Simple metric | Semantic | Direct query |
| Metric + filter | Semantic | Add dimension filter |
| Metric + breakdown | Semantic | Group by dimension |
| Multi-step analysis | Funnel or SQL | Depends on data |
| Cross-table | SQL | Joins required |
| Historical comparison | Semantic | Time dimension |

## Avoiding Common Mistakes

### Don't Create Discovery When

- Already said the same thing recently
- Information is trivial/obvious
- User didn't ask for insight
- Just acknowledging without adding value
- Repeating what user already knows

### Do Create Discovery When

- New actionable insight found
- Significant change detected
- User explicitly requested analysis
- Important pattern identified
- Anomaly requires attention

### Quality Gates

Before creating any discovery:

1. **Novelty**: Is this new information?
2. **Value**: Does this help the user?
3. **Accuracy**: Is the data correct?
4. **Actionable**: Can user do something with this?
5. **Timing**: Is now the right time?

## Reference Files

- [Insight type selection](references/insight-selection.md)
- [Duplicate prevention](references/duplicate-prevention.md)
- [Discovery workflow](references/discovery-workflow.md)
