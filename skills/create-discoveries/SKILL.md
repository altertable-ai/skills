---
name: create-discoveries
compatibility: Requires Altertable MCP server
description: "Reports a change, anomaly, root cause, recommendation, or warning to users. Use when analysis produces something worth telling someone. Returns a discovery that enters review."
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Create Discoveries

## Quick Start

To create a discovery:

1. Call `initialize` before using Altertable MCP tools
2. Confirm the finding is meaningful, novel, actionable, and timely
3. Write `title`, `summary`, `explanation`, and markdown `content`
4. Add valid `context_slugs` for related insights, dashboards, tables, or connections
5. Call `create_discovery`; omit `notify` unless the finding should be recorded without delivery-channel fanout

## When to Use This Skill

- Creating an anomaly, trend, root-cause, recommendation, warning, or contextual discovery
- Turning analysis output into a structured notification
- Explaining what changed, why it likely happened, and why it matters
- Deciding whether a finding is strong enough to enter the discovery workflow

Use `create-insights` for saved charts, tables, funnels, cohorts, or semantic visualizations. Use `manage-discoveries` for approval, rejection, and feedback after a discovery exists.

## Platform Context

Altertable discoveries are the proactive output of the AI-driven analysis lifecycle:

1. Users ingest operational and analytical data into the lakehouse.
2. Humans define context through insights, dashboards, tables, and connections.
3. Analysis happens through agents, user requests, or automated workflows using that context.
4. Most analysis produces no persisted output unless something meaningful is found.
5. When something is worth attention, a discovery records the finding and triggers a notification.
6. Users review discoveries with feedback so the system learns what signals matter.

Discovery creation is therefore not the same as insight creation. An insight is user-defined context or a saved visualization. A discovery is an agent-generated finding that should enter a notification and review workflow.

## Creation Criteria

Create a discovery only when all of these are true:

- **Meaningful**: The finding is large, unusual, strategically relevant, or explicitly requested.
- **Supported**: The claim is backed by data, history, comparison, or traceable investigation.
- **Novel**: It is not a duplicate of an existing recent discovery.
- **Timely**: The data is current enough for the user to act.
- **Actionable**: The user can decide, investigate, fix, monitor, or ignore with confidence.

If any criterion fails, do not create a discovery. Continue analysis, update a related artifact, or report that nothing meaningful was found.

## Core Workflow

### Step 1: Validate the Finding

Before creating:

- Verify the numbers and timeframe
- Compare against relevant baselines or historical patterns
- Search existing discoveries to avoid duplicates
- Check whether the finding matches the user's request or analysis goal
- Identify confidence and uncertainty

### Step 2: Classify the Discovery

Use the most specific type supported by the current MCP tool surface. Common categories:

| Category | Use when |
| --- | --- |
| Anomaly | A metric spikes, drops, or deviates from expected range |
| Trend | A sustained increase, decrease, or pattern emerges |
| Root cause | Analysis identifies likely drivers behind a change |
| Recommendation | The main value is a suggested action |
| Warning | A threshold, quota, data quality issue, or operational risk needs attention |
| Context | The finding provides useful background, caveats, or operational context |

### Step 3: Write the Discovery

A useful discovery answers:

- **What changed?** State the specific observation with numbers.
- **Why did it likely happen?** Summarize the strongest evidence and caveats.
- **Why does it matter?** Connect the finding to business, product, data, or operational impact.
- **What should happen next?** Give one concrete next step.

### Step 4: Create and Notify

Use `create_discovery` when the finding should enter the user-facing workflow. A notification record is always created. Notifications fan out through enabled delivery channels by default.

Required inputs:

- `title`: What was found and why it matters
- `summary`: Short text for activity and notification feeds
- `explanation`: Why the discovery was created and the reasoning behind the finding
- `content`: Markdown content for display

Optional inputs:

- `context_slugs`: Slugs of related entities. Use `search_entities` first when unsure of valid slugs.
- `notify`: Defaults to `true`. Set `false` for minor findings that should not fan out through enabled delivery channels.

The tool returns `id`, `slug`, `explanation`, and `notification_slug`.

## Discovery States

Discoveries flow through an approval workflow:

```
pending  -->  approved | rejected
```

| State | Description |
| --- | --- |
| `pending` | Awaiting review |
| `approved` | Approved |
| `rejected` | Rejected |

Both transitions are reversible: an approved discovery can later be rejected, and a rejected one can later be approved.

## Writing Effective Titles

Good titles are:

- **Specific**: Include the metric, object, and timeframe
- **Actionable**: Make the reason to care obvious
- **Concise**: Keep under 100 characters

| Good | Bad |
| --- | --- |
| "Mobile conversion dropped 20% after checkout redesign" | "Conversion issue" |
| "API error rate doubled after billing deploy" | "Errors increased" |
| "Q4 warehouse data is incomplete for revenue dashboards" | "Data note" |

## Writing Summary, Explanation, and Content

Use `summary` for feed text, `explanation` for why the finding exists, and `content` for the full markdown body.

The summary should lead with the key point:

```markdown
[What changed], from [baseline] to [current] during [timeframe].
```

The explanation should capture the reasoning:

```markdown
This discovery was created because [analysis trigger] found [evidence].
The likely driver is [cause], with [caveat] as the main uncertainty.
```

Keep `content` readable and complete. Put longer supporting analysis in the markdown body or related context rather than overloading the summary.

## Content Structure

Use `content` for the full markdown body:

```markdown
## What changed
[Specific finding with numbers, timeframe, and affected entity.]

## Why it likely happened
[Reasoning, evidence, and important caveats.]

## Why it matters
[Business, product, data, or operational impact.]

## Recommended next step
[One concrete action.]
```

## Troubleshooting Rejected Discoveries

If a discovery is rejected:

- Re-check whether the finding was actionable, novel, timely, and supported
- Parse the free-text `reason` for specific user preference or accuracy feedback
- Strengthen the "so what" only if the underlying finding still matters
- Do not recreate similar discoveries until new evidence changes the situation

| Reason | Fix |
| --- | --- |
| "Already known" | Search existing discoveries before creating |
| "Not actionable" | Add a concrete recommendation or do not create |
| "Too vague" | Include numbers, timeframe, and affected entity |
| "Wrong audience" | Match the requester, dashboard, or domain context |
| "Stale data" | Verify the timeframe is current before creating |

## Common Pitfalls

- Creating discoveries for every analysis result instead of only meaningful findings
- Treating discoveries as saved charts; create insights for visual context instead
- Omitting the likely cause or impact
- Over-alerting on duplicate or low-signal changes
- Not searching existing discoveries before creating
- Sending notifications for internal notes that should use `notify: false`
- Ignoring user feedback from rejected discoveries

## Reference Files

- [Discovery content](references/discovery-content.md)
