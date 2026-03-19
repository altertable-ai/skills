# Identity and Aliasing Reference

Extended details for identity flows and session management.

## Anonymous User Flow

1. User arrives, client SDK assigns a device-based `distinct_id` automatically
2. Events are tracked against the anonymous `distinct_id`
3. User authenticates, call `identify()` with the known user ID
4. SDK links the anonymous visitor ID to the authenticated user ID
5. The previous `distinct_id` becomes `anonymous_id`, connecting pre-login behavior

Server-side SDKs require you to pass a `distinct_id` with each call. Use your own anonymous ID (e.g. a session token) until the user authenticates.

## Session Reset Guidelines

When to reset:
- On logout, so events aren't attributed to the previous user
- For privacy compliance, when users clear their data or revoke consent

## Alias Best Practices

- Identify the user first, then alias secondary IDs
- Add source prefixes: `stripe:`, `crm:`, `hubspot:`, `legacy:`
- Link aliases directly to a primary user ID, not to each other
- Avoid repeatedly sending the same alias pair
