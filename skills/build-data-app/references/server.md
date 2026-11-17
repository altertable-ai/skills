# Server

Import `createDataHandler()` and the `RequestAccess` type from
`@altertable/data-app/server`. The handler accepts a Web `Request` and returns a
`Promise<Response>` in Node or Bun.

```ts
import { createDataHandler } from '@altertable/data-app/server';
import { operations } from './operations.ts';

export const handleDataRequest = createDataHandler(
  operations,
  async (request, operation) => {
    const viewer = await authenticate(request);
    return {
      lakehouse: await lakehouseFor(viewer, operation),
      queryParams: { orgId: viewer.organizationId },
    };
  }
);
```

The app supplies `authenticate()` and `lakehouseFor()`, then routes `/api/data/*`
requests to the handler. Authorize every viewer and operation, and scope the
returned lakehouse to the viewer's permitted data. Supply trusted registry
parameters through `queryParams`; query callers cannot override them. Origin and Fetch Metadata
checks reject cross-site browser requests; they do not authenticate viewers.

The handler validates operation input, enforces query row and duration
bounds, propagates cancellation, and returns query evidence and request IDs.
Keep credentials and operation implementations on the server.

See [operation contracts](contract.md), the [client](client.md), and the
[local Bun adapter](server-bun.md).

## Request input limits

JSON request bodies are limited to 16,384 encoded bytes. Oversized bodies return
`413/input_too_large`; invalid or interrupted bodies return `400/invalid_input`.
`maxDurationMs` bounds execution after parsing; configure body-read deadlines in
the hosting runtime.
