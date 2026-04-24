---
name: configuring-tasks
compatibility: Requires Altertable MCP server
description: Configures scheduled AI tasks that analyze Insights and Dashboards on a cron and create discoveries for anomaly detection, forecasting, or open-ended monitoring. Use when the user wants recurring automated analysis, alerts, or monitoring driven by AI instructions.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Configuring Tasks

## Quick Start

A task is a scheduled AI agent that runs on a cron, analyzes an Insight or Dashboard, and creates a discovery when the analysis produces a finding. Your `instructions` string is the prompt the AI follows on each run.

To create a task:

1. Identify what the user wants the AI to watch for (anomalies, a forecast, or open-ended analysis)
2. Choose the task type and target slug
3. Write clear natural-language instructions -- these are the AI's prompt every run
4. Pick a cron schedule that fits the task instructions
5. Call `create_task` on the Altertable MCP server

## When to Use This Skill

- User wants an Insight monitored for anomalies on a schedule
- User wants a metric forecast recurring on a cadence
- User wants ongoing AI analysis of an Insight or Dashboard
- User asks for automated alerts when something changes

## Task Types

All three types run AI analysis driven by your `instructions`. They differ in what the AI is asked to focus on.

| Type                 | Target               | AI focus                                                    |
| -------------------- | -------------------- | ----------------------------------------------------------- |
| `anomaly_detection`  | Insight slug           | Find outliers and unusual values in the Insight's data        |
| `forecast`           | Insight slug           | Project future values and flag divergence from expectations |
| `monitor`            | Insight/Dashboard slug | Open-ended analysis -- whatever the instructions describe   |

## Core Workflow

### Step 1: Identify the Target

The user needs an existing resource to target. If they don't have one yet:

1. Help them create the Insight, Dashboard, or connection first (see creating-insights or exploring-data skills)
2. Use the resulting slug as the `target_slug`

### Step 2: Choose Task Type

Match the user's goal to a task type:

- "Alert me if signups drop unexpectedly" -> `anomaly_detection` on the signup Insight
- "Forecast next month's revenue" -> `forecast` on the revenue Insight
- "Analyze my dashboard for anything unusual" -> `monitor` on the dashboard

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

- the task type -- one of `anomaly_detection`, `forecast`, or `monitor`
- the target Insight or Dashboard slug the AI will analyze
- a cron schedule (standard 5-field, UTC)
- the natural-language instructions -- the prompt the AI follows on each run
- the author (the user creating the task)

Refer to the MCP tool description for the exact parameter names and any additional required fields -- the MCP schema is the source of truth.

## Common Pitfalls

- **Wrong task type** -- `anomaly_detection` detects outliers; `forecast` projects future values; `monitor` does open-ended analysis. Don't mix them up
- **Vague instructions** -- "watch this Insight" produces noisy discoveries; be specific about thresholds and patterns
- **Creating duplicate tasks** -- check if a task already exists on the target before creating a new one
- **Missing the target** -- the user needs an existing Insight or Dashboard slug; help them create one first if needed
- **Using `monitor` when `anomaly_detection` suffices** -- `monitor` is more general but less focused; prefer `anomaly_detection` for pure outlier detection

## Reference Files

- [Task types](references/task-types.md) - Read when choosing between anomaly_detection, forecast, and monitor
