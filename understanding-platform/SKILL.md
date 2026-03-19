---
name: understanding-platform
compatibility: Requires Altertable MCP server
description: Explains Altertable platform concepts and architecture. Use when user asks about organizations, environments, connections, versioning, or how the platform works.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Understanding Platform

## Quick Start

Altertable is a data intelligence platform that:
1. Connects to data sources
2. Models data semantically
3. Creates discoveries through agents
4. Learns and remembers context

## When to Use This Skill

- Explaining platform concepts
- Understanding architecture
- Navigating organization structure
- Working with environments
- Managing connections
- Understanding versioning

## Core Concepts

### Organization

Top-level entity containing:
- Users and teams
- Environments
- Connections
- Agents and watchers
- Memories and discoveries

### Environment

Isolated workspace within organization:
- Separate data contexts
- Independent configurations
- Own semantic models
- Distinct memories

### Connection

Link to external data source:
- Database connections
- Data warehouse links
- API integrations
- File sources

## Architecture Overview

```
Organization
├── Users/Teams
├── Environments
│   ├── Connections
│   ├── Semantic Sources
│   ├── Dashboards/Charts
│   ├── Segments
│   ├── Watchers
│   └── Memories
└── Discoveries
```

## Key Components

### Semantic Layer

Abstraction over raw data:
- Dimensions (attributes)
- Measures (metrics)
- Relations (joins)
- Sources (tables)

### Agents

AI entities that:
- Analyze data
- Create discoveries
- Learn from feedback
- Execute tasks

### Watchers

Automated monitors that:
- Run on schedules
- Watch for changes
- Create discoveries
- Alert on conditions

### Discoveries

Insights that flow through:
- Creation
- Approval
- Delivery
- Review

### Memory

Persistent knowledge:
- Episodic (events)
- Semantic (facts)
- Procedural (how-to)

## Platform Workflow

### Data Flow

```
Raw Data → Connection → Semantic Model → Analysis → Discovery → User
```

### Analysis Flow

```
Question → Agent → Query → Results → Insight → Discovery
```

### Learning Flow

```
Feedback → Intent Detection → Memory → Future Behavior
```

## Environment Types

### Production

Live environment:
- Real data
- Active users
- Critical operations
- Careful changes

### Staging

Test environment:
- Production-like
- Safe to experiment
- Validation space
- Pre-production

### Development

Build environment:
- Experimentation
- New features
- Model development
- Low risk

## Version Control

### Semantic Model Versioning

Models are versioned:
- Track changes
- Rollback capability
- Audit trail
- Collaboration

### Version States

| State | Description |
|-------|-------------|
| draft | Work in progress |
| published | Active version |
| archived | Previous version |

### Publishing Workflow

```
Create draft → Make changes → Review → Publish → Active
```

## Connection Types

### Databases

Direct database connections:
- PostgreSQL
- MySQL
- SQL Server
- Oracle

### Data Warehouses

Warehouse connections:
- Snowflake
- BigQuery
- Redshift
- Databricks

### DuckDB Lakehouse

Built-in analytics:
- Local processing
- Fast queries
- File-based data
- SQL interface

## User Roles

### Organization Level

| Role | Capabilities |
|------|--------------|
| Owner | Full control |
| Admin | Configuration access |
| Member | Standard access |
| Viewer | Read-only |

### Resource Level

| Role | Capabilities |
|------|--------------|
| Editor | Modify resource |
| Viewer | View resource |
| None | No access |

## Resource Types

### Data Resources

- Connections
- Semantic Sources
- Tables/Views

### Analytics Resources

- Dashboards
- Charts
- Segments
- Funnels

### Automation Resources

- Watchers
- Agents
- Workflows

### Knowledge Resources

- Memories
- Discoveries
- Reports

## Platform APIs

### GraphQL API

Main interface for:
- Data operations
- Resource management
- Analysis requests
- Discovery handling

### MCP Protocol

Agent interface for:
- Tool execution
- Memory operations
- Discovery creation
- Context access

## Best Practices

### Organization Setup

- Clear naming conventions
- Appropriate user roles
- Environment separation
- Connection management

### Environment Management

- Separate prod from dev
- Test in staging
- Document differences
- Sync configurations

### Connection Security

- Secure credentials
- Minimal permissions
- Regular rotation
- Access logging

## Common Pitfalls

- Mixing environments
- Unclear resource ownership
- Over-permissive access
- Unversioned changes
- Missing documentation

## Reference Files

- [Organization model](references/organization-model.md)
- [Environments](references/environments.md)
- [Versioning](references/versioning.md)
- [Connections](references/connections.md)
