# React

Import views, bound widgets, and layouts from `@altertable/data-app-react`.
React and React DOM 19.2 or newer are required. Start with
[app authoring](app-authoring.md).

## Mount the app

```tsx
import { injectDataAppStyles, mountDataApp } from '@altertable/data-app-react';

injectDataAppStyles();
mountDataApp({ app: dataApp, component: App });
```

The app supplies `dataApp`, `App`, and a `#root` element.

Keep the selected starter's mounting and client wiring. The
app brief selects the starter and content structure; the available runtime
starters are listed in [app authoring](app-authoring.md#use-release-matched-starters).
Use declared views and bound widgets for data-backed content. Use `/ui` for
setup/static screens or a custom component only when bound components cannot
express the requirement.

Hosts embedding an app use the separate `@altertable/data-app-embed` package;
that integration is outside ordinary app authoring.
