# Task Types Reference

`create_task` accepts three task types. Every call requires `type`, `target_slugs`, and `cron_expression`. `instructions` is optional.

## `anomaly_detection`

Detects outliers and unusual values in an Insight. Pass exactly one Insight slug.

```yaml
type: anomaly_detection
target_slugs: [INSIGHT-SLUG]
cron_expression: "0 * * * *"
instructions: Detect unusual spikes or drops in signup conversion.
```

## `forecast`

Projects future values from an Insight. Pass exactly one Insight slug.

```yaml
type: forecast
target_slugs: [INSIGHT-SLUG]
cron_expression: "0 0 * * 1"
instructions: Forecast next month's revenue and flag material divergence.
```

## `ask`

Runs open-ended scheduled analysis. Pass zero or more entity slugs, including Insights or Dashboards.

```yaml
type: ask
target_slugs: [DASHBOARD-SLUG]
cron_expression: "0 9 * * 1"
instructions: Analyze weekly trends and highlight correlations or anomalies.
```

Use `target_slugs: []` when the instructions do not need entity context.
