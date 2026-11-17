import { defineDataApp } from '@altertable/data-app';
import {
  createDataContext,
  createDataHooks,
  DataApp,
  DataSection,
  DataValue,
  TableWidget,
  Stack,
  TextContent,
  injectDataAppStyles,
  mountDataApp,
  MetricWidget,
} from '@altertable/data-app-react';
import { createDataClient } from '@altertable/data-app/client';
import { parseCount, searchFilter } from '@altertable/data-app/contract';
import { formatMetric } from '@altertable/data-app/format';

const dataApp = defineDataApp({
  title: 'Sample counts',
  description: 'Explore sample counts by group.',
  scope: { organization: 'demo', environment: 'sample' },
  appearance: { theme: 'system' },
  queries: {
    sampleCountsByGroup: {
      projections: {
        group_name: { type: 'string' },
        sample_count: { type: 'number' },
      },
      statement: `
WITH sample_counts(group_name, sample_count) AS (VALUES ('Alpha', 2200000), ('Beta', 0))
SELECT group_name, sample_count FROM sample_counts
WHERE $groupName = '' OR group_name = $groupName
ORDER BY group_name LIMIT $limit`,
      params: {
        groupName: { type: 'string', defaultValue: '' },
        limit: { type: 'number', defaultValue: 10 },
      },
    },
    sampleTotal: {
      projections: { sample_count: { type: 'number' } },
      statement: `
WITH sample_counts(group_name, sample_count) AS (VALUES ('Alpha', 2200000), ('Beta', 0))
SELECT CAST(COALESCE(SUM(sample_count), 0) AS BIGINT) AS sample_count FROM sample_counts
WHERE $groupName = '' OR group_name = $groupName`,
      params: { groupName: { type: 'string', defaultValue: '' } },
    },
  },
});
// Declare each filter once; operations list the filters they read, and views,
// controls, and scope derive from them.
const groupName = searchFilter({ key: 'group', label: 'Group' });
const operations = {
  sampleCountsByGroup: dataApp.defineOperation({
    filters: { groupName },
    policy: { maxQueryRows: 10, maxDurationMs: 15000 },
    async run({ query }, { groupName }) {
      const queryResult = await query('sampleCountsByGroup', { groupName });
      return queryResult.rows.map(row => ({
        groupName: row.group_name,
        sampleCount: parseCount(row.sample_count),
      }));
    },
  }),
  sampleTotal: dataApp.defineOperation({
    filters: { groupName },
    policy: { maxQueryRows: 1, maxDurationMs: 15000 },
    async run({ query }, { groupName }) {
      const queryResult = await query('sampleTotal', { groupName });
      return { sampleCount: parseCount(queryResult.rows[0]?.sample_count) };
    },
  }),
};
const queryNames = {
  ...operations.sampleCountsByGroup.queryNames,
  ...operations.sampleTotal.queryNames,
};
const sampleDataContext = createDataContext(queryNames)({
  description:
    'Two SQL VALUES rows demonstrate the host query path. Replace them with inspected source data before publishing findings.',
  glossary: {
    sampleCount: {
      term: 'Sample count',
      definition:
        'A fixture value: Alpha is 2,200,000 and Beta is a measured zero.',
      queryNames: [queryNames.sampleCountsByGroup, queryNames.sampleTotal],
    },
  },
});
const { defineView } = createDataHooks(createDataClient({ operations }));
const sampleCountsView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleCountsByGroup',
  isEmpty: sampleCounts => sampleCounts.length === 0,
  emptyFallback: {
    title: 'No matching groups',
    description: 'Try Alpha, Beta, or clear the group filter.',
  },
});
const sampleCounts = sampleCountsView.dataset({
  name: 'Sample counts',
  select: rows => rows,
  rowKey: row => row.groupName,
  columns: {
    groupName: { label: 'Group', value: row => row.groupName },
    sampleCount: { value: row => row.sampleCount, format: { kind: 'count' } },
  },
  evidence: {
    id: 'counts-by-group',
    glossaryIds: ['sampleCount'],
  },
});
const sampleTotalView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleTotal',
});
const totalSamples = sampleTotalView.metric(
  {
    id: 'total-samples',
    glossaryId: 'sampleCount',
    label: 'Total samples',
    format: { kind: 'count', compact: true },
  },
  total => ({ current: total.sampleCount })
);
const totalContent = sampleTotalView.content(result => (
  <Stack>
    <TextContent>
      <p>
        Showing <DataValue scope={result.scope} />
      </p>
    </TextContent>
    <MetricWidget
      metric={totalSamples}
      source={result}
      description="Sum of the fixture counts in the selected groups."
    />
  </Stack>
));
const countsContent = sampleCountsView.content(result => (
  <TableWidget
    dataset={sampleCounts}
    source={result}
    title="Counts by group"
    description="Alpha and Beta demonstrate measured values, including zero."
    pagination={false}
  />
));
function App() {
  return (
    <DataApp
      view={sampleCountsView}
      summaryViews={[sampleTotalView]}
      datasets={[sampleCounts]}
      story={(countsSnapshot, totalSnapshot) => {
        const total = totalSamples.read(totalSnapshot);
        const scope = sampleCountsView.scope(countsSnapshot);
        return [
          {
            id: 'total-samples',
            headline: `Total samples: ${formatMetric(total.value.current, totalSamples.definition.format)}`,
            context: `Demonstration values for ${scope}.`,
            visual: (
              <MetricWidget metric={totalSamples} source={totalSnapshot} />
            ),
            visualKind: 'metric',
            evidence: totalSamples,
          },
          {
            id: 'counts-by-group',
            headline: 'Counts by group',
            context: `Demonstration values for ${scope}.`,
            visual: (
              <TableWidget
                dataset={sampleCounts}
                source={countsSnapshot}
                pagination={false}
              />
            ),
            evidence: sampleCounts,
          },
        ];
      }}
    >
      <Stack>
        <TextContent>
          <h2>Sample counts</h2>
        </TextContent>
        <DataSection content={totalContent} label="Sample total" />
        <DataSection content={countsContent} label="Group counts" />
      </Stack>
    </DataApp>
  );
}
injectDataAppStyles();
mountDataApp({ app: dataApp, component: App });
