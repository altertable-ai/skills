---
name: instrument-product-analytics
description: Instruments Altertable product analytics with SDK or HTTP API calls. Use when adding or reviewing event tracking, page or screen tracking, user identification, traits, aliases, reset behavior, or tracking consent.
metadata:
  author: altertable-ai
---

# Instrument Product Analytics

Use the official Altertable documentation as the source of truth for current SDKs, payloads, and API behavior.

## Quick Start

1. Read the Product Analytics ingestion overview and choose the SDK or HTTP API for the application.
2. Follow the tracking, identification, and aliasing guides for the requested lifecycle.
3. Implement the calls in the user's codebase using the documented API for that platform.
4. Verify event delivery, identity transitions, logout reset behavior, and consent handling where applicable.

## Official Documentation

- [Ingest data](https://altertable.ai/docs/product-analytics/ingest-data)
- [Track product events](https://altertable.ai/docs/product-analytics/tracking)
- [Identify users](https://altertable.ai/docs/product-analytics/identifying)
- [Alias users](https://altertable.ai/docs/product-analytics/aliasing)
- [SDKs](https://altertable.ai/docs/product-analytics/sdks)
- [REST API](https://altertable.ai/docs/product-analytics/reference/api)

## Common Pitfalls

- Use `identify()` for login and signup; reserve `alias()` for explicit identity merges.
- Call `reset()` on logout so later events are not attributed to the previous user.
- Pass `distinct_id` explicitly with server-side SDK calls.
- Avoid duplicate events when combining automatic and manual page or screen tracking.
- Never send secrets or regulated sensitive data in event properties or traits.

## References

- [Event tracking details](references/event-tracking.md)
- [Identity and aliasing](references/identity-and-aliasing.md)
