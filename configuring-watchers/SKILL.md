---
name: configuring-watchers
compatibility: Requires Altertable MCP server
description: Configures monitoring agents (watchers) with intervals and targets. Use when setting up automated monitoring, scheduled analysis, alerts, or autonomous data observation.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Configuring Watchers

## Quick Start

To create a watcher:
1. Identify what the user wants to monitor (a chart, dashboard, or metric)
2. Choose the watcher type and interval
3. Write clear instructions for what the watcher should focus on
4. Create the watcher via the Altertable MCP server with the target slug, type, interval, and instructions

## When to Use This Skill

- User wants to set up automated monitoring or alerts
- User asks to watch a chart, dashboard, or metric over time
- User wants anomaly detection or forecasting on a recurring schedule

## Watcher Types

Create a watcher via the Altertable MCP server with one of these types:

| Type | Target | Use Case |
|------|--------|----------|
| `chart` | Chart slug | Monitor a specific chart for changes, trends, or threshold breaches |
| `dashboard` | Dashboard slug | Monitor all charts on a dashboard for cross-metric patterns |
| `anomaly_detection` | Chart slug | Automatically detect anomalies in chart data |
| `forecast` | Chart slug | Generate recurring forecasts from chart data |

## Intervals

| Interval | Quota Cost | When to Use |
|----------|------------|-------------|
| `hourly` | 5 | Fast-changing metrics, data freshness checks |
| `daily` | 1 | Most common -- standard KPI monitoring |
| `weekly` | 1 | Slower trends, weekly summaries |
| `monthly` | 1 | Long-term strategic metrics |

Default to `daily` unless the user specifies otherwise or the metric clearly requires more frequent monitoring.

## Core Workflow

### Step 1: Identify the Target

The user needs a chart or dashboard to monitor. If they don't have one yet:
1. Help them create the chart or insight first (see creating-insights skill)
2. Use the resulting slug as the `target_slug`

### Step 2: Choose Type and Interval

Match the user's goal to a watcher type:
- "Alert me if revenue drops" -> `chart` watcher on the revenue chart
- "Watch my dashboard for anything unusual" -> `dashboard` watcher
- "Detect anomalies in signups" -> `anomaly_detection` on the signup chart
- "Forecast next month's traffic" -> `forecast` on the traffic chart

### Step 3: Write Instructions

Instructions tell the watcher what to focus on. Be specific about:
- What patterns to look for
- What thresholds matter
- When to create a discovery

Example:
```
Monitor weekly revenue trends. Create a discovery if:
- Revenue drops more than 10% week-over-week
- Revenue exceeds forecast by 20%
- Unusual patterns in regional breakdown
```

### Step 4: Create the Watcher

Create the watcher via the Altertable MCP server with:
- `type` -- one of: chart, dashboard, anomaly_detection, forecast
- `target_slug` -- slug of the chart or dashboard to monitor
- `interval` -- hourly, daily, weekly, or monthly (optional, defaults to type's default)
- `instructions` -- what to focus on (optional but recommended)
- `author_id` -- ID of the user creating the watcher

The tool returns the watcher's slug, state, type, and interval.

## Quota System

Each organization has a quota limit. Each watcher consumes quota based on its interval (see Quota Cost column above). Only active watchers (idle or running) consume quota -- paused and terminated watchers do not.

Before creating a watcher, check if the user has enough quota. If not, suggest:
- Downgrading an existing watcher's interval (e.g., hourly -> daily)
- Pausing or terminating watchers that are no longer needed
- Using a lower-frequency interval for the new watcher

## Common Pitfalls

- **Using hourly when daily suffices** -- wastes quota (5x vs 1x) with minimal benefit for most metrics
- **Vague instructions** -- "watch this chart" produces noisy discoveries; be specific about thresholds and patterns
- **Not checking quota first** -- the create call fails if quota is exceeded
- **Creating duplicate watchers** -- check if a watcher already exists on the target before creating a new one
- **Missing the target** -- the user needs an existing chart or dashboard slug; help them create one first if needed

## Reference Files

- [Watcher types](references/watcher-types.md) - Read when choosing between chart, dashboard, anomaly_detection, and forecast types
- [Intervals guide](references/intervals.md) - Read when the user is unsure which interval to use or wants layered monitoring
- [Quota management](references/quotas.md) - Read when the create call fails due to quota limits or when optimizing existing watchers
