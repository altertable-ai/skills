# Memory Scopes Reference

Guide to memory visibility and access scopes.

## Scope Hierarchy

```
Organization (broadest)
    └── Workflow
        └── Agent
            └── Entity (narrowest)
```

## Organization Scope

### Definition

Memories visible to all agents and users in the organization.

### Characteristics

- Broadest visibility
- Shared knowledge
- Company-wide relevance
- Persistent

### Use Cases

| Use Case | Example |
|----------|---------|
| Business terminology | "MRR means Monthly Recurring Revenue" |
| Standard procedures | "All reports require approval" |
| Shared preferences | "Company uses fiscal year starting April" |
| Domain knowledge | "Product X launched in Q3 2023" |

### Best Practices

- Only store widely relevant information
- Ensure accuracy (affects everyone)
- Use for stable, long-term knowledge
- Review periodically for relevance

### Access Pattern

```
Any agent in org → Can read
Authorized agents → Can write
Admins → Can delete/modify
```

## Workflow Scope

### Definition

Memories specific to the current conversation or workflow.

### Characteristics

- Session-bound
- Temporary context
- Current task focus
- Auto-expires

### Use Cases

| Use Case | Example |
|----------|---------|
| Active topic | "Currently analyzing Q4 revenue" |
| Session context | "User started by asking about churn" |
| Working state | "Already queried customers table" |
| Pending tasks | "Need to follow up on anomaly" |

### Best Practices

- Use for temporary context
- Don't rely on long-term persistence
- Clear when workflow completes
- Transfer important learnings to other scopes

### Access Pattern

```
Current workflow → Full access
Other workflows → No access
Workflow end → May expire
```

## Agent Scope

### Definition

Memories private to a specific agent.

### Characteristics

- Agent-specific
- Personal learning
- Not shared
- Specialized knowledge

### Use Cases

| Use Case | Example |
|----------|---------|
| Personal style | "I format tables with headers" |
| Agent learning | "This approach worked for me" |
| Specialized knowledge | "My domain expertise in funnels" |
| Performance patterns | "Complex queries take longer" |

### Best Practices

- Use for agent-specific optimizations
- Store personal learnings
- Keep specialized knowledge
- Don't duplicate org-level info

### Access Pattern

```
Own agent → Full access
Other agents → No access
Agent replacement → May transfer
```

## Entity Scope

### Definition

Memories about or for specific entities (users, resources).

### Characteristics

- Entity-bound
- Contextual to entity
- Follows entity lifecycle
- Highly specific

### Use Cases

| Use Case | Example |
|----------|---------|
| User preferences | "User X prefers weekly reports" |
| Resource details | "Dashboard Y tracks marketing" |
| Relationship context | "User is CMO, focuses on growth" |
| Historical interaction | "Last discussed churn on Jan 5" |

### Best Practices

- Link clearly to entity
- Update when entity changes
- Clean up when entity removed
- Keep relevant and current

### Access Pattern

```
Entity context → Full access
Related queries → Searchable
Entity deletion → May archive
```

## Scope Selection

### Decision Tree

```
Is this org-wide knowledge?
├── Yes → Organization
└── No
    ├── Is this session-specific?
    │   ├── Yes → Workflow
    │   └── No
    │       ├── Is this about a specific entity?
    │       │   ├── Yes → Entity
    │       │   └── No → Agent
```

### Scope Comparison

| Factor | Organization | Workflow | Agent | Entity |
|--------|--------------|----------|-------|--------|
| Visibility | All | Session | Self | Contextual |
| Duration | Long | Short | Medium | Medium |
| Audience | Everyone | Current | Self | Specific |
| Examples | Policies | Context | Learning | Preferences |

## Scope Interactions

### Cross-Scope Search

When searching, typically:
1. Check workflow scope first (current context)
2. Check entity scope (if entity relevant)
3. Check agent scope (personal knowledge)
4. Check organization scope (shared knowledge)

### Scope Promotion

Memories can move up in scope:
```
Workflow finding → Organization knowledge
Agent learning → Organization procedure
Entity preference → Organization default
```

### Scope Demotion

Less common, but possible:
```
Organization → Entity override
Agent → Workflow specific
```

## Privacy Considerations

### Sensitive Information

| Scope | Sensitivity |
|-------|-------------|
| Organization | Low (shared) |
| Workflow | Medium (temporary) |
| Agent | High (private) |
| Entity | High (personal) |

### Access Control

- Organization: All authorized users
- Workflow: Participants only
- Agent: Agent only
- Entity: Entity owner + relevant agents
