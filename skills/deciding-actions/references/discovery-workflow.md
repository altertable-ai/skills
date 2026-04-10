# Discovery Workflow Reference

End-to-end guide for discovery creation decisions.

## Discovery Lifecycle

```
Trigger → Evaluate → Decide → Create/Skip → Deliver → Learn
```

### 1. Trigger

What initiates a potential discovery:

| Trigger Type | Example |
|--------------|---------|
| User question | "How is revenue doing?" |
| Watcher alert | Threshold exceeded |
| Scheduled analysis | Daily summary |
| Pattern detection | Anomaly found |
| Follow-up | Continuing conversation |

### 2. Evaluate

Assess the situation:

| Assessment | Question |
|------------|----------|
| Relevance | Does user care about this? |
| Novelty | Is this new information? |
| Accuracy | Is the data correct? |
| Timing | Is now appropriate? |
| Format | What type of discovery? |

### 3. Decide

Make the create/skip decision:

```
Should I create a discovery?
│
├─ User explicitly asked? → YES, create
│
├─ Watcher triggered? → Check threshold, likely YES
│
├─ Duplicate detected? → NO, skip
│
├─ Adds value? → YES if adds value
│
└─ Just acknowledging? → FYI only if needed
```

### 4. Create or Skip

| Decision | Action |
|----------|--------|
| CREATE | Build discovery with proper type |
| SKIP | Respond without discovery |
| DEFER | Save for later (batching) |
| ESCALATE | Needs human review |

### 5. Deliver

How discovery reaches user:

| Channel | Use When |
|---------|----------|
| In-conversation | Direct response |
| Slack | Alert/notification |
| Email | Summary/digest |
| Dashboard | Persistent display |

### 6. Learn

After delivery:

| Feedback | Learning |
|----------|----------|
| Useful | Reinforce approach |
| Not useful | Adjust threshold |
| Already knew | Raise novelty bar |
| Wrong | Investigate and correct |

## Decision Matrix by Trigger

### User Question Trigger

```
User asks question
│
├─ Needs analysis?
│   ├─ YES → Select insight type → CREATE
│   └─ NO → Acknowledge → FYI or no discovery
│
├─ Asked before recently?
│   ├─ YES → Check if data changed
│   │   ├─ Changed → CREATE with update
│   │   └─ Same → Brief response, no discovery
│   └─ NO → CREATE
│
└─ Clear what they want?
    ├─ YES → Proceed with analysis
    └─ NO → Ask clarifying question
```

### Watcher Trigger

```
Watcher fires
│
├─ Above significance threshold?
│   ├─ YES → CREATE alert discovery
│   └─ NO → Log but don't alert
│
├─ Already alerted today?
│   ├─ YES → Skip unless escalation
│   └─ NO → CREATE
│
└─ User acknowledged previous?
    ├─ YES → Batch updates
    └─ NO → May remind
```

### Scheduled Trigger

```
Schedule fires
│
├─ Anything notable to report?
│   ├─ YES → CREATE summary
│   └─ NO → CREATE minimal summary or skip
│
├─ User preferences?
│   ├─ Always send → CREATE
│   └─ Only if notable → Check threshold
│
└─ Previous was read?
    ├─ YES → Continue schedule
    └─ NO → Consider reducing frequency
```

### Pattern Detection Trigger

```
Pattern detected
│
├─ Significant anomaly?
│   ├─ YES → CREATE insight
│   └─ NO → Log for context
│
├─ Seen this pattern before?
│   ├─ YES → Skip unless escalating
│   └─ NO → CREATE
│
└─ Actionable?
    ├─ YES → CREATE with recommendation
    └─ NO → Consider skipping
```

## Create vs Update vs New

### When to CREATE NEW

| Scenario | Action |
|----------|--------|
| First time finding | Create new |
| Significantly different data | Create new |
| Different time period | Create new |
| User explicitly asked | Create new |
| Contradicts previous | Create new with reference |

### When to UPDATE (if supported)

| Scenario | Action |
|----------|--------|
| Minor data refresh | Update existing |
| Same finding, newer data | Update existing |
| Correction to previous | Update with note |

### When to SKIP

| Scenario | Action |
|----------|--------|
| Exact duplicate | Skip entirely |
| Near duplicate | Skip, maybe acknowledge |
| No new value | Skip |
| Too soon after previous | Skip |
| User indicated not interested | Skip |

## Quality Gates

### Before Creating Any Discovery

| Gate | Pass Criteria |
|------|---------------|
| Novelty | Not duplicate of recent |
| Accuracy | Data verified correct |
| Relevance | Matches user interest |
| Actionable | User can act on it |
| Timing | Appropriate moment |
| Format | Right discovery type |

### Red Flags (Don't Create)

- Same finding in last hour
- User marked similar as not useful
- Data looks suspicious
- No clear value add
- Would overwhelm user

### Green Flags (Do Create)

- User explicitly asked
- Significant anomaly detected
- New insight discovered
- Scheduled delivery time
- Follows up on user interest

## Workflow by Discovery Type

### Insight Discovery Flow

```
1. Receive trigger (question/detection)
2. Determine insight type (funnel/semantic/SQL)
3. Run analysis
4. Verify results
5. Check for duplicates
6. Create if passes gates
7. Deliver appropriately
```

### Alert Discovery Flow

```
1. Watcher triggers
2. Verify threshold breach
3. Check if already alerted
4. Assess severity
5. Create if passes gates
6. Deliver via appropriate channel
7. Track acknowledgment
```

### Summary Discovery Flow

```
1. Schedule triggers
2. Gather period data
3. Identify notable items
4. Format summary
5. Create discovery
6. Deliver per schedule
```

### FYI Discovery Flow

```
1. Determine acknowledgment needed
2. Check if adds any value
3. Create minimal FYI if needed
4. Or respond without discovery
```

## Conversation Context

### Within Same Conversation

```
Message 1: User asks about revenue
→ Create insight discovery

Message 2: User says "break it down by region"
→ Create follow-up insight (not duplicate)

Message 3: User says "thanks"
→ FYI or no discovery (don't over-acknowledge)

Message 4: User asks "what about orders?"
→ Create new insight (different topic)
```

### Across Conversations

```
Yesterday: Created revenue insight
Today: User asks about revenue again
→ Check if data changed
→ If changed: Create with comparison
→ If same: Brief response, maybe skip discovery
```
