# Views and displayed results

Keep the starter's client and hooks. Define one view per operation, and one
operation per widget. The examples continue the hosted starter's
`sampleCountsByGroup` operation and `sampleDataContext`.

## Bind a view

```tsx
import {
  createDataHooks,
  DataApp,
  DataSection,
  TableWidget,
} from '@altertable/data-app-react';

// ... client, operations, and sampleDataContext
const { defineView } = createDataHooks(client);

const sampleCountsView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleCountsByGroup',
  isEmpty: rows => rows.length === 0,
  emptyFallback: { title: 'No matching groups' },
});
// ... sampleCounts dataset and story callback
const sampleContent = sampleCountsView.content(result => (
  <TableWidget dataset={sampleCounts} source={result} />
));

function App() {
  return (
    <DataApp view={sampleCountsView} story={story} datasets={[sampleCounts]}>
      <DataSection content={sampleContent} />
    </DataApp>
  );
}
```

The view's filters, reporting period, metric comparisons, and scope come from
the [filters](filters.md) its operation declares. Set `describeInput` only when
the derived scope needs specific copy.

## Give each widget its own view

The hosted starter gives its total and its group counts separate operations and
views. `<DataApp view>` loads with the page; every other `<DataSection>` loads
when it nears the viewport. Both operations read the same `groupName` filter,
and `<DataApp>` renders its control once:

```tsx
// ... client, operations, sampleDataContext, and section contents
const { defineView } = createDataHooks(client);

const sampleCountsView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleCountsByGroup',
  isEmpty: rows => rows.length === 0,
  emptyFallback: { title: 'No matching groups' },
});
const sampleTotalView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleTotal',
});

function App() {
  return (
    <DataApp view={sampleCountsView}>
      <Stack>
        <DataSection content={totalContent} />
        <DataSection content={countsContent} />
      </Stack>
    </DataApp>
  );
}
```

Define every view rendered inside one `<DataApp>` from the same
`createDataHooks()` result; its client owns their filter controls.

Share one [data context](data-context.md) across the app's views. Group widgets
in one view only when they show the same result, such as a chart and the table
of its rows. A story or export that reads other views lists them in
[`summaryViews`](stories-and-export.md).

## Preserve displayed results

Use the source from `view.content()` for every widget. Derive narrative, story,
export, and scope from that source and its displayed input, including during
refresh or failure. Use `result.scope` in content and `view.scope(snapshot)` in
stories. Let views and bound widgets own request state and loading feedback.
Keep static introductions outside loading boundaries.

A measured zero is valid data. Set `isEmpty` and useful `emptyFallback` copy when
a result can be empty; omit both when it never is, such as a total.

## Detail destinations

Add `defineDetailView()` only when readers need a scoped population or entity.
The destination owns its input parser, operation, datasets, context, and content.
Pass its content to `<DataApp details={[groupDetail]}>`:

```tsx
// ... operations, sampleDataContext, main view, datasets, and story
// ... defineDetailView from the main view's createDataHooks() result
const groupView = defineDetailView({
  id: 'group',
  title: 'Group counts',
  operation: 'sampleCountsByGroup',
  dataContext: sampleDataContext,
  parseInput: operations.sampleCountsByGroup.input,
  describeInput: ({ groupName }) => `group ${groupName}`,
  isEmpty: rows => rows.length === 0,
  emptyFallback: { title: 'No matching group' },
});
const groupCounts = groupView.dataset({
  name: 'Group counts',
  select: rows => rows,
  rowKey: row => row.groupName,
  columns: {
    groupName: { value: row => row.groupName },
    sampleCount: { value: row => row.sampleCount, format: { kind: 'count' } },
  },
  evidence: { id: 'group-counts', glossaryIds: ['sampleCount'] },
});
const groupDetail = groupView.content(result => (
  <TableWidget dataset={groupCounts} source={result} />
));

function App() {
  return (
    <DataApp
      view={sampleCountsView}
      datasets={[sampleCounts]}
      story={story}
      details={[groupDetail]}
    >
      <DataSection content={sampleContent} />
    </DataApp>
  );
}
```

- The destination's operation lists the displayed filters it reads in
  `filters` and parses only its own fields, such as a record ID, with `input`.
- An action or `metric.records()` returns those own fields and any filter it
  narrows, such as the clicked group; the other filters carry over.
- Pass serializable IDs, never records or credentials. `parseInput` can reuse
  the operation's `input`.
- Detail content receives `result.scope`; `describeInput` defaults to the
  filters' description.

### Contributing metric records

Use `metric.records()` when a detail shows the records behind that metric, then
pass it to `<MetricWidget records={...}>`. Match record inclusion to the metric
and explain non-additive measures or completeness limits. Query matching records
rather than filtering a capped dashboard preview; use server pagination for
larger populations.
