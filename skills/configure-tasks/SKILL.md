---
name: configure-tasks
compatibility: Requires Altertable MCP server with read-write access
description: "Drafts, creates, and updates Altertable Tasks that run SQL, code, or AI work on a schedule. Use for recurring analysis, anomaly checks, forecasts, monitoring, or Findings delivered through Notifications."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Configure Tasks

Altertable Tasks run scheduled work and produce a Finding only when something is worth the user's attention. Findings are delivered as Notifications through the channels configured for the current environment.

## Workflow

1. Confirm the intended environment and use `list_tasks` to avoid duplicating an existing task on the same context.
2. Resolve the target and read its current definition. A task can run on an insight, dashboard, connection, database, segment, or semantic model.
3. Inspect the current creation or draft schema for supported task types and targets. Do not copy enum values from memory.
4. Write instructions that define what to examine, what is noteworthy, relevant thresholds, comparison periods, and when silence is correct.
5. Use `draft_task` while the user is iterating. Use `create_task` only after the schedule, target, and instructions are settled and persistence is requested.
6. Use `update_task` for an existing task; omitted fields remain unchanged.

## Task Instructions

Write instructions as a durable prompt that will run without the current conversation. Include:

- the metric, behavior, or condition to evaluate;
- the comparison or baseline to use;
- thresholds or qualitative criteria for a noteworthy change;
- relevant segments, exclusions, and business context;
- the expected Finding content and useful next action;
- an instruction to remain quiet when nothing meaningful changed.

Do not tell a task to report on every run unless the user explicitly wants a scheduled report. Avoid generic instructions such as “monitor this” because they create noisy Notifications.

## Task Modes

Choose among general AI analysis, anomaly detection, and forecasting according to the live schema. Use the direct `ask` tool or a query for a one-off forecast or anomaly investigation; use a Task only when the user wants recurring work.

## Scheduling and Scope

- Match cadence to data freshness and the decision window.
- Confirm the timezone represented by the schedule; do not silently assume local time or UTC.
- Keep the task in the same environment as its target and notification preferences.
- Check the live tool schema for CRON syntax and supported target combinations.
- If the connection is read-only, provide a proposed task definition instead of attempting persistence.

## Updates

Before updating, retrieve the existing task and preserve fields the user did not ask to change. Deactivate rather than delete when the intent is to pause recurring work. Reuse the task's slug and verify the returned schedule, active state, targets, and instructions.

## Documentation

Use `search_docs` for current task types, scheduling behavior, and Notification delivery. The live MCP schema is authoritative for arguments.
