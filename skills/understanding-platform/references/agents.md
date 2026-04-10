# Agents

Altertable agents are autonomous data collaborators that operate continuously alongside human teams.

## Core Definition

Agents are not one-shot chat assistants. They are long-running analytical operators that can:

- Keep data workflows moving (sync, model, query, visualize)
- Monitor existing analyses in the background
- Surface findings when conditions change
- Learn from user feedback and prior runs

## What Agents Do

### Foundational Work

- Synchronize and prepare data sources
- Build or update models and analytical logic
- Create queries, visualizations, and dashboards

### Continuous Work

- Monitor metrics for anomalies and trend shifts
- Track user and segment behavior changes
- Detect meaningful schema or model changes
- Generate discoveries with recommendations

## Execution Model

Agents orchestrate multiple LLM providers through a unified asynchronous job system. This lets Altertable route different tasks to the right model while maintaining a consistent user-facing workflow.

## Human + Agent Collaboration

The intended operating mode is collaborative:

- Humans provide business context, goals, and constraints
- Agents execute repetitive and high-frequency analysis work
- Humans review discoveries and guide quality thresholds
- Agents adapt based on this feedback over time

## Common Misunderstandings

- Agents do not replace business judgment
- Agents do not operate as isolated chat sessions
- Agent quality depends on data quality and feedback loops
- Agents are most valuable when attached to persistent analysis artifacts (insights/dashboards), not only ad-hoc prompts
