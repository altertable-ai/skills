# Identity Resolution Reference

Guide to user identity management and resolution.

## Identity Concepts

### User Identity

A user has multiple identifiers:

```
User Profile
├── Anonymous IDs (pre-login)
│   ├── anon_abc123
│   └── anon_def456
├── User ID (post-login)
│   └── user_789
├── Device IDs
│   ├── device_mobile_111
│   └── device_desktop_222
└── External IDs
    ├── stripe_cus_xyz
    └── salesforce_00123
```

### Identity Graph

Relationships between identities:

```
anon_abc123 ──────┐
                  │
anon_def456 ──────┼──→ user_789 (canonical)
                  │
device_mobile ────┤
                  │
stripe_cus_xyz ───┘
```

## Identity Operations

### Identify

Link anonymous to known user:

```yaml
operation: identify
anonymous_id: anon_abc123
user_id: user_789
traits:
  email: user@example.com
```

**When to Use:**
- User logs in
- User signs up
- User authenticates

### Alias

Link two identities:

```yaml
operation: alias
previous_id: anon_abc123
user_id: user_789
```

**When to Use:**
- Linking anonymous session to user
- Merging duplicate profiles
- Cross-device linking

### Merge

Combine two profiles:

```yaml
operation: merge
primary_id: user_789
secondary_id: user_duplicate_456
strategy: prefer_primary
```

**When to Use:**
- Duplicate user cleanup
- Account consolidation
- Data migration

## Identity Types

### Anonymous ID

**Characteristics:**
- Generated automatically
- Device/browser specific
- Persists until identified
- Can be multiple per user

**Generation:**
```
UUID or fingerprint-based
Example: anon_a1b2c3d4-e5f6-7890
```

### User ID

**Characteristics:**
- Your system's identifier
- Unique per user
- Permanent
- Canonical identity

**Best Practices:**
- Use stable IDs (not email)
- Don't use PII directly
- Keep consistent across systems

### Device ID

**Characteristics:**
- Per device
- May persist across sessions
- Used for cross-session tracking

### External ID

**Characteristics:**
- From third-party systems
- Enables integration
- Multiple per user possible

## Resolution Strategies

### Simple Resolution

One anonymous → one user:

```
anon_123 → (login) → user_456
```

### Cross-Device Resolution

Multiple devices → one user:

```
anon_mobile_123 ─┐
                 ├─→ user_456
anon_desktop_789 ┘
```

### Cross-Session Resolution

Multiple sessions → one user:

```
session_1 (anon_abc) ─┐
                      ├─→ user_456
session_2 (anon_def) ─┘
session_3 (user_456) ─┘
```

## Resolution Rules

### Precedence

When merging identities:

1. User ID (highest priority)
2. Email (if verified)
3. Phone (if verified)
4. Device ID
5. Anonymous ID (lowest)

### Conflict Resolution

When traits conflict:

| Strategy | Description |
|----------|-------------|
| prefer_newest | Use most recent |
| prefer_oldest | Use first seen |
| prefer_primary | Use primary profile |
| merge_arrays | Combine array values |

## Identity Lifecycle

### Pre-Login

```
User arrives → Anonymous ID assigned
Events tracked → Associated with anon ID
Traits set → Stored with anon ID
```

### Login/Signup

```
User authenticates → User ID known
Identify called → Link anon to user
History merged → Events attributed to user
```

### Post-Login

```
User ID used → Direct identification
No anonymous → Clean tracking
Cross-device → Unified profile
```

## Common Patterns

### Login Flow

```
1. User on site (anon_123)
2. User logs in
3. identify(anon_123, user_456)
4. Future events use user_456
```

### Signup Flow

```
1. User on site (anon_789)
2. User signs up
3. Create user_456
4. identify(anon_789, user_456)
5. Set initial traits
```

### Cross-Device Flow

```
1. User on mobile (anon_mobile)
2. User logs in → identify → user_456
3. User on desktop (anon_desktop)
4. User logs in → identify → user_456
5. Both linked to same user_456
```

## Best Practices

### Identity Management

- Identify as early as possible
- Use stable user IDs
- Handle anonymous gracefully
- Clean up duplicates

### Implementation

- Always pass user_id when known
- Don't generate new user_ids client-side
- Handle login/logout transitions
- Test cross-device scenarios

### Data Quality

- Monitor duplicate rates
- Track resolution success
- Audit identity graph
- Clean stale identities

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Duplicate profiles | No identify call | Call identify on login |
| Lost history | Wrong ID passed | Use consistent anon ID |
| Split users | Timing issue | Identify before new events |
| Merged wrong | ID collision | Use unique IDs |

### Debugging

Check for:
- identify() being called
- Correct IDs being passed
- Timing of identify vs events
- Anonymous ID persistence
