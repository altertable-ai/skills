---
name: managing-discoveries
compatibility: Altertable
description: Manages the discovery approval workflow and user feedback processing. Use when handling discovery reviews, understanding approval states, processing user feedback, or managing discovery lifecycle.
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

Use the `list_discoveries` tool to retrieve discoveries. Filter by status, data type, date range, or search query.

### Filtering by Status

Available statuses:
- `pending_review` - Awaiting user review
- `accepted` - User found it useful
- `rejected` - User rejected it
- `ignored` - User dismissed without feedback

### Filtering by Data Type

Filter discoveries by their data type to focus on specific categories:
- `Discoveries::NewInsight` - Data-driven insights with charts
- `Discoveries::FYI` - Informational updates (markdown content)
- `Discoveries::ConnectData` - Data connection prompts
- `Discoveries::NewSemanticModels` - Semantic model suggestions
- `Discoveries::WebAnalyticsEventsDetected` - Web analytics event findings

### Example Usage

```
# List pending insights
list_discoveries(status: "pending_review", data_type: "Discoveries::NewInsight")

# Search recent FYIs
list_discoveries(data_type: "Discoveries::FYI", created_after: "2024-01-01T00:00:00Z")
```

## Discovery Lifecycle

```
created → pending_approval → approved → delivered → reviewed
                ↓
            rejected
```

### State Flow

| State | Description | Next States |
|-------|-------------|-------------|
| `created` | Just generated | pending_approval |
| `pending_approval` | Awaiting review | approved, rejected |
| `approved` | Ready for delivery | delivered |
| `rejected` | Not suitable | (terminal) |
| `delivered` | Sent to user | reviewed |
| `reviewed` | User responded | (terminal) |

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

## Discovery Types

### Insight Discovery

Data-driven finding:
- Trend identified
- Anomaly detected
- Pattern found
- Metric change

### Alert Discovery

Time-sensitive notification:
- Threshold breach
- Error spike
- Data quality issue
- System event

### Summary Discovery

Periodic overview:
- Daily summary
- Weekly report
- Monthly review
- Trend analysis

### FYI Discovery

Informational update:
- Status change
- Completion notice
- Progress update
- Acknowledgment

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
