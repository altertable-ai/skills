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

Build a self-contained app around the user's question and audience, with no prescribed structure.

## Finding explorations

Help readers verify and explore the evidence behind a dated Finding.

- **Initial view:** reproduce the Finding's scope, absolute dates, grain, comparison, and headline numbers. Fixed dates do not freeze source data; investigate and resolve or disclose discrepancies.
- **Views:** support a claim, test a hypothesis, or enable a check. For example, lead with the main evidence, add a relevant decomposition, and offer secondary access to detail. Adapt to the Finding, including evidence without a time dimension. Decomposition does not establish causality.
- **Controls:** stay on the Finding's metric and entities unless asked otherwise. Offer query-backed period, grain, dimension, or baseline controls where supported. Identify changed dates or filters as exploration and provide a return to the original scope.
- **Rates:** expose numerator and denominator when needed to verify a change.

If the Finding is absent from context, read it with `read_resource` on its entity URI. The response excludes the run's transcript and SQL; use its `context_slugs` for supporting evidence. If a transcript is supplied, adapt its successful SQL to the controls.

## Metric illustrations

Explore one reusable semantic metric. When asked to edit its app, explain that the next metric definition change regenerates it and replaces manual edits.

- **Main view:** show the metric over time when relevant; otherwise choose a suitable categorical view.
- **Decomposition:** add one useful breakdown when supported; a second only if complementary.
- **Consistency:** query the same semantic definition across views; align period, grain, comparison, and filters.
- **Aggregation:** additive measures can show contributions. Recompute averages and rates at the displayed grain; never sum them across groups or periods. Expose rate numerators and denominators when needed, through tooltips or secondary detail.
- **Presentation:** focus on charts, without extra KPI cards.
