---
name: managing-discoveries
compatibility: Requires Altertable MCP server
description: Manages the discovery approval workflow and user feedback processing. Use when handling discovery reviews, understanding approval states, processing user feedback, or managing discovery lifecycle.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Managing Discoveries

## Quick Start

To manage discoveries:
1. List discoveries filtered by status via the Altertable MCP server
2. Inspect each discovery to get full details (title, description, reasoning, status, data type, tags, plan)
3. Accept, reject, or ignore based on your assessment
4. When feedback arrives, extract the user's intent and act on it

## Listing Discoveries

Use the Altertable MCP server to retrieve and act on discoveries:

- **List discoveries** -- filter by status, date range, or search query
- **View a discovery** -- inspect full details including reasoning and plan
- **Update a discovery** -- change status to accepted, rejected, or ignored
- **Suggest replies** -- generate reply suggestions for user feedback

Available statuses for filtering: `pending_review`, `accepted`, `rejected`, `ignored`.

## Reviewing a Discovery

When you need to review a discovery, follow these steps in order:

1. **Check factual accuracy** -- Does the title match the underlying data? Are the numbers correct?
2. **Verify it is not a duplicate** -- Search existing discoveries for overlapping findings before approving.
3. **Assess actionability** -- Can the reader do something with this information? If not, reject.
4. **Evaluate timing** -- Is this finding still current, or has the data gone stale?
5. **Decide**:
   - **Accept** if steps 1-4 all pass.
   - **Reject** if the analysis is wrong, duplicated, or not actionable.
   - **Ignore** if the finding is low-priority and not worth surfacing.

For batch reviews, sort by priority first, then group by topic, and apply the same five-step check to each.

## Discovery Lifecycle

Discoveries flow through these states:

```
pending_visualization_generation
         |
    pending_admin_review  -->  admin_rejected
         |
    pending_review
         |
  accepted | rejected | ignored
```

| State | Description | Next States |
|-------|-------------|-------------|
| `pending_visualization_generation` | Waiting for chart to be generated | pending_admin_review |
| `pending_admin_review` | Awaiting admin approval | pending_review, admin_rejected |
| `pending_review` | Approved by admin, awaiting organization action | accepted, rejected, ignored |
| `accepted` | Accepted by organization | (terminal) |
| `rejected` | Rejected by organization | (terminal) |
| `ignored` | Ignored by organization | (terminal) |
| `admin_rejected` | Admin rejected before organization sees it | (terminal) |

Some discoveries auto-approve (skip `pending_admin_review`) based on watcher configuration, confidence score, or organization settings. Do not assume every discovery passes through admin review.

## Processing User Feedback

When a user provides feedback on a discovery, follow this procedure:

1. **Identify the feedback type** from the table below.
2. **Extract explicit instructions** -- Did the user ask for a specific follow-up or correction?
3. **Detect implicit preferences** -- Does the feedback signal a topic they care more or less about?
4. **Take the corresponding action** immediately.

| Feedback Type | Meaning | What to Do |
|---------------|---------|------------|
| `useful` | Valuable insight | Note what made it useful; produce more findings like it |
| `not_useful` | No value | Identify why it missed; avoid similar findings |
| `already_knew` | Known information | Deprioritize this topic unless new data appears |
| `incorrect` | Wrong analysis | Investigate the error source; correct and re-create if warranted |
| `follow_up` | Wants more detail | Continue the analysis and surface deeper findings |

When feedback includes free-text comments, parse them for:
- Direct requests ("show me this by region")
- Threshold adjustments ("only alert me if the change is over 10%")
- Topic preferences ("I don't care about this metric")

## Common Pitfalls

- **Approving without checking for duplicates.** Always search existing discoveries before accepting a new one.
- **Ignoring `already_knew` feedback.** This signals you are surfacing stale knowledge -- deprioritize that topic.
- **Treating `incorrect` as `not_useful`.** Incorrect means the analysis has a bug; investigate and fix the root cause rather than just moving on.
- **Over-alerting.** If a user has rejected or ignored several discoveries on the same topic, stop surfacing similar findings until new data changes the picture.
- **Not acting on free-text feedback.** Users often embed specific requests inside rejection comments. Always parse the text for actionable instructions.

## Reference Files

- [Approval states](references/approval-states.md) - Read when a discovery is in an unexpected state or when you need to understand valid state transitions
- [Review patterns](references/review-patterns.md) - Read when batch-reviewing multiple discoveries or designing a review strategy
- [Intent detection](references/intent-detection.md) - Read when processing free-text feedback to extract actionable instructions
