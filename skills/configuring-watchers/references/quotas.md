# Quota Management Reference

## How Quota Works

Each active watcher consumes quota based on its interval:

| Interval | Quota Cost |
|----------|------------|
| hourly | 5 |
| daily | 1 |
| weekly | 1 |
| monthly | 1 |

Only **idle** and **running** watchers consume quota. Paused and terminated watchers cost nothing.

```
Total Usage = sum of each active watcher's interval cost
Available   = Plan Limit - Total Usage
```

## Plan Limits

| Plan | Quota Limit |
|------|-------------|
| Trial | 100 |
| Starter | 50 |
| Pro | 200 |
| Enterprise | 500+ |

## Optimization Strategies

1. **Right-size intervals** -- downgrade hourly watchers to daily if same-day response is acceptable (saves 4 quota per watcher)
2. **Consolidate** -- use one dashboard watcher instead of multiple chart watchers on the same dashboard
3. **Pause unused** -- if a watcher has produced no discoveries in 30+ days, pause it
4. **Terminate old** -- remove watchers targeting deleted resources or metrics no longer relevant

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Quota exceeded on create | Pause or downgrade existing watchers to free quota |
| Unexpected high usage | List all watchers and check for duplicates or forgotten hourly watchers |
| Watcher stuck in running | Check if the target resource still exists |
