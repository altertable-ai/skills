# Watcher Types Reference

Detailed capabilities and examples for each watcher type.

## chart

Monitors a specific chart for metric changes.

**Target**: Chart slug
**Default interval**: daily

**Capabilities**: Access chart data, analyze trends, compare periods, detect threshold breaches.

**Example**:
```
create_watcher(
  type: "chart",
  target_slug: "revenue-daily",
  interval: "daily",
  instructions: "Monitor daily revenue. Flag drops > 10% day-over-day or week-over-week growth > 25%."
)
```

## dashboard

Monitors all charts on a dashboard for cross-metric patterns.

**Target**: Dashboard slug
**Default interval**: daily

**Capabilities**: Access all charts on the dashboard, cross-chart correlation, multi-KPI analysis.

**Example**:
```
create_watcher(
  type: "dashboard",
  target_slug: "exec-dashboard",
  interval: "weekly",
  instructions: "Analyze weekly trends across all metrics. Highlight correlations and anomalies."
)
```

## anomaly_detection

Automatically detects anomalies in chart data.

**Target**: Chart slug
**Default interval**: daily

**Capabilities**: Statistical anomaly detection on chart data, automatic discovery creation when anomalies are found.

**Example**:
```
create_watcher(
  type: "anomaly_detection",
  target_slug: "signup-funnel",
  interval: "hourly",
  instructions: "Detect unusual spikes or drops in signup conversion rates."
)
```

## forecast

Generates recurring forecasts from chart data.

**Target**: Chart slug
**Default interval**: weekly

**Capabilities**: Time series forecasting, trend projection, prediction interval generation.

**Example**:
```
create_watcher(
  type: "forecast",
  target_slug: "monthly-revenue",
  interval: "monthly",
  instructions: "Forecast next month revenue. Flag if actual diverges > 15% from forecast."
)
```

## Choosing the Right Type

| Goal | Type |
|------|------|
| Track a specific KPI | `chart` |
| Monitor multiple KPIs together | `dashboard` |
| Find unexpected patterns automatically | `anomaly_detection` |
| Project future values | `forecast` |
