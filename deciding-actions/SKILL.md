---
name: deciding-actions
compatibility: Requires Altertable MCP server
description: Decision matrices for choosing insight types, discovery actions, and avoiding duplicates. Use when deciding between funnel, retention, semantic, segmentation, or SQL insights, or when determining whether to create, update, or skip discoveries.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Deciding Actions

## Quick Start

This skill provides decision frameworks for:
1. Choosing the right insight type
2. Deciding discovery actions (new/update/skip)
3. Avoiding duplicate discoveries
4. Selecting analysis approaches

## When to Use This Skill

- Choosing between funnel, retention, semantic, or SQL insights
- Deciding whether to create a new discovery
- Checking for duplicate discoveries
- Selecting the right analysis method
- Planning discovery workflow

## Insight Type Decision Matrix

### How to Use

1. Match the user's question against the decision tree below
2. If ambiguous, check the signal matrix for matching phrases
3. If still ambiguous, use the disambiguation blocks to resolve the overlap
4. Cross-check against the common misclassifications before creating

### Quick Decision Tree

```
User Question
│
├─ About conversion/steps/flow?
│   └─ → FUNNEL INSIGHT
│
├─ About whether users come back after an event?
│   └─ → RETENTION INSIGHT
│
├─ About metrics/dimensions/trends?
│   └─ → SEMANTIC INSIGHT
│
├─ Complex/custom/joins needed?
│   └─ → SQL INSIGHT
│
├─ About segments/cohorts (by attributes, not sequence)?
│   └─ → SEGMENTATION INSIGHT
│
└─ Just informing/acknowledging?
    └─ → FYI DISCOVERY
```

### Detailed Decision Matrix

| Signal | Funnel | Retention | Semantic | SQL | Segmentation | FYI |
|--------|--------|-----------|----------|-----|--------------|-----|
| "conversion rate" | ✓✓✓ | | | | | |
| "drop-off" | ✓✓✓ | | | | | |
| "steps to purchase" | ✓✓✓ | | | | | |
| "user journey" | ✓✓✓ | | | | | |
| "stuck at step/level" | ✓✓✓ | | | | | |
| "progression from X to Y" | ✓✓✓ | | | | | |
| "did X but not Y" | ✓✓✓ | | | | | |
| "come back" | | ✓✓✓ | | | | |
| "return after" | | ✓✓✓ | | | | |
| "retained" | | ✓✓✓ | | | | |
| "churn" | | ✓✓✓ | | | | |
| "how many" | | | ✓✓✓ | | | |
| "trend over time" | | | ✓✓✓ | | | |
| "breakdown by" | | | ✓✓✓ | | | |
| "compare periods" | | | ✓✓✓ | | | |
| "join tables" | | | | ✓✓✓ | | |
| "custom calculation" | | | | ✓✓✓ | | |
| "raw data" | | | | ✓✓✓ | | |
| "complex query" | | | | ✓✓✓ | | |
| "users who [have property]" | | | | | ✓✓✓ | |
| "cohort of" | | | | | ✓✓✓ | |
| "segment where" | | | | | ✓✓✓ | |
| "acknowledge" | | | | | | ✓✓✓ |
| "got it" | | | | | | ✓✓✓ |
| "thanks" | | | | | | ✓✓✓ |

**Disambiguation — Segmentation vs Funnel:**

The phrase "users who" is ambiguous. Apply this test:

| Pattern | Type | Why |
|---------|------|-----|
| "users who **have** property X" | Segmentation | Defining a group by attributes |
| "users who **did** event A **then** event B" | Funnel | Sequential event analysis |
| "users **stuck at** step/level X" | Funnel | Step-to-step progression |
| "users who **completed** X but **not** Y" | Funnel | Measuring drop-off between steps |
| "users **in** segment/group X" | Segmentation | Pre-defined cohort |

**Key test:** Is the finding about *who users are* (properties/attributes → segmentation) or *what users did in sequence* (events/steps → funnel)?

**Disambiguation — Semantic vs SQL:**

Both produce metric values. Apply this test:

| Factor | Semantic | SQL |
|--------|----------|-----|
| Metric/dimension exists in semantic model | ✓ | |
| Requires joins across tables | | ✓ |
| Custom calculation or formula | | ✓ |
| Data not modeled in semantic layer | | ✓ |
| Standard breakdown (e.g., revenue by region) | ✓ | |

**Key test:** Does the semantic model already expose this metric and dimension? Yes → **Semantic**. No → **SQL**. When unsure, check the semantic model first.

**Disambiguation — Funnel vs Retention:**

Both involve user events over time. Apply this test:

| Pattern | Type | Why |
|---------|------|-----|
| "users who **go from** A **to** B" | Funnel | Sequential step progression |
| "users who **come back** after A" | Retention | Return behavior over time |
| "**drop-off** between steps" | Funnel | Measuring where users stop in a sequence |
| "**churn** after event X" | Retention | Measuring who doesn't return |

**Key test:** Is the finding about *moving through a sequence of steps* (→ funnel) or *coming back after a starting event* (→ retention)?

### When to Use Each Type

#### Use FUNNEL INSIGHT When

- User asks about conversion rates
- Question involves sequential steps or progression
- Analyzing user journey/flow
- Finding where users drop off or get stuck
- Measuring completion rates between stages
- Comparing progression across levels, tiers, or milestones

**Keywords**: conversion, funnel, steps, journey, drop-off, flow, complete, abandon, stuck, progression, level, stage, bottleneck

#### Use RETENTION INSIGHT When

- Analyzing whether users return after a starting event
- Measuring churn or repeat behavior over time
- Comparing retention across cohorts or time periods
- Tracking if users who did event A come back to do event B

**Keywords**: retention, churn, come back, return, repeat, re-engage, day 1/7/30

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

- The output is a **user group**, not a metric value
- Users are grouped by attributes or properties, not by sequential behavior
- Building cohorts for targeting, comparison, or further analysis
- Filtering users by dimensions like device, plan, region, etc.

**Keywords**: segment, cohort, group of, target, users with, users in

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
| "Do users come back after..." | Retention | Funnel fallback |
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

## Common Misclassifications

Findings that are frequently assigned the wrong insight type:

| Finding | Wrong Choice | Right Choice | Why |
|---------|-------------|-------------|-----|
| "Users stuck at step/level X" | Segmentation | Funnel | Step progression = sequential analysis |
| "Drop-off between A and B" | SQL | Funnel | Sequential steps with conversion |
| "Users who did X but not Y" | Segmentation | Funnel | Sequential dependency between events |
| "Metric broken down by property" | SQL | Semantic | Standard breakdown = use semantic model |
| "Metric X by dimension Y" | SQL | Semantic | Dimension likely exists in model |
| "Users with property X" | Funnel | Segmentation | Attribute-based group, not a flow |
| "Do users come back after X?" | Funnel | Retention | Return behavior, not step progression |
| "Churn after event X" | Segmentation | Retention | Measuring who doesn't return over time |

## Reference Files

- [Insight type selection](references/insight-selection.md)
- [Duplicate prevention](references/duplicate-prevention.md)
- [Discovery workflow](references/discovery-workflow.md)
