---
name: configure-tasks
compatibility: Requires Altertable MCP server
description: Configures scheduled AI tasks that analyze Insights and Dashboards. Use for anomaly detection, forecasting, alerts, or recurring automated monitoring.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Configuring Tasks

## Quick Start

A task is a scheduled AI agent that runs on a cron and creates a discovery when the analysis produces a finding. Your `instructions` string is the prompt the AI follows on each run.

To create a task:

1. Call `initialize`, then identify what the user wants the AI to watch for (anomalies, a forecast, or open-ended analysis)
2. Choose the task type and target slugs
3. Write clear natural-language instructions. These are the AI's prompt every run
4. Pick a cron schedule that fits the task instructions
5. Call `create_task` on the Altertable MCP server

## When to Use This Skill

- User wants an Insight monitored for anomalies on a schedule
- User wants a metric forecast recurring on a cadence
- User wants ongoing AI analysis of an Insight or Dashboard
- User asks for automated alerts when something changes

## Task Types

All three types run AI analysis driven by your `instructions`. They differ in what the AI is asked to focus on.

| Type                | Target                         | AI focus                                                    |
| ------------------- | ------------------------------ | ----------------------------------------------------------- |
| `anomaly_detection` | Exactly one Insight slug       | Find outliers and unusual values in the Insight's data      |
| `forecast`          | Exactly one Insight slug       | Project future values and flag divergence from expectations |
| `ask`               | Zero or more entity slugs      | Run the open-ended analysis described by the instructions   |

## Core Workflow

### Step 1: Identify the Target

`anomaly_detection` and `forecast` require an existing Insight. Help the user create or find one with create-insights or `list_insights`, then pass its slug as `target_slugs: [slug]`.

`ask` accepts `target_slugs: []` for ambient analysis or multiple entity slugs for contextual analysis. Use `search_entities` when the requested entities are unclear.

### Step 2: Choose Task Type

Match the user's goal to a task type:

- "Alert me if signups drop unexpectedly" -> `anomaly_detection` with the signup Insight slug
- "Forecast next month's revenue" -> `forecast` with the revenue Insight slug
- "Analyze my dashboard for anything unusual" -> `ask` with the dashboard slug

### Step 3: Write Instructions

Instructions tell the task what to focus on. Be specific about:

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

### Step 4: Create the Task

Use the Altertable MCP task-creation tool. Supply:

- `type`: one of `anomaly_detection`, `forecast`, or `ask`
- `target_slugs`: an array following the target rules above
- a cron schedule (standard 5-field, UTC)
- the natural-language instructions, which become the prompt for each run

Refer to the MCP tool description for the exact parameter names and any additional required fields. The MCP schema is the source of truth.

## Common Pitfalls

- **Wrong task type**: `anomaly_detection` detects outliers, `forecast` projects future values, and `ask` runs open-ended analysis
- **Wrong target count**: anomaly detection and forecast require exactly one Insight slug; ask accepts zero or more entity slugs
- **Vague instructions**: "watch this Insight" produces noisy discoveries; be specific about thresholds and patterns
- **Creating duplicate tasks**: check if a task already exists on the target before creating a new one

## Reference Files

- [Task types](references/task-types.md) - Read when choosing between anomaly_detection, forecast, and ask
