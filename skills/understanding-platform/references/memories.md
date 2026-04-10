# Memories

Memories are persistent knowledge objects that agents accumulate while working with data and user feedback.

## Why Memories Matter

Without memory, every run starts from zero. With memory, agents preserve context and improve over time.

Memories help agents:

- Remember business preferences and KPI expectations
- Learn from accepted or rejected discoveries
- Reuse proven analytical strategies
- Avoid repeating known mistakes

## Memory Types

### Episodic ("what happened")

Specific events tied to a time or run context.

Example: "Revenue dropped 15% during a migration week."

### Semantic ("what is generally true")

Generalized facts and patterns extracted from repeated episodes.

Example: "Revenue often dips during infrastructure migrations."

### Procedural ("how to handle this")

Reusable methods and analysis playbooks.

Example: "For churn analysis, segment by acquisition channel first."

## Memory Lifecycle

```text
Created -> Active -> Consolidated -> Faded
```

- **Created:** generated during analysis or review
- **Active:** retrieved and used in current work
- **Consolidated:** related memories distilled into higher-value knowledge
- **Faded:** unused memories decay and are eventually removed

## Retention Dynamics

Memory relevance is a function of:

- Importance
- Recency
- Frequency of retrieval

Frequently useful memories persist; stale low-value memories decay.

## Relationship to Discoveries

Discoveries and memories form a closed learning loop:

- Discoveries create opportunities to capture or refine memory
- Review decisions confirm or challenge agent assumptions
- Memory updates shape future monitoring and analysis quality
