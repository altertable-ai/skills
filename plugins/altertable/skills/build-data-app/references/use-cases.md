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

Build around the user's question and audience; standalone apps have no prescribed structure.

- **Context:** supply the title, description, and scope needed to understand the app independently of a Finding or metric page.
- **Views and controls:** choose representations and interactions that help answer or explore the question. Include only useful views; add an analytical narrative when requested.

## Finding explorations

The page supplies the dated Finding's title, summary, and full text. The app supplies interactive evidence; limit prose to titles, captions, and necessary caveats.

- **Initial view:** reproduce the Finding's scope, absolute dates, grain, comparison, and headline numbers. Avoid dates relative to today. Fixed dates do not freeze source data; investigate and resolve or disclose discrepancies.
- **Views:** support a claim, test a hypothesis, or enable a check. For example: main evidence, relevant decomposition, secondary access to detail. Adapt to the Finding, including non-temporal evidence; no fixed stack of views. Decomposition does not establish causality.
- **Controls:** stay on the Finding's metric and entities unless asked otherwise. Offer query-backed period, grain, dimension, or baseline controls where supported. Identify changed dates or filters as exploration and provide a return to the original scope.
- **Rates:** expose numerator and denominator when needed to verify a change.

For source evidence:

- Read a missing Finding with `read_resource` on its entity URI. It excludes the run's transcript and SQL; read its `context_slugs` entities and write verified queries.
- When a transcript is supplied, start from its SQL, parameterize controls, and discard failed or exploratory statements.

## Metric illustrations

The app explores one reusable semantic metric; the metric page supplies its context. Build from the starter. Definition changes regenerate the app, so explain that they replace manual edits when the user requests one.

- **Main view:** use time when relevant; otherwise choose a suitable categorical view.
- **Decomposition:** add one useful breakdown when supported; a second only if complementary.
- **Consistency:** query the same semantic definition across views; align period, grain, comparison, and filters.
- **Aggregation:** additive measures can show contributions. Recompute averages and rates at the displayed grain; never sum them across groups or periods. Expose rate numerators and denominators when needed, through tooltips or secondary detail.
- **Presentation:** focus on charts. Omit introductory text, page headings, extra KPI cards, standalone headline numbers, and repeated metric metadata. Titles identify the plotted measure, units, and relevant filters; descriptions or tooltips carry caveats.
