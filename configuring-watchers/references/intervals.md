# Intervals Guide

## Selection Framework

```
Is immediate action required within the hour?
  Yes -> hourly
  No -> Does the metric change meaningfully within a day?
    Yes -> daily
    No -> Is this a weekly or monthly trend?
      Weekly cadence -> weekly
      Monthly cadence -> monthly
```

## By Metric Type

| Metric Type | Recommended | Why |
|-------------|-------------|-----|
| Operational (errors, pipeline health) | hourly | Fast feedback loop needed |
| Revenue, conversion, engagement | daily | Changes meaningfully day-to-day |
| Growth, retention, strategic KPIs | weekly | Week-over-week is the natural cadence |
| MRR/ARR, market trends | monthly | Only meaningful at monthly scale |

## Layered Monitoring

Combine intervals for comprehensive coverage on the same domain:

```
Pipeline health     -> hourly (data freshness, errors)
Business metrics    -> daily (revenue, conversions)
Strategic review    -> weekly (growth, retention)
```

## Changing Intervals

- **Upgrade** (daily -> hourly): verify quota is available first, then monitor for noise -- more frequent runs may produce more discoveries
- **Downgrade** (hourly -> daily): review recent discovery history to confirm nothing time-sensitive will be missed
