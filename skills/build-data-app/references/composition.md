# Compose data components

Define the question, population, period, measures, and comparison before choosing
widgets. A focused answer may need only a chart and a paragraph.

## Choose components

The app brief determines the content and section order.
Choose components for the information each section needs to convey:

| Element   | Purpose                                                |
| --------- | ------------------------------------------------------ |
| Metric    | Establish magnitude or change                          |
| Chart     | Reveal the pattern that answers the section's question |
| Narrative | Interpret, qualify, or suggest the next comparison     |
| Table     | Support exact comparisons and inspection               |
| Filter    | Test a hypothesis or change scope                      |

Place explanations beside their evidence. Use [layout primitives](layout.md)
for reading order and peer comparisons, and [choose charts](widgets.md#choose-a-visualization)
by the question they answer. Use app tabs for distinct questions and widget
`views` for alternate representations of one dataset.

## Keep comparisons consistent

Choose useful filter defaults with adequate coverage. Keep related metrics,
charts, and prose consistent in population, definitions, units, and periods;
explain deliberate differences. Show counts alongside rates when sample size
matters. Compute overall rates from numerators and denominators rather than
averaging subgroup rates.

Derive claims from the [displayed result and its input](views.md#preserve-displayed-results).
A claim about all channels may stop being valid after selecting one. Observed
differences support investigation; they do not establish a cause.
