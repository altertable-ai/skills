# Task Types Reference

The MCP task-creation tool accepts three type values. All three run AI analysis driven by your natural-language `instructions` and create a discovery when the analysis produces a finding.

## anomaly_detection

AI detects outliers and unusual values in a chart's data.

**Target**: Chart slug

**Good for**: flagging sudden spikes, drops, or anomalies that break from the metric's recent pattern.

**Instructions example**:
> "Detect unusual spikes or drops in signup conversion rates."

## forecast

AI projects future values from a chart's data and flags divergence from expectations.

**Target**: Chart slug

**Good for**: projecting future values, setting expectations, and alerting when actuals diverge from the projection.

**Instructions example**:
> "Forecast next month's revenue. Flag if actuals diverge more than 15% from the forecast."

## monitor

Open-ended AI analysis of a chart or dashboard.

**Target**: Chart or dashboard slug

**Good for**: cross-metric analysis, narrative insights, or any analysis not captured by the other types.

**Instructions example**:
> "Analyze weekly trends across all metrics on this dashboard. Highlight correlations and anomalies."

## Choosing the Right Type

| Goal | Type |
|------|------|
| Find unexpected patterns in a metric | `anomaly_detection` |
| Project future values | `forecast` |
| Open-ended AI analysis of charts or dashboards | `monitor` |
