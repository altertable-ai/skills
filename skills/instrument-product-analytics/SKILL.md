---
name: instrument-product-analytics
description: Instruments applications with Altertable Product Analytics. Use when adding event tracking, identifying users, updating traits, resetting sessions, managing consent, or aliasing identifiers.
---

# Instrument Product Analytics

## Quick Start

1. Inspect the application stack, installed Altertable packages, existing client initialization, and current tracking conventions.
2. Read the canonical [ingestion guide](https://altertable.ai/docs/product-analytics/ingest-data.md) and the page for the operation being implemented:
   - [Track events](https://altertable.ai/docs/product-analytics/ingest-data/track.md)
   - [Identify users](https://altertable.ai/docs/product-analytics/ingest-data/identify.md)
   - [Alias identifiers](https://altertable.ai/docs/product-analytics/ingest-data/alias.md)
   - [Authenticate clients](https://altertable.ai/docs/product-analytics/ingest-data/authentication.md)
3. Use the project's installed SDK and types as the exact API reference. Reuse its existing Altertable client rather than creating another instance.
4. Add the smallest instrumentation change at the source of truth for the action.
5. Verify the success path, identity lifecycle, consent behavior, and the project's targeted checks.

Use the [Product Analytics API reference](https://altertable.ai/docs/api-references/product-analytics.md) only when an SDK is unavailable or a direct HTTP integration is intentional.

## When to Use This Skill

- Adding or changing product event instrumentation in an application
- Initializing an Altertable SDK
- Identifying users after signup, login, or restored authentication
- Updating user or account traits
- Resetting client identity on logout
- Managing tracking consent, page views, or screen views
- Aliasing IDs during an identity migration or external-system integration

For questions about events already stored in Altertable, use `query-product-events`. For ordered conversion journeys, use `analyze-funnels`.

## Implementation Workflow

### 1. Inspect Before Editing

Determine:

- whether the application is browser, React, mobile, server, or a mixed architecture
- which Altertable SDK and version are installed
- where the shared client is initialized
- how configuration and environment-specific API keys are supplied
- whether event names or properties already have project-owned types
- how authentication, logout, and consent are represented

Follow the repository's local conventions and the installed package types. Do not infer a signature from a skill example or from another SDK.

### 2. Define the Event Contract

Before adding a call, establish:

- the user action or business outcome the event represents
- the stable event name
- only the properties needed for filtering, grouping, or decisions
- the correct identity context
- whether the browser or backend is the source of truth

Prefer a small number of durable business events over low-level interaction noise. Track server-owned outcomes such as successful billing changes or completed background jobs from the backend.

### 3. Place Calls at Durable Boundaries

- Track an outcome after it succeeds, not when the user merely attempts it.
- Identify as soon as authenticated state is established or restored.
- Reset client identity on logout.
- Update traits when analytically relevant account state changes.
- Use aliasing only for explicit ID merges or migrations; normal signup and login flows use identification.
- Preserve existing consent gates and privacy behavior.

### 4. Verify

- Exercise the relevant success path and confirm the call occurs once.
- Check that failed or cancelled actions do not emit success events.
- Check anonymous-to-known identity behavior when authentication is involved.
- Check logout does not leave the prior user's identity active.
- Run the repository's focused lint, type, and test commands.
- If runtime access is available, confirm a non-production event reaches the intended Altertable environment without exposing user data.

## Safety Rules

- Never send passwords, tokens, secrets, payment details, or regulated sensitive data as properties or traits.
- Do not hardcode environment-specific credentials in source files.
- Do not silently broaden tracking beyond the user's requested behavior.
- Do not initialize multiple competing clients.
- Do not replace established event names or property shapes without checking downstream dashboards, queries, and consumers.
- Do not bypass consent, privacy, or data-residency requirements to make an event appear.

## Common Pitfalls

1. Tracking before an operation succeeds, which inflates conversion metrics
2. Adding duplicate initialization or duplicate listeners
3. Using mutable data such as email as the stable user ID
4. Forgetting to identify an already-authenticated user after a full reload
5. Forgetting to reset identity on logout
6. Using aliasing for routine authentication instead of an explicit ID merge
7. Copying an API signature without checking the installed SDK version
8. Sending properties that have no planned analytical use
