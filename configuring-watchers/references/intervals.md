# Intervals Guide

Choosing and configuring watcher intervals.

## Interval Overview

| Interval | Frequency | Quota | Response Time |
|----------|-----------|-------|---------------|
| REALTIME | Continuous | 10 | Immediate |
| HOURLY | Every hour | 5 | Within hour |
| DAILY | Once per day | 1 | Within 24h |
| WEEKLY | Once per week | 1 | Within 7d |
| MONTHLY | Once per month | 1 | Within 30d |

## REALTIME

Continuous monitoring with immediate alerting.

### Characteristics
- Highest quota cost (10)
- Fastest response
- Continuous analysis

### Best For
- Critical business metrics
- Time-sensitive alerts
- Live dashboards
- Operational monitoring

### Examples
- Payment failure rates
- Site availability
- Critical error rates
- Real-time fraud detection

### Considerations
- High quota consumption
- Use sparingly
- Only for truly time-critical metrics

## HOURLY

Hourly monitoring for fast-changing metrics.

### Characteristics
- High quota cost (5)
- Quick response (< 1 hour)
- Regular updates

### Best For
- Fast-moving metrics
- Intraday patterns
- Operational KPIs
- Data freshness checks

### Examples
- Hourly revenue tracking
- API performance
- Traffic spikes
- Data pipeline status

### Considerations
- Balance with quota
- Consider if daily is sufficient
- Good for business hours monitoring

## DAILY

Standard daily monitoring - most common choice.

### Characteristics
- Low quota cost (1)
- Balanced response
- Comprehensive analysis

### Best For
- Most business metrics
- Standard KPIs
- Growth metrics
- Quality checks

### Examples
- Daily active users
- Daily revenue
- Conversion rates
- Engagement metrics

### Considerations
- Default choice for most cases
- Good for trend analysis
- Sufficient for most needs

## WEEKLY

Weekly summary and trend analysis.

### Characteristics
- Low quota cost (1)
- Strategic view
- Trend-focused

### Best For
- Week-over-week analysis
- Slower-moving metrics
- Strategic KPIs
- Summary reports

### Examples
- Weekly retention
- Growth rates
- Market trends
- Competitive metrics

### Considerations
- Good for strategic metrics
- Complements daily watchers
- Less urgent findings

## MONTHLY

Monthly strategic analysis.

### Characteristics
- Low quota cost (1)
- Long-term view
- Strategic insights

### Best For
- Monthly trends
- Long-term patterns
- Strategic metrics
- Executive reporting

### Examples
- Monthly active users
- MRR/ARR trends
- Market share
- Long-term retention

## Selection Framework

### Decision Tree

```
Is immediate action required?
├── Yes → REALTIME
└── No
    ├── Does it change hourly?
    │   ├── Yes → HOURLY
    │   └── No
    │       ├── Does daily analysis help?
    │       │   ├── Yes → DAILY
    │       │   └── No → WEEKLY or MONTHLY
```

### By Metric Type

| Metric Type | Recommended |
|-------------|-------------|
| Operational | REALTIME/HOURLY |
| Revenue | DAILY |
| Engagement | DAILY |
| Growth | DAILY/WEEKLY |
| Strategic | WEEKLY/MONTHLY |
| Quality | HOURLY/DAILY |

### By Urgency

| Response Need | Interval |
|---------------|----------|
| Immediate | REALTIME |
| Same day | HOURLY |
| Next day | DAILY |
| This week | WEEKLY |
| This month | MONTHLY |

## Interval Patterns

### Layered Monitoring

Combine intervals for comprehensive coverage:

```
Critical Alert → REALTIME
Operational → HOURLY
Business Metrics → DAILY
Strategic Review → WEEKLY
```

### Time-Zone Considerations

- DAILY runs at consistent time (UTC)
- Consider business hours
- Align with report cadence

### Peak vs Off-Peak

Some metrics need different coverage:
- Business hours: More frequent
- Off hours: Less frequent
- Consider variable intervals

## Migration Patterns

### Upgrading Interval

When more urgency needed:
1. Verify quota available
2. Update interval
3. Monitor for noise
4. Adjust instructions

### Downgrading Interval

When less urgency needed:
1. Review discovery history
2. Confirm slower is acceptable
3. Update interval
4. Free up quota

## Best Practices

### Start Conservative

- Begin with DAILY
- Upgrade if needed
- Don't over-monitor

### Match Business Rhythm

- Align with decision cycles
- Consider reporting schedules
- Match team capacity

### Balance Coverage

- Not everything needs REALTIME
- Distribute quota wisely
- Focus on actionable metrics
