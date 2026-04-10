# Intent Detection Reference

Detecting user intent from feedback and interactions.

## Intent Categories

### Positive Intents

| Intent | Signals | Response |
|--------|---------|----------|
| `wants_more` | "Tell me more", "Interesting" | Expand analysis |
| `agrees` | "Good", "Useful", "Thanks" | Reinforce approach |
| `wants_similar` | "More like this" | Note preference |
| `understands` | "Got it", "Makes sense" | Continue pattern |

### Negative Intents

| Intent | Signals | Response |
|--------|---------|----------|
| `not_relevant` | "Don't care", "Not for me" | Adjust targeting |
| `already_knew` | "Old news", "Known" | Increase threshold |
| `too_frequent` | "Too many", "Stop" | Reduce frequency |
| `incorrect` | "Wrong", "That's not right" | Investigate error |

### Action Intents

| Intent | Signals | Response |
|--------|---------|----------|
| `follow_up` | "Why?", "How?", "Details" | Provide more info |
| `delegate` | "Tell team", "Share" | Route to others |
| `schedule` | "Remind me", "Later" | Set reminder |
| `investigate` | "Dig deeper", "Analyze" | Perform analysis |

### Preference Intents

| Intent | Signals | Response |
|--------|---------|----------|
| `format_change` | "Shorter", "More detail" | Adjust format |
| `timing_change` | "Earlier", "Morning" | Adjust timing |
| `topic_focus` | "Focus on X", "Less Y" | Adjust topics |
| `threshold_change` | "Bigger changes only" | Adjust thresholds |

## Signal Detection

### Explicit Signals

Direct statements of preference:
- "I want..."
- "Don't show me..."
- "Always tell me about..."
- "Never..."

### Implicit Signals

Behavioral indicators:
- Quick dismiss = not relevant
- Long engagement = interested
- No action = unclear value
- Immediate action = high value

### Contextual Signals

Consider context:
- Time of day feedback given
- Device used
- Response speed
- Historical patterns

## Text Analysis

### Sentiment Markers

| Positive | Negative | Neutral |
|----------|----------|---------|
| Great | Wrong | OK |
| Thanks | Stop | Got it |
| Useful | Don't | Fine |
| Interesting | Enough | Noted |

### Action Words

| Request | Rejection | Modification |
|---------|-----------|--------------|
| Tell me | Stop | Less/more |
| Show | Hide | Different |
| Analyze | Remove | Change |
| Find | Skip | Adjust |

### Intensity Markers

- Strong: "Always", "Never", "Very"
- Moderate: "Usually", "Sometimes", "Quite"
- Weak: "Maybe", "Perhaps", "Slightly"

## Response Strategies

### For Positive Intent

1. Acknowledge appreciation
2. Note what worked
3. Continue similar approach
4. Offer to expand

### For Negative Intent

1. Acknowledge feedback
2. Understand specific issue
3. Explain or apologize
4. Adjust behavior

### For Action Intent

1. Confirm understanding
2. Take requested action
3. Report back
4. Offer next steps

### For Preference Intent

1. Confirm preference
2. Record in memory
3. Apply immediately
4. Confirm change

## Learning from Intent

### Short-term Adjustments

- Immediate response
- Session-level changes
- Quick corrections

### Long-term Learning

- Pattern recognition
- Preference modeling
- Threshold calibration
- Topic weighting

### Memory Integration

Store learnings as:
- Episodic memories (specific events)
- Semantic memories (user preferences)
- Procedural memories (how to respond)

## Edge Cases

### Ambiguous Feedback

When unclear:
1. Ask for clarification
2. Default to safe option
3. Note ambiguity
4. Watch for patterns

### Contradictory Feedback

When conflicting:
1. Note contradiction
2. Ask about context
3. Weight recent higher
4. Consider situation

### No Feedback

When silent:
1. Don't assume
2. Watch behavior
3. Occasionally ask
4. Default to neutral
