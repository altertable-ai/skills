# Memory Types Reference

Detailed guide to memory type classification.

## Episodic Memory

### Definition

Memories of specific events and experiences.

### Characteristics

- Time-bound
- Context-rich
- Personally experienced
- Sequentially organized

### Examples

```
"On Monday at 2pm, user asked about revenue drop"
"Discovery about churn spike was rejected on Jan 15"
"User said they prefer shorter summaries during morning standup"
```

### When to Use

- Recording interactions
- Tracking discoveries
- Noting feedback events
- Documenting conversations

### Structure

```yaml
type: episodic
content: "User requested weekly revenue analysis"
context:
  when: "2024-01-15T14:30:00Z"
  where: "Dashboard review session"
  who: "User and Nelson"
  what_happened: "Discussed revenue trends"
```

### Decay Pattern

- Recent episodes: High strength
- Older episodes: Gradual decay
- Accessed episodes: Reinforced
- Similar episodes: May consolidate

## Semantic Memory

### Definition

General knowledge and facts, independent of specific events.

### Characteristics

- Context-independent
- Factual
- Conceptual relationships
- Organized by meaning

### Examples

```
"User prefers daily summaries over weekly"
"Revenue is the most important metric for this org"
"The marketing team uses Dashboard X for campaigns"
```

### When to Use

- User preferences
- Business knowledge
- Domain facts
- Relationships
- Definitions

### Structure

```yaml
type: semantic
content: "User prefers concise bullet points over paragraphs"
entities:
  - type: user
    id: user_123
tags:
  - preference
  - formatting
```

### Decay Pattern

- Core facts: Very slow decay
- Preferences: Moderate decay
- Contextual: Faster decay
- Validated: Reinforced

## Procedural Memory

### Definition

Knowledge of how to do things.

### Characteristics

- Action-oriented
- Step-by-step
- Skill-based
- Often implicit

### Examples

```
"To create a funnel: 1) Define steps 2) Set time window 3) Add filters"
"When analyzing charts, first check the time range"
"For data quality issues, query the connection first"
```

### When to Use

- Workflows
- Best practices
- Techniques
- Processes
- Methods

### Structure

```yaml
type: procedural
content: |
  Creating a segment:
  1. Identify target population
  2. Choose primary dimension
  3. Add filter conditions
  4. Validate segment size
  5. Document purpose
tags:
  - workflow
  - segments
```

### Decay Pattern

- Core procedures: Very slow
- Context-specific: Moderate
- Rarely used: Faster decay
- Successfully used: Reinforced

## Choosing Memory Type

### Decision Framework

| Question | Yes → Type |
|----------|------------|
| Is this a specific event? | Episodic |
| Is this a general fact? | Semantic |
| Is this how to do something? | Procedural |

### Hybrid Memories

Some memories span types:

**Episodic → Semantic**
```
Event: "User said they dislike long reports"
Becomes: "User preference: concise reports"
```

**Episodic → Procedural**
```
Event: "Funnel analysis failed due to wrong time window"
Becomes: "Always verify time window before funnel analysis"
```

## Memory Type Transitions

### Consolidation

Multiple episodic → One semantic:
```
Episodes:
- "User asked for short summary on Monday"
- "User asked for brief update on Tuesday"
- "User said 'keep it short' on Wednesday"

Consolidates to:
Semantic: "User consistently prefers brief communications"
```

### Abstraction

Specific episodes → General procedure:
```
Episodes:
- "Fixed chart by changing date range"
- "Fixed dashboard by adjusting filters"
- "Fixed report by updating parameters"

Abstracts to:
Procedural: "When output looks wrong, verify parameters first"
```

## Storage Considerations

### Episodic

- Higher storage per memory
- Rich context preserved
- More temporal metadata
- Query by time range

### Semantic

- Moderate storage
- Entity relationships
- Query by concept
- Good for preferences

### Procedural

- Variable storage
- Step structure
- Query by action
- Good for workflows
