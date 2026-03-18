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

A discovery is an insight that:
1. Gets created by agents or watchers
2. Flows through approval workflow
3. Reaches users for review
4. Captures user feedback

## When to Use This Skill

- Handling discovery reviews
- Understanding approval states
- Processing user feedback
- Managing discovery lifecycle
- Detecting user intent from feedback

## Listing Discoveries

Use the `list_discoveries` tool to retrieve discoveries. Filter by status, date range, or search query.

### Filtering by Status

Available statuses:
- `pending_review` - Approved by admin, awaiting organization action
- `accepted` - Accepted by organization
- `rejected` - Rejected by organization
- `ignored` - Ignored by organization

### Example Usage

```
# List pending discoveries awaiting action
list_discoveries(status: "pending_review")

# List discoveries by state if needed
list_discoveries(status: "accepted")
list_discoveries(status: "rejected")

# Search recent discoveries
list_discoveries(created_after: "2024-01-01T00:00:00Z")
```

## Discovery Lifecycle

| State | Description | Next States |
|-------|-------------|-------------|
| `pending_visualization_generation` | Waiting for chart to be generated | pending_admin_review |
| `pending_admin_review` | Awaiting admin approval | pending_review, admin_rejected |
| `pending_review` | Approved by admin, awaiting organization action | accepted, rejected, ignored |
| `accepted` | Accepted by organization | (terminal) |
| `rejected` | Rejected by organization | (terminal) |
| `ignored` | Ignored by organization | (terminal) |
| `admin_rejected` | Admin rejected before organization sees it | (terminal) |

## Approval Workflow

### Automatic Approval

Some discoveries auto-approve based on:
- Watcher configuration
- Confidence score
- Discovery type
- Organization settings

### Manual Approval

High-stakes discoveries require manual review:
- Large impact findings
- Anomaly alerts
- Strategic insights

### Rejection Criteria

Reject discoveries that are:
- Low quality or vague
- Duplicate of recent finding
- Not actionable
- Incorrect analysis

## User Feedback

### Feedback Types

| Type | Meaning | Agent Action |
|------|---------|--------------|
| `useful` | Valuable insight | Reinforce pattern |
| `not_useful` | No value | Learn to avoid |
| `already_knew` | Known information | Reduce priority |
| `incorrect` | Wrong analysis | Investigate error |
| `follow_up` | Wants more detail | Continue analysis |

### Intent Detection

Analyze feedback text for:
- Explicit instructions
- Implicit preferences
- Context clues
- Emotional signals

### Learning from Feedback

Feedback informs:
- Future analysis focus
- Presentation style
- Threshold calibration
- Topic priorities

## Review Patterns

### Quick Review

For routine discoveries:
1. Check headline accuracy
2. Verify data support
3. Assess actionability
4. Approve or reject

### Deep Review

For complex findings:
1. Validate methodology
2. Check data sources
3. Verify conclusions
4. Consider alternatives
5. Assess impact

### Batch Review

For multiple discoveries:
1. Sort by priority
2. Group by topic
3. Review systematically
4. Apply consistent criteria

## Quality Criteria

### Good Discovery

- Clear headline
- Supported by data
- Actionable insight
- Appropriate urgency
- Proper context

### Poor Discovery

- Vague language
- Unsupported claims
- Not actionable
- Wrong urgency level
- Missing context

## Workflow Best Practices

### Creating Discoveries

- Be specific in headlines
- Include relevant data
- Set appropriate priority
- Provide clear context
- Make actionable

### Reviewing Discoveries

- Check data accuracy
- Verify relevance
- Assess timing
- Consider audience
- Ensure actionability

### Processing Feedback

- Acknowledge promptly
- Extract learnings
- Update preferences
- Adjust future analysis
- Close the loop

## Common Pitfalls

- Approving low-quality discoveries
- Ignoring user feedback
- Missing intent signals
- Over-alerting users
- Under-explaining findings
- Not learning from rejections

## Reference Files

- [Approval states](references/approval-states.md)
- [Review patterns](references/review-patterns.md)
- [Intent detection](references/intent-detection.md)
