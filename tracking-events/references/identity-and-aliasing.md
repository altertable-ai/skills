# Identity and Aliasing Reference

Extended details for identity flows, session management, and querying identity data.

## Anonymous User Flow

1. User arrives, client SDK assigns a device-based `distinct_id` automatically
2. Events are tracked against the anonymous `distinct_id`
3. User authenticates, call `identify()` with the known user ID
4. SDK links the anonymous visitor ID to the authenticated user ID
5. The previous `distinct_id` becomes `anonymous_id`, connecting pre-login behavior

Server-side SDKs require you to pass a `distinct_id` with each call. Use your own anonymous ID (e.g. a session token) until the user authenticates.

## Session Reset Details

Call `reset()` on logout:

```typescript
altertable.reset();                          // keep device ID
altertable.reset({ resetDeviceId: true });   // clear all IDs
```

When to reset:
- On logout, so events aren't attributed to the previous user
- For privacy compliance, when users clear their data or revoke consent

## identify() vs alias() Decision Table

| Scenario | Method | Why |
|----------|--------|-----|
| Login or signup | `identify()` | Automatically links anonymous activity |
| Known user on another device | `identify()` | Call with same user ID on each device |
| Migrate from old ID format | `alias()` | Preserves history when changing ID schemes |
| Attach CRM or billing ID | `alias()` | Connects external system identifier |
| Merge profiles across platforms | `alias()` | Links two existing identified profiles |

## Alias Best Practices

- Identify the user first, then alias secondary IDs
- Add source prefixes: `stripe:`, `crm:`, `hubspot:`, `legacy:`
- Link aliases directly to a primary user ID, not to each other
- Avoid repeatedly sending the same alias pair

## Querying Identity Data

### All Traits for a User

```sql
SELECT
  distinct_id,
  traits->>'email' AS email,
  traits->>'plan' AS plan,
  updated_at
FROM altertable.analytics.identities
ORDER BY updated_at DESC;
```

### Events Enriched with Identity Traits

```sql
SELECT
  e.event,
  e.properties,
  e.timestamp,
  e.identity_traits->>'email' AS email,
  e.identity_traits->>'plan' AS plan
FROM altertable.analytics.events e
WHERE e.distinct_id = 'u_01jza857w4f23s1hf2s61befmw'
ORDER BY e.timestamp DESC;
```
