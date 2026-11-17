# React embedding

Import `<DataAppBridge>` from `@altertable/data-app-embed/react`.
The bridge owns iframe setup and communication. The host owns bundle fetching,
layout, loading/error UI, and retry controls.

## Source-managed iframe

Use `source` for local URL apps or hosted bundles. The bridge creates the iframe,
configures its sandbox, loads its source, and reports connection status. It renders
only the iframe; it adds no loading, error, or retry UI and does not hide the frame.

```tsx
import { useReducer, useState } from 'react';
import { DataAppBridge } from '@altertable/data-app-embed/react';
import type { DataAppStatus } from '@altertable/data-app-embed';

// ... authorized router
function Shell() {
  const [status, setStatus] = useState<DataAppStatus>('connecting');
  const [attempt, retry] = useReducer(value => value + 1, 0);

  return (
    <div className="app-shell">
      {status !== 'ready' && status !== 'failed' && <p>Loading report…</p>}
      {status === 'failed' && <button onClick={retry}>Retry report</button>}
      <DataAppBridge
        key={attempt}
        title="Activity report"
        source={{ type: 'url', url: 'http://127.0.0.1:25837/' }}
        onMessage={router.dispatch}
        onStatusChange={setStatus}
        iframeProps={{ className: 'app-frame', hidden: status !== 'ready' }}
      />
    </div>
  );
}
```

The host supplies `router` using [message contracts](embed.md#message-routes).
The local URL must have a different origin from its shell. For hosted bundles,
replace `source` with:

```tsx
function Shell() {
  // ... javascript bundle and router
  return (
    <DataAppBridge
      title="Activity report"
      source={{ type: 'bundle', javascript }}
      onMessage={router.dispatch}
    />
  );
}
```

The host supplies the JavaScript bundle. Omit `bootstrapUrl` for the packaged
opaque bootstrap, or supply an HTTP(S) URL for an external bootstrap. See [embedding](embed.md) for trust,
sandbox, CSP, and bootstrap setup.

Source URL or JavaScript content changes replace the entire iframe. Change the
bridge's React `key` to retry with a fresh frame. Handler changes use the latest
callbacks without resetting the session. `startupTimeoutMs`, `onStatusChange`, and
`onDiagnostic` have the same meaning as in the framework-neutral API.

Use `iframeProps` for styling, visibility, and accessibility attributes; supply
`title` directly. The bridge owns source, sandbox, loading, and ref attributes.

## Host-owned iframe

Use the same `<DataAppBridge>` with `iframe` and `connection` when the host already
owns a loaded iframe and its security policy:

```tsx
import { useState, type ComponentRef } from 'react';
import { DataAppBridge } from '@altertable/data-app-embed/react';

// ... appUrl and authorized router
function Host() {
  const [iframe, setIframe] = useState<ComponentRef<'iframe'> | null>(null);
  return (
    <>
      <iframe ref={setIframe} title="Report" src={appUrl} />
      <DataAppBridge
        iframe={iframe}
        connection={{ type: 'origin', origin: new URL(appUrl).origin }}
        onMessage={router.dispatch}
      />
    </>
  );
}
```

Supply `appUrl` and `router`. A callback ref tracks iframe mounting and
replacement. This mode renders nothing; the host owns loading and security policy.

## Parent-owned presentation

Pass `presentation={{ surface: 'embedded', theme: resolvedTheme }}`
to `<DataAppBridge>` in either source or connection mode. Use `'standalone'` when the app should render its own page chrome.
Prop updates publish trusted state without reloading the iframe or reconnecting
the session. Resolve system preference in the parent to `'light'` or `'dark'`.
Inside an embedded surface, `<DataApp>` retains toolbar actions and hides its header
and footer. See [parent presentation](embed.md#parent-presentation).
