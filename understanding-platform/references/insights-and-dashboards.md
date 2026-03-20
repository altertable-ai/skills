# Insights and Dashboards

Insights and dashboards are the persistent analysis layer that agents monitor.

## Insights

Insights are saved analyses over lakehouse data. They turn raw data into reusable, shareable analytical views.

### Common Insight Types

- **Funnel:** conversion through sequential steps
- **Segmentation:** cohort comparisons by behavior or attributes
- **Semantic:** model-driven business metrics without raw SQL
- **SQL:** fully custom analysis for advanced use cases

### Why Insights Matter

- Standardize recurring analyses
- Keep metric logic reusable
- Provide monitorable assets for agents
- Support collaborative decision-making

## Dashboards

Dashboards organize multiple insights into one operational view for KPI tracking and reporting.

### Core Capabilities

- Mixed widgets (charts, tables, metrics, text)
- Shared variables for cross-widget filtering
- Flexible layout for role-specific monitoring
- Agent attachment for continuous change detection

## How Agents Use These Artifacts

Agents monitor insights and dashboards to detect:

- Significant trend changes
- Outlier behavior
- Segment-level shifts
- KPI deviations from expected patterns

When notable changes are detected, agents produce discoveries for human review.

## Practical Distinction

- **Insights/Dashboards:** persistent analytical assets (what is being monitored)
- **Discoveries:** agent-generated findings (what was detected)
- **Memories:** learned context that improves future monitoring (what was learned)
