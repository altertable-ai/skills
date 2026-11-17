# Local Bun server

Use this Bun server for local data apps. Start from the CLI scaffold or
[local data app starter](app-authoring.md#use-release-matched-starters).

Import `serveLocalApp()` and `localLakehouse()` from
`@altertable/data-app-bun`. This entry requires Bun; install `@types/bun`
when typechecking a Bun app.

```ts
import { serveLocalApp } from '@altertable/data-app-bun';
import page from './index.html';
import { operations } from './operations.ts';

serveLocalApp({ page, operations, title: 'Activity' });
```

The server binds to `127.0.0.1`. Its default port is `25837`, overridable through
`PORT` or the `port` option. It serves the Bun HTML bundle and operation requests.

`localLakehouse()` reads the CLI proxy URL and token from
`ALTERTABLE_DATA_PROXY_URL` and `ALTERTABLE_DATA_PROXY_TOKEN`. It also supports
server-only `ALTERTABLE_LAKEHOUSE_USERNAME` and
`ALTERTABLE_LAKEHOUSE_PASSWORD`, with an optional `ALTERTABLE_API_BASE`.
Missing credentials fail at startup. Keep these variables out of browser code.

Local serving does not authenticate hosted viewers.
Use [the portable server handler](server.md) with per-request authorization when
hosting an app for other people.
