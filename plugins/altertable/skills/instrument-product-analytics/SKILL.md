---
name: instrument-product-analytics
description: "Adds or changes Altertable Product Analytics instrumentation in application code. Use for SDK setup, event tracking, user identification, traits, consent, session reset, page or screen tracking, and identity aliasing."
---

# Instrument Product Analytics

Implement the smallest durable instrumentation change using the project's installed Altertable SDK and types as the API authority.

## Workflow

1. Inspect the application stack, installed package and version, shared client initialization, authentication lifecycle, consent model, and existing event conventions.
2. Read the current Product Analytics ingestion guide with `search_docs` or at [Product Analytics ingestion](https://altertable.ai/docs/ingest-data/product-analytics).
3. Define the stable event name, identity context, and only the properties needed for filtering, grouping, or decisions.
4. Instrument the successful business outcome at its source of truth.
5. Exercise success, failure, anonymous-to-known, logout, and consent paths relevant to the change.
6. When runtime access is available, verify a non-production event in the intended environment.

Use the direct Product Analytics HTTP API only when an SDK is unavailable or intentionally unsuitable. Direct requests must include the target environment; use SDK batching and retry behavior rather than rebuilding it when available.

## Identity Rules

- Track server-owned outcomes such as completed billing changes from the backend.
- Identify a known user when authenticated state is established or restored.
- Use a stable identifier rather than mutable profile data such as email.
- Reset client identity on logout so the next person's events are not joined to the prior user.
- Use aliasing only for an explicit identifier merge or migration; ordinary login and signup use identification.
- Preserve established anonymous-ID behavior across page reloads and sessions.

## Safety

- Never send secrets, payment details, passwords, or regulated sensitive data as properties or traits.
- Do not hardcode environment credentials.
- Do not broaden tracking beyond the requested behavior or bypass consent.
- Do not initialize a second client when the application already has one.
- Do not rename an established event or property without checking downstream consumers.
- Confirm successful actions emit once and failed or cancelled actions do not emit success events.

Use the `analyze-product-behavior` skill to inspect events already stored in Altertable.
