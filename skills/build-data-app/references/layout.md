# Layout

Use `<Stack>` for reading order, `<Grid>` for peer widgets, and `<GridItem>` for
spans. The shell owns page width and gutters; parents own spacing and widgets
own internal padding. Lay out sections the same way as widgets; static headings
and prose stay outside their loading boundaries. Keep default density unless
customization is requested.

```tsx
// ... sampleCountsView, countsContent, and totalContent
function App() {
  return (
    <DataApp view={sampleCountsView}>
      <Stack>
        <SectionHeading>Sample counts</SectionHeading>
        <TextContent>
          <p>Explore the sources behind this finding.</p>
        </TextContent>
        <Grid columns={3}>
          <GridItem span={2}>
            <DataSection content={countsContent} />
          </GridItem>
          <GridItem>
            <DataSection content={totalContent} />
          </GridItem>
        </Grid>
      </Stack>
    </DataApp>
  );
}
```

Grids wrap to fit their container and spans collapse when needed. Set widget
`headingLevel={3}` beneath a section heading.

Use `<DataApp footer={...}>` for static source, coverage, or methodology notes.
Compose paragraphs, links, and inline components directly; no `<TextContent>`
wrapper is needed. Keep headings and widgets in the body and controls in
`footerActions`.

## Verify rendered layouts

Review authored composition with realistic labels and values. For custom layout
or sizing, check spacing and overflow at narrow and wide iframe widths. Keep
the same grid during loading and ready states.
