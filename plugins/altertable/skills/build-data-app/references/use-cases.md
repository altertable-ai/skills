# Data-app use cases

Use this guidance for hosted and local data apps. Choose the app's kind from the request, independently of its execution workflow:

- [Standalone apps](#standalone-apps) answer a user's request, including a request about a Finding or metric that does not edit the app it owns.
- [Finding explorations](#finding-explorations) let readers explore the evidence behind a Finding.
- [Metric illustrations](#metric-illustrations) chart one semantic metric.

Follow the corresponding section below. Select the starter for the app's kind and execution mode:

| Use case | Hosted | Local |
| --- | --- | --- |
| Standalone | `starter-data-app/index.tsx` | `starter-local-data-app/` |
| Finding exploration | `starter-finding-data-app/index.tsx` | `starter-local-finding-data-app/` |
| Metric illustration | `starter-metric-data-app/index.tsx` | `starter-local-metric-data-app/` |

Paths are relative to `packages/data-app-examples/templates/` in the SDK repository or `templates/` in a release-matched `@altertable/data-app-examples` package. Use only starters available in the target SDK version; otherwise adapt that version's shared runtime starter. The metric and Finding examples use demo objects seeded by the SDK mock, including a semantic view for the metric starter. Replace those queries and content with verified evidence from the requested metric or Finding; never create demo objects in the user's lakehouse. Keep the app's declared identity even when the host does not provide one.

The metric and Finding starters omit page actions and presentation/export configuration. Enable those features only when the app brief needs them, using the installed SDK's supported props.

## Presentation and export

Explanatory prose does not require an SDK Present story. Add an authored presentation when it serves the request. Choose export datasets that support the app's purpose and preserve the displayed grain. Verify exposed stories and exports against the displayed result. Follow the SDK documentation for component selection, frame options, and story/export contracts.

## Standalone apps

Provide enough title, description, and scope context for the app to make sense on its own.

Answer the user's question first, with as few focused views as the answer needs. Tell a story of the strongest results only when the user asks for an analysis of a topic.

For example, an investigation of signup conversion might show overall conversion, its trend, differences by funnel step or channel, then supporting counts and rates. Use only the parts that answer the request; this is not a required app layout.

## Finding explorations

The Finding page supplies the title, summary, and full text of a dated observation. The app supplies interactive evidence to check and explore it. Limit prose to titles, captions, and necessary caveats.

The initial view must reproduce the Finding's scope, absolute dates, grain, comparison, and headline numbers. Use the Finding's dates rather than a range relative to today. Fixed dates preserve the period, not an immutable data snapshot. If the initial results disagree with the Finding, verify the queries and source data, and resolve or disclose the discrepancy before presenting the app as evidence.

Choose each visualization to support a claim, test a hypothesis, or enable a check. For example, lead with the main evidence, add a relevant decomposition, and make detailed data available as a secondary view. Adapt the representation to the Finding, including Findings without a time dimension. This is not a required stack of KPIs, trends, breakdowns, and tables. A decomposition reveals differences or contributions; it does not establish causality.

Unless the user asks for more, keep the exploration on the Finding's own metric and entities. Add query-backed controls only where the evidence supports them, such as period, grain, dimensions, or baseline. When dates or filters change, clearly identify the result as an exploration distinct from the original Finding and provide a way to return to the Finding's initial scope. For rate changes, let readers inspect the numerator and denominator when needed to verify the claim.

- When the Finding is not in your context, read it with `read_resource` on its entity URI. It does not return the run's transcript or SQL: read the entities in its `context_slugs` and write the queries yourself.
- When a transcript is supplied, its SQL is the starting point; parameterize it for the controls and drop failed or exploratory statements.

## Metric illustrations

A metric's own app explores a reusable metric with a stable semantic definition. It is embedded in the metric page, which supplies the metric context. Query that definition consistently across views. The app is regenerated from the starter when the metric's definition changes. Always build it from the starter, and when the user asks to edit it, explain that the next definition change replaces the edit.

Keep the app focused on charts, without introductory text, page headings, extra KPI cards, standalone headline numbers, or repeated metric metadata. Use chart titles to identify what is plotted, including units and relevant filters; put caveats in descriptions or tooltips. For rates, allow inspection of the numerator and denominator when needed, for example in tooltips or secondary detail.

- Lead with a temporal view when time is relevant; otherwise choose a suitable categorical view.
- Add one useful decomposition by default when the metric's dimensions support it. Add a second only when it supplies complementary information.
- Keep period, grain, comparison, and filters coherent across views and controls.
- Respect aggregation semantics: additive measures can show contributions; averages and rates must be recomputed at the displayed grain, never summed across groups or periods.
