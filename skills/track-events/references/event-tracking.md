# Event Tracking Reference

Extended details for platform-specific behavior, SSR, and consent management.

## Auto-Capture by Platform

| Platform | Behavior |
|----------|----------|
| JavaScript/React | Listens for `popstate` and `hashchange`. Disable with `autoCapture: false` during init, then call `altertable.page(url)` manually |
| Kotlin/Android | Auto-tracks Activity screen views when `captureScreenViews` is enabled (default). In Compose, use `.screenView(name:)` modifier |
| Swift/iOS | Auto-tracks UIKit view controller appearances when `captureScreenViews` is enabled (default). In SwiftUI, use `.screenView(name:)` modifier |
| Python/Ruby | No auto-capture. Include page context in event properties when relevant |

## SSR Setup (Next.js, Remix)

Initialize in `useEffect` to avoid running in the server environment:

```typescript
import { useEffect } from 'react';
import { altertable } from '@altertable/altertable-js';
import { AltertableProvider } from '@altertable/altertable-react';

function App() {
  useEffect(() => {
    altertable.init('YOUR_API_KEY');
  }, []);

  return (
    <AltertableProvider client={altertable}>
      <YourApp />
    </AltertableProvider>
  );
}
```

## Tracking Consent

Client-side SDKs include built-in consent management. Events are queued while consent is pending.

| State | Behavior |
|-------|----------|
| `granted` | Events sent immediately |
| `denied` | Events dropped, queue cleared |
| `pending` | Events queued until consent changes |
| `dismissed` | Events queued (same as pending) |

```typescript
altertable.init('YOUR_API_KEY', { trackingConsent: 'pending' });
altertable.configure({ trackingConsent: 'granted' });
```

Server-side SDKs don't manage consent. Handle it in your application before sending events.

## Client-Side vs Server-Side Capabilities

| Capability | Client-side | Server-side |
|------------|-------------|-------------|
| Event tracking | Yes | Yes |
| User identification | Yes | Yes |
| Aliasing | Yes | Yes |
| Auto page/screen tracking | Yes | No |
| Session & device ID management | Automatic | You provide `distinct_id` |
| Tracking consent | Built-in | Manage externally |
| Event queuing & offline support | Yes | No |
