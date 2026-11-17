# Direct UI composition

Import from `@altertable/data-app-react/ui` for setup/static screens, custom
controls, or a deliberately custom shell. For data-backed content, prefer declared views
and bound widgets from `@altertable/data-app-react`.

`<DataApp>` here renders a static screen and accepts optional direct CSV data.
Direct widget forms accept local values or rows. `<DataWidget>` supplies a generic
frame for deliberately custom content. Use `<GettingStarted>` for
connection setup. Fetched data belongs to a declared view; avoid inventing
request states to populate a shell.

Custom controls own values and change handlers; use `useAppFilters()` for
custom URL state. Use `<DataTable>` for custom tables and `<Tabs>`, `<Sheet>`,
and `<HelpPopover>` for navigation and overlays.

Standalone `<AboutData>`, glossary components, and `<PresentStory>` support
custom inspection and presentation. Supply registered context and evidence, and
derive findings from the displayed data. Standard widgets and `<DataApp>`
already own these experiences.

For framework mounting, `<DataAppProvider app={dataApp}>` supplies app identity, shared requests and one inspection sheet. Wrap custom shells in it; app components inherit identity and appearance.
Call `injectDataAppStyles()` before mounting either entry; imports do not install
styles.

## Tooltips and explanations

Use `<Tooltip>` for a short, supplemental description of an already labeled
control. Pass one child that forwards `aria-describedby` to its focusable DOM
element. Keep the accessible name on the control itself. `<IconButton>` already
includes a tooltip; use its `tooltip` prop to customize the hint.

```tsx
import { Button } from '@altertable/data-app-react';
import { Tooltip, TooltipProvider } from '@altertable/data-app-react/ui';

function ExportActions({ exportRows }: { exportRows: () => void }) {
  return (
    <TooltipProvider>
      <Tooltip content="Download the rows in the current view">
        <Button onClick={exportRows}>Export CSV</Button>
      </Tooltip>
      <Tooltip
        content="Available after data loads"
        tabIndex={0}
        role="group"
        aria-label="Export all rows unavailable"
      >
        <Button disabled>Export all rows</Button>
      </Tooltip>
    </TooltipProvider>
  );
}
```

`<AppLayout>` already provides shared timing. A standalone `<Tooltip>` works
without a provider; wrap adjacent custom controls in `<TooltipProvider>` to share
the first-hover delay and open subsequent hints immediately. Keyboard focus opens
hints immediately. The pointer can move onto the hint to keep it visible; Escape
or pressing the control dismisses it. Existing descriptions, child handlers, and
refs are preserved. Native span props and `ref` target the wrapper; make that
wrapper focusable for disabled controls or plain text.

Keep tooltip content non-interactive. Use `<HelpPopover>` for links, actions,
longer explanations, or information users must be able to open on touch devices.
Use `content={null}` to suppress an unavailable hint. Portals escape clipping
containers and stay inside a surrounding native dialog automatically; use
`portalRoot` only when a custom overlay needs a specific destination.

## Custom activity labels

For a custom activity label, wrap `<ShimmerText>` in `<output>`:

```tsx
import { ShimmerText } from '@altertable/data-app-react/ui';

function LoadingLabel() {
  return (
    <output>
      <ShimmerText>Loading results</ShimmerText>
    </output>
  );
}
```

## Keyboard actions

Use `isPlainKeyEvent()` from `@altertable/data-app-react/ui` in custom key handlers so local actions
leave shortcut modifiers and IME composition untouched:

```tsx
function SearchInput() {
  // ... submit handler
  return (
    <input
      aria-label="Search"
      onKeyDown={event => {
        if (event.key === 'Enter' && isPlainKeyEvent(event.nativeEvent)) {
          event.preventDefault();
          submit();
        }
      }}
    />
  );
}
```

Pass `{ allowShift: true }` when the handler also supports Shift gestures.

## Choose a selection control

Use `<DimensionPicker>` for typed field filters and `<ChoicePicker>` for searchable
values.

Use `<MenuTrigger>`, `<MenuButton>`, `<MenuPopover>`, `<Menu>`, and `<MenuItem>`
for commands or short choice menus
such as sort order or display mode. Actions use `onAction`. Set
`selectionMode="single"` for mutually exclusive choices (radio menu items), or
`selectionMode="multiple"` for independent toggles (checkbox menu items). Keep search fields and form inputs outside menus.

```tsx
<MenuTrigger>
  <MenuButton>Sort order</MenuButton>
  <MenuPopover>
    <Menu
      aria-label="Sort order"
      selectionMode="single"
      selectedKeys={[sortOrder]}
      onSelectionChange={keys => {
        if (keys !== 'all') setSortOrder(String([...keys][0]));
      }}
    >
      <MenuItem id="highest">Highest first</MenuItem>
      <MenuItem id="lowest">Lowest first</MenuItem>
    </Menu>
  </MenuPopover>
</MenuTrigger>
```

`<MenuButton>` accepts text or icons; give icon-only buttons an accessible name.
`<MenuPopover>` owns placement and popup styling.

Use `<MenuSection>` for grouped choices and `<MenuSeparator>` between groups.
Selection indicators derive from `selectionMode`; do not add checkbox markup.

## Charts

Choose a chart using the [visualization guide](widgets.md#choose-a-visualization).
Import `<BarChart>`, `<LineChart>`, `<AreaChart>`, `<PieChart>`, or `<ScatterChart>` from
`@altertable/data-app-react/ui`; `<ComposedChart>` exposes the series primitives for custom plots.
Compose the visual inside `<VisualizationWidget dataset={dataset} source={result}>`
so rows, loading state, evidence, and inspection come from that dataset.
Pass ordered items with unique, nonblank IDs and finite numbers. Bar and pie
values must be nonnegative. Use `formatValue` for domain formatting.

Line and area charts space samples equally; include missing periods and use
composed charts for irregular intervals. Distinguish missing observations from zero.
Pie slices represent mutually exclusive parts of one total; shares
use the sum of supplied items, so include Other when showing a subset of the
whole. Scatter points represent independent X/Y observations.

Use `useSvgId()` for stable IDs when composing custom SVG definitions.

### Product analytics charts

Use `<FunnelChart>`, `<RetentionChart>`, and `<JourneyChart>` from `@altertable/data-app-react/ui`
inside `<VisualizationWidget>`. Derive inputs from the displayed rows; the
binding owns loading, evidence, CSV, and story content. The query owns counting,
conversion windows, and cohort definitions; these components visualize results.

- `<FunnelChart>`: ordered steps and aligned, nonincreasing counts per population.
- `<RetentionChart>`: numeric offsets, fractional rates (`0.25`, not `25`), retained
  counts, and cohort size. Distinguish unobserved (`null`), observed zero, and
  observed but still accumulating (`incomplete`) periods. Offset labels come from
  supplied points; numeric spacing preserves elapsed distance.
- `<JourneyChart>`: full ordered paths with counts and outcomes; preserve repeated
  events and mark cut-off paths as `truncated`.

See the [complete component examples](https://github.com/altertable-ai/data-app/blob/main/dev/fixtures/gallery-basics.tsx)
for input shapes and composition. Read the exported types and JSDoc for exact
constraints before adapting displayed rows.

### Composed charts

Use `<ComposedChart>` from `@altertable/data-app-react/ui` for multiple series or mixed marks inside
`<VisualizationWidget>`. Pass the displayed rows and select fields with `dataKey`.
`<ComposedChart.Bar>`, `<ComposedChart.Line>`, and `<ComposedChart.Area>` share the
standalone charts' themed series primitives; axes, scatter, tooltip, and reference
primitives are also available.

Declare shared measure semantics with `valueFormat` (currency, count, or ratio).
Numeric Y axes automatically use a common k/M/B/T scale and precision derived from
visible ticks; tooltips retain the measure format. Ratios use percentages without
compact scaling. Set an axis `tickFormatter` or tooltip `formatter` to override
presentation, including when different axes represent different units.

```tsx
// ... revenueView and its revenue dataset
const revenueContent = revenueView.content(result => (
  <VisualizationWidget dataset={revenue} source={result}>
    {rows => (
      <ComposedChart
        data={rows}
        ariaLabel="Monthly revenue and target in euros"
        valueFormat={{ kind: 'currency', currency: 'EUR' }}
      >
        <ComposedChart.XAxis dataKey="month" />
        <ComposedChart.YAxis />
        <ComposedChart.Tooltip />
        <ComposedChart.Legend />
        <ComposedChart.Bar dataKey="revenue" name="Revenue (€)" />
        <ComposedChart.Line
          dataKey="target"
          name="Target (€)"
          stroke="var(--atbl-chart-2)"
        />
      </ComposedChart>
    )}
  </VisualizationWidget>
));
```

For irregular time intervals, use `<ComposedChart.XAxis>` with ISO dates, zoned
ISO timestamps, or `Date` values; spacing follows elapsed time. Use `scale="utc"`
for epoch milliseconds, or `type="category"` to keep date-like labels categorical.
On UTC axes, supplied `ticks` and `tickFormatter` take precedence over automatic labels.
Axes with `<ComposedChart.Bar>` reserve half the smallest date interval at both ends
to keep edge bars inside the plot. An explicit `domain` overrides this spacing.
Preserve missing measures as `null` and choose `connectNulls` deliberately; do not
replace missing observations with zero.

Label series and units clearly. See component JSDoc and the
[Recharts API](https://recharts.github.io/en-US/api/ComposedChart/) for options.
The dataset owns loading, empty results, evidence, CSV, and story content; keep
its columns aligned with the displayed measures.

### Legends

Include `<ComposedChart.Legend />` to derive labels and colored square markers from the series;
omit it when no legend is needed. For any chart, compose `<ChartLegend>` with
`<ChartLegend.Item>`, `<ChartLegend.Marker>`, and `<ChartLegend.Label>` using the
same names and colors as the plot. `<PieChart>` includes a legend by default; `showLegend={false}` omits it.

Legends describe series; authored toggles or a composed legend's `onClick`
leave series visibility to the app.

## Filter controls

Direct controls own accessible input and call the supplied change handler;
filter declarations own URL state, validation, and operation meaning.

| Control                            | Use                                                               |
| ---------------------------------- | ----------------------------------------------------------------- |
| `<SearchField>`                    | Search text                                                       |
| `<Select>`                         | One choice from a small fixed list                                |
| `<ChoicePicker>`                   | Searchable choices with explicit `selectionMode`                  |
| `<RadioGroup>` and `<Radio>`       | Visible exclusive choices                                         |
| `<CheckboxGroup>` and `<Checkbox>` | Visible independent choices                                       |
| `<SegmentedControl>`               | Compact radio choices                                             |
| `<NumberField>`                    | Localized numeric input; empty is `null`                          |
| `<NumberRangeField>`               | Exact, inclusive minimum/maximum; omitted bounds are unrestricted |
| `<DateTimeRangePicker>`            | Datetime ranges with an exclusive end                             |
| `<DimensionPicker>`                | Typed categorical predicates with fixed or facet options          |

```tsx
function FilterChoices() {
  // ... metric, statuses, and their change handlers
  return (
    <>
      <RadioGroup label="Metric" value={metric} onChange={setMetric}>
        <Radio value="orders">Orders</Radio>
        <Radio value="revenue">Revenue</Radio>
      </RadioGroup>

      <CheckboxGroup label="Statuses" values={statuses} onChange={setStatuses}>
        <Checkbox value="paid" label="Paid" />
        <Checkbox value="pending" label="Pending" />
      </CheckboxGroup>
    </>
  );
}
```

A standalone `<Checkbox>` uses `checked` and `onChange`; group items use `value`.

Use `<FilterBar>` to arrange predicates and `<ControlBar>` for a row of mixed
search, filter, and display controls. Use `<FilterActions>` for Clear or paired Apply/Cancel actions on
app-owned drafts; provide the handlers for your applied state.

Use `<NumberFilterPicker>` for a numeric predicate popover or numeric fields
for inline forms.

Use `<Button variant="primary">` for the main committing action, such as Apply.
Use outline and ghost buttons for secondary actions.
Use `<Button variant="inline">` for actions within text or table cells. Use buttons for opening sheets and links for URL navigation.

## Datetime selection

Prefer a [datetime filter](filters.md#date-ranges)
for generated controls and URL state. For custom screens, `<DateTimeRangePicker>`
accepts the same `DateTimeRange` and preset sets, with calendar and natural-language
entry. Pass `policy={period.policy}` to apply a date filter's coverage and time
zone. See its props in [REFERENCE.md](../REFERENCE.md).
