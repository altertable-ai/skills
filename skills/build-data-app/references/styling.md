# Styling

Keep default appearance unless customization is requested. Use components and
typed props first. Configure appearance once through
`dataApp.appearance`; see [formatting and appearance](formatting-and-appearance.md).
Call `injectDataAppStyles()` before mounting and use one `<DataApp>` per document.

## Customize

Add app-owned classes through `className` and override public tokens. Render
package components; do not copy their classes or select private descendants.
Public hooks are listed in the [style contract](https://github.com/altertable-ai/data-app/blob/main/packages/data-app-react/src/style-contract.ts).

```css
.app-action {
  --atbl-control-height: 40px;
  --atbl-focus-color: var(--atbl-accent);
}
```

Type inline overrides with `DataAppStyle`. Give optional tokens a `var()` fallback.
Use `:root` for overrides shared with menus and overlays. Prefer `dataApp.appearance`
for brand and chart colors; pair accent overrides with a contrasting foreground.
Keep text inputs at least 16px on mobile.

## Native controls

Prefer package controls. For a custom native control:

```tsx
<button type="button" data-atbl-control="action" data-atbl-focus="ring">
  Run
</button>
```

These hooks style cursor and focus. Supply accessible names, disabled state, and
keyboard behavior, then verify [UI quality](ui-quality.md).
