# Author a data app

Use the SDK to connect queries, operations, views, and widgets. The app brief determines the content structure. Component examples do not prescribe
which sections or features every app must contain.

## Use release-matched starters

For an existing app, keep its runtime and structure; apply only the steps needed
for the requested change. For a new app, use the starter supplied by the authoring workflow, matched to the app's SDK version.
`@altertable/data-app-examples` ships these templates:

| Runtime                 | Template in `node_modules/@altertable/data-app-examples/templates/` |
| ----------------------- | ------------------------------------------------------------------- |
| Hosted / remote / cloud | `starter-data-app/index.tsx`                                        |
| Local                   | `starter-local-data-app`                                            |
| Hosted metric           | `starter-metric-data-app/index.tsx`                                 |
| Hosted Finding          | `starter-finding-data-app/index.tsx`                                |
| Local metric            | `starter-local-metric-data-app`                                     |
| Local Finding           | `starter-local-finding-data-app`                                    |

Choose the runtime and use case supplied by the app brief. Each starter is editable
source; replace fixture queries and sample content before publishing. The hosted starter demonstrates query → operation
→ context → view → dataset → widget composition, including a story example.
Hosted apps stay in one file with public package imports
and a literal `defineDataApp()` declaration. Local apps use the same composition
with their existing server/client wiring. Replace fixture data and connectivity screens; edit
app-owned files, not installed packages.

## Connect data and components

1. **Define the question and scope.** Inspect relevant fields, definitions, time
   coverage, and missing or incomplete observations. Establish the population,
   grain, measures, and comparison. Choose a chart that answers the question.
2. **Write one query and operation per widget.** Give each metric, chart, and
   table its own named query and operation; do not combine unrelated results
   into one query. Write queries against inspected data and preserve supplied
   metric definitions. Declare `params` and result aliases in `projections`.
   Execute named queries with `query()` and derive results from its typed rows.
3. **Update context and bindings.** Describe definitions and coverage in the data
   context, using the operation's `queryNames` for evidence. Declare each dataset
   and metric once, with stable row keys, raw column values, and shared formats.
4. **Declare filters once, then one view per operation.** Declare each filter
   and display choice as a constant and list the ones each operation reads in
   its `filters`; the operation receives one flat input field per filter. Define
   each view with `defineView({ operation, dataContext })`: its filters,
   reporting period, and scope derive from the operation. Pass the headline view
   to `<DataApp view>`, which renders every filter's control, and render each
   view in its own `<DataSection>`. Keep protected values such as `orgId`
   backend-owned. See [views](views.md#give-each-widget-its-own-view) and
   [filters](filters.md).
5. **Compose the content.** Follow the app brief for section order and narrative.
   Use `<Stack>` for sections, `<Grid>` for peers, and bound widgets
   from `@altertable/data-app-react`. Keep static explanations outside loading
   boundaries. Use app tabs only for distinct questions and widget `views` only
   for alternate representations of one dataset. Keep default appearance;
   customize when requested. Use custom UI only when bound components cannot
   express the requirement.
6. **Connect shell features.** See [stories and export](stories-and-export.md)
   for the current `<DataApp>` requirements and how to bind these features to the
   displayed result. The app brief determines presentation content and export
   coverage.

Keep credentials, authorization, and enforced query limits in the host/backend.
The starter supplies transport and mounting; change them only for an explicit
integration task.

## Link to external pages

Use `<ExternalLink>` for HTTPS destinations in widget content:

```tsx
import { ExternalLink } from '@altertable/data-app-react';

function ReportLink() {
  return (
    <ExternalLink href="https://example.com/report">
      View full report
    </ExternalLink>
  );
}
```

For programmatic navigation, import `navigateNewTab`, `navigateNewWindow`, or
`navigateNewWindowOrTab` from `@altertable/data-app/client`. For example,
`navigateNewWindowOrTab(url, event)` accepts a DOM or React event: Shift requests
a window, Ctrl/Cmd requests a tab, and an unmodified event does nothing.

Embedded hosts must enable the [external link route](embed.md#external-links).

## Verify the app

Run the authoring workflow's validation, then inspect the app:

- Check findings against the source population, units, ordering, and coverage.
  Distinguish measured zero, missing values, and empty results.
- Change filters and exercise loading, empty, error, refresh, and stale states.
  Narrative, scope, story, and export must agree with the displayed result.
- For exposed presentation and export features, check the story, exported
  columns, raw values, filename, and scope.
- Review app-owned content for clipping and readability at its intended width.
  Check custom layout or CSS at narrow and wide widths; check custom colors in
  both themes.

When an app fails, use the host's repair or copy action to send observed diagnostics
together. Repair requests preserve the existing authorization boundary and cover
only exercised checks and interactions. See [diagnostics and repair](diagnostics.md)
for host integration.

## Look up only what is missing

Search [REFERENCE.md](../REFERENCE.md) for the exact symbol first:

```sh
rg '^LineChart\b' REFERENCE.md
```

Open only the section needed for a requirement the starter does not cover:

| When                                         | Read                                                              |
| -------------------------------------------- | ----------------------------------------------------------------- |
| Adding categorical, numeric, or time filters | [Filters](filters.md)                                             |
| Adding a chart or narrative binding          | [Widgets](widgets.md)                                             |
| Adding supplemental control hints            | [Tooltips](ui.md#tooltips-and-explanations)                       |
| Adding a detail destination                  | [Detail views](views.md#detail-destinations)                      |
| Registering physical sources                 | [Source identifiers](data-context.md#register-source-identifiers) |
| Customizing appearance or CSS                | [Formatting](formatting-and-appearance.md), [styling](styling.md) |

Keep the starter's working pattern when it meets the requirement. Host integration
guides apply only when building or changing a host.
