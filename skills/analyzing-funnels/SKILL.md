---
name: analyzing-funnels
compatibility: Requires Altertable MCP server
description: Creates and analyzes conversion funnels to understand user journeys and drop-off points. Use when analyzing conversion, onboarding, checkout flows, or multi-step processes.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Analyzing Funnels

## Quick Start

To analyze a funnel:
1. Clarify the user journey the user wants to measure
2. Use the Altertable MCP server to create the funnel with the right steps, window, and ordering
3. Query the funnel data and calculate drop-off rates per step
4. Identify the biggest bottleneck and present actionable findings

## When to Use This Skill

- User asks about conversion rates, drop-offs, or completion rates
- Analyzing a multi-step process (signup, checkout, onboarding, feature adoption)
- Comparing funnel performance across segments or time periods
- Identifying where users abandon a flow

## Core Workflow

### Step 1: Define the Funnel

Ask the user (or infer from context) what journey to measure. You need:
- **Steps**: Ordered list of events from entry to conversion goal
- **Conversion window**: Maximum time allowed to complete the funnel
  - Use short windows (30 min) for session flows like checkout
  - Use medium windows (24 hr) for day-bounded flows
  - Use long windows (7+ days) for consideration flows like onboarding
- **Ordering**: Strict (exact sequence required) or Any (steps in any order)

Default to **strict ordering** unless the user specifies otherwise.

### Step 2: Preview and Create the Funnel

Use the Altertable MCP server to:
1. Preview the funnel first to validate step definitions and check the data looks correct
2. Once validated, create the funnel insight (or funnel insight discovery to save and share it)
3. Query the funnel to retrieve per-step user counts

### Step 3: Calculate Metrics

For each step transition, compute:

| Metric | Formula |
|--------|---------|
| Step conversion rate | Users at step N+1 / Users at step N |
| Step drop-off rate | 1 - Step conversion rate |
| Overall conversion rate | Users at final step / Users at step 1 |

### Step 4: Identify Bottlenecks

Find the step transition with:
- The largest absolute user drop-off
- The largest percentage drop-off
- Any unexpected pattern (e.g., later steps dropping more than early steps)

### Step 5: Present Results

Present results as a step-by-step breakdown:
- Show each step with user count, conversion rate, and drop-off rate
- Highlight the primary bottleneck
- Provide a concise recommendation tied to the bottleneck (what to investigate or improve)

Format example:
```
Step 1: Page View         - 10,000 users
Step 2: Add to Cart       -  1,200 users (12.0% conversion, 88.0% drop-off) <-- biggest drop
Step 3: Checkout Started  -    800 users (66.7% conversion, 33.3% drop-off)
Step 4: Purchase Complete -    720 users (90.0% conversion, 10.0% drop-off)

Overall conversion: 7.2% (720 / 10,000)
Bottleneck: Step 1 to Step 2 -- 88% of users drop off before adding to cart.
```

## Segmented Analysis

When comparing funnels across segments (device, traffic source, user type):
- Always compare identical step definitions and time periods
- Call out which segment has the worst conversion and at which step
- Account for sample size -- small segments can produce misleading rates

## Common Pitfalls

- **Wrong conversion window**: Too short cuts off legitimate conversions; too long inflates rates with unrelated sessions. Match the window to the expected user behavior.
- **Too many steps**: Including minor intermediate events dilutes the analysis. Keep funnels to 3-7 meaningful steps.
- **Too few steps**: Jumping from entry to conversion hides where users actually drop off.
- **Ignoring ordering**: Using "any" ordering when the flow is inherently sequential produces misleading results.
- **Comparing mismatched periods**: Ensure segments or time comparisons use the same date ranges and funnel definitions.
- **Not previewing before creating an insight**: Always preview funnel results to verify step definitions are correct before saving.

## Reference Files

- [Funnel parameters](references/funnel-parameters.md)
- [Conversion metrics](references/conversion-metrics.md)
