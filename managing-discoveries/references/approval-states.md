# Approval States Reference

Detailed guide to discovery approval states.

## State Definitions

### created

Initial state when discovery is generated.

**Characteristics:**
- Just created by agent
- Not yet evaluated
- May have draft content
- Timestamp recorded

**Transitions:**
- → pending_approval (always)

### pending_approval

Awaiting approval decision.

**Characteristics:**
- Content finalized
- Ready for review
- In approval queue
- May auto-approve

**Transitions:**
- → approved (passes criteria)
- → rejected (fails criteria)

### approved

Cleared for delivery to user.

**Characteristics:**
- Meets quality standards
- Appropriate for user
- Ready to send
- May be scheduled

**Transitions:**
- → delivered (sent to user)

### rejected

Not suitable for delivery.

**Characteristics:**
- Failed quality check
- Not appropriate
- Will not be sent
- May log reason

**Transitions:**
- (terminal state)

### delivered

Sent to user, awaiting response.

**Characteristics:**
- User can see it
- Awaiting feedback
- Tracking engagement
- May expire

**Transitions:**
- → reviewed (user responds)

### reviewed

User has provided feedback.

**Characteristics:**
- Feedback captured
- Learning extracted
- Lifecycle complete
- Archived

**Transitions:**
- (terminal state)

## Auto-Approval Rules

### Confidence-Based

| Confidence | Action |
|------------|--------|
| > 0.9 | Auto-approve |
| 0.7 - 0.9 | Queue for review |
| < 0.7 | Auto-reject or flag |

### Type-Based

| Discovery Type | Default |
|----------------|---------|
| Alert | Auto-approve if high confidence |
| Insight | Manual review |
| Summary | Auto-approve |
| FYI | Auto-approve |

### Watcher-Based

Watchers can configure:
- Auto-approve all findings
- Auto-approve above threshold
- Require manual approval
- Custom rules

## Rejection Reasons

### Content Quality

- `too_vague` - Unclear message
- `not_actionable` - No clear action
- `missing_context` - Insufficient detail
- `poorly_written` - Quality issues

### Relevance

- `duplicate` - Similar recent discovery
- `outdated` - Data too old
- `off_topic` - Not relevant to user
- `low_impact` - Not significant

### Accuracy

- `incorrect_data` - Wrong numbers
- `wrong_conclusion` - Bad analysis
- `methodology_error` - Flawed approach
- `missing_validation` - Unverified claims

## State Tracking

### Timestamps

Each state transition records:
- `entered_at` - When state was entered
- `exited_at` - When state was left
- `duration` - Time in state
- `actor` - Who/what triggered

### Metrics

Track state metrics:
- Time to approval
- Approval rate
- Rejection reasons
- Review latency

## Audit Trail

Maintain history of:
- All state changes
- Who made decisions
- Why (reason codes)
- When (timestamps)
