# Forgetting Curve Reference

## How It Works

Memories decay over time without reinforcement, following the Ebbinghaus forgetting curve.

**Formula:** `Relevance = e^(-t/S) × (importance / 10)`

Where:
- `t` = hours since last access
- `S` = stability (based on importance and access count)

## Decay Rates

| Rate | Half-life | Use For |
|------|-----------|---------|
| Daily | ~24h | Session context, temporary notes |
| Weekly | ~168h | Short-term patterns (default) |
| Monthly | ~720h | Core knowledge, stable facts |

## Importance Effect

Higher importance = slower decay + higher initial relevance.

| Importance | Decay Speed | Example |
|------------|-------------|---------|
| 9-10 | Very slow | Critical business rules |
| 7-8 | Slow | Confirmed patterns |
| 5-6 | Normal | Useful but unconfirmed |
| 1-4 | Fast | Minor details |

## Reinforcement

Memories get stronger when accessed or validated.

**Access reinforcement:**
- Each search that returns a memory increases its strength
- Decay timer resets
- Memory stays relevant longer

**Validation reinforcement:**
- When memory is confirmed correct, larger strength boost
- Importance may increase
- Decay rate may slow

## Relevance Scores

| Score | Meaning |
|-------|---------|
| 0.8-1.0 | Highly relevant, just accessed or very important |
| 0.5-0.8 | Relevant, recent or frequently accessed |
| 0.2-0.5 | Moderately relevant, starting to decay |
| 0.0-0.2 | Low relevance, candidate for removal |

## Garbage Collection

Memories below relevance threshold (0.1) are automatically removed.

- Only AI-authored memories are garbage collected
- User-created memories are never auto-deleted
- Runs daily during off-peak hours

## Best Practices

**To keep memories alive:**
- Search for them regularly (reinforcement)
- Set appropriate importance (higher = slower decay)
- Use monthly decay for core knowledge

**To let memories fade:**
- Set low importance
- Use daily decay
- Don't search for them
