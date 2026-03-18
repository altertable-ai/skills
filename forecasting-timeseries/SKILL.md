---
name: forecasting-timeseries
compatibility: Requires Python 3.12+, Altertable MCP server, chronos, statsforecast, and statsmodels
description: Analyzes time series data for trends, anomalies, and forecasts. Use when detecting spikes or drops, predicting future values, identifying anomalies in metrics over time, or when the user asks about forecasting, projections, or unusual patterns in hourly/daily/weekly/monthly data.
metadata:
  author: altertable-ai
  requires: "altertable-mcp, python, chronos, statsforecast, statsmodels"
---

# Forecasting Time Series

## Quick Start

1. Query time series data with the lakehouse (daily granularity, 30-90 days covers both tools well)
2. Use `Analyze Time Series Insight` to detect anomalies and get a statistical forecast
3. If you need higher accuracy or uncertainty bands, follow up with `Forecast with Chronos` (needs 14+ days, best with 30+)

## When to Use This Skill

- User asks about trends, spikes, or drops in a metric over time
- User wants to predict or forecast future values
- User asks "is this normal?" about a metric value
- Investigating anomalies or unexpected changes
- User asks for projections, predictions, or what to expect next week/month
- Keywords: "forecast", "predict", "anomaly", "spike", "drop", "trend", "projection", "unusual", "normal range"

## Two Tools, Two Purposes

There are two complementary time series tools. Use one or both depending on the question.

| | Analyze Time Series Insight | Forecast with Chronos |
|---|---|---|
| **Best for** | "What happened?" | "What will happen?" |
| **Anomaly detection** | Yes (Z-score + IQR) | No |
| **Forecasting method** | Exponential smoothing | Chronos-2 ML model |
| **Uncertainty bands** | No | Yes (10th/90th percentile) |
| **Minimum data** | 3 days | 14 days |
| **Recommended data** | 14-90 days | 30-365 days |
| **Default horizon** | 7 days | 14 days |
| **Max input size** | 2000 chars | 3000 chars |

### When to Use Each

```
User question about a metric over time
  │
  ├─ "Is this value normal?" / "Why did X spike?"
  │   → Analyze Time Series Insight (anomaly detection)
  │
  ├─ "What will happen next week?" / "Forecast revenue"
  │   → Forecast with Chronos (ML forecast with uncertainty)
  │
  └─ "Analyze this trend and predict what's next"
      → Both: Analyze first, then Chronos for deeper forecast
```

## Workflow

### Step 1: Query the Data

Use `query_lakehouse` to get daily time series data. Format the result as:

```json
[{"date": "2024-01-01", "value": 100}, {"date": "2024-01-02", "value": 105}]
```

**Keep the data compact.** Aggregate to weekly if the date range exceeds 90 days. The tools have strict character limits on input.

### Step 2: Run Analysis

Start with `Analyze Time Series Insight` for a statistical overview:
- Detects anomalous values using Z-score and IQR methods
- Identifies whether the latest value is anomalous
- Provides trend direction and day-over-day change
- Generates a short-term exponential smoothing forecast

### Step 3: Enhance with Chronos (Optional)

If the user needs a more accurate forecast or wants confidence intervals, run `Forecast with Chronos`:
- Provides point forecast plus 10th/90th percentile uncertainty bands
- Better at capturing complex seasonal patterns
- Indicates forecast confidence (high/medium/low based on band width)

## Interpreting Results

### Anomaly Detection

The analysis tool flags anomalies using two combined methods:
- **Z-score**: Values more than 2 standard deviations from the mean
- **IQR**: Values below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR

A value flagged by either method is reported. If the latest value is anomalous, it requires attention.

### Trend Direction

| Forecast Change | Interpretation |
|-----------------|----------------|
| > +5% | Increasing trend |
| -5% to +5% | Stable |
| < -5% | Decreasing trend |

### Chronos Confidence Levels

| Uncertainty Band Width | Confidence |
|------------------------|------------|
| < 20% of forecast mean | High — narrow band, reliable |
| 20-50% | Medium |
| > 50% | Low — wide band, treat with caution |

## Common Pitfalls

1. **Sending too much data** — Tools have 2000/3000 char limits. Aggregate to weekly for long ranges
2. **Too few data points** — Chronos needs 14+ days. Analysis needs 3+ but works best with 14+
3. **Using Chronos for anomaly detection** — Chronos only forecasts; use Analyze Time Series for anomalies
4. **Skipping aggregation** — Hourly data quickly exceeds size limits. Always use daily or weekly granularity
5. **Ignoring uncertainty bands** — A Chronos forecast with wide bands means low confidence; communicate this clearly
6. **Not checking seasonality** — Weekly patterns (weekday vs weekend) need at least 14 days to detect
7. **Forecasting without context** — Always pair forecasts with what the current trend shows

## References

- [Chronos forecasting details](references/chronos-forecasting.md)
- [Anomaly detection methods](references/anomaly-detection.md)
