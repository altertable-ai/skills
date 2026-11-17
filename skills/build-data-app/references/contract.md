# Queries and operations

Keep the starter's `defineDataApp()` declaration and operation registry. Declare
named SQL queries with typed `params` and `projections`; execute them through
`dataApp.defineOperation()`. Write one query and operation per widget result,
and use descriptive `lowerCamelCase` query names.

## Execute named queries

This is the hosted starter's query contract inside `defineDataApp()`:

```ts
import { defineDataApp } from '@altertable/data-app';

const dataApp = defineDataApp({
  // ... title, description, and scope
  queries: {
    sampleCountsByGroup: {
      statement: `
WITH sample_counts(group_name, sample_count) AS (VALUES ('Alpha', 2200000), ('Beta', 0))
SELECT group_name, sample_count FROM sample_counts
WHERE $groupName = '' OR group_name = $groupName
ORDER BY group_name LIMIT $limit`,
      params: {
        groupName: { type: 'string', defaultValue: '' },
        limit: { type: 'number', defaultValue: 10 },
      },
      projections: {
        group_name: { type: 'string' },
        sample_count: { type: 'number' },
      },
    },
  },
});
```

Replace fixture SQL with inspected data. Keep query declarations and projections
in sync when adapting SQL to the app's inputs. Preserve metric definitions.
List the [filters](filters.md) an operation reads; `run()` receives one flat
field per filter, and you derive SQL parameters inside it:

```ts
import { parseCount, searchFilter } from '@altertable/data-app/contract';

// ... dataApp
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
};
```

The filters validate input and supply the operation's checks; enforce business
rules in `run()`. Omit `filters` for an operation without inputs. An operation
with its own fields, such as a detail record ID, adds an `input` parser and
representative valid `checks` for those fields; its `filters` still parse the
scope it reads. Derive results from `query()` rows
without duplicate schemas or type assertions; clients and views infer the
returned type. HTTP results must be JSON-serializable.

Host `queryParams` supplies protected parameters that callers cannot override.
Other values come from `query()` arguments or defaults. The host/backend enforces
data access and limits. Operation policies must set `maxQueryRows` to a positive
integer no greater than 10,000. The shared SQL host handler also rejects requests
for more than 10,000 rows.

### Declare query projections

Declare every returned SQL alias with `{ type, nullable? }` and keep its exact
casing. Infer nullability from the schema and SQL, not sampled rows. Update
projections when changing SQL. `query()` converts cells to declared types;
return SQL text and declare `string` when exact numeric precision matters.

Use `operations.sampleCountsByGroup.queryNames` for context and evidence.

### Bind date ranges

Declare `{ type: 'dateTimeRange' }` and pass a date filter's `range` or
`comparison`. Reference its bounds as `$period.from` (inclusive) and
`$period.to` (exclusive):

```ts
const dataApp = defineDataApp({
  // ... title, description, and scope
  queries: {
    dailyOrders: {
      statement: `SELECT CAST(ordered_at AS DATE) AS day, count(*) AS orders
        FROM orders
        WHERE ordered_at >= $period.from AND ordered_at < $period.to
        GROUP BY day ORDER BY day`,
      params: { period: { type: 'dateTimeRange' } },
      projections: {
        day: { type: 'string' },
        orders: { type: 'number' },
      },
    },
  },
});
```

Date filters pass resolved bounds in their `timeZone`, encoded as UTC wall-clock
fields: 4 PM in the reporting zone is 16:00Z. SQL bounds are therefore
timezone-free timestamps; interpret timestamp-with-timezone columns in that same
zone. Coverage and duration limits live on the
[date filter](filters.md#date-ranges).
