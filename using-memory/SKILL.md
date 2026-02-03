---
name: using-memory
compatibility: Altertable
description: Stores and retrieves agent memories for learning and context persistence. Use when saving findings, recalling past analysis, building knowledge, managing memory lifecycle, or understanding forgetting curves.
---

# Using Memory

## Quick Start

Memory enables agents to:
1. Remember past interactions
2. Learn from experience
3. Build knowledge over time
4. Maintain context across sessions

## When to Use This Skill

- Saving important findings
- Recalling past analysis
- Building persistent knowledge
- Managing memory lifecycle
- Understanding memory decay
- Searching for relevant context

## Memory Types

| Type | Purpose | Example |
|------|---------|---------|
| `episodic` | Specific events | "User asked about revenue on Monday" |
| `semantic` | Facts and knowledge | "User prefers weekly summaries" |
| `procedural` | How-to knowledge | "Steps to create a funnel" |

### Episodic Memory

What happened:
- Conversations
- Discoveries made
- User interactions
- Specific analyses

### Semantic Memory

What is known:
- User preferences
- Business context
- Domain knowledge
- Relationships

### Procedural Memory

How to do things:
- Workflows
- Best practices
- Patterns
- Techniques

## Memory Scopes

| Scope | Visibility | Use Case |
|-------|------------|----------|
| `organization` | All in org | Company-wide knowledge |
| `workflow` | Current workflow | Session context |
| `agent` | Single agent | Agent-specific learning |
| `entity` | About entity | User/resource knowledge |

### Organization Scope

Shared across organization:
- Company terminology
- Business rules
- Shared preferences
- Standard procedures

### Workflow Scope

Current conversation:
- Session context
- Active topic
- Recent findings
- Temporary state

### Agent Scope

Agent-specific:
- Personal learnings
- Individual style
- Specialized knowledge
- Performance patterns

### Entity Scope

About specific entities:
- User preferences
- Resource details
- Historical context
- Relationships

## Creating Memories

### What to Remember

Remember things that:
- Will be useful later
- Are hard to rediscover
- Represent learnings
- Indicate preferences

### Memory Content

Include:
- Clear summary
- Relevant context
- Source reference
- Timestamp indication

### Importance Rating

| Score | Meaning | Decay Rate |
|-------|---------|------------|
| 9-10 | Critical | Very slow |
| 7-8 | Important | Slow |
| 5-6 | Standard | Normal |
| 3-4 | Minor | Fast |
| 1-2 | Trivial | Very fast |

## Searching Memories

### Semantic Search

Find relevant memories by:
- Natural language query
- Topic similarity
- Context matching
- Entity association

### Filtering

Narrow results by:
- Memory type
- Scope
- Time range
- Tags
- Author

### Ranking

Results ranked by:
- Relevance to query
- Importance score
- Recency
- Access frequency

## Memory Lifecycle

### Creation

When memory is formed:
- Content captured
- Metadata attached
- Importance assigned
- Initial strength set

### Consolidation

Over time:
- Related memories link
- Patterns emerge
- Knowledge strengthens
- Redundancy reduced

### Decay

Without reinforcement:
- Strength decreases
- Relevance fades
- Eventually forgotten
- Space reclaimed

### Reinforcement

When accessed/validated:
- Strength increases
- Decay resets
- Importance adjusted
- Connections strengthen

## Forgetting Curve

### Decay Rates

| Rate | Half-life | Use For |
|------|-----------|---------|
| `hourly` | ~24h | Session context |
| `daily` | ~168h | Short-term |
| `weekly` | ~720h | Medium-term |
| `monthly` | ~4320h | Long-term |

### Factors Affecting Decay

- Initial importance
- Access frequency
- Validation events
- Connection count

## Best Practices

### Creating Memories

- Be specific, not vague
- Include context
- Set appropriate importance
- Use descriptive tags
- Link to entities

### Searching Memories

- Use natural language
- Try multiple queries
- Filter appropriately
- Check relevance

### Managing Lifecycle

- Review periodically
- Validate important memories
- Clean up outdated
- Consolidate related

## Memory Patterns

### Learning Pattern

1. Experience event
2. Extract learning
3. Create memory
4. Apply in future

### Preference Pattern

1. Observe preference
2. Confirm with user
3. Store as semantic
4. Apply consistently

### Context Pattern

1. Start conversation
2. Search relevant memories
3. Load context
4. Use in responses

### Feedback Pattern

1. Receive feedback
2. Interpret intent
3. Update memories
4. Adjust behavior

## Common Pitfalls

- Storing too much detail
- Missing important context
- Wrong importance scores
- Not searching before acting
- Ignoring memory decay
- Duplicate memories

## Reference Files

- [Memory types](references/memory-types.md)
- [Memory scopes](references/memory-scopes.md)
- [Forgetting curve](references/forgetting-curve.md)
