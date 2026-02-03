# Duplicate Prevention Reference

Strategies for avoiding redundant discoveries.

## Why Prevent Duplicates

- Avoid alert fatigue
- Maintain user trust
- Keep signal-to-noise high
- Respect user attention
- Ensure quality over quantity

## Duplicate Detection Framework

### Same Discovery Check

Before creating, verify:

| Dimension | Check |
|-----------|-------|
| Topic | Same subject matter? |
| Metric | Same data point? |
| Time range | Same period analyzed? |
| Finding | Same conclusion? |
| Recency | Created recently? |

### Similarity Scoring

| Factor | Weight | Same = Skip |
|--------|--------|-------------|
| Same metric | 30% | > 25% |
| Same time range | 20% | > 15% |
| Same finding | 30% | > 25% |
| Same dimensions | 10% | > 8% |
| < 24 hours ago | 10% | > 8% |
| **Total** | **100%** | **> 80%** |

If similarity > 80%, likely duplicate.

## Time-Based Rules

### Recency Windows

| Time Since Last | Same Topic Rule |
|-----------------|-----------------|
| 0-1 hour | Always skip (unless contradicts) |
| 1-4 hours | Skip unless major new info |
| 4-24 hours | Skip if same finding |
| 1-3 days | Create if adds value |
| 3-7 days | Create with context |
| > 7 days | Treat as new |

### Refresh Scenarios

When to create despite recency:

| Scenario | Action |
|----------|--------|
| Data significantly changed | Create with comparison |
| User explicitly asked again | Create fresh |
| Previous was wrong | Create correction |
| New dimension adds value | Create enhanced |
| Contradicts previous | Create with explanation |

## Content-Based Rules

### Exact Duplicate

```
Previous: "Revenue dropped 15% yesterday"
New:      "Revenue dropped 15% yesterday"
→ SKIP (exact same)
```

### Near Duplicate

```
Previous: "Revenue dropped 15% yesterday"
New:      "Revenue decreased 15% compared to the day before"
→ SKIP (same meaning)
```

### Valuable Update

```
Previous: "Revenue dropped 15% yesterday"
New:      "Revenue dropped 15% yesterday, driven by 40% decline in mobile"
→ CREATE (adds new insight)
```

### Different Finding

```
Previous: "Revenue dropped 15% yesterday"
New:      "Revenue recovered today, up 10%"
→ CREATE (new information)
```

## Before Creating Checklist

Run through before every discovery:

### Step 1: Search Memory

```
Search for:
- Same metric name
- Same topic keywords
- Same time period
- Recent discoveries (24h)
```

### Step 2: Compare Findings

| Question | If Yes |
|----------|--------|
| Exact same finding? | SKIP |
| Same finding, minor wording diff? | SKIP |
| Same topic, different finding? | CREATE |
| Same metric, different period? | CREATE |
| Contradicts previous? | CREATE + reference |

### Step 3: Assess Value Add

| Question | If No |
|----------|-------|
| Does this add new information? | SKIP |
| Would user want to know this? | SKIP |
| Is this actionable? | Consider SKIP |
| Is timing appropriate? | SKIP |

## Discovery Types & Duplicates

### Insight Discoveries

Higher bar for uniqueness:
- Must provide new analysis
- Must add actionable value
- Must not repeat recent findings

### Alert Discoveries

Can repeat if:
- Condition still active
- User hasn't acknowledged
- Severity increased

Should not repeat if:
- Already alerted today
- User marked as seen
- Condition resolved

### Summary Discoveries

Scheduled, so less duplicate concern:
- Daily summary = 1 per day
- Weekly summary = 1 per week
- Avoid ad-hoc duplicates of scheduled

### FYI Discoveries

Rarely duplicate concern:
- Acknowledgments are contextual
- Each conversation is unique
- Don't over-acknowledge

## Anti-Patterns to Avoid

### Parroting

```
User: "Revenue is down"
Bad:  "I see that revenue is down" (adds nothing)
Good: "Revenue is down 15%, primarily from mobile" (adds insight)
```

### Trivial Variations

```
Discovery 1: "Orders increased 10%"
Discovery 2: "There was a 10% increase in orders"
→ These are duplicates
```

### Over-Reporting

```
10:00 - "Metric X changed"
10:15 - "Update on metric X"
10:30 - "Another update on metric X"
→ Batch into single discovery
```

### Missing Context

```
Discovery 1: "Revenue up 15%"
Discovery 2: "Revenue up 15%" (next day, no reference)
→ Should reference "continued trend" or "still elevated"
```

## Implementation Patterns

### Memory Search Before Create

```ruby
# Pseudo-code
def should_create_discovery?(new_finding)
  recent = search_memory(
    topic: new_finding.topic,
    time_range: 24.hours.ago..Time.now
  )

  return false if exact_match?(recent, new_finding)
  return false if semantic_match?(recent, new_finding) > 0.8
  return true
end
```

### Deduplication Tags

Use tags to track:
- `topic:revenue`
- `metric:orders_count`
- `period:2024-01-15`
- `finding_hash:abc123`

### Finding Hash

Create hash of finding essence:
```
hash = MD5(metric + time_range + finding_type + key_value)
```

Check hash before creating.

## Edge Cases

### User Asks Same Question

```
User asks again → Create fresh response
(They may want confirmation or missed previous)
```

### Scheduled vs Ad-hoc

```
Scheduled summary exists
User asks for same data
→ Create ad-hoc (different context)
```

### Error Correction

```
Previous discovery was wrong
→ Create correction, reference previous
→ Mark previous as superseded
```
