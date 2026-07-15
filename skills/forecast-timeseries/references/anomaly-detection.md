# Anomaly Detection Methods

## Z-Score Method

Flags values more than 2 standard deviations from the mean.

- **Strengths**: Simple, effective for normally distributed data
- **Weaknesses**: Sensitive to outliers in the mean/std calculation itself
- **Minimum data**: 3 points (but unreliable below ~20)

## IQR Method (Interquartile Range)

Flags values below Q1 - 1.5 * IQR or above Q3 + 1.5 * IQR.

- **Strengths**: Robust to extreme outliers, no distribution assumption
- **Weaknesses**: May miss anomalies in highly skewed data
- **Minimum data**: 4 points

## Combined Approach

The `Analyze Time Series Insight` tool uses **both methods together** — a value flagged by either method is reported as anomalous. This reduces false negatives at the cost of slightly more false positives.

## Interpreting Anomaly Results

| Scenario | Interpretation |
|----------|----------------|
| Latest value is anomalous | Requires immediate attention — investigate cause |
| Multiple clustered anomalies | May indicate a regime change, not isolated events |
| Single past anomaly | Likely a one-off event (deploy, campaign, outage) |
| No anomalies | Metric is within expected range |

## Limitations

- Neither method accounts for seasonality — a weekend dip on a metric with strong weekly patterns may be flagged as anomalous even though it is expected
- The *forecasting* component (exponential smoothing) has a separate seasonal mode that activates with 14+ data points, but this does not affect anomaly detection — anomalies are always evaluated without seasonal adjustment
- The tools do not correlate anomalies with external events — that interpretation is up to the analyst
