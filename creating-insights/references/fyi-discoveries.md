# FYI Discoveries Reference

Creating informational discoveries without visualizations.

## When to Use FYI Discoveries

- Text-based observations
- Recommendations and suggestions
- Warnings and alerts
- Context for other findings
- Qualitative insights

## Characteristics

- No visualization required
- Skip visualization generation step
- Immediately enter review workflow
- Focus on written communication

## Workflow

### 1. Identify the Finding

What observation needs to be shared?
- Data quality issue
- Process recommendation
- Contextual information
- Warning about trends

### 2. Write Clear Title

Concise summary of the finding.

### 3. Write Detailed Description

Full context and recommendations.

### 4. Create Discovery

Submit as FYI type.

## Discovery Types That Skip Review

Some FYI-like discoveries bypass user review:
- `OrganizationBlurb` - Organization description
- `ConnectData*` - Data connection suggestions
- `NewSemanticModels` - New model recommendations
- `WebAnalyticsEventsDetected` - Auto-detected events

## Writing Effective FYIs

### Title Guidelines

- **Clear**: State the finding directly
- **Concise**: Under 100 characters
- **Actionable**: Imply what to do

#### Examples

| Good | Bad |
|------|-----|
| "Data quality issue: 15% of orders missing customer_id" | "Missing data" |
| "Recommend adding index on events.timestamp" | "Performance" |
| "Q4 data not yet available in warehouse" | "Data note" |

### Description Structure

```markdown
## Observation
[What was found]

## Context
[Why this matters]

## Recommendation
[What to do about it]

## Supporting Data
[Any relevant numbers or references]
```

### Example FYI

**Title**: "Mobile traffic up 40% but conversion down 20%"

**Description**:
```
## Observation
Mobile traffic increased 40% month-over-month, but mobile
conversion rate dropped from 2.5% to 2.0%.

## Context
This divergence suggests the checkout experience may not be
optimized for the increasing mobile audience. Desktop conversion
remained stable at 3.8%.

## Recommendation
1. Review mobile checkout flow for friction points
2. Consider mobile-specific A/B tests
3. Analyze mobile user journey drop-offs

## Supporting Data
- Mobile sessions: 145,000 → 203,000 (+40%)
- Mobile conversions: 3,625 → 4,060 (+12%)
- Mobile CVR: 2.5% → 2.0% (-20%)
```

## Common Use Cases

### Data Quality Alerts

```
Title: "Duplicate user records detected in CRM sync"

Found 342 user records with duplicate email addresses
after the March 15 CRM sync. This may affect user counts
and attribution accuracy.

Recommendation: Run deduplication script before next analysis.
```

### Process Recommendations

```
Title: "Consider adding UTM tracking to email campaigns"

Email traffic shows as "direct" in analytics, making it
impossible to attribute conversions to specific campaigns.

Recommendation: Add UTM parameters to all email links
using the standard format: utm_source=email&utm_campaign=[name]
```

### Contextual Information

```
Title: "Website was down for 2 hours on March 10"

Traffic and conversion data for March 10 will show anomalies
due to a 2-hour outage (14:00-16:00 UTC).

Consider excluding this period from trend analysis.
```

### Warnings

```
Title: "Approaching API rate limit on Amplitude connection"

Current usage: 85% of monthly quota
Projected to exceed limit by March 25

Recommendation: Review query frequency or upgrade plan.
```

## Best Practices

### Be Specific

- Include numbers when relevant
- Reference specific dates/periods
- Name affected systems/reports

### Be Actionable

- Always include recommendation
- Suggest next steps
- Provide resources if available

### Be Concise

- Lead with the key point
- Use bullet points
- Keep under 500 words

### Consider Audience

- Technical vs business readers
- Level of detail appropriate
- Include context for non-experts

## Metadata

FYI discoveries can include metadata:

```yaml
metadata:
  category: "data_quality"
  priority: "high"
  affected_reports: ["daily_dashboard", "weekly_summary"]
```

Common metadata fields:
- `category`: Type of FYI
- `priority`: Urgency level
- `affected_reports`: Related dashboards
- `source`: Where finding came from
