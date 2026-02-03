# Organization Model Reference

Detailed guide to organization structure.

## Organization Hierarchy

```
Organization
├── Settings
│   ├── Billing
│   ├── Security
│   └── Integrations
├── Members
│   ├── Users
│   └── Teams
├── Environments
│   └── (see environments.md)
└── Global Resources
    ├── Agent Configurations
    └── Shared Templates
```

## Organization Properties

### Identity

| Property | Description |
|----------|-------------|
| `id` | Unique identifier |
| `name` | Display name |
| `slug` | URL-safe identifier |
| `created_at` | Creation timestamp |

### Configuration

| Property | Description |
|----------|-------------|
| `plan` | Subscription tier |
| `quota` | Resource limits |
| `features` | Enabled features |
| `settings` | Custom configuration |

## Membership

### User Roles

| Role | Access Level |
|------|--------------|
| `owner` | Full administrative control |
| `admin` | Configuration and management |
| `member` | Standard operational access |
| `viewer` | Read-only access |

### Role Capabilities

**Owner:**
- All admin capabilities
- Delete organization
- Transfer ownership
- Manage billing

**Admin:**
- Manage members
- Configure environments
- Manage connections
- View all resources

**Member:**
- Create resources
- Use agents
- View discoveries
- Limited configuration

**Viewer:**
- View dashboards
- Read discoveries
- No modification
- No creation

## Teams

### Team Structure

```yaml
team:
  name: "Marketing Analytics"
  members:
    - user_id: user_1
      role: lead
    - user_id: user_2
      role: member
  permissions:
    dashboards: [dashboard_1, dashboard_2]
    connections: [connection_1]
```

### Team Permissions

Teams can have access to:
- Specific dashboards
- Specific connections
- Specific environments
- Specific resources

## Resource Ownership

### Ownership Model

Every resource has:
- `created_by` - Original creator
- `owner` - Current owner
- `organization` - Parent org

### Access Control

Resources inherit from:
1. Organization defaults
2. Environment settings
3. Resource-specific permissions

## Quotas and Limits

### Plan-Based Limits

| Resource | Starter | Pro | Enterprise |
|----------|---------|-----|------------|
| Users | 5 | 25 | Unlimited |
| Environments | 1 | 3 | Unlimited |
| Connections | 3 | 10 | Unlimited |
| Watchers | 50 | 200 | 500+ |

### Usage Tracking

Monitor usage of:
- Active watchers
- Query volume
- Storage used
- API calls

## Settings

### General Settings

| Setting | Description |
|---------|-------------|
| Timezone | Default timezone |
| Date format | Display format |
| Currency | Default currency |
| Language | Interface language |

### Security Settings

| Setting | Description |
|---------|-------------|
| SSO | Single sign-on |
| MFA | Multi-factor auth |
| IP whitelist | Allowed IPs |
| Session timeout | Auto logout |

### Integration Settings

| Setting | Description |
|---------|-------------|
| Slack | Notifications |
| Email | Alerts |
| Webhooks | Custom integrations |
| API keys | External access |

## Multi-Tenancy

### Isolation

Each organization has:
- Separate data
- Separate users
- Separate configuration
- Separate billing

### Cross-Org

No sharing between organizations:
- No data sharing
- No user sharing
- No resource sharing

## Audit and Compliance

### Audit Log

Track organization events:
- User actions
- Configuration changes
- Resource modifications
- Access events

### Compliance Features

| Feature | Description |
|---------|-------------|
| Data residency | Location control |
| Retention | Data lifecycle |
| Export | Data portability |
| Deletion | Right to forget |
