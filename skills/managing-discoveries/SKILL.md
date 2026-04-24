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
2. Inspect each discovery to get full details (title, summary, explanation, content, status)
3. Approve or reject based on your assessment
4. When feedback arrives, extract the user's intent and act on it

## Listing Discoveries

Use the Altertable MCP server to retrieve and act on discoveries:

- **List discoveries** -- filter by status, date range, or search query
- **View a discovery** -- inspect full details including explanation
- **Review a discovery** -- approve or reject

Available statuses for filtering: `pending`, `approved`, `rejected`.

## Reviewing a Discovery

When you need to review a discovery, follow these steps in order:

1. **Check factual accuracy** -- Does the title match the underlying data? Are the numbers correct?
2. **Verify it is not a duplicate** -- Search existing discoveries for overlapping findings before approving.
3. **Assess actionability** -- Can the reader do something with this information? If not, reject.
4. **Evaluate timing** -- Is this finding still current, or has the data gone stale?
5. **Decide**:
   - **Approve** if steps 1-4 all pass.
   - **Reject** if the analysis is wrong, duplicated, or not actionable.

For batch reviews, sort by priority first, then group by topic, and apply the same five-step check to each.

## Discovery Lifecycle

Discoveries flow through these states:

```
pending  -->  approved | rejected
```

| State      | Description             | Transitions                    |
| ---------- | ----------------------- | ------------------------------ |
| `pending`  | Awaiting review         | approve → approved; reject → rejected |
| `approved` | Approved                | reject → rejected              |
| `rejected` | Rejected                | approve → approved             |

Both `approve` and `reject` are reversible: an approved discovery can later be rejected, and a rejected one can later be approved.

## Processing User Feedback

Feedback on a discovery has two fields: a **reaction** (`approved` or `rejected`) and an optional **reason** (free-text, max 1000 chars).

When processing feedback:

1. **Note the reaction** -- approved or rejected.
2. **Parse the reason text** -- free-text comments often contain the actionable signal.
3. **Detect implicit preferences** -- does the feedback signal a topic the user cares more or less about?
4. **Take action** immediately on anything concrete in the reason.

When feedback includes free-text comments, parse them for:

- Direct requests ("show me this by region")
- Threshold adjustments ("only alert me if the change is over 10%")
- Topic preferences ("I don't care about this metric")
- Accuracy challenges ("the number is wrong because...")

## Common Pitfalls

- **Approving without checking for duplicates.** Always search existing discoveries before approving a new one.
- **Ignoring the free-text reason.** The `approved`/`rejected` reaction alone carries little information; the reason text is where the actionable signal usually lives.
- **Over-alerting.** If a user has rejected several discoveries on the same topic, stop surfacing similar findings until new data changes the picture.

## Reference Files

- [Review patterns](references/review-patterns.md) - Read when batch-reviewing multiple discoveries or designing a review strategy
- [Intent detection](references/intent-detection.md) - Read when processing free-text feedback to extract actionable instructions
