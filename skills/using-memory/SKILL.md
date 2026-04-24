---
name: using-memory
compatibility: Requires Altertable MCP server
description: Stores and retrieves agent memories for learning and context persistence. Use when saving findings, recalling past analysis, building knowledge, or searching for relevant context.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Using Memory

## Purpose

Memory transforms agents from stateless tools into learning entities. Instead of starting fresh each run, agents can:
- Recall what worked before
- Avoid repeating mistakes
- Apply organization-specific knowledge
- Build expertise over time

## When to Search

**At the start of every workflow** - proactively recall relevant context before taking action.

Search when:
- Beginning a new analysis
- Before creating discoveries or insights
- When context from past runs would help
- When working with familiar entities (tables, metrics, users)

## When to Create

**Only after something valuable happens** - quality over quantity.

Create a memory when:
- A discovery was approved or rejected (learn from feedback)
- You found an organization-specific pattern or threshold
- A technique worked well (or failed in a specific context)
- You learned something that would help future runs

**Do not create memories for:**
- Routine success ("query returned results")
- Minor details ("table has 1M rows")
- Information easily re-discoverable
- Duplicates of existing memories

## Memory Types

### Episodic - What Happened

Record specific events with outcomes.

**Use when:** Something happened that you should remember
- Discovery was created, approved, or rejected
- Analysis succeeded or failed
- User gave feedback

**Include:** The outcome (success, failure, rejected, approved)

**Example:** "Created DSC-789 for 15% revenue drop. User rejected - said threshold should be 20%."

### Semantic - What You Know

Record facts and knowledge independent of specific events.

**Use when:** You learned a fact or pattern
- Organization prefers certain thresholds
- Data has specific characteristics
- Business rules or preferences

**Include:** Confidence level if uncertain

**Example:** "Organization ignores metric changes under 20% - confirmed by user feedback."

### Procedural - How To Do Things

Record techniques and approaches that work.

**Use when:** You discovered a technique
- Query pattern that performs well
- Workaround for a limitation
- Best practice for a specific situation

**Include:** Success rate and failure contexts

**Example:** "For sales table: use date_trunc with timezone filter for accurate daily aggregations. Fails without timezone on UTC data."

## Decision Tree

1. **Did something HAPPEN?** (event with outcome)
   → Episodic

2. **Did you LEARN A FACT?** (pattern, threshold, preference)
   → Semantic

3. **Did you DISCOVER A TECHNIQUE?** (approach, workaround)
   → Procedural

4. **None of the above?**
   → Probably not worth saving

## Decision Matrix

Quick reference for common situations:

| Situation | Type | Scope | Importance | Decay |
|-----------|------|-------|------------|-------|
| Discovery approved | Episodic | Workflow | 8 | Weekly |
| Discovery rejected with feedback | Episodic | Workflow | 9 | Monthly |
| User stated preference | Semantic | Organization | 9 | Monthly |
| Data pattern found | Semantic | Organization | 7 | Weekly |
| Query optimization worked | Procedural | Organization | 8 | Monthly |
| Workaround for edge case | Procedural | Workflow | 6 | Weekly |
| Entity-specific behavior | Semantic | Entity | 7 | Weekly |
| Workflow failed for specific reason | Episodic | Workflow | 8 | Weekly |
| Business rule confirmed | Semantic | Organization | 9 | Monthly |
| Technique failed in context | Procedural | Workflow | 7 | Weekly |

## Memory Scopes

### Organization
Knowledge that applies to everyone in the org.
- Business rules and thresholds
- Company-wide preferences
- Domain terminology

### Workflow
Context specific to this workflow type.
- Patterns for this analysis type
- Workflow-specific learnings

### Agent
Knowledge private to a specific agent.
- Agent-specific optimizations
- Personal learnings
- Specialized expertise

### Entity
Facts about a specific entity (insight, discovery, table).
- Entity-specific preferences
- Historical context for that entity

### Scope Decision Tree

1. **Does this apply to the entire organization?**
   → Organization

2. **Is this specific to this workflow type?**
   → Workflow

3. **Is this about a specific entity (INS-*, DSC-*)?**
   → Entity

4. **Is this my personal learning/optimization?**
   → Agent

## Source Linking

Link memories to specific entities when relevant:
- **Insights**: INS-123
- **Discoveries**: DSC-456
- **Segments**: SGM-789
- **Dashboards**: DSH-101

This enables searching for all memories related to a specific entity.

## Importance

Rate importance honestly - it affects how long memories persist.

| Score | Meaning | Examples |
|-------|---------|----------|
| 9-10 | Critical | Major outage cause, critical business rule |
| 7-8 | Valuable | Clear pattern, confirmed preference |
| 5-6 | Moderate | Potentially useful, unconfirmed |
| 1-4 | Low | Minor detail, easily rediscovered |

**Guideline:** Only save memories with importance >= 7. Lower importance creates noise.

## Forgetting Curve

Memories decay over time without reinforcement.

- **Searching** reinforces memories (they stay relevant longer)
- **Higher importance** = slower decay
- **Frequent access** = slower decay

Decay rates:
- **Daily** - Session context, temporary learnings
- **Weekly** - Short-term patterns (default)
- **Monthly** - Core knowledge, stable facts

## Consolidation

Over time, the system automatically:

**Episodic → Semantic**: When multiple similar events occur, they get abstracted into a general pattern.
- 3+ similar episodic memories → 1 semantic memory
- Example: "Revenue drop triggered discovery" (x3) → "Revenue anomalies consistently trigger discoveries"

**Procedural merging**: Similar techniques get consolidated into best practices.
- Preserves success rates and failure contexts

**Scope promotion**: Patterns seen across multiple workflows get promoted to organization scope.
- Workflow patterns that repeat → Organization-level knowledge

## Writing Effective Content

Good memories are **specific**, **actionable**, and **include context**.

### Good vs Bad Examples

| Bad | Good |
|-----|------|
| "Revenue issue" | "Revenue dropped 15% in Q4 due to seasonal churn" |
| "User didn't like it" | "User rejected DSC-123 - said 10% threshold is too low, prefers 20%" |
| "Query was slow" | "Sales table aggregation: use date_trunc with index, reduced from 30s to 2s" |
| "Something about funnels" | "Funnel analysis requires strict event ordering for accurate conversion rates" |

### Content Checklist

- **What happened or what did you learn?** (the core fact)
- **Why does it matter?** (impact or implication)
- **What should change?** (actionable guidance)
- **Any constraints?** (when this applies or doesn't)

## Best Practices

### Searching
- Search broadly at workflow start
- Use natural language queries
- Filter by type when you know what you need
- Search parent scopes to find org-level knowledge

### Creating
- Be specific, not vague
- Include context that makes the memory actionable
- Set importance honestly
- Add relevant tags for discoverability
- Link to entities when applicable

### Quality Over Quantity
- One high-quality memory > many low-quality ones
- If unsure whether to save, don't
- Duplicate memories create noise
- Let unimportant memories decay naturally

## Common Pitfalls

- Not searching at workflow start (missing valuable context)
- Saving everything (creates noise, reduces signal)
- Vague content ("something happened with revenue")
- Wrong type selection (fact stored as event)
- Importance inflation (everything marked as 9-10)
- Missing outcome for episodic memories
- Missing success_rate for procedural memories

## Troubleshooting

**Search returns no results:**
- Broaden query terms (use synonyms, related concepts)
- Search parent scopes (workflow → organization)
- Check if memories existed but decayed (low importance + no recent access)

**Search returns low relevance:**
- Refine query to be more specific
- Filter by memory type if you know what you need
- Results may have decayed - consider if re-learning is needed

**Expected memory is missing:**
- May have decayed due to low importance or infrequent access
- Check if it was saved at wrong scope (entity vs workflow)
- Re-create if the knowledge is still valuable

**Too much noise in results:**
- Be more selective when creating (importance >= 7)
- Let low-value memories decay naturally
- Use more specific search queries

## Reference Files

- [Memory types](references/memory-types.md) - Read when choosing between episodic, semantic, and procedural memory types
- [Memory scopes](references/memory-scopes.md) - Read when deciding the right scope (organization, workflow, agent, entity, user)
- [Forgetting curve](references/forgetting-curve.md) - Read when tuning decay rates or understanding why memories disappeared
