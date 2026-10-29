# Data-app composition

Read this when deciding the content structure of a hosted or local data app.
Use the SDK documentation for component selection, bindings, formatting, loading
states, and technical constraints. Choose the app's purpose independently of its
execution mode or whether it is currently embedded.

## Select the starting point

Use the SDK's release-matched starter for the selected use case when available.
If only a shared runtime starter exists, retain its working wiring and adapt its
sample content. Do not invent paths for starters the SDK has not shipped.
For existing apps, preserve the current source unless the metric-illustration
regeneration workflow explicitly calls for rebuilding from a starter.

## Standalone apps

Answer the requested question with as few focused views as it needs. An analytical
report can lead with the strongest supported result, then comparisons and evidence.
A tracker, tool, or focused chart need not adopt that sequence. Add headings,
explanations, and detail tables where they help the requested task.

For example, an investigation of signup conversion might show overall conversion,
its trend, differences by funnel step or channel, then supporting counts and rates.
Use only the parts that answer the request; this is not a required app layout.

## Finding documents and metric illustrations

Follow the corresponding sections of `build-data-app`. A Finding document keeps
its existing argument and structure, with small supporting visuals. A metric
illustration focuses on its main chart and useful dimensional breakdowns.
Neither inherits a standalone analytical report's introduction or section sequence.

## Frame and viewing surface

Keep app identity in the declaration. Avoid duplicating title, summary, or scope
in the body when the containing page already supplies them. Let the SDK's host
presentation control the supported embedded versus standalone frame behavior.
Do not permanently erase identity just because the first view is embedded.
Use available frame configuration; do not invent props or hide SDK controls with
private CSS selectors. Keep content responsive to its container.

## Presentation stories and export

Explanatory prose is distinct from the SDK's Present story feature. Add an authored
presentation when it serves the request, rather than because the starter shows one.
Choose export datasets that support the app's purpose and preserve the displayed
grain. Verify every exposed story and export against the displayed result.

Respect the installed SDK's actual contracts. The current bound `DataApp` requires
a story callback and a nonempty export dataset list. A story callback returning
`[]` keeps a disabled presentation action; it does not remove the toolbar. Do not promise
optional controls that the installed version does not support. Use the documented
composition options until configurable frame support is available.
