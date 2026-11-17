# Stories and CSV export

The bound `<DataApp>` from `@altertable/data-app-react` accepts an optional `story`
callback and optional nonempty `datasets` list. Omit either prop to omit its toolbar
control. Supplied features use the displayed snapshot, including during refresh or
failure. A story callback returning `[]` leaves a disabled presentation action.
Set `showToolbar={false}` to omit page actions together; data loading, error states,
and declared filters remain available. Setup and static screens can use `<DataApp>`
from `/ui`.

These are component contracts. The app brief determines the
intended presentation and export coverage. A presentation story is distinct from
explanatory prose in the app body.

## Present data with stories

Continue the starter's `totalSamples` binding. Return one to four findings with a
headline, visual, and registered dataset or
metric as `evidence`. The story receives `view`'s displayed snapshot, then one
snapshot per entry in `summaryViews`. Reuse each binding with its own view's
snapshot and derive scope from it:

```tsx
// ... sampleCountsView, sampleTotalView, sampleCounts, totalSamples, and contents
function App() {
  return (
    <DataApp
      view={sampleCountsView}
      summaryViews={[sampleTotalView]}
      datasets={[sampleCounts]}
      story={(countsSnapshot, totalSnapshot) => {
        const total = totalSamples.read(totalSnapshot);
        return [
          {
            id: 'total-samples',
            headline: `Total samples: ${formatMetric(total.value.current, totalSamples.definition.format)}`,
            context: sampleCountsView.scope(countsSnapshot),
            visual: (
              <MetricWidget metric={totalSamples} source={totalSnapshot} />
            ),
            evidence: totalSamples,
          },
        ];
      }}
    >
      <DataSection content={totalContent} />
      <DataSection content={countsContent} />
    </DataApp>
  );
}
```

List a view in `summaryViews` only when the story or export reads it: summary
views load with the page instead of when their sections near the viewport.

Keep the starter's `formatMetric()` import for formatted headlines.

## Export displayed data as CSV

Declare [datasets](widgets.md#declare-datasets-and-metrics) once and pass
`datasets={[sampleCounts]}`. List datasets from `view` or a summary view; each
exports its bound rows and columns. Preserve the displayed grain; reuse a dataset
for visuals sharing the same rows.

One dataset downloads as CSV; multiple datasets offer individual downloads and
**Export all** as ZIP. Filenames use the displayed scope. Accessors must return
raw values: null and undefined export as empty cells, and measured zero stays
zero. Export handles quoting and spreadsheet formula protection.
