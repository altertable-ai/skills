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

A funnel tracks users through sequential steps:
1. Define the steps (events)
2. Set conversion window
3. Analyze drop-offs between steps

## When to Use This Skill

- Analyzing conversion flows
- Measuring process completion
- Identifying friction points
- Optimizing user journeys
- Comparing funnel performance

## Funnel Concepts

### Funnel Steps

Events that users must complete in sequence:
- Step 1: Entry (e.g., page view)
- Step 2-N: Intermediate actions
- Final Step: Conversion goal

### Conversion Window

Maximum time allowed to complete funnel:
- Short (30 min): Session-based
- Medium (24 hr): Day-based
- Long (7+ days): Consideration flows

### Ordering

- **Strict**: Steps must happen in exact order
- **Any**: Steps can happen in any sequence

## Analysis Framework

### Step 1: Understand the Flow

Map the intended user journey:
- What is the entry point?
- What actions lead to conversion?
- What is the end goal?

### Step 2: Examine Overall Conversion

Start with the big picture:
- Total users entering funnel
- Total conversions
- Overall conversion rate

### Step 3: Analyze Step-by-Step

For each transition:
- How many users proceed?
- What's the drop-off rate?
- Is this expected?

### Step 4: Identify Bottlenecks

Find the biggest problems:
- Largest absolute drop-off
- Largest percentage drop
- Unexpected patterns

### Step 5: Recommend Actions

Based on findings:
- Which step needs attention?
- What might improve it?
- What to test?

## Key Metrics

### Per-Step Metrics

| Metric | Formula |
|--------|---------|
| Step Entry | Users reaching step |
| Step Completion | Users moving to next |
| Step Conversion | Completion / Entry |
| Step Drop-off | 1 - Conversion |

### Overall Metrics

| Metric | Formula |
|--------|---------|
| Total Entry | Users at Step 1 |
| Total Conversion | Users at Final Step |
| Overall CVR | Final / Entry |
| Overall Drop-off | 1 - Overall CVR |

## Common Funnel Patterns

### E-commerce Checkout

```
Product View → Add to Cart → Checkout → Payment → Confirmation
```

Typical metrics:
- View → Cart: 5-10%
- Cart → Checkout: 40-60%
- Checkout → Payment: 70-85%
- Payment → Confirm: 95-99%

### SaaS Signup

```
Landing Page → Start Signup → Complete Form → Verify Email → Activated
```

Typical metrics:
- Landing → Start: 10-20%
- Start → Complete: 60-80%
- Complete → Verify: 70-90%
- Verify → Active: 80-95%

### Onboarding

```
Account Created → Profile Setup → First Action → Core Value → Retained
```

### Feature Adoption

```
Feature Discovered → Feature Tried → Feature Used Again → Regular Use
```

## Interpretation Guidelines

### Healthy Drop-offs

Some drop-off is normal:
- Browsing without intent
- Research phase
- Changed mind (okay)

### Concerning Drop-offs

Investigate when:
- Drop-off exceeds benchmarks
- Drop-off increased suddenly
- Drop-off at unexpected step

### Comparing Funnels

When comparing:
- Same time periods
- Same user segments
- Account for seasonality

## Segmented Analysis

### By Device

Mobile vs Desktop funnels:
- Mobile often has higher drop-off
- Different UX challenges
- Network/speed factors

### By Traffic Source

Source quality varies:
- Paid traffic may convert differently
- Organic often higher intent
- Social may browse more

### By User Type

New vs Returning:
- New users need more guidance
- Returning may skip steps
- Different expectations

## Recommendations Framework

### High Drop-off at Early Steps

Possible issues:
- Wrong traffic/expectations
- Poor value proposition
- Confusing entry point

Actions:
- Improve ad targeting
- Clarify landing page
- A/B test messaging

### High Drop-off at Middle Steps

Possible issues:
- Friction in process
- Missing information
- Technical issues

Actions:
- Simplify forms
- Add progress indicators
- Fix UX issues

### High Drop-off at Final Steps

Possible issues:
- Trust concerns
- Unexpected costs
- Technical failures

Actions:
- Add trust signals
- Transparent pricing
- Monitor errors

## Common Pitfalls

- Too many steps (simplify)
- Too few steps (missing insight)
- Wrong conversion window
- Ignoring segment differences
- Not accounting for data lag
- Comparing incomparable periods

## Reference Files

- [Funnel parameters](references/funnel-parameters.md)
- [Conversion metrics](references/conversion-metrics.md)
