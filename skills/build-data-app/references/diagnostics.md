# App diagnostics and repair

Live capture reports observed query, operation, and widget failures together.
Repair actions send the complete observed report. Unvisited views and interactions
remain unverified. Reports include unfinished checks and omitted failure counts.

## Host integration

Create one session outside the viewer lifecycle. Restore and retain its updated
state across revisions, reloads, and viewer recreation, even if saving fails.
Change the revision identifier when app source changes.

```tsx
import { createDataAppRepairSession } from '@altertable/data-app-embed';
import {
  DataAppBridge,
  DataAppRepairBanner,
} from '@altertable/data-app-embed/react';

const session = createDataAppRepairSession({
  state: restoredState, // New app: { automaticRequests: 0, attemptedRevisions: [] }
  onStateChange: saveRepairState,
  onRepairRequest: requestAgentRepair,
});

const viewer = (
  <>
    <DataAppRepairBanner session={session} />
    <DataAppBridge
      source={{ type: 'bundle', javascript }}
      title="Data app"
      repair={{ session, revision }}
      onMessage={onMessage}
    />
  </>
);
```

The host owns authorization, delivery, and state retention. `onStateChange` is
awaited before automatic delivery; reject if state cannot be retained. Three automatic
requests are allowed per session; manual requests and healthy revisions do not
reset the allowance. Callback resolution means acceptance, not agent execution.
Omit `onRepairRequest` when delivery or reliable state retention is unavailable;
the banner offers diagnostics to copy instead. Avoid sensitive values in errors.
Source locations use generated filenames and positions.

## Custom banners

Use `session.snapshot()` to read diagnostics, delivery status, the automatic
request count, and the latest request's start time. Subscribe with
`session.subscribe()` and request a fix with `session.requestRepair()`. These APIs
work without React or the default banner.

In React, pass the snapshot to your own banner:

```tsx
import type { DataAppRepairSession } from '@altertable/data-app-embed';
import { useSyncExternalStore } from 'react';

import { RepairBanner } from './RepairBanner';

function AppRepair({ session }: { session: DataAppRepairSession }) {
  const repair = useSyncExternalStore(
    listener => session.subscribe(listener),
    session.snapshot,
    session.snapshot
  );

  return (
    <RepairBanner
      repair={repair}
      onRequestRepair={() => void session.requestRepair()}
    />
  );
}
```

The host owns agent activity and revision loading. Request acceptance does not
mean the agent has started or finished. Clear the previous attempt's activity
when requesting another fix, and clear progress when the updated revision's
diagnostics settle. Custom banners choose their own presentation; the default
`<DataAppRepairBanner>` accepts observed host activity through `progress`.
