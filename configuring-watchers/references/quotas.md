# Quota Management Reference

Managing watcher quotas effectively.

## Quota Fundamentals

### How Quota Works

Each watcher consumes quota based on interval:

| Interval | Quota Units |
|----------|-------------|
| REALTIME | 10 |
| HOURLY | 5 |
| DAILY | 1 |
| WEEKLY | 1 |
| MONTHLY | 1 |

### Plan Limits

Quota limits vary by plan:

| Plan | Quota Limit |
|------|-------------|
| Trial | 100 |
| Starter | 50 |
| Pro | 200 |
| Enterprise | 500+ |

### Calculating Usage

```
Total Usage = Σ(Watcher Interval Quota)
```

Example calculation:
```
Watchers:
- 1 × REALTIME = 10
- 3 × HOURLY = 15
- 10 × DAILY = 10
- 5 × WEEKLY = 5
──────────────────
Total: 40 units
```

## Checking Quota Status

### Current Usage

Sum quota from all active watchers:
- Running: Full quota
- Idle: Full quota
- Paused: 0 quota
- Terminated: 0 quota

### Available Quota

```
Available = Plan Limit - Current Usage
```

## Quota Optimization

### Strategy 1: Right-Size Intervals

Review if current intervals are necessary:

| Question | Action |
|----------|--------|
| Needs immediate response? | REALTIME |
| Hour-level matters? | HOURLY |
| Day-level sufficient? | DAILY |
| Week/month trends? | WEEKLY/MONTHLY |

### Strategy 2: Consolidate Watchers

Instead of multiple specific watchers:
- Use one dashboard watcher
- Cover multiple metrics
- Reduce total quota

### Strategy 3: Pause Unused

Identify and pause watchers:
- No discoveries in 30+ days
- Metrics no longer relevant
- Duplicate coverage

### Strategy 4: Terminate Old

Remove watchers that:
- Target deleted resources
- No longer needed
- Have been paused > 90 days

## Quota Allocation

### Priority Framework

Allocate quota by business priority:

| Priority | % of Quota | Interval |
|----------|------------|----------|
| Critical | 20% | REALTIME |
| Important | 30% | HOURLY/DAILY |
| Standard | 40% | DAILY |
| Nice-to-have | 10% | WEEKLY |

### By Function

| Function | Recommended |
|----------|-------------|
| Revenue | 15-20% |
| Operations | 20-25% |
| Growth | 15-20% |
| Quality | 10-15% |
| Strategic | 10-15% |
| Reserve | 10-15% |

### Reserve Buffer

Always keep 10-15% quota free:
- Emergency monitoring
- New initiatives
- Testing new watchers

## Troubleshooting

### Quota Exceeded

When over quota:
1. Identify lowest-priority watchers
2. Pause or downgrade intervals
3. Wait for paused to take effect
4. Review quota usage

### Cannot Create Watcher

If quota insufficient:
1. Check current usage
2. Review plan limit
3. Free up quota or upgrade

### Unexpected Usage

If usage seems wrong:
1. List all watchers
2. Check for duplicates
3. Verify intervals
4. Look for stuck watchers

## Monitoring Quota

### Regular Review

Monthly quota review:
1. List all watchers
2. Calculate usage
3. Review discovery output
4. Optimize as needed

### Alerts

Consider alerts for:
- Quota > 80% used
- New watcher would exceed
- Watchers with no output

## Best Practices

### Document Watchers

Track for each watcher:
- Purpose
- Owner
- Priority
- Last useful discovery

### Review Quarterly

Every quarter:
- Audit all watchers
- Remove unused
- Rebalance quota
- Align with priorities

### Budget for Growth

Plan quota for:
- New dashboards
- New team members
- New initiatives
- Experiments

### Avoid Quota Hoarding

Don't:
- Keep paused watchers indefinitely
- Hold quota "just in case"
- Create watchers without purpose

Do:
- Terminate unused watchers
- Free quota for active use
- Create watchers as needed
