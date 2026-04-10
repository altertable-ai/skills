# Chronos Forecasting

## What is Chronos

Chronos-2 is Amazon's open-source time series forecasting model (120M parameters). It provides point forecasts plus quantile-based uncertainty bands, making it suitable for business projections where understanding confidence matters.

## Input Requirements

- **Format**: JSON array of `{"date": "YYYY-MM-DD", "value": number}` pairs
- **Minimum**: 14 data points
- **Recommended**: 30-365 data points
- **Max size**: 3000 characters

## Output

The tool returns a markdown report with:

| Section | Contents |
|---------|----------|
| Forecast Table | Date, predicted value, low (10th percentile), high (90th percentile) |
| Trend | Direction, percentage change, confidence level |
| Summary | Mean, min, max forecast, average uncertainty range |

## When Chronos Outperforms Statistical Methods

- Complex seasonal patterns (not just simple weekly cycles)
- Non-linear trends
- Data with multiple overlapping periodicities
- Longer forecast horizons (14+ days)

## When Statistical Methods Suffice

- Short forecast horizons (< 7 days)
- Stable, predictable metrics
- When you only need trend direction, not precise values
- When you have fewer than 14 data points
