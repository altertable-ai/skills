# Platform Overview

Altertable is an operational data platform built for the agentic era: continuous ingestion, continuous querying, and continuous analysis.

## Why Altertable Exists

Traditional data infrastructure was designed for:

- Batch pipelines
- Dashboard refreshes
- Humans asking occasional questions

That model breaks when always-on agents need to monitor and explore data continuously. The bottleneck is often the data layer, not model intelligence.

## Core Foundation

Altertable combines:

- Real-time ingestion
- High-performance columnar storage
- Open, builder-friendly access patterns
- Lakehouse economics that improve at higher query volume

This foundation supports both human analytics workflows and autonomous software agents.

## What Makes the Platform Different

The platform is designed so intelligence operates directly on top of the data layer:

- Agents monitor metrics and structures continuously
- Analysis runs in the background without waiting for manual intervention
- Noteworthy changes are surfaced as reviewable discoveries
- Human feedback closes the loop and improves future agent behavior

## Primary Concept Graph

```text
Lakehouse data layer
  -> Insights and Dashboards
    -> Agents monitor continuously
      -> Discoveries generated
        -> Human review decisions
          -> Memories updated
            -> Better future analysis
```

## Mental Model for Explanations

When explaining Altertable to users, use this progression:

1. **Infrastructure:** always-queryable operational lakehouse
2. **Analysis objects:** insights and dashboards
3. **Autonomous execution:** agents running continuously
4. **Human collaboration:** discoveries requiring review
5. **Learning system:** memories that improve future runs
