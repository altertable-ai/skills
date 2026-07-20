---
name: track-events
description: Routes legacy track-events requests to current Altertable Product Analytics skills. Use when an existing invocation references track-events and must migrate to instrumentation or event querying.
metadata:
  author: altertable-ai
---

# Track Events (Deprecated)

## Quick Start

`track-events` is a compatibility router. Do not use it for new requests.

1. Use `instrument-product-analytics` when the request adds or changes events, identification, traits, consent, session reset, or identity aliasing in an application.
2. Use `query-product-events` when the request queries or analyzes stored events, identities, traits, or instrumentation delivery.
3. Pass the original request through unchanged to the selected skill.

## When to Use This Skill

- An existing prompt, command, link, or automation explicitly invokes `track-events`
- A consumer has not yet migrated to the replacement skill names
- The request must be routed without breaking a legacy identifier

Do not select this skill for a new request when either replacement skill is available directly.

## Migration Routing

| Legacy intent | Replacement |
|---------------|-------------|
| Add or change event tracking | `instrument-product-analytics` |
| Identify users or update traits | `instrument-product-analytics` |
| Manage consent, logout reset, or aliases | `instrument-product-analytics` |
| Count, inspect, or analyze stored events | `query-product-events` |
| Validate whether instrumentation is arriving | `query-product-events` |

## Common Pitfalls

1. Implementing work in this compatibility skill instead of activating a replacement
2. Routing every legacy request to instrumentation without checking whether it is analytical
3. Routing stored-event queries to instrumentation because the request mentions tracking
4. Dropping the original request context during the handoff
5. Recommending `track-events` in new prompts, documentation, or automation
