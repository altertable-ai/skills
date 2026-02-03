# Environments Reference

Guide to environment management.

## Environment Concept

### Definition

An environment is an isolated workspace containing:
- Its own connections
- Its own semantic models
- Its own resources
- Its own memories

### Purpose

Environments enable:
- Separation of concerns
- Safe experimentation
- Staged deployments
- Access control

## Environment Types

### Production

**Characteristics:**
- Live data
- Real users
- Critical operations
- Change control

**Best for:**
- Daily operations
- Real analysis
- Live dashboards
- Production agents

### Staging

**Characteristics:**
- Production-like
- Test data (or prod copy)
- Pre-deployment
- Validation

**Best for:**
- Testing changes
- Validating models
- User acceptance
- Performance testing

### Development

**Characteristics:**
- Experimental
- Sandbox data
- Low risk
- High flexibility

**Best for:**
- Building models
- Trying ideas
- Learning
- Prototyping

## Environment Structure

```
Environment
├── Connections
│   └── Data sources
├── Semantic Sources
│   ├── Dimensions
│   ├── Measures
│   └── Relations
├── Resources
│   ├── Dashboards
│   ├── Charts
│   ├── Segments
│   └── Funnels
├── Automation
│   ├── Watchers
│   └── Workflows
└── Knowledge
    └── Memories
```

## Environment Configuration

### Properties

| Property | Description |
|----------|-------------|
| `name` | Display name |
| `slug` | URL identifier |
| `type` | production/staging/development |
| `settings` | Environment config |

### Settings

| Setting | Description |
|---------|-------------|
| Default timezone | Query timezone |
| Data retention | How long to keep data |
| Agent config | Agent behavior |
| Notification rules | Alert settings |

## Environment Isolation

### What's Isolated

| Resource | Isolated? |
|----------|-----------|
| Connections | Yes |
| Semantic models | Yes |
| Dashboards | Yes |
| Memories | Yes |
| Users | No (org-level) |

### Cross-Environment

Generally avoided:
- No direct data sharing
- No memory sharing
- No resource sharing
- Manual sync if needed

## Environment Workflow

### Development Flow

```
Development → Staging → Production
```

1. Build in development
2. Test in staging
3. Deploy to production
4. Monitor and iterate

### Promotion

Moving resources between environments:

1. Export from source
2. Review changes
3. Import to target
4. Validate
5. Activate

## Access Control

### Environment Permissions

| Permission | Description |
|------------|-------------|
| `admin` | Full environment control |
| `write` | Create and modify resources |
| `read` | View resources only |
| `none` | No access |

### Role Mapping

| Org Role | Default Env Access |
|----------|-------------------|
| Owner | Admin on all |
| Admin | Admin on all |
| Member | Write on assigned |
| Viewer | Read on assigned |

## Environment Operations

### Creating Environments

Consider:
- Purpose and type
- Data sources needed
- Users who need access
- Naming convention

### Copying Environments

To clone an environment:
1. Export configuration
2. Create new environment
3. Import configuration
4. Update connections
5. Validate

### Deleting Environments

Before deletion:
- Archive important data
- Notify users
- Export configurations
- Document learnings

## Best Practices

### Naming Convention

```
{purpose}-{descriptor}
```

Examples:
- `prod-main`
- `staging-v2`
- `dev-experiment-1`

### Environment Parity

Keep environments similar:
- Same schema structure
- Same model definitions
- Same configurations
- Different data

### Change Management

For production:
- Test in lower environments
- Document changes
- Review before deploy
- Have rollback plan

## Common Patterns

### Feature Development

```
1. Create dev environment
2. Build and test feature
3. Promote to staging
4. User acceptance testing
5. Deploy to production
```

### Data Refresh

```
1. Schedule refresh in staging
2. Validate data quality
3. Update production if needed
```

### Experimentation

```
1. Clone environment
2. Try experiments
3. Measure results
4. Adopt or discard
```
