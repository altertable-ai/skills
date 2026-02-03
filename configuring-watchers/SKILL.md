---
name: configuring-watchers
compatibility: Altertable
description: Configures monitoring agents (watchers) with intervals and targets. Use when setting up automated monitoring, scheduled analysis, alerts, or autonomous data observation.
---

# Configuring Watchers

## Quick Start

A watcher is an autonomous agent that:
1. Monitors a target (chart, dashboard, connection)
2. Runs at specified intervals
3. Creates discoveries when findings occur

## When to Use This Skill

- Setting up automated monitoring
- Creating scheduled analysis
- Configuring alerts
- Enabling proactive insights
- Managing watcher quotas

## Watcher Types

| Type | Target | Purpose |
|------|--------|---------|
| PlatformWatcher | Organization | Org-wide monitoring |
| ChartWatcher | Chart | Monitor specific chart |
| DashboardWatcher | Dashboard | Monitor dashboard metrics |
| ConnectionWatcher | Connection | Monitor data source |
| SemanticSourceWatcher | Source | Monitor semantic model |
| SegmentWatcher | Segment | Monitor user segment |
| EventsActivityWatcher | Events | Monitor event patterns |
| WebAnalyticsWatcher | Web Data | Monitor web traffic |

## Intervals

| Interval | Quota | Use Case |
|----------|-------|----------|
| REALTIME | 10 | Critical metrics, live dashboards |
| HOURLY | 5 | Time-sensitive metrics |
| DAILY | 1 | Standard monitoring |
| WEEKLY | 1 | Trends, summaries |
| MONTHLY | 1 | Long-term patterns |

### Choosing Intervals

- **REALTIME**: When immediate awareness matters
- **HOURLY**: For fast-changing metrics
- **DAILY**: Most common, balanced approach
- **WEEKLY**: For slower-moving trends
- **MONTHLY**: For strategic metrics

## Quota System

Each organization has a watcher quota limit based on their plan.

### Quota Calculation

```
Total Quota Used = Σ(Active Watcher × Interval Quota)
```

Example:
- 2 REALTIME watchers: 2 × 10 = 20
- 3 HOURLY watchers: 3 × 5 = 15
- 5 DAILY watchers: 5 × 1 = 5
- Total: 40 quota units

### Quota Status

| State | Quota Impact |
|-------|--------------|
| Running | Full quota |
| Idle | Full quota |
| Paused | 0 quota |
| Terminated | 0 quota |

## Watcher States

```
idle → running → idle (normal cycle)
idle → paused (user paused)
paused → running (resumed)
any → terminated (permanently stopped)
```

### State Descriptions

| State | Description |
|-------|-------------|
| `idle` | Ready for next run |
| `running` | Currently executing |
| `paused` | Temporarily stopped |
| `terminated` | Permanently disabled |

## Configuration Workflow

### Step 1: Choose Target

What should be monitored?
- A specific chart
- A dashboard
- A data connection
- A semantic source

### Step 2: Set Interval

How often should it run?
- Consider data freshness
- Balance with quota
- Match business needs

### Step 3: Add Instructions

What should it look for?
- Specific patterns
- Thresholds
- Comparisons
- Anomalies

### Step 4: Review Quota

Check quota availability:
- Current usage
- Planned addition
- Remaining capacity

## Watcher Instructions

### Writing Effective Instructions

Be specific about:
- What to analyze
- What patterns matter
- When to create discoveries

### Example Instructions

**For ChartWatcher:**
```
Monitor weekly revenue trends. Create a discovery if:
- Revenue drops more than 10% week-over-week
- Revenue exceeds forecast by 20%
- Unusual patterns in regional breakdown
```

**For ConnectionWatcher:**
```
Monitor data freshness and quality:
- Alert if data is more than 2 hours stale
- Check for unusual NULL rates
- Monitor table row counts
```

**For WebAnalyticsWatcher:**
```
Analyze weekly web traffic patterns:
- Identify top growing pages
- Flag significant traffic changes
- Note unusual referrer patterns
```

## Common Patterns

### Revenue Monitoring

```yaml
type: ChartWatcher
target: revenue-chart-slug
interval: DAILY
instructions: |
  Monitor daily revenue and flag:
  - Day-over-day drops > 15%
  - Week-over-week growth > 25%
  - Unusual hourly patterns
```

### User Engagement

```yaml
type: SemanticSourceWatcher
target: events-source
interval: WEEKLY
instructions: |
  Analyze weekly engagement trends:
  - Active user changes
  - Feature adoption rates
  - Session duration trends
```

### Data Quality

```yaml
type: ConnectionWatcher
target: warehouse-connection
interval: HOURLY
instructions: |
  Monitor data pipeline health:
  - Data freshness (alert if > 1hr stale)
  - Row count anomalies (±50%)
  - Schema changes
```

## Best Practices

### Interval Selection

- Start with DAILY, adjust as needed
- REALTIME only for critical alerts
- Balance coverage with quota

### Instructions Clarity

- Be specific about thresholds
- Define what "significant" means
- Give context on business impact

### Quota Management

- Review usage regularly
- Pause unnecessary watchers
- Consolidate where possible

### Discovery Quality

- Configure meaningful watchers
- Avoid alert fatigue
- Focus on actionable insights

## Common Pitfalls

- Using REALTIME for non-critical metrics
- Vague instructions leading to noise
- Exceeding quota with too many watchers
- Not reviewing watcher effectiveness
- Missing important metrics

## Reference Files

- [Watcher types](references/watcher-types.md)
- [Intervals guide](references/intervals.md)
- [Quota management](references/quotas.md)
