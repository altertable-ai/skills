# Identity and Aliasing Reference

Extended details for identity flows and session management.

## Anonymous User Flow

1. A user arrives and the client SDK assigns a device-based `distinct_id`.
2. Events are tracked against the anonymous `distinct_id`.
3. The user authenticates and the application calls `identify()` with the known user ID.
4. The SDK links the anonymous visitor ID to the authenticated user ID.
5. The previous `distinct_id` becomes `anonymous_id`, connecting pre-login behavior.

Server-side SDKs require a `distinct_id` on each call. Use an application-owned anonymous ID, such as a session token, until authentication.

## Session Reset Guidelines

Reset identity:

- On logout, so events are not attributed to the previous user.
- When a user clears data or revokes consent and the product's privacy behavior requires it.
- In shared-device flows before another user can authenticate.

## Alias Best Practices

- Identify the primary user before aliasing secondary IDs.
- Prefix external IDs with their source: `stripe:`, `crm:`, `hubspot:`, or `legacy:`.
- Link aliases directly to a primary user ID instead of chaining aliases.
- Avoid repeatedly sending the same alias pair.
- Document migrations so an alias cannot accidentally merge unrelated people.
