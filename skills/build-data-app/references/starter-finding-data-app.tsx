import { defineDataApp } from '@altertable/data-app';
import {
  createDataContext,
  injectDataAppStyles,
  mountDataApp,
} from '@altertable/data-app-react';
import {
  createDataHooks,
  DataApp,
  DataSection,
  MetricWidget,
  Stack,
  TableWidget,
  VisualizationWidget,
} from '@altertable/data-app-react';
import { BarChart, ComposedChart } from '@altertable/data-app-react/ui';
import { createDataClient } from '@altertable/data-app/client';
import {
  dateTimeRangeFilter,
  displayChoice,
  parseCount,
} from '@altertable/data-app/contract';
// One query per widget: each section loads its own result when it nears the viewport.
const dataApp = defineDataApp({
  title: 'Sample finding',
  description:
    'Fixture evidence; replace with the Finding and its supporting queries.',
  scope: { organization: 'demo', environment: 'sample' },
  appearance: { theme: 'system' },
  queries: {
    sampleTotal: {
      projections: { sample_count: { type: 'number' } },
      statement: `
SELECT COALESCE(SUM(sample_count), 0) AS sample_count
FROM starter_demo.daily_samples
WHERE sample_date >= $period.from AND sample_date < $period.to`,
      params: { period: { type: 'dateTimeRange' } },
    },
    samplesOverTime: {
      projections: {
        period_start: { type: 'string' },
        sample_count: { type: 'number' },
      },
      statement: `
SELECT strftime(date_trunc($grain, sample_date), '%Y-%m-%d') AS period_start,
  SUM(sample_count) AS sample_count
FROM starter_demo.daily_samples
WHERE sample_date >= $period.from AND sample_date < $period.to
GROUP BY ALL ORDER BY period_start LIMIT 200`,
      params: {
        period: { type: 'dateTimeRange' },
        grain: { type: 'string', defaultValue: 'day' },
      },
    },
    samplesByMember: {
      projections: {
        member: { type: 'string' },
        sample_count: { type: 'number' },
      },
      statement: `
SELECT CASE WHEN $breakdown = 'group' THEN group_name ELSE segment_name END AS member,
  SUM(sample_count) AS sample_count
FROM starter_demo.daily_samples
WHERE sample_date >= $period.from AND sample_date < $period.to
GROUP BY ALL ORDER BY sample_count DESC LIMIT 50`,
      params: {
        period: { type: 'dateTimeRange' },
        breakdown: { type: 'string', defaultValue: 'segment' },
      },
    },
    sampleRows: {
      projections: {
        period_start: { type: 'string' },
        member: { type: 'string' },
        sample_count: { type: 'number' },
      },
      statement: `
SELECT strftime(date_trunc($grain, sample_date), '%Y-%m-%d') AS period_start,
  CASE WHEN $breakdown = 'group' THEN group_name ELSE segment_name END AS member,
  SUM(sample_count) AS sample_count
FROM starter_demo.daily_samples
WHERE sample_date >= $period.from AND sample_date < $period.to
GROUP BY ALL ORDER BY period_start, member LIMIT 500`,
      params: {
        period: { type: 'dateTimeRange' },
        grain: { type: 'string', defaultValue: 'day' },
        breakdown: { type: 'string', defaultValue: 'segment' },
      },
    },
  },
});
// Declare each filter once; each operation lists the filters it reads.
const findingPeriod = {
  from: new Date('2026-03-09T00:00:00Z'),
  to: new Date('2026-03-16T00:00:00Z'),
};
const period = dateTimeRangeFilter({
  key: 'period',
  defaultValue: findingPeriod,
  minDate: '2026-01-05',
  maxDate: '2026-03-29',
  maxRangeDays: 28,
  comparison: 'off',
  presets: [{ label: 'Finding period', range: findingPeriod }],
});
const grain = displayChoice({
  key: 'grain',
  label: 'Grain',
  defaultValue: 'day',
  options: [
    { id: 'day', label: 'Day' },
    { id: 'week', label: 'Week' },
  ],
  presentation: { control: 'widget' },
});
const breakdown = displayChoice({
  key: 'breakdown',
  label: 'Breakdown',
  defaultValue: 'segment',
  options: [
    { id: 'segment', label: 'Segment' },
    { id: 'group', label: 'Group' },
  ],
  presentation: { control: 'widget' },
});
const policy = { maxQueryRows: 500, maxDurationMs: 15000 };
const operations = {
  sampleTotal: dataApp.defineOperation({
    filters: { period },
    policy,
    async run({ query }, { period }) {
      const current = await query('sampleTotal', { period: period.range });
      const previous = period.comparison
        ? await query('sampleTotal', { period: period.comparison })
        : null;
      return {
        current: parseCount(current.rows[0]!.sample_count),
        previous: previous && parseCount(previous.rows[0]!.sample_count),
      };
    },
  }),
  samplesOverTime: dataApp.defineOperation({
    filters: { period, grain },
    policy,
    async run({ query }, { period, grain }) {
      // With the comparison on, the trend starts at the previous period.
      const range = {
        from: period.comparison?.from ?? period.range.from,
        to: period.range.to,
      };
      const result = await query('samplesOverTime', { period: range, grain });
      return result.rows.map(row => ({
        periodStart: row.period_start,
        sampleCount: parseCount(row.sample_count),
      }));
    },
  }),
  samplesByMember: dataApp.defineOperation({
    filters: { period, breakdown },
    policy,
    async run({ query }, { period, breakdown }) {
      const result = await query('samplesByMember', {
        period: period.range,
        breakdown,
      });
      return result.rows.map(row => ({
        member: row.member,
        sampleCount: parseCount(row.sample_count),
      }));
    },
  }),
  sampleRows: dataApp.defineOperation({
    filters: { period, grain, breakdown },
    policy,
    async run({ query }, { period, grain, breakdown }) {
      const result = await query('sampleRows', {
        period: period.range,
        grain,
        breakdown,
      });
      return result.rows.map(row => ({
        periodStart: row.period_start,
        member: row.member,
        sampleCount: parseCount(row.sample_count),
      }));
    },
  }),
};
const queryNames = {
  ...operations.sampleTotal.queryNames,
  ...operations.samplesOverTime.queryNames,
  ...operations.samplesByMember.queryNames,
  ...operations.sampleRows.queryNames,
};
const sampleDataContext = createDataContext(queryNames)({
  description:
    'Fictional daily samples from starter_demo.daily_samples. Replace this evidence with the actual Finding queries.',
  glossary: {
    sampleCount: {
      term: 'Sample count',
      definition: 'Fixture samples recorded per day, group, and segment.',
      queryNames: Object.values(queryNames),
    },
  },
});
const { defineView } = createDataHooks(createDataClient({ operations }));
const count = { kind: 'count' } as const;
const emptyFallback = {
  title: 'No samples in this period',
  description: 'No observations are available for this period.',
};
const totalView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleTotal',
});
const totalSamples = totalView.metric(
  {
    id: 'total-samples',
    label: 'Samples',
    glossaryId: 'sampleCount',
    format: count,
  },
  total => ({
    current: total.current,
    ...(total.previous !== null && { previous: total.previous }),
  })
);
const trendView = defineView({
  dataContext: sampleDataContext,
  operation: 'samplesOverTime',
  isEmpty: rows => rows.length === 0,
  emptyFallback,
});
const trend = trendView.dataset({
  name: 'Samples over time',
  select: rows => rows,
  rowKey: row => row.periodStart,
  columns: {
    periodStart: { label: 'Period start', value: row => row.periodStart },
    sampleCount: { value: row => row.sampleCount, format: count },
  },
  evidence: { id: 'samples-over-time', glossaryIds: ['sampleCount'] },
});
const memberView = defineView({
  dataContext: sampleDataContext,
  operation: 'samplesByMember',
  isEmpty: rows => rows.length === 0,
  emptyFallback,
});
const byMember = memberView.dataset({
  name: 'Samples by member',
  select: rows => rows,
  rowKey: row => row.member,
  columns: {
    member: { label: 'Member', value: row => row.member },
    sampleCount: { value: row => row.sampleCount, format: count },
  },
  evidence: { id: 'samples-by-member', glossaryIds: ['sampleCount'] },
});
const rowsView = defineView({
  dataContext: sampleDataContext,
  operation: 'sampleRows',
  isEmpty: rows => rows.length === 0,
  emptyFallback,
});
const sampleRows = rowsView.dataset({
  name: 'Samples',
  select: rows => rows,
  rowKey: row => `${row.periodStart}:${row.member}`,
  columns: {
    periodStart: { label: 'Period start', value: row => row.periodStart },
    member: { label: 'Member', value: row => row.member },
    sampleCount: { value: row => row.sampleCount, format: count },
  },
  evidence: { id: 'samples', glossaryIds: ['sampleCount'] },
});
// The Finding's text is shown above the app; keep content to charts and captions.
const totalContent = totalView.content(result => (
  <MetricWidget metric={totalSamples} source={result} />
));
const trendContent = trendView.content(result => (
  <VisualizationWidget
    dataset={trend}
    source={result}
    title="Samples over time"
    description="Includes the previous period when comparison is on."
    breakdown={trendView.breakdown('grain')}
  >
    {rows => (
      <ComposedChart
        ariaLabel="Samples over time"
        data={rows}
        valueFormat={count}
      >
        <ComposedChart.XAxis dataKey="periodStart" />
        <ComposedChart.YAxis />
        <ComposedChart.Line dataKey="sampleCount" name="Samples" />
        <ComposedChart.Tooltip />
      </ComposedChart>
    )}
  </VisualizationWidget>
));
const memberContent = memberView.content(result => (
  <VisualizationWidget
    dataset={byMember}
    source={result}
    title="Samples by member"
    breakdown={memberView.breakdown('breakdown')}
  >
    {rows => (
      <BarChart
        ariaLabel="Samples by member"
        unit="samples"
        items={rows.map(row => ({
          ...row,
          id: row.member,
          label: row.member,
          value: row.sampleCount,
        }))}
      />
    )}
  </VisualizationWidget>
));
const rowsContent = rowsView.content(result => (
  <TableWidget dataset={sampleRows} source={result} title="Samples" />
));
function App() {
  return (
    <DataApp view={totalView} showToolbar={false}>
      <Stack>
        <DataSection content={totalContent} />
        <DataSection content={trendContent} />
        <DataSection content={memberContent} />
        <DataSection content={rowsContent} />
      </Stack>
    </DataApp>
  );
}
injectDataAppStyles();
mountDataApp({ app: dataApp, component: App });
