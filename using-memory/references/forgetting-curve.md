# Forgetting Curve Reference

Understanding memory decay and retention.

## The Forgetting Curve

### Concept

Memory strength decays over time without reinforcement.

```
Strength
  100% |*
       | **
       |   ***
       |      ****
       |          *****
       |               ******
    0% |________________________
       0   1   2   3   4   5  Time
```

### Formula

```
Retention = e^(-t/S)

Where:
- t = time since creation
- S = stability (based on importance, reinforcement)
```

## Decay Rates

### Hourly Decay

**Half-life**: ~24 hours

**Use for**:
- Session context
- Temporary notes
- Working memory
- Quick references

**Behavior**:
| Time | Retention |
|------|-----------|
| 1 hour | 95% |
| 6 hours | 75% |
| 24 hours | 50% |
| 48 hours | 25% |
| 72 hours | 12% |

### Daily Decay

**Half-life**: ~7 days (168 hours)

**Use for**:
- Short-term learnings
- Recent events
- Active projects
- Current priorities

**Behavior**:
| Time | Retention |
|------|-----------|
| 1 day | 90% |
| 3 days | 70% |
| 7 days | 50% |
| 14 days | 25% |
| 30 days | 6% |

### Weekly Decay

**Half-life**: ~30 days (720 hours)

**Use for**:
- Medium-term knowledge
- Project context
- Recurring patterns
- Seasonal information

**Behavior**:
| Time | Retention |
|------|-----------|
| 1 week | 85% |
| 2 weeks | 72% |
| 30 days | 50% |
| 60 days | 25% |
| 90 days | 12% |

### Monthly Decay

**Half-life**: ~180 days (4320 hours)

**Use for**:
- Core knowledge
- Important learnings
- Stable preferences
- Long-term facts

**Behavior**:
| Time | Retention |
|------|-----------|
| 1 month | 90% |
| 3 months | 70% |
| 6 months | 50% |
| 1 year | 25% |
| 2 years | 6% |

## Importance and Decay

### Importance Mapping

| Importance | Recommended Decay | Rationale |
|------------|-------------------|-----------|
| 9-10 | Monthly | Critical, must persist |
| 7-8 | Weekly | Important, moderate retention |
| 5-6 | Daily | Standard, normal lifecycle |
| 3-4 | Daily | Minor, faster turnover |
| 1-2 | Hourly | Trivial, quick expiration |

### Combined Effect

```
Effective Decay = Base Decay × (1 + Importance/10)
```

Higher importance = slower effective decay

## Reinforcement

### Access Reinforcement

When memory is accessed:
- Strength increases
- Decay timer resets
- Importance may adjust

**Boost Formula**:
```
New Strength = Old Strength + (100 - Old Strength) × 0.3
```

### Validation Reinforcement

When memory is validated as correct:
- Larger strength boost
- Importance may increase
- Decay rate may slow

### Connection Reinforcement

When memory connects to others:
- Network effect
- Mutual reinforcement
- Longer retention

## Consolidation

### What It Is

Over time, memories consolidate:
- Similar memories merge
- Redundancy reduced
- Core knowledge strengthened

### Process

```
Day 1: Memory A (80%)
Day 1: Memory B (80%) [similar to A]
Day 7: Memory A+B consolidated (90%)
```

### Benefits

- Reduced storage
- Stronger retention
- Cleaner knowledge base

## Practical Guidelines

### Setting Decay Rates

| Memory Content | Decay Rate |
|----------------|------------|
| User preferences | Monthly |
| Business rules | Monthly |
| Recent events | Daily |
| Session context | Hourly |
| Procedures | Weekly/Monthly |
| One-time facts | Daily |

### When to Use Each Rate

**Hourly**: Information that's only relevant now
- Current query context
- Active filters
- Working calculations

**Daily**: Information relevant this week
- Recent discoveries
- Active project context
- Short-term learnings

**Weekly**: Information relevant this quarter
- Project knowledge
- Medium-term patterns
- Recurring events

**Monthly**: Information relevant long-term
- Core preferences
- Stable business rules
- Fundamental procedures

## Monitoring Decay

### Health Checks

Monitor for:
- Memories approaching expiration
- Important memories decaying
- Unreinforced knowledge

### Maintenance Actions

- Review aging memories
- Reinforce important ones
- Clean up expired
- Consolidate similar

## Edge Cases

### Never Forget

Some memories should never decay:
- Set importance = 10
- Set decay = monthly
- Regularly reinforce
- Mark as critical

### Immediate Forget

Some should expire immediately:
- Set importance = 1
- Set decay = hourly
- Don't reinforce
- Let expire naturally
