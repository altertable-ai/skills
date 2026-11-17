# UI quality

Make the main result easy to identify and compare. Make its scope, units, and
supporting evidence explicit, using context supplied by the host where available
instead of repeating it. Explain each chart's purpose and measures. Use package typography and formatters;
keep primary values prominent and preserve exact values in records and exports.

Compose with `<Stack>`, `<Grid>`, and `<TextContent>`; parents own spacing and
widgets own padding. Let labels and values wrap, and keep tables and menus
scrolling inside their frames. Use the [layout](layout.md) and [styling](styling.md)
guides for customization.

Keep static context visible during loading. Skeletonize only dynamic content;
refresh, errors, and retry retain the displayed result and scope. Loading
geometry should match ready content.

The SDK owns standard theme handling, responsive components, and keyboard/focus
behavior for its controls. Review app-owned content at its intended width with realistic labels
and values. When adding custom layout or CSS, check narrow and wide widths for
clipping and overflow; check custom colors in both themes and custom controls
with the keyboard.
