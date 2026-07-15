---
name: instrument-product-analytics
compatibility: Requires an Altertable SDK or HTTP API access
description: Instruments product analytics events and identity lifecycle calls with Altertable SDKs or HTTP APIs. Use when adding or reviewing track, page, identify, alias, reset, consent, or event-property code.
metadata:
  author: altertable-ai
---

# Instrument Product Analytics

Implement product analytics collection without querying collected data. Keep event names stable, identity transitions explicit, and sensitive data out of payloads.

## Quick Start

1. Choose the client-side SDK, server-side SDK, or HTTP API that matches the application.
2. Define the event name and analysis-ready properties before adding the call.
3. Track anonymous activity, call `identify()` after authentication, and call `reset()` on logout.
4. Validate consent behavior and inspect a development event before shipping.

## Event Model

All SDKs and the API share the same core payload:

| Field | Required | Description |
|-------|----------|-------------|
| `event` | Yes | Stable action name, such as `Checkout Completed` |
| `properties` | Yes for direct API, optional in SDK helpers | Analysis dimensions; send `{}` when empty |
| `distinct_id` | No | User or device identifier; client SDKs set it automatically |
| `timestamp` | No | Server time is used when omitted |

Prefer object-action event names in title case. Put changing details such as plan, currency, source, or experiment variant in properties instead of creating new event names.

## Track Events

### HTTP API

```bash
curl -X POST https://api.altertable.ai/track \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event":"Purchase Completed",
    "environment":"production",
    "distinct_id":"u_01jza857w4f23s1hf2s61befmw",
    "properties":{"amount":99.99,"currency":"USD"}
  }'
```

### TypeScript SDK

```typescript
altertable.track('Purchase Completed', {
  amount: 99.99,
  currency: 'USD',
});
```

Client SDKs can capture page or screen views automatically. Disable auto-capture only when the application needs explicit routing control:

```typescript
altertable.init('YOUR_API_KEY', { autoCapture: false });
altertable.page('https://example.com/products');
```

Server-side SDKs do not auto-capture page views and require an explicit `distinct_id`.

## Manage Identity

Call `identify()` after login or signup to connect anonymous activity to a known user:

```typescript
altertable.identify('u_01jza857w4f23s1hf2s61befmw', {
  plan: 'premium',
  email: 'user@example.com',
});
```

Update traits as account state changes and reset identity on logout:

```typescript
altertable.updateTraits({ plan: 'enterprise', onboarding_completed: true });
altertable.reset();
```

Use `alias()` for ID migrations and external system identifiers, not for normal login flows:

| Scenario | Method |
|----------|--------|
| Login or signup | `identify()` |
| Known user on another device | `identify()` |
| Migrate an old ID | `alias()` |
| Attach a CRM or billing ID | `alias()` |
| Logout | `reset()` |

## Validate the Implementation

- Confirm calls happen once at the intended lifecycle point.
- Verify anonymous events precede `identify()` and post-login events use the known identity.
- Test logout so the next user's events cannot inherit the previous identity.
- Exercise granted, denied, and pending consent states for client-side SDKs.
- Confirm properties contain no passwords, secrets, payment details, or regulated sensitive data.
- Inspect a development event for its name, environment, identity, timestamp, and properties.

## Boundaries

- Use `query-product-events` to inspect or aggregate events already stored in Altertable.
- Use `analyze-funnels` for ordered conversion and drop-off analysis.
- Use `analyze-web-traffic` for sessions, pageviews, acquisition, and web engagement.
- Use `query-lakehouse` when the task spans non-product catalogs or general SQL work.

## Common Pitfalls

- **Using `alias()` for login**: call `identify()` for authentication transitions.
- **Skipping reset on logout**: subsequent activity may be attributed to the previous user.
- **Dynamic event names**: encode variable values as properties so metrics remain aggregatable.
- **Missing server-side identity**: provide `distinct_id` explicitly outside client SDKs.
- **Duplicate capture**: do not combine auto-capture with equivalent manual calls unintentionally.
- **Ignoring consent**: do not emit client events until the configured consent state permits it.
- **Sending sensitive values**: never include secrets or regulated data in traits or properties.

## References

- [Event tracking details](references/event-tracking.md) - Read for SSR, consent, auto-capture, and platform behavior.
- [Identity and aliasing](references/identity-and-aliasing.md) - Read for login, logout, anonymous identity, and ID migration flows.
