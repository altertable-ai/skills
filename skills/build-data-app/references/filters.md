# Filters and display options

Declare each filter once as a constant and list it in `filters` on every
operation that reads it. Everything else derives from that list: input
validation, checks, the view's period and scope, and the controls `<DataApp>`
renders. Import filters from `@altertable/data-app/contract`.

## Declare filters on operations

The hosted starter's operations both read one group search:

```tsx
import { parseCount, searchFilter } from '@altertable/data-app/contract';

// ... dataApp, sampleDataContext, and section contents
const groupName = searchFilter({ key: 'group', label: 'Group' });

const operations = {
  sampleCountsByGroup: dataApp.defineOperation({
    filters: { groupName },
    policy: { maxQueryRows: 10, maxDurationMs: 15000 },
    async run({ query }, { groupName }) {
      const result = await query('sampleCountsByGroup', { groupName });
      return result.rows.map(row => ({
        groupName: row.group_name,
        sampleCount: parseCount(row.sample_count),
      }));
    },
  }),
  // ... sampleTotal reads the same { groupName }
};
const { defineView } = createDataHooks(createDataClient({ operations }));
const sampleCountsView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleCountsByGroup',
  isEmpty: rows => rows.length === 0,
  emptyFallback: { title: 'No matching groups' },
});

function App() {
  return (
    <DataApp view={sampleCountsView}>
      <DataSection content={countsContent} />
    </DataApp>
  );
}
```

- Reuse the same constant on every operation that reads it; two filters with one
  name, or one URL key, fail.
- Omit `filters` for an operation without inputs.
- A detail operation that also needs its own fields, such as a record ID, keeps
  `filters` for the scope and adds `input` and `checks` for those fields only.
- The view's scope reads like “Mar 1–7, 2026 UTC · group Alpha” or “all data”.
  Pass `describeInput` only for different copy.
- Use `searchFilter()` to query the server; use a table's `search` prop to filter
  rows already loaded.

## Read filter values

`run(context, input)` receives one field per declared filter:

| Filter                                                 | Input value                                    |
| ------------------------------------------------------ | ---------------------------------------------- |
| `searchFilter()`                                       | `string`, at most `maxLength` (200 by default) |
| `choiceFilter()`, `displayChoice()`                    | Selected option ID                             |
| `multiChoiceFilter()`                                  | Selected option IDs                            |
| `dimensionFilter()`, `facetFilter()`, source dimension | `DimensionSelection`                           |
| `numberFilter()`, `booleanFilter()`                    | `NumberSelection`, `BooleanSelection`          |
| `dateTimeRangeFilter()`                                | `{ range, comparison }` of resolved dates      |

Pass values to declared query parameters; never interpolate them into SQL. Date
ranges bind as [`dateTimeRange` parameters](contract.md#bind-date-ranges). A
dimension selection binds whole to a `{ type: 'dimension', valueType }`
parameter; `$country.matches(column)` keeps the selected rows, including
multiple members, missing values, and exclusion:

```ts
// ... in defineDataApp({ queries })
revenueByCampaign: {
  statement: `SELECT o.campaign, sum(o.amount) AS revenue
    FROM demo.orders o JOIN demo.customers c ON c.id = o.customer_id
    WHERE $country.matches(c.country)
    GROUP BY o.campaign`,
  params: { country: { type: 'dimension', valueType: 'string' } },
  projections: { campaign: { type: 'string' }, revenue: { type: 'number' } },
},
// ... in the operation: query('revenueByCampaign', { country: input.country })
```

Dimension, number, and boolean selections support `{ kind: 'all' }`. Offer only
predicates the registered query supports.

## Categorical dimensions

For source-backed members, use `dataApp.defineDimension()`:

```ts
// ... dataApp with its registered groups query
const group = dataApp.defineDimension({
  key: 'group',
  label: 'Group',
  valueType: 'string',
  selectionMode: 'multiple',
  source: { query: 'groups' },
});
```

Declare the source query in `defineDataApp()` with a nullable `member` parameter
matching `valueType`. Its nonnullable projections are `value` (same type),
`label` (string), and optional `count` (number). Null requests options; a selected
member requests exact lookup. Other parameters need defaults or trusted values:

```sql
SELECT DISTINCT group_name AS value, group_name AS label
FROM sample_counts
WHERE ($member IS NULL OR group_name = $member)
ORDER BY label
```

Operations reading `group` check selected members against this query before
`run()`. Use `dimensionFilter()` when options are known constants:

```ts
const group = dimensionFilter({
  key: 'group',
  label: 'Group',
  valueType: 'string',
  selectionMode: 'multiple',
  options: [
    { value: 'Alpha', label: 'Alpha' },
    { value: 'Beta', label: 'Beta' },
  ],
});
```

Set `defaultValue` to start from a narrower selection, such as
`{ kind: 'include', members: [{ kind: 'value', value: 'paid' }] }`; clearing
filters still returns to every member.

No selection means every member. Enable `allowExclusion` and `allowMissing` only
when the query handles them. Use `multiChoiceFilter()` for fixed multiselect
choices; empty means no choices, unlike an unrestricted dimension.

## Facet filters

Use `facetFilter()` only when options must follow other selections:

```ts
// ... period filter
const group = facetFilter({
  key: 'group',
  label: 'Group',
  valueType: 'string',
  selectionMode: 'multiple',
  options: 'groupOptions',
});
const operations = {
  groupOptions: dataApp.defineOperation({
    filters: { period },
    // ... policy, and run() returning DimensionOption[] for the period
  }),
  groupCounts: dataApp.defineOperation({
    filters: { period, group },
    // ... policy and run()
  }),
};
```

- `options` names a registered operation. Its filters decide what narrows the
  options: here, changing `period` reloads them.
- Return `{ value, label, count? }[]` from `run()`, at most 200 values. The picker
  shows `count` beside each option.
- The server checks a facet selection's shape, not its members; use a source
  dimension when unknown members must be rejected.

## Display choices and breakdowns

Use `displayChoice()` for a choice that changes how results are shown rather
than which data is included. List it on the operation, which receives the
selected ID and groups its results accordingly:

```ts
const countsBy = displayChoice({
  key: 'counts-by',
  label: 'Counts breakdown',
  defaultValue: 'group',
  options: [
    { id: 'group', label: 'Group' },
    { id: 'country', label: 'Country' },
  ],
  presentation: { control: 'widget' },
});
// ... sampleCountsByGroup declares filters: { groupName, countsBy }
```

Pass `view.breakdown('countsBy')` to `<VisualizationWidget breakdown>`. Without
`control: 'widget'`, the choice renders in the toolbar's display options. Use one
choice per independently controlled chart. Use
`presentation.prominence: 'secondary'` for less frequent filters.

## Date ranges

Use one `dateTimeRangeFilter()` per operation. It sets the view's reporting
period, time zone, and metric comparisons:

```ts
import {
  dateTimeRangeFilter,
  dateTimeRangePresets,
} from '@altertable/data-app/contract';

const period = dateTimeRangeFilter({
  key: 'period',
  defaultValue: '30d',
  maxRangeDays: 90,
  comparison: 'off',
  presets: dateTimeRangePresets.analytics,
});
const dailyCounts = dataApp.defineOperation({
  filters: { period, groupName },
  policy: { maxQueryRows: 100, maxDurationMs: 15000 },
  async run({ query }, { period, groupName }) {
    const current = await query('dailyCounts', {
      period: period.range,
      groupName,
    });
    // ... query { period: period.comparison } when it is not null
    return current.rows;
  },
});
```

- `run()` receives `{ range, comparison }` with resolved dates. Ranges include
  `from` and exclude `to`: September 24–30 queries `2026-09-24T00:00:00Z`
  through `2026-10-01T00:00:00Z`. Bind them to a
  [`dateTimeRange` parameter](contract.md#bind-date-ranges).
- A range that runs past now ends at now: today picked in the calendar queries
  midnight through the current time.
- `comparison: 'off'` or `'on'` offers the previous-period toggle, starting in
  that state. `period.comparison` is the same window one selected length
  earlier, such as yesterday through the same time, while the toggle is on, and
  `null` otherwise. Omit `comparison` for no toggle.
- `defaultValue` and preset `range` take range text such as `'24h'`, `'7d'`, or
  `'6mo'`, or `{ from, to }`. `dateTimeRangePresets.analytics` covers days to a
  year; `dateTimeRangePresets.monitoring` covers minutes to 24 hours.
- Relative ranges such as `'7d'` resolve in `timeZone`, UTC by default.
- `minDate`, `maxDate`, and `maxRangeDays` limit what readers can pick.
  Coverage runs through now; set `completeDays: true` to end it yesterday when
  the source loads whole days.

## Exclusion, clear, and reset

Clear removes filter predicates and returns dates to defaults, preserving search
and display choices. `resetAll()` restores all defaults. Filters apply immediately;
use app-owned drafts only when the task needs Apply/Cancel.

Custom control ownership is needed only when generated controls cannot express
the requirement; use `/ui` for that case. Do not reuse reserved inspection,
presentation, or navigation URL keys.

## Share filters with HTTP and local apps

HTTP and local apps keep operations on the server, so the browser imports them
as types only. Declare filters in a browser-safe module that both sides import:

```ts
// src/filters.ts
import { choiceFilter } from '@altertable/data-app/contract';

const groupName = choiceFilter({
  // ... key, label, defaultValue, and options
});

export const operationFilters = {
  sampleCountsByGroup: { groupName },
  sampleCountsBySegment: { groupName },
};
```

Each operation in `src/operations.ts` declares
`filters: operationFilters.sampleCountsByGroup`, and the browser client receives
the same map:

```ts
// src/App.tsx
import { operationFilters } from '#app/filters.ts';
import type { operations } from '#app/operations.ts';

const { defineView } = createDataHooks(
  createDataClient<typeof operations>({ filters: operationFilters })
);
```

The client's types require `filters` whenever an operation declares them.
