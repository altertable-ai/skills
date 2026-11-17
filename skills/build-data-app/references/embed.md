# Embed a data app

Import framework-neutral host APIs from `@altertable/data-app-embed`. For React
hosts, see [React embedding](react-embed.md). Neither embedding entry requires the
app UI stylesheet.

## Sources

`attachDataAppBridge()` in source mode owns iframe loading, sandbox policy, startup timeout, and
message delivery. The host supplies an iframe and a validated message dispatcher:

```ts
import { attachDataAppBridge } from '@altertable/data-app-embed';

// ... iframe and authorized router
const host = attachDataAppBridge({
  iframe,
  source: { type: 'url', url: 'https://apps.example.com/report' },
  onMessage: router.dispatch,
});
```

The host defines `iframe` and `router`; see [message contracts](#message-routes).
Call `host.dispose()` before replacing the source or retrying. A URL source requires HTTP(S)
and a different origin from its host. The source bridge adds `__altertable_parent` to the
app URL. An app loaded by URL must install a transport to its configured,
trusted parent origin using the [client API](client.md#iframe-transport).
The query parameter alone does not establish trust.

A bundle source has this shape:

```ts
const source = {
  type: 'bundle' as const,
  javascript: bundle.javascript,
};
```

Omit `bootstrapUrl` to load the SDK's packaged bootstrap as a `data:` document.
This supports MCP hosts that permit opaque child frames but block remote frame
URLs. The SDK embeds the exact host origin and applies a CSP that prohibits
direct network access. Data requests go through the host's dispatcher.

Supply an HTTP(S) `bootstrapUrl` to use an externally served trusted bootstrap,
such as the [Worker asset](worker.md).

Supply a self-contained JavaScript bundle. Bundle mode uses an opaque
`sandbox="allow-scripts"` frame; both modes use `referrerPolicy="no-referrer"`.

## Trusted bootstrap

For Cloudflare hosting, upload the [Worker asset](worker.md). It includes the
bootstrap HTML and security policy; deployments supply the runtime domain and
trusted parent origins through bindings.

For other hosts that own their HTML and security policy, bundle this initializer
into the bootstrap document before any app code:

```ts
import { startDataAppBootstrap } from '@altertable/data-app-embed';

const dispose = startDataAppBootstrap({
  parentOrigin: 'https://host.example.com',
});
```

The bootstrap URL is trusted executable code: it receives the app script and
session token. Its hosting service must enforce its CSP. The bridge cannot impose
CSP on a remote response. A starting policy for self-contained scripts and styles
is `default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline';
img-src data: blob:; connect-src 'none'; base-uri 'none'; form-action 'none'`.
The initializer installs the transport before evaluating app code. Non-React
apps attach [navigation](client.md#app-navigation) separately.

## Delivery and navigation

For an already loaded, host-owned iframe, supply
`connection: { type: 'origin', origin }` or `{ type: 'opaque', token }` with
`onMessage`. The host then owns loading and sandbox policy. Use source mode for
bundle loading and session setup.

`createNavigationHandler({ window, reservedSearchParams })` handles the shared
`navigation:update` route using browser history. Reserved host query parameters
survive app changes. Supply your own handler when integrating a framework router.
Host Back/Forward events publish opaque host state through the bridge. The app's
optional navigation adapter interprets search/hash and synchronizes controls;
opaque apps keep that state in memory rather than modifying their document URL.

## External links

Register the external link route to let apps request HTTPS navigation without
relaxing the iframe sandbox:

```ts
import {
  createMessageRouter,
  openExternalLinkRoute,
} from '@altertable/data-app/contract';
import { createExternalLinkHandler } from '@altertable/data-app-embed';

const router = createMessageRouter(
  { 'navigation:openExternal': openExternalLinkRoute },
  {
    'navigation:openExternal': createExternalLinkHandler({
      allowedOrigins: ['https://example.com'],
    }),
  }
);
// Pass router.dispatch as the bridge's onMessage handler.
```

To use an existing modifier-based host navigation helper, register it directly:

```ts
const openExternalLink = createExternalLinkHandler({
  navigate: navigateNewWindowOrTab,
});
// Register openExternalLink for navigation:openExternal in the host router.
```

Here `navigateNewWindowOrTab` is the host's `(url, event)` navigation helper.
Use the frontend helper, not the app-side bridge client with the same name.

Choose permitted origins according to the host's data policy: URLs can carry app
data, and the initial origin check does not constrain redirects at the destination.

## Status and diagnostics

`onStatusChange` receives `connecting`, `connected`, `ready`, `failed`, or
`disconnected`. `connected` means transport initialization; `ready` means a URL
client acknowledged initialization or a bundle script finished evaluation. It
does not mean asynchronous data queries finished. Script errors report `failed`.
The source bridge's `startupTimeoutMs` defaults to 30 seconds.

Use `onDiagnostic` or `logger` to inspect delivery and failures. Diagnostics omit
tokens and payloads. Handlers must authorize every data request; message
validation and iframe isolation do not grant data access.

## Message routes

Message contracts describe the payloads allowed between an embedded app and its
host. Share these contracts with the app; keep handlers and authorization in the
host/server.

Name routes `{scope}:{action}`, for example `data:query` or `navigation:update`.

```ts
import {
  createMessageRouter,
  defineMessageRoute,
  navigationUpdateRoute,
} from '@altertable/data-app/contract';
import { createNavigationHandler } from '@altertable/data-app-embed';

function parseString(value: unknown) {
  if (typeof value !== 'string') throw new Error('Expected a string.');
  return value;
}

const routes = {
  'demo:echo': defineMessageRoute({ input: parseString, output: parseString }),
  'navigation:update': navigationUpdateRoute,
};
const router = createMessageRouter(routes, {
  'demo:echo': value => value,
  'navigation:update': createNavigationHandler(),
});
```

`router.dispatch()` validates route input and output. Use `MessageRoutingError`
for intentional public failures; other handler errors are hidden.

Use `defineDataQueryRoute(operationContracts)` for typed named operations or
`dataAppRoutes` for generic operation and navigation routes. Handlers must
validate operations, authorize data access, and enforce backend query limits.

## SQL query route

Hosts serving browser-owned operations register `sqlQueryRoute` explicitly:

```ts
import {
  createMessageRouter,
  sqlQueryRoute,
} from '@altertable/data-app/contract';
import { createSqlQueryHandler } from '@altertable/data-app-embed';

const router = createMessageRouter(
  { 'data:sql': sqlQueryRoute },
  {
    'data:sql': createSqlQueryHandler(async (query, { signal }) => {
      return authorizedLakehouseForCurrentViewer(query, signal);
    }),
  }
);
// Supply router.dispatch as the shell's onMessage handler.
```

The host supplies `authorizedLakehouseForCurrentViewer()`. Its backend must enforce
viewer/dataset permissions, permitted query behavior, maximum rows, execution
time, concurrency, and response size independently of browser policy. Route
validation is not SQL authorization. `createSqlQueryHandler()` calls authorization
for each query, forwards cancellation, and preserves `DataSourceError` reasons
as public `source_*` errors with request IDs. Authorization failures return
`forbidden`; unknown query errors are hidden. Custom handlers can return deliberate
public failures with `MessageRoutingError`.

The SQL route carries `{ statement, limit, params? }` and returns column
metadata and row arrays; see `SqlQueryInput` and `QueryResult` in the
[API reference](../REFERENCE.md). Keep SQL and parameters unchanged.
For server-owned named operations, use `dataAppRoutes` and `data:query` instead.

## Parent presentation

The parent declares where the iframe is mounted and owns its resolved theme:

```ts
// ... iframe and authorized router
const host = attachDataAppBridge({
  iframe,
  source: { type: 'url', url: 'https://apps.example.com/report' },
  presentation: { surface: 'embedded', theme: 'dark' },
  onMessage: router.dispatch,
});

// Update presentation without replacing the iframe or its bridge session.
host.setPresentation({ surface: 'embedded', theme: 'light' });
```

Use `surface: 'embedded'` when the parent supplies page chrome and
`'standalone'` when the app supplies it. Resolve the parent theme to `'light'` or
`'dark'`. React `<DataApp>` applies presentation automatically: embedded surfaces
keep toolbar actions and hide header/footer. Updates do not reload the iframe.
Call `host.setPresentation(undefined)` to restore standalone defaults.

### Content sizing

By default the parent sizes the iframe and the app scrolls inside it. Set
`sizing: 'content'` when the parent page should scroll instead, as in a details
panel that stacks the app with other content:

```ts
host.setPresentation({
  surface: 'embedded',
  theme: 'light',
  sizing: 'content',
});
```

React `<DataApp>` supports content sizing automatically; framework-neutral apps
call `bridge.supportContentSizing()`. Keep iframe flex/grid stretching and
`max-height` constraints off so the reported height can apply. Keep app document
and body heights automatic.

If sizing fails to settle, the bridge restores frame scrolling. Toggle sizing or
reload to retry. Switching to `'frame'` or disposing restores the authored height.

For shared diagnostic reports, bounded agent repair and the in-flow banner, see
[App diagnostics and repair](diagnostics.md).
