# Conversion Metrics Reference

Understanding and calculating funnel metrics.

## Core Metrics

### Conversion Rate

Percentage of users who complete an action.

```
Conversion Rate = (Conversions / Total Users) × 100
```

Example:
- 1,000 users entered
- 150 completed purchase
- CVR = 15%

### Drop-off Rate

Percentage of users who don't continue.

```
Drop-off Rate = 1 - Conversion Rate
```

Or:
```
Drop-off Rate = (Dropped / Entered) × 100
```

### Step Metrics

For each step transition:

| Metric | Calculation |
|--------|-------------|
| Entered | Users reaching this step |
| Continued | Users moving to next step |
| Dropped | Users who stopped here |
| Step CVR | Continued / Entered |
| Cumulative CVR | This Step / Step 1 |

## Funnel Visualization

### Basic Funnel Table

```
Step              Users    CVR    Drop-off
─────────────────────────────────────────────
1. Page View      10,000   100%      -
2. Add to Cart     2,000    20%     80%
3. Checkout        1,200    60%     40%
4. Payment         1,000    83%     17%
5. Confirmation      950    95%      5%
─────────────────────────────────────────────
Overall             950    9.5%    90.5%
```

### Interpreting the Table

- **Users**: Absolute count at step
- **CVR**: From previous step
- **Drop-off**: Lost at this transition
- **Overall**: From Step 1 to Final

## Advanced Metrics

### Average Time Between Steps

How long users take:

```
Avg Time = Σ(Step N timestamp - Step N-1 timestamp) / Users
```

Insights:
- Very fast = impulsive or automated
- Very slow = friction or consideration
- Varying = different user types

### Conversion Velocity

How quickly users convert:

| Bucket | % of Conversions |
|--------|------------------|
| < 1 hour | 45% |
| 1-24 hours | 30% |
| 1-7 days | 20% |
| > 7 days | 5% |

### Re-engagement Rate

Users who left but returned:

```
Re-engagement = Users who completed after leaving / Total dropped
```

## Benchmark Ranges

### E-commerce

| Metric | Low | Average | High |
|--------|-----|---------|------|
| Cart Addition | 5% | 10% | 20% |
| Checkout Start | 30% | 50% | 70% |
| Payment Complete | 60% | 75% | 90% |
| Overall | 1% | 3% | 6% |

### SaaS Signup

| Metric | Low | Average | High |
|--------|-----|---------|------|
| Start Form | 10% | 20% | 35% |
| Complete Form | 50% | 70% | 85% |
| Email Verify | 60% | 80% | 95% |
| Activation | 30% | 50% | 70% |

### Mobile App

| Metric | Low | Average | High |
|--------|-----|---------|------|
| Install → Open | 80% | 90% | 95% |
| Open → Register | 20% | 35% | 50% |
| Register → Activate | 40% | 60% | 80% |
| Day 1 Retention | 20% | 30% | 45% |

## Segmented Analysis

### By Device

```
Device      Entry    Final    CVR    Index
─────────────────────────────────────────────
Desktop     5,000      600   12.0%   1.00
Mobile      4,000      280    7.0%   0.58
Tablet        800       80   10.0%   0.83
```

Index = Segment CVR / Best CVR

### By Source

```
Source      Entry    Final    CVR    Index
─────────────────────────────────────────────
Organic     3,000      450   15.0%   1.00
Paid        4,000      320    8.0%   0.53
Social      2,500      150    6.0%   0.40
Email       1,500      225   15.0%   1.00
```

## Diagnostic Metrics

### Drop-off Diagnosis

For each major drop-off, check:

| Check | Metric | Target |
|-------|--------|--------|
| Page load | Time to interactive | < 3s |
| Form completion | Field errors | < 5% |
| Mobile UX | Mobile CVR gap | < 30% |
| Trust signals | Exit survey | Positive |

### Funnel Health Score

Composite metric:

```
Health = (Actual CVR / Benchmark CVR) × 100
```

| Score | Status |
|-------|--------|
| > 120 | Excellent |
| 100-120 | Good |
| 80-100 | Average |
| 60-80 | Needs work |
| < 60 | Critical |

## Trend Analysis

### WoW Comparison

```
Week    Entry    Final    CVR     Δ
────────────────────────────────────────
W1      8,000      720    9.0%    -
W2      8,500      850   10.0%  +11%
W3      9,000      990   11.0%  +10%
W4      8,800      792    9.0%  -18%  ← Issue
```

### Seasonality Adjustment

Compare to same period last year:

```
Period       This Year    Last Year    Index
─────────────────────────────────────────────────
Q1             8.5%         7.2%       1.18
Q2             9.2%         8.0%       1.15
Q3             7.8%         7.5%       1.04
Q4            12.1%        10.8%       1.12
```

## Statistical Significance

### Sample Size Requirements

For reliable results:

| CVR Level | Min Sample |
|-----------|------------|
| 1% | 10,000+ |
| 5% | 2,000+ |
| 10% | 1,000+ |
| 20% | 500+ |

### Confidence Intervals

Report with uncertainty:

```
Conversion Rate: 12.5% ± 1.2% (95% CI)
```

### A/B Test Significance

When comparing variants:

```
Control: 10.0% (n=5,000)
Variant: 11.5% (n=5,000)
Lift: +15%
p-value: 0.02 (Significant)
```
