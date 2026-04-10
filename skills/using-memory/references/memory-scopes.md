# Memory Scopes Reference

## Scope Hierarchy

```
Organization (broadest)
    └── Workflow
        └── Agent
            └── Entity (narrowest)
```

## Organization

Knowledge that applies to everyone in the org.

**Use for:**
- Business rules and thresholds
- Company-wide preferences
- Domain terminology
- Standard procedures

**Examples:**
- "Organization ignores metric changes under 20%"
- "Fiscal year starts in April"
- "MRR means Monthly Recurring Revenue"

**Visibility:** All agents and users in the organization

## Workflow

Context specific to a workflow type.

**Use for:**
- Patterns for this analysis type
- Workflow-specific learnings
- Session context

**Examples:**
- "Revenue analysis workflow: always check seasonality first"
- "Funnel workflows need strict event ordering"

**Visibility:** Current workflow only

## Agent

Knowledge private to a specific agent.

**Use for:**
- Agent-specific optimizations
- Personal learnings
- Specialized expertise

**Examples:**
- "I work faster with CTEs than subqueries"
- "My analysis style emphasizes visualization"

**Visibility:** Single agent only

## Entity

Facts about a specific entity (insight, discovery, table).

**Use for:**
- Entity-specific preferences
- Historical context
- Relationship information

**Examples:**
- "INS-123: User prefers weekly refresh"
- "DSC-456: Was rejected for being too granular"
- "events_table: Has NULL values on weekends"

**Visibility:** When working with that entity

## Quick Decision

1. **Does this apply to the entire organization?** → Organization
2. **Is this specific to this workflow type?** → Workflow
3. **Is this about a specific entity?** → Entity
4. **Is this my personal learning?** → Agent

## Scope Promotion

Patterns can be promoted to broader scopes:

```
Entity learning → Workflow pattern → Organization rule
```

Example:
- Entity: "INS-123 rejected for low threshold"
- Workflow: "Revenue insights need >15% change"
- Organization: "All insights need >20% change to be actionable"
