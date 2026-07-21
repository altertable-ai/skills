# Duplicate Prevention Reference

Avoid redundant discoveries by comparing their content and context. Recency alone is not a reason to skip or create one.

## Compare Before Creating

Check the candidate finding against existing discoveries or recalled context:

| Dimension | Question |
|-----------|----------|
| Topic | Is it about the same subject? |
| Metric | Does it use the same metric or event? |
| Time range | Does it analyze the same period? |
| Finding | Does it reach the same conclusion? |
| Context | Does it add a driver, dimension, correction, or action? |

## Decide

| Situation | Action |
|-----------|--------|
| Same metric, period, and finding with no new context | Skip |
| Same topic with a materially different finding | Create |
| New driver, dimension, or actionable context | Create a follow-up |
| Contradicts a previous discovery | Create and explain the contradiction |
| Corrects a previous result | Create and identify the correction |
| User explicitly asks again | Answer the request; create a discovery only for a verified finding worth review or notification |

## Examples

### Exact Duplicate

```
Previous: Revenue dropped 15% yesterday.
Candidate: Revenue decreased 15% yesterday.
Action: Skip because the finding and period are unchanged.
```

### Valuable Follow-up

```
Previous: Revenue dropped 15% yesterday.
Candidate: The drop came from a 40% decline on mobile.
Action: Create because the driver adds material context.
```

### Changed Result

```
Previous: Revenue dropped 15% yesterday.
Candidate: Revenue recovered 10% today.
Action: Create because the period and conclusion changed.
```

## Common Mistakes

- Applying fixed age thresholds without comparing the finding
- Rephrasing an existing discovery without adding information
- Skipping a correction because the topic is recent
- Creating a discovery for a trivial acknowledgement
- Omitting the relationship to a relevant previous discovery
