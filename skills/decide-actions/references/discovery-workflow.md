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
| User analysis | A verified, notable finding emerges while answering a question |
| Task alert | Threshold exceeded |
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
| Format | Is this a response, a saved Insight, or a discovery? |

### 3. Decide

Make the create/skip decision:

```
Should I create a discovery?
│
├─ User asked only for analysis? → Answer directly
│   └─ User wants a persistent chart? → Create an Insight, not a discovery
│
├─ Verified finding worth review or notification? → Continue
│
├─ Task triggered? → Check threshold, likely YES
│
├─ Duplicate detected? → NO, skip
│
├─ Adds value? → YES if adds value
│
└─ Just acknowledging? → Skip discovery
```

### 4. Create or Skip

| Decision | Action |
|----------|--------|
| CREATE | Create a finding backed by verified evidence |
| SKIP | Respond without discovery |
| DEFER | Save for later (batching) |
| ESCALATE | Needs human review |

### 5. Deliver

`create_discovery` always creates an inbox notification record. Its `notify` argument defaults to `true`, which also fans out through enabled delivery channels.

| Delivery | Use When |
|----------|----------|
| Inbox notification | Every discovery |
| Enabled external channels | The finding warrants attention and `notify` remains `true` |
| Inbox only | The finding is worth review but not interruption, so set `notify: false` |

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
│   ├─ YES → Select analysis type → Run and answer
│   └─ NO → Acknowledge without discovery
│
├─ Wants the analysis saved as a chart?
│   ├─ YES → Create an Insight after previewing it
│   └─ NO → Keep the result in the response
│
└─ Did analysis reveal a verified, notable finding worth review or notification?
    ├─ YES → Check duplicates, then create a discovery if it passes the gates
    └─ NO → Do not create a discovery
```

### Task Trigger

```
Task fires
│
├─ Above significance threshold?
│   ├─ YES → CREATE alert discovery
│   └─ NO → Log but don't alert
│
├─ Same finding already reported with no new value?
│   ├─ YES → Skip
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
│   ├─ YES → CREATE discovery
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

## Create vs Skip

### When to CREATE NEW

| Scenario | Action |
|----------|--------|
| First time finding | Create new |
| Significantly different data | Create new |
| Different period with a materially different finding | Create new |
| User explicitly asked to notify or review a verified finding | Create new |
| Contradicts previous | Create new with reference |

### When to SKIP

| Scenario | Action |
|----------|--------|
| Exact duplicate | Skip entirely |
| Near duplicate | Skip, maybe acknowledge |
| No new value | Skip |
| Recent and unchanged, with no new value | Skip |
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
| Format | A discovery is more appropriate than a response or saved Insight |

### Red Flags (Don't Create)

- Same finding with no material new context
- User marked similar as not useful
- Data looks suspicious
- No clear value add
- Would overwhelm user

### Green Flags (Do Create)

- User explicitly asked to notify or review a verified finding
- Significant anomaly detected
- New insight discovered
- Scheduled delivery time
- Follows up on user interest

## Workflow by Trigger

### Analysis Finding Flow

```
1. Receive trigger (question/detection)
2. Determine analysis type (funnel/semantic/SQL)
3. Run analysis
4. Verify results
5. Answer the question
6. Save an Insight only when persistence is requested
7. If a notable finding warrants review or notification, check duplicates and create a discovery
```

### Alert Discovery Flow

```
1. Task triggers
2. Verify threshold breach
3. Check if already alerted
4. Assess severity
5. Create if passes gates
6. Choose whether `notify` should fan out through enabled channels
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

### Acknowledgement Flow

```
1. Determine acknowledgment needed
2. Check if adds any value
3. Respond without discovery
```

## Conversation Context

### Within Same Conversation

```
Message 1: User asks about revenue
→ Analyze and answer

Message 2: User says "break it down by region"
→ Analyze and answer; save an Insight only if persistence is requested

Message 3: User says "thanks"
→ Respond without discovery (don't over-acknowledge)

Message 4: User asks "what about orders?"
→ Analyze and answer the different question
```

### Across Conversations

```
Yesterday: Created revenue insight
Today: User asks about revenue again
→ Check if data changed
→ Answer with the comparison
→ Create a discovery only if the changed result is a verified, notable finding worth review or notification
```
