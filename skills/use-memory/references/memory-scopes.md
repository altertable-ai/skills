# Memory Scopes Reference

Scopes classify retrieval breadth and influence default decay. They are not equivalent to access-control boundaries. Only `user` scope enforces owner filtering. Searches for `workflow`, `agent`, and `entity` scopes filter by the scope value, not by a workflow, agent, or entity identifier. Do not store sensitive context under those scopes on the assumption that the label makes it private.

## Scope Hierarchy

```
Organization (broadest)
    └── Workflow
        └── Agent
            └── Entity
                └── User (narrowest)
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

**Retrieval:** Broadest non-user classification within the environment.

## Workflow

Knowledge labeled as specific to a workflow type.

**Use for:**
- Patterns for this analysis type
- Workflow-specific learnings
- Reusable workflow context

**Examples:**
- "Revenue analysis workflow: always check seasonality first"
- "Funnel workflows need strict event ordering"

**Retrieval:** Scope filtering does not restrict results to one workflow instance.

## Agent

Knowledge labeled as agent-specific.

**Use for:**
- Agent-specific optimizations
- Personal learnings
- Specialized expertise

**Examples:**
- "I work faster with CTEs than subqueries"
- "My analysis style emphasizes visualization"

**Retrieval:** Scope filtering does not restrict results to the creating agent.

## Entity

Knowledge labeled as specific to an entity (insight, discovery, table).

**Use for:**
- Entity-specific preferences
- Historical context
- Relationship information

**Examples:**
- "INS-123: User prefers weekly refresh"
- "DSC-456: Was rejected for being too granular"
- "events_table: Has NULL values on weekends"

**Retrieval:** Add entity slugs to `entities`, then pass the same slugs to `search_memory` to filter by them. The scope alone does not restrict results to an entity.

## User

Context or preferences that should be visible only to one user.

**Use for:**
- User-specific preferences
- Personal working context
- Information that should not become an organization-wide rule

**Retrieval:** The owning user only. User scope is available only in user sessions, not agentic workflows.

## Quick Decision

1. **Does this apply to the entire organization?** → Organization
2. **Is this specific to one user, and is the current author a user?** → User
3. **Is this specific to this workflow type?** → Workflow
4. **Is this about a specific entity?** → Entity
5. **Is this my personal learning?** → Agent

## Scope Promotion

Patterns can be promoted to broader scopes:

```
Entity learning → Workflow pattern → Organization rule
```

Example:
- Entity: "INS-123 rejected for low threshold"
- Workflow: "Revenue insights need >15% change"
- Organization: "All insights need >20% change to be actionable"
