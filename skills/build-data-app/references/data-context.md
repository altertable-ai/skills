# Data context and evidence

Continue the starter's operations and context. Build one context from every
operation's `queryNames` and share it across the app's views. Reference only
queries the app executes.

## Bind evidence

```tsx
import { createDataContext } from '@altertable/data-app-react';

// ... operations
const queryNames = {
  ...operations.sampleCountsByGroup.queryNames,
  ...operations.sampleTotal.queryNames,
};
const sampleDataContext = createDataContext(queryNames)({
  description: 'Sample counts for the selected groups.',
  glossary: {
    sampleCount: {
      term: 'Sample count',
      definition: 'The number of samples in each group.',
      queryNames: [queryNames.sampleCountsByGroup, queryNames.sampleTotal],
    },
  },
});
```

Import `createDataContext()` from `@altertable/data-app-react`. Supply
`dataContext: sampleDataContext` on each view, then use its glossary IDs
in `view.metric()` and `view.dataset()`. Reuse those bindings in widgets and stories.
Detail views need their own context when their queries differ.

## Register source identifiers

Once the queries use inspected physical sources, use `defineDataIdentifiers()` from `@altertable/data-app-react` to register exact catalog, schema,
table, and field names. Use `<DataIdentifier>` in descriptions and glossary
entries to render those source references consistently.

```tsx
import {
  createDataContext,
  defineDataIdentifiers,
} from '@altertable/data-app-react';

const identifiers = defineDataIdentifiers({
  tables: {
    events: {
      catalog: 'product_analytics',
      schema: 'analytics',
      name: 'events',
    },
  },
  columns: { identity: { table: 'events', name: 'identity_uuid' } },
});
const { DataIdentifier } = identifiers;

// ... queryNames for the inspected source
const eventDataContext = createDataContext(queryNames)({
  identifiers: identifiers.definitions,
  description: (
    <>
      Distinct <DataIdentifier id="columns.events.identity" /> values in{' '}
      <DataIdentifier id="tables.events" />.
    </>
  ),
  glossary: {
    // ... business definitions
  },
});
```
