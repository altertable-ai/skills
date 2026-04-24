# Task Types Reference

The MCP task-creation tool accepts three type values. All three run AI analysis driven by your natural-language `instructions` and create a discovery when the analysis produces a finding.

## anomaly_detection

AI detects outliers and unusual values in an Insight's data.

**Target**: Insight slug

**Good for**: flagging sudden spikes, drops, or anomalies that break from the metric's recent pattern.

**Instructions example**:
> "Detect unusual spikes or drops in signup conversion rates."

## forecast

AI projects future values from an Insight's data and flags divergence from expectations.

**Target**: Insight slug

**Good for**: projecting future values, setting expectations, and alerting when actuals diverge from the projection.

**Instructions example**:
> "Forecast next month's revenue. Flag if actuals diverge more than 15% from the forecast."

## monitor

Open-ended AI analysis of an Insight or Dashboard.

**Target**: Insight or Dashboard slug

**Good for**: cross-metric analysis, narrative insights, or any analysis not captured by the other types.

**Instructions example**:
> "Analyze weekly trends across all metrics on this dashboard. Highlight correlations and anomalies."

## Choosing the Right Type

| Goal | Type |
|------|------|
| Find unexpected patterns in a metric | `anomaly_detection` |
| Project future values | `forecast` |
| Open-ended AI analysis of Insights or Dashboards | `monitor` |
