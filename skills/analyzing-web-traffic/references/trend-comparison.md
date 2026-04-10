# Trend Comparison Reference

Methods for comparing web traffic across time periods.

## Comparison Periods

### Week-over-Week (WoW)

**Best for**: Short-term trends, recent changes

**Calculation**:
```
WoW Change = (This Week - Last Week) / Last Week × 100
```

**When to use**:
- Monitoring recent campaigns
- Detecting sudden changes
- Weekly reporting

**Considerations**:
- Accounts for day-of-week patterns
- Holidays can skew comparison
- Single-week events may distort

### Month-over-Month (MoM)

**Best for**: Medium-term trends, monthly planning

**Calculation**:
```
MoM Change = (This Month - Last Month) / Last Month × 100
```

**When to use**:
- Monthly performance reviews
- Budget planning
- Campaign evaluation

**Considerations**:
- Months have different lengths
- Some months have holidays
- Beginning/end of month effects

### Year-over-Year (YoY)

**Best for**: Long-term trends, seasonality

**Calculation**:
```
YoY Change = (This Year - Last Year) / Last Year × 100
```

**When to use**:
- Annual planning
- Seasonal analysis
- Long-term growth tracking

**Considerations**:
- Best accounts for seasonality
- Business may have changed significantly
- External factors (market, economy)

## Comparison Methods

### Same Period Last Year (SPLY)

Compare to exact same dates last year:
- March 1-31, 2024 vs March 1-31, 2023

**Best for**: Highly seasonal businesses

### Same Week Last Year (SWLY)

Compare to same week number:
- Week 12, 2024 vs Week 12, 2023

**Best for**: Accounts for day-of-week patterns

### Rolling Comparisons

Compare rolling periods:
- Last 30 days vs Prior 30 days
- Last 7 days vs Prior 7 days

**Best for**: Continuous monitoring

## Comparison Reporting

### Basic Comparison Table

```
Metric          This Week   Last Week   Change
────────────────────────────────────────────────
Sessions          15,234      14,567    +4.6%
Pageviews         45,678      43,210    +5.7%
Users             12,345      11,890    +3.8%
Bounce Rate         42%         44%    -4.5%
Avg Duration       3:15        3:05    +5.4%
```

### Multi-Period Comparison

```
Metric       This Week  Last Week  4 Wks Ago  YoY
──────────────────────────────────────────────────
Sessions       15,234     14,567     13,890  +22%
Pageviews      45,678     43,210     41,234  +18%
```

### Trend Sparkline

```
Sessions (last 8 weeks):
▁▂▃▃▄▅▆▇  Trending Up (+23%)
```

## Interpreting Changes

### Significant Changes

| Change | Interpretation |
|--------|----------------|
| +/-5% | Normal variance |
| +/-10-20% | Notable change |
| +/-20-50% | Significant change |
| +/-50%+ | Major shift |

### Context Matters

Always consider:
- Were there campaigns?
- Any technical issues?
- Seasonal factors?
- Competitive changes?
- Site changes?

## Accounting for Seasonality

### Weekly Seasonality

Traffic often varies by day:
```
Day        Index
──────────────────
Monday      1.05
Tuesday     1.10
Wednesday   1.08
Thursday    1.05
Friday      0.95
Saturday    0.85
Sunday      0.82
```

**Solution**: Compare same day of week

### Monthly Seasonality

Some months are consistently higher/lower:
```
Month      Index
──────────────────
January     0.85
February    0.90
March       1.00
...
November    1.15
December    1.25
```

**Solution**: Use YoY comparisons

### Event-Based Seasonality

- Black Friday
- Back to school
- Tax season
- Industry conferences

**Solution**: Compare to same event period

## Trend Analysis Techniques

### Moving Averages

Smooth out daily variance:
```
7-day MA: Average of last 7 days
28-day MA: Average of last 28 days
```

**Use for**: Identifying true trend direction

### Trend Lines

Fit a line to see direction:
- Positive slope = growth
- Negative slope = decline
- Flat = stable

### Growth Rate

Calculate compound growth:
```
CAGR = (End/Start)^(1/periods) - 1
```

## Comparison Pitfalls

### Calendar Effects

- Different number of weekdays
- Holiday positioning
- Leap years

### Data Quality

- Tracking changes
- Bot filtering
- Attribution changes

### External Factors

- Market conditions
- Competitive landscape
- Algorithm changes

### Business Changes

- Pricing changes
- Product launches
- Website redesigns

## Best Practices

### Always Provide Context

Don't just say "traffic up 15%":
- What drove the change?
- Is it sustainable?
- How does it compare to goals?

### Use Multiple Timeframes

Look at WoW, MoM, and YoY together:
- Short-term: recent effects
- Medium-term: trends
- Long-term: growth

### Segment Your Comparisons

Don't just compare totals:
- By traffic source
- By device
- By geography
- By page type

### Account for Anomalies

Note and adjust for:
- Site outages
- Tracking issues
- One-time events
- Data backfills
