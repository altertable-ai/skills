# Memory Types Reference

## Episodic - What Happened

Record specific events with outcomes.

**Characteristics:**
- Time-bound (when did it happen?)
- Context-rich (what was the situation?)
- Has an outcome (success, failure, rejected, accepted)

**Examples:**
- "Created DSC-789 for 15% revenue drop. User rejected - threshold should be 20%."
- "Analysis of churn patterns completed successfully, identified weekend spike."
- "Funnel insight DSC-456 was accepted - user confirmed conversion drop was actionable."

**Include:**
- What happened
- The outcome
- Why it matters for future runs

## Semantic - What You Know

Record facts and knowledge independent of specific events.

**Characteristics:**
- Context-independent (true regardless of when learned)
- Factual (can be verified)
- May have confidence level

**Examples:**
- "Organization ignores metric changes under 20% threshold."
- "Sales data has NULL values on weekends due to batch processing."
- "Marketing team owns Dashboard DSH-101 for campaign tracking."

**Include:**
- The fact or pattern
- Confidence level if uncertain
- Source or evidence if available

## Procedural - How To Do Things

Record techniques and approaches that work.

**Characteristics:**
- Action-oriented (how to do something)
- Has success rate (how often it works)
- May have failure contexts (when it doesn't work)

**Examples:**
- "For sales table: use date_trunc with timezone filter. Fails without timezone on UTC data."
- "Window functions outperform subqueries for running totals on events table."
- "Preview insight before creating to catch validation errors early."

**Include:**
- The technique
- Success rate
- When it fails (failure contexts)

## Type Transitions

Over time, memories can transition:

**Episodic → Semantic:**
```
3x "User rejected discovery for being under threshold"
→ "Organization ignores changes under 20%"
```

**Episodic → Procedural:**
```
3x "Fixed by adjusting time window"
→ "Always verify time window when results look wrong"
```

## Quick Decision

| Question | Type |
|----------|------|
| Did something happen? | Episodic |
| Did I learn a fact? | Semantic |
| Did I find a technique? | Procedural |
