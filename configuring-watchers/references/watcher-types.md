# Watcher Types Reference

Detailed guide to each watcher type.

## PlatformWatcher

Organization-wide monitoring agent.

### Purpose
- Monitor overall platform health
- Detect cross-system patterns
- Generate organization-level insights

### Target
- Organization (one per org)

### Default Interval
- REALTIME

### Capabilities
- Access to all data sources
- Can monitor multiple metrics
- Creates org-level discoveries

### Use Cases
- Overall health monitoring
- Cross-functional insights
- Executive dashboards

## ChartWatcher

Monitors a specific chart.

### Purpose
- Track chart metric changes
- Alert on significant variations
- Analyze visualization data

### Target
- Specific chart (by slug)

### Default Interval
- DAILY

### Capabilities
- Access chart data
- Analyze trends
- Compare periods
- Detect anomalies

### Use Cases
- KPI monitoring
- Revenue tracking
- Conversion monitoring

### Configuration Example

```yaml
type: ChartWatcher
target: INS-42
interval: DAILY
instructions: |
  Monitor this revenue chart for:
  - Significant drops (>10%)
  - Unusual patterns
  - Compare to prior period
```

## DashboardWatcher

Monitors an entire dashboard.

### Purpose
- Track multiple metrics together
- Identify correlations
- Dashboard-level insights

### Target
- Dashboard (by slug)

### Default Interval
- DAILY

### Capabilities
- Access all charts on dashboard
- Cross-chart analysis
- Correlation detection

### Use Cases
- Executive dashboards
- Department metrics
- Multi-KPI monitoring

## ConnectionWatcher

Monitors a data connection.

### Purpose
- Data quality monitoring
- Pipeline health
- Schema changes

### Target
- Connection (by slug)

### Default Interval
- DAILY

### Capabilities
- Query connection
- Check data freshness
- Monitor schema
- Row count analysis

### Use Cases
- ETL monitoring
- Data freshness alerts
- Quality checks

### Configuration Example

```yaml
type: ConnectionWatcher
target: snowflake-prod
interval: HOURLY
instructions: |
  Monitor data pipeline:
  - Check last_updated timestamps
  - Alert if data > 2 hours stale
  - Monitor key table row counts
```

## SemanticSourceWatcher

Monitors a semantic source.

### Purpose
- Semantic model metrics
- Business metric tracking
- Model health

### Target
- Semantic source (by slug)

### Default Interval
- DAILY

### Capabilities
- Query semantic metrics
- Track dimension distributions
- Monitor measure values

### Use Cases
- Business metric monitoring
- Model validation
- Automated reporting

## SegmentWatcher

Monitors a user segment.

### Purpose
- Segment size tracking
- Population changes
- Cohort monitoring

### Target
- Segment (by slug)

### Default Interval
- DAILY

### Capabilities
- Track segment size
- Monitor composition
- Detect changes

### Use Cases
- Audience monitoring
- Churn tracking
- Growth metrics

### Configuration Example

```yaml
type: SegmentWatcher
target: SGM-15
interval: WEEKLY
instructions: |
  Monitor premium user segment:
  - Track size changes
  - Alert on significant drops
  - Analyze composition shifts
```

## EventsActivityWatcher

Monitors event activity.

### Purpose
- Event volume tracking
- Pattern detection
- Activity monitoring

### Target
- Events (org-wide or filtered)

### Capabilities
- Event volume analysis
- Pattern detection
- Anomaly identification

### Use Cases
- Activity monitoring
- Engagement tracking
- Feature usage

## WebAnalyticsWatcher

Monitors web analytics data.

### Purpose
- Traffic monitoring
- User behavior analysis
- Web performance

### Target
- Web analytics data

### Capabilities
- Traffic analysis
- Source tracking
- Page performance
- Session metrics

### Use Cases
- Traffic monitoring
- SEO tracking
- Marketing attribution

### Configuration Example

```yaml
type: WebAnalyticsWatcher
interval: WEEKLY
instructions: |
  Analyze web traffic trends:
  - Top page changes
  - Traffic source shifts
  - Engagement patterns
  - Notable anomalies
```

## Choosing the Right Type

| Need | Watcher Type |
|------|--------------|
| Monitor a specific KPI | ChartWatcher |
| Track multiple KPIs | DashboardWatcher |
| Data quality/freshness | ConnectionWatcher |
| Business metrics | SemanticSourceWatcher |
| Audience changes | SegmentWatcher |
| User activity | EventsActivityWatcher |
| Website metrics | WebAnalyticsWatcher |
| Organization overview | PlatformWatcher |
