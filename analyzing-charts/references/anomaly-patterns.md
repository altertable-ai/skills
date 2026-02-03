# Anomaly Patterns Reference

Identifying and interpreting data anomalies in charts.

## Types of Anomalies

### Spikes

Sudden, significant increase in value.

**Characteristics**:
- Sharp upward movement
- Often followed by return to normal
- Magnitude significantly above baseline

**Common Causes**:
- Marketing campaigns
- Viral content
- External events
- System issues (double counting)
- Bot traffic

**Analysis Approach**:
1. Note the exact timing
2. Quantify the magnitude (% above normal)
3. Check duration
4. Look for correlating events
5. Verify data quality

### Drops

Sudden, significant decrease in value.

**Characteristics**:
- Sharp downward movement
- May or may not recover
- Magnitude significantly below baseline

**Common Causes**:
- System outages
- Tracking issues
- Seasonal effects
- Competition
- Product issues

**Analysis Approach**:
1. Identify when it started
2. Check if it recovered
3. Look for system alerts
4. Verify tracking is working
5. Check for external factors

### Gaps

Missing data points.

**Characteristics**:
- Breaks in the line
- Zero values where non-zero expected
- Missing time periods

**Common Causes**:
- Data pipeline issues
- Tracking failures
- Deployment problems
- System downtime

**Analysis Approach**:
1. Identify gap duration
2. Check data pipeline logs
3. Verify other data sources
4. Note for future analysis

### Plateaus

Sudden flattening after trend.

**Characteristics**:
- Abrupt end to growth/decline
- Consistent values over time
- May indicate a cap or floor

**Common Causes**:
- Market saturation
- Capacity limits
- Policy changes
- Seasonal caps

### Step Changes

Sudden, permanent shift in level.

**Characteristics**:
- Jump to new baseline
- Sustained at new level
- Not a temporary spike/drop

**Common Causes**:
- Product launches
- Pricing changes
- Major algorithm updates
- Market shifts
- Tracking changes

**Analysis Approach**:
1. Identify the exact date
2. Compare before/after levels
3. Look for known changes
4. Verify it's real (not data issue)

## Detection Methods

### Visual Inspection

- Look for obvious departures
- Check both extremes
- Compare to typical patterns

### Statistical Thresholds

- Values > 2 standard deviations
- Values > 3x typical range
- Percentage change thresholds

### Comparison-Based

- Compare to same period last year
- Compare to same day last week
- Compare to moving average

## Anomaly Analysis Checklist

### 1. Confirm the Anomaly

- [ ] Is this a real change or data issue?
- [ ] Does it appear in raw data?
- [ ] Is tracking working correctly?

### 2. Characterize

- [ ] When exactly did it start?
- [ ] How long did it last?
- [ ] What's the magnitude?
- [ ] Has it happened before?

### 3. Investigate Causes

- [ ] Any known events at that time?
- [ ] System changes or deployments?
- [ ] Marketing campaigns?
- [ ] External factors?

### 4. Assess Impact

- [ ] How significant is the impact?
- [ ] What metrics are affected?
- [ ] What's the business impact?

### 5. Document

- [ ] Record findings
- [ ] Note for future analysis
- [ ] Create alert if appropriate

## Common Patterns by Metric

### Traffic Anomalies

**Spikes**:
- Viral content
- PR mentions
- Marketing launches
- Bot attacks

**Drops**:
- Site outages
- Tracking failures
- Algorithm changes
- Competitive launches

### Conversion Anomalies

**Spikes**:
- Promotions
- Price changes
- Site improvements
- Seasonal demand

**Drops**:
- Checkout bugs
- Payment issues
- UX problems
- Competitive pricing

### Revenue Anomalies

**Spikes**:
- Large orders
- Campaign success
- Price increases
- New products

**Drops**:
- Chargebacks
- Refund batches
- System issues
- Market conditions

## Communicating Anomalies

### Spike Example

> **Traffic Spike on March 15**
>
> Website traffic increased 340% (from 10,000 to 44,000 sessions)
> on March 15, returning to normal levels the following day.
>
> **Cause**: Product mentioned in TechCrunch article published at 2pm.
>
> **Impact**: 500 new user signups (vs. typical 50/day).
>
> **Recommendation**: Prepare for similar events; consider PR outreach.

### Drop Example

> **Conversion Rate Drop: March 10-12**
>
> Conversion rate dropped from 3.2% to 0.8% over 48 hours,
> recovering on March 12 at 10am.
>
> **Cause**: Checkout button unclickable on mobile after March 9 deploy.
>
> **Impact**: Estimated 450 lost orders (~$22,500 revenue).
>
> **Recommendation**: Add mobile checkout monitoring; hotfix deployed.

## False Positives

Not every unusual value is a true anomaly:

### Expected Variations

- Weekday/weekend differences
- Holiday effects
- Seasonal patterns
- Month-end spikes

### Data Artifacts

- Timezone transitions
- Daylight saving time
- Reporting delays
- Backfills

### One-time Events

- Known promotions
- Scheduled maintenance
- Product launches

Always verify anomalies before escalating or acting.
