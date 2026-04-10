# Discoveries

Discoveries are the reviewable findings that agents produce when they detect something noteworthy in data.

## Purpose

Discoveries convert continuous monitoring into actionable team decisions:

- Surface important changes quickly
- Reduce noise by prioritizing relevance
- Add context and recommendations
- Keep humans in control through explicit review

## Typical Discovery Content

A discovery should include:

- Clear statement of the finding
- Why it matters
- Supporting context or visualization
- Suggested next action
- Source reference (insight, dashboard, connection, segment, model, or events stream)

## Discovery Lifecycle

```text
Needs review -> Accepted | Rejected
```

- **Needs review:** awaiting human decision
- **Accepted:** validated as meaningful and actionable
- **Rejected:** dismissed as irrelevant, noisy, or incorrect

## Common Discovery Types

- Trend changes (for example, week-over-week drops)
- Anomalies (unexpected spikes or dips)
- Segment shifts (cohort behavior changes)
- Schema/model changes (new structures or semantics)
- Event readiness signals (new event streams available for analysis)

## Feedback Loop with Memories

Review outcomes inform agent memory:

- Accepted discoveries reinforce useful detection patterns
- Rejected discoveries reduce similar false positives
- Repeated feedback calibrates sensitivity and relevance

This loop is how discovery quality improves over time.
