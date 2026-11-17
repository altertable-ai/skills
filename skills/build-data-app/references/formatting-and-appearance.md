# Formatting and appearance

Use package helpers so a value has the same meaning in prose, tables, charts,
and stories. TypeScript and JSDoc describe options and supported values.

## Format values

Import formatting helpers from `@altertable/data-app/format`.

| Helper              | Use                                                    |
| ------------------- | ------------------------------------------------------ |
| `formatNumber()`    | General numerical values                               |
| `formatCount()`     | Nonnegative integer counts, optionally compact         |
| `formatPercent()`   | Ratios represented as a fraction, such as 0.12 for 12% |
| `formatMetric()`    | A metric definition's count, ratio, or currency format |
| `formatDate()`      | Calendar dates without time-zone shifts                |
| `formatDateTime()`  | Event timestamps in the reporting time zone            |
| `formatTime()`      | Intraday chart labels                                  |
| `formatDateRange()` | Inclusive calendar ranges                              |
| `pluralize()`       | Count-dependent labels                                 |

Missing values render distinctly from measured zero. Declare formatting once on
`view.metric()` so widgets, comparisons, and narrative share it; reuse the
definition with `formatMetric()` in story headlines.

Use compact counts for headline metrics and chart labels. Declare count metrics
with `format: { kind: 'count', compact: true }`. Keep full counts in tables used
for precise comparisons and raw numeric values in datasets for CSV export.

```ts
formatCount(2_200_000, { compact: true }); // "2.2M"
formatCount(2_200_000); // "2,200,000"
```

For signed or fractional measures, use `formatNumber()` with
`notation: 'compact'` and preserve the measure's units.

Use `chartColor()` from `@altertable/data-app-react` for palette colors.

## Display dates consistently

Declare date meaning on dataset columns so tables use readable values and CSV
keeps the originals:

```ts
// ... dailyCountsView with day and observed result fields
const dailyCounts = dailyCountsView.dataset({
  // ... name, select, rowKey, and evidence
  columns: {
    day: { value: row => row.day, format: { kind: 'date' } },
    observed: {
      value: row => row.observed,
      format: { kind: 'dateTime', precision: 'second' },
    },
  },
});
```

Calendar dates use `YYYY-MM-DD`. Instants accept epoch milliseconds or timestamp
strings; `<DateDisplay>` also accepts `Date`. Timestamp strings require `Z` or an explicit
offset; convert database-local timestamps in the operation using their known
source zone. Ambiguous or invalid values display as missing.

Use `<DateDisplay>` for prose and `useDateFormatting()` with format helpers for
custom chart labels. Defaults are `en-US` and UTC; configure app-wide
`dateFormatting: { locale, timeZone }` when appropriate. A time view supplies its
reporting zone, and an explicit field zone overrides it. Keep seconds when event
ordering matters; exact-time details remain available on timestamps.

## Configure identity and appearance

Set `title`, `description`, and connection `scope` in `defineDataApp()`. Scope
labels describe the connection; they do not grant access.

Keep default appearance. Customize only when requested, configuring it once: `baseColor` for
the base palette, `accentColor` and optional `darkAccentColor` for emphasis,
and `chartColors` for charts. Preserve semantic favorable/unfavorable colors.
Embedded apps follow the parent's resolved theme.
