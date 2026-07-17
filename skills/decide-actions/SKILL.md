---
name: decide-actions
compatibility: Requires Altertable MCP server
description: Decision matrices for picking insight types (funnel, retention, semantic, segmentation, SQL), task types, and discovery actions. Use when choosing types or whether to create or skip discoveries.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Deciding Actions

## Quick Start

This skill provides decision frameworks for:
1. Choosing the right insight type (funnel, retention, semantic, segmentation, SQL)
2. Choosing the right task type (anomaly_detection, forecast, ask)
3. Deciding discovery actions (create/skip)
4. Avoiding duplicate discoveries
5. Selecting analysis approaches

## When to Use This Skill

- Choosing between funnel, retention, semantic, segmentation, or SQL insights
- Choosing a task type for automated monitoring (anomaly_detection, forecast, ask)
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
├─ Need individual rows or a membership list?
│   └─ → SQL INSIGHT
│
├─ About comparing event metrics across segments/cohorts?
│   └─ → SEGMENTATION INSIGHT
│
├─ About non-event metrics/dimensions/trends?
│   ├─ Modeled metric, dimension, relation, or inline measure? → SEMANTIC INSIGHT
│   └─ Unmodeled data, unsupported grain, or custom join? → SQL INSIGHT
│
├─ Need automated recurring analysis?
│   └─ → TASK (see configure-tasks skill)
│
└─ Just informing/acknowledging?
    └─ → RESPOND WITHOUT DISCOVERY
```

### Detailed Decision Matrix

| Signal | Funnel | Retention | Semantic | SQL | Segmentation |
|--------|--------|-----------|----------|-----|--------------|
| "conversion rate" | ✓✓✓ | | | | |
| "drop-off" | ✓✓✓ | | | | |
| "steps to purchase" | ✓✓✓ | | | | |
| "user journey" | ✓✓✓ | | | | |
| "stuck at step/level" | ✓✓✓ | | | | |
| "progression from X to Y" | ✓✓✓ | | | | |
| "did X but not Y" | ✓✓✓ | | | | |
| "come back" | | ✓✓✓ | | | |
| "return after" | | ✓✓✓ | | | |
| "retained" | | ✓✓✓ | | | |
| "churn" | | ✓✓✓ | | | |
| "how many" | | | ✓✓✓ | | |
| "trend over time" | | | ✓✓✓ | | |
| "breakdown by" | | | ✓✓✓ | | |
| "compare periods" | | | ✓✓✓ | | |
| "modeled relation" | | | ✓✓✓ | | |
| "inline calculation on a modeled table" | | | ✓✓✓ | | |
| "unmodeled/custom join" | | | | ✓✓✓ | |
| "unsupported grain or window" | | | | ✓✓✓ | |
| "raw data" | | | | ✓✓✓ | |
| "complex query" | | | | ✓✓✓ | |
| "event activity for users with [property]" | | | | | ✓✓✓ |
| "compare cohorts" | | | | | ✓✓✓ |
| "break down event by property" | | | | | ✓✓✓ |

**Disambiguation — Segmentation vs Funnel:**

The phrase "users who" is ambiguous. Apply this test:

| Pattern | Type | Why |
|---------|------|-----|
| "show **which users have** property X" | SQL | Returning identity rows |
| "compare **event activity for users with** property X" | Segmentation | Aggregate behavioral comparison |
| "users who **did** event A **then** event B" | Funnel | Sequential event analysis |
| "event count by plan/device/source" | Segmentation | Event metric comparison across property values |
| "users **stuck at** step/level X" | Funnel | Step-to-step progression |
| "users who **completed** X but **not** Y" | Funnel | Measuring drop-off between steps |
| "event activity for users **in** segment/group X" | Segmentation | Aggregate behavior for a pre-defined cohort |

**Key test:** Is the request for identity rows (→ SQL), aggregate event behavior across cohorts or properties (→ segmentation), or movement through ordered steps (→ funnel)?

**Disambiguation — Semantic vs SQL:**

Both produce metric values. Apply this test:

| Factor | Semantic | SQL |
|--------|----------|-----|
| Metric/dimension exists in semantic model | ✓ | |
| Join is covered by modeled relations | ✓ | |
| Calculation fits an inline measure on a modeled table | ✓ | |
| Join is unmodeled or needs custom SQL | | ✓ |
| Calculation needs an unsupported grain or window | | ✓ |
| Data not modeled in semantic layer | | ✓ |
| Standard breakdown (e.g., revenue by region) | ✓ | |

**Key test:** Does the semantic model expose the needed metric and dimension, or can the calculation be expressed as an inline measure on a modeled table? Yes → **Semantic**. Use **SQL** when the data or relationship is unmodeled, or when the calculation needs an unsupported grain or window. When unsure, check the semantic model first.

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
- Calculations expressible as inline measures on modeled tables

**Keywords**: how many, trend, breakdown, compare, metric, daily, weekly, growth

#### Use SQL INSIGHT When

- Semantic model doesn't have needed data
- Unmodeled joins or custom join logic required
- Calculation requires an unsupported grain or window
- Raw data exploration
- Individual rows or membership lists
- Ad-hoc analysis

**Keywords**: join, custom, raw, specific table, complex, calculate

#### Use SEGMENTATION INSIGHT When

- Comparing event metrics across cohorts (e.g., feature usage by plan, device, or region)
- Breaking down events by event, user, or session properties
- Segmenting behavior over time without requiring ordered steps
- Comparing aggregate event activity across existing cohorts, properties, or traits
- Filtering event series by dimensions like device, plan, or region

**Keywords**: segment, cohort comparison, event breakdown, property, trait

#### Respond Without Creating a Discovery When

- Acknowledging user input
- No analysis needed
- Informational response
- Status update
- Simple confirmation

**Keywords**: thanks, got it, understood, noted, will do

## Task Type Decision Matrix

When the user needs **automated, recurring analysis** rather than a one-off insight, choose a task type:

```
User wants automation
│
├─ Detect outliers/anomalies in an Insight?
│   └─ → anomaly_detection task
│
├─ Project future values from an Insight?
│   └─ → forecast task
│
└─ Open-ended AI analysis, optionally with Insight or Dashboard context?
    └─ → ask task
```

See the **configure-tasks** skill for full task creation workflow.

## Discovery Action Decision Matrix

### Create vs Skip

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
| Same metric, time range, and finding with no new context? | SKIP |
| Same topic, minor variation? | SKIP |
| Contradicts recent discovery? | CREATE (with explanation) |
| Adds significant new context? | CREATE |
| User explicitly asked again? | ANSWER; create only for a verified finding worth review or notification |

Recency alone does not determine the action. Compare the finding and its context. Create a follow-up when it adds material information, corrects a prior result, and warrants review or notification.

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
| Flexibility | | ✓ |
| Joins covered by modeled relations | ✓ | |
| Unmodeled or custom joins | | ✓ |
| Inline measure on a modeled table | ✓ | |
| Unsupported grain or window | | ✓ |
| Standard metrics | ✓ | |

## Analysis Approach Selection

### Question Type → Approach

| Question Pattern | Primary Approach | Fallback |
|------------------|------------------|----------|
| "Why did X happen?" | Semantic breakdown | SQL drill-down |
| "How is X performing?" | Semantic trend | Dashboard |
| "Who are the users that..." | SQL filter | Segmentation for aggregate behavior only |
| "What's the conversion..." | Funnel | SQL with steps |
| "Do users come back after..." | Retention | Funnel fallback |
| "Compare modeled metric A vs B" | Semantic comparison | SQL union |
| "Predict/forecast" | Optional local forecast tool when available | Forecast task for recurring analysis |

### Complexity Assessment

| Complexity | Approach | Notes |
|------------|----------|-------|
| Simple metric | Semantic | Direct query |
| Metric + filter | Semantic | Add dimension filter |
| Metric + breakdown | Semantic | Group by dimension |
| Multi-step analysis | Funnel or SQL | Depends on data |
| Cross-table with modeled relation | Semantic | SQL when the relation is not modeled |
| Historical comparison | Semantic | Time dimension |

## Avoiding Common Mistakes

### Don't Create Discovery When

- Same metric, period, and finding already exist with no material new context
- Information is trivial/obvious
- Analysis produced no verified finding worth review or notification
- Just acknowledging without adding value
- Repeating what user already knows

### Do Create Discovery When

- New actionable insight found
- Significant change detected
- User explicitly requested notification or review of a verified finding
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
| "Modeled metric X by semantic dimension Y" | SQL | Semantic | The metric and dimension use governed model definitions |
| "Event count by event property or user trait" | Semantic | Segmentation | Event-series breakdowns belong to segmentation |
| "Users with property X" | Funnel | SQL or Segmentation | Use SQL for identity rows; use Segmentation for aggregate event behavior |
| "Do users come back after X?" | Funnel | Retention | Return behavior, not step progression |
| "Churn after event X" | Segmentation | Retention | Measuring who doesn't return over time |

## Reference Files

- [Insight type selection](references/insight-selection.md)
- [Duplicate prevention](references/duplicate-prevention.md)
- [Discovery workflow](references/discovery-workflow.md)
