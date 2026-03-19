---
name: tracking-events
compatibility: Requires Altertable MCP server
description: Works with Altertable product analytics events, user identification, and aliasing. Use when tracking events, identifying users, managing traits, resolving identities, or querying analytics data.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Tracking Events

## Quick Start

1. **Track an event**: Call the track API or SDK method with event name and properties
2. **Identify a user**: Link anonymous activity to a known user after authentication
3. **Query events**: Use SQL to analyze tracked events and identity traits

## When to Use This Skill

- Tracking user actions (page views, purchases, feature usage)
- Identifying users after login or signup
- Updating user traits (plan, email, account state)
- Aliasing identifiers across systems (Stripe, CRM, legacy IDs)
- Querying event data or identity traits via SQL
- Building funnels, cohorts, or retention analysis from events

## Event Model

All SDKs and the API share the same payload shape:

| Field | Required | Description |
|-------|----------|-------------|
| `event` | Yes | Event name, e.g. `Checkout Completed` |
| `properties` | No | Event attributes for filtering and analysis |
| `distinct_id` | No | User or device identifier (client SDKs set automatically) |
| `timestamp` | No | Server uses current time when omitted |

## Tracking Events

### Via API

```bash
curl -X POST https://api.altertable.ai/track \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event":"Purchase Completed",
    "properties":{"amount":99.99,"currency":"USD"},
    "distinct_id":"u_01jza857w4f23s1hf2s61befmw"
  }'
```

### Via SDK (TypeScript)

```typescript
altertable.track('Purchase Completed', {
  amount: 99.99,
  currency: 'USD'
});
```

### Auto-Capture

Client-side SDKs automatically capture page/screen views. Disable with:

```typescript
altertable.init('YOUR_API_KEY', { autoCapture: false });
altertable.page('https://example.com/products');
```

Server-side SDKs (Python, Ruby) do not auto-capture pages.

## Identifying Users

Call `identify()` after authentication to link anonymous activity to a known user.

### Via API

```bash
curl -X POST https://api.altertable.ai/identify \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "distinct_id":"u_01jza857w4f23s1hf2s61befmw",
    "traits":{"plan":"premium","email":"user@example.com"}
  }'
```

### Via SDK (TypeScript)

```typescript
altertable.identify('u_01jza857w4f23s1hf2s61befmw', {
  plan: 'premium',
  email: 'user@example.com'
});
```

### Updating Traits

After identification, update traits as account state changes:

```typescript
altertable.updateTraits({ plan: 'enterprise', onboarding_completed: true });
```

Server-side SDKs update traits by calling `identify()` again with new trait values.

### Session Reset

Call `reset()` on logout to clear identity context:

```typescript
altertable.reset();
altertable.reset({ resetDeviceId: true }); // also clears device ID
```

## Aliasing Users

Use `alias()` to link multiple identifiers to the same user profile. This is for ID migrations and external system IDs, not for login flows (use `identify()` for those).

### When to Use alias() vs identify()

| Scenario | Method |
|----------|--------|
| Login or signup | `identify()` |
| Known user on another device | `identify()` |
| Migrate from old ID format | `alias()` |
| Attach CRM or billing ID | `alias()` |
| Merge profiles across platforms | `alias()` |

### Via API

```bash
curl -X POST https://api.altertable.ai/alias \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "distinct_id":"user_123",
    "alias_id":"stripe:cus_abc123"
  }'
```

### Via SDK (TypeScript)

```typescript
altertable.alias(`stripe:${stripeCustomerId}`);
altertable.alias(`hubspot:${hubspotContactId}`);
```

## Querying Events

### Event Counts by Type

```sql
SELECT
  event,
  properties->>'currency' AS currency,
  COUNT(*) AS total
FROM altertable.analytics.events
GROUP BY ALL
ORDER BY total DESC;
```

### Events with Identity Traits

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

### Identity Traits

```sql
SELECT
  distinct_id,
  traits->>'email' AS email,
  traits->>'plan' AS plan,
  updated_at
FROM altertable.analytics.identities
ORDER BY updated_at DESC;
```

## Available SDKs

| Language | Install |
|----------|---------|
| TypeScript/JS | `npm install @altertable/altertable-js` |
| React | `npm install @altertable/altertable-js @altertable/altertable-react` |
| Python | `pip install altertable` |
| Ruby | `gem install altertable` |
| Swift | Swift Package Manager |
| Kotlin | `implementation("ai.altertable.sdk:altertable-kotlin:0.1.0")` |

## Common Pitfalls

1. **Not identifying after page reload** - Call `identify()` after authentication, including after full page loads when user is already authenticated
2. **Using alias() for login flows** - Use `identify()` for login/signup, `alias()` for ID migrations and external system links
3. **Missing distinct_id in server-side calls** - Server-side SDKs require you to pass `distinct_id` explicitly
4. **Forgetting reset() on logout** - Future events get attributed to the previous user
5. **Sensitive data in traits** - Never send secrets or regulated sensitive data in traits or event properties

## Reference Files

- [Event tracking details](references/event-tracking.md) - Read when working with SSR setup, tracking consent, auto-capture configuration, or platform-specific behavior
- [Identity and aliasing](references/identity-and-aliasing.md) - Read when implementing login/signup flows, session reset, alias migrations, or querying identity data
