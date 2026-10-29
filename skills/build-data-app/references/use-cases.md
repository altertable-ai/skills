# Data-app use cases

Use this guidance for hosted and local apps. Choose the app's kind from the request, independently of its execution workflow:

- [Standalone apps](#standalone-apps) answer a user's request, including a request about a Finding or metric that does not edit the app it owns.
- [Finding documents](#finding-documents) present a Finding.
- [Metric illustrations](#metric-illustrations) chart one semantic metric.

Follow the corresponding section below, plus [Charting semantic metrics](#charting-semantic-metrics) whenever the app shows a semantic metric.

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

## Charting semantic metrics

- `list_semantic_metrics` takes no arguments. Pick each metric from its output by name and layer, and keep its semantic definition and metric and dimension member identifiers unchanged. Extend the supplied query with supported `DIMENSIONS`, `WHERE` filters, and time grain to produce trends or breakdowns; do not recompute the metric from raw tables. Its `data_app_slug` is on the metric entity, not in this list. When data is missing, never switch to a similar metric or another environment.
- A plain SUM or COUNT adds up across groups and periods, so stacking and shares of the total are valid. Otherwise (distinct counts, ratios, averages, percentiles, min or max), compare groups against the overall value, and never stack, sum, chart a pie or a share of the total, or group a remainder as "Other".
- For balances, snapshots, or running totals, show the latest value of each period, never a sum over time.
- Label units, periods, grain, and active filters, and show missing values as gaps or "No data", never as zero.
