# Data-app use cases

Use this guidance for hosted and local apps. Choose the app's kind from the request, independently of its execution workflow:

- [Standalone apps](#standalone-apps) answer a user's request, including a request about a Finding or metric that does not edit the app it owns.
- [Finding documents](#finding-documents) present a Finding.
- [Metric illustrations](#metric-illustrations) chart one semantic metric.

Follow the corresponding section below. Select the starter for the app's kind and execution mode:

| Use case | Hosted | Local |
| --- | --- | --- |
| Standalone | `starter-data-app/index.tsx` | `starter-local-data-app/` |
| Finding document | `starter-finding-data-app/index.tsx` | `starter-local-finding-data-app/` |
| Metric illustration | `starter-metric-data-app/index.tsx` | `starter-local-metric-data-app/` |

Paths are relative to `packages/data-app-examples/templates/` in the SDK repository or `templates/` in a release-matched `@altertable/data-app-examples` package. Use only starters available in the target SDK version; otherwise adapt that version's shared runtime starter. Replace fixture queries and content with verified evidence. Keep declared app identity even when the host omits its header.

The metric and Finding starters omit page actions and presentation/export configuration. Enable those features only when the app brief needs them, using the installed SDK's supported props.

## Presentation and export

Explanatory prose does not require an SDK Present story. Add an authored presentation when it serves the request. Choose export datasets that support the app's purpose and preserve the displayed grain. Verify exposed stories and exports against the displayed result. Follow the SDK documentation for component selection, frame options, and story/export contracts.

## Standalone apps

Provide enough title, description, and scope context for the app to make sense on its own.

Answer the user's question first, with as few focused views as the answer needs. Tell a story of the strongest results only when the user asks for an analysis of a topic.

For example, an investigation of signup conversion might show overall conversion, its trend, differences by funnel step or channel, then supporting counts and rates. Use only the parts that answer the request; this is not a required app layout.

## Finding documents

The Finding page shows this app in place of the Finding's text, under its title and summary, in a narrow column that the page scrolls. Skip the title and summary in the body, stack sections in one column, and keep heights automatic: no full-height layouts or nested document scroll areas. Tables and menus may retain their own scrolling.

Keep the Finding's structure: headings and paragraphs stay, markdown tables become data tables, and bold, code, and lists become tags. Keep it mostly text, and add a small chart only where it best shows a trend, distribution, or correlation.

- When the Finding is not in your context, read it with `read_resource` on its entity URI. It does not return the run's transcript or SQL: read the entities in its `context_slugs` and write the queries yourself.
- When a transcript is supplied, its SQL is the starting point; drop failed or exploratory statements.

## Metric illustrations

A metric's own app, embedded in the metric page, which supplies the metric context. It is rebuilt from the starter whenever the metric changes. Always build it from the starter, and when the user asks to edit it, say that the next metric change replaces the edit.

Render only charts: no introductory text, headings, KPI cards, standalone numbers, tables, or repeated metric metadata. Chart titles carry only the unit and the filters in the metric's expression; caveats go in chart descriptions or tooltips.

- Lead with one main chart; with a time dimension, choose an appropriate range and grain.
- Add up to two charts that break the metric down by complementary business dimensions, fewer when none fit.
