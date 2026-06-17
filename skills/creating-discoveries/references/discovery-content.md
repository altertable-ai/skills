# Discovery Content Reference

How to write `create_discovery` inputs.

## Tool Shape

`create_discovery` requires:

- `title`: Title that conveys what was found and why it matters.
- `summary`: Short summary used in activity and notification feeds.
- `explanation`: Why this discovery was created; the reasoning behind the finding.
- `content`: Markdown content of the discovery for display.

Optional fields:

- `context_slugs`: Related entity slugs for insights, dashboards, tables, connections, or other context.
- `notify`: Defaults to `true`. Set `false` only for minor findings that should not fan out through enabled delivery channels.

## Field Guidance

### `title`

Keep it specific and under the tool's max title length.

Good:

- "Mobile conversion dropped 20% after checkout redesign"
- "API error rate doubled after billing deploy"
- "Q4 warehouse data is incomplete for revenue dashboards"

Bad:

- "Conversion issue"
- "Errors increased"
- "Data note"

### `summary`

Write one short sentence for feeds and notifications:

```text
Mobile conversion fell from 2.5% to 2.0% while mobile traffic rose 40%, suggesting checkout friction.
```

### `explanation`

Explain why the discovery exists:

```text
Checkout analysis found a statistically meaningful divergence between mobile traffic and mobile conversion after the March 1 redesign. Desktop conversion stayed stable, making mobile checkout friction the most likely driver.
```

### `content`

Use markdown for the user-facing body:

```markdown
## What changed
Mobile sessions increased from 145,000 to 203,000 month-over-month (+40%), but mobile conversion dropped from 2.5% to 2.0% (-20%).

## Why it likely happened
The drop begins after the March 1 checkout redesign. Desktop conversion stayed stable at 3.8%, which narrows the likely issue to the mobile checkout experience.

## Why it matters
Mobile now accounts for a larger share of traffic, so the lower conversion rate is offsetting part of the traffic growth.

## Recommended next step
Review the mobile checkout flow and compare step-level drop-off before and after March 1.
```

## Context Slugs

Use `context_slugs` to attach related entities:

- Insight showing the metric or chart
- Dashboard or entity that provides relevant context
- Table or connection involved in the finding
- Related prior discovery when relevant

If you do not know a slug is valid, use `search_entities` first. Invalid slugs cause `create_discovery` to fail.

## Notification Behavior

A notification record is always created. By default, the discovery also fans out through enabled delivery channels such as inbox, Slack, or email.

Set `notify: false` only when:

- The finding is minor
- The record is useful for history but does not require attention
- The user or workflow explicitly requested quiet logging

Do not set `notify: false` for material anomalies, risks, root causes, or recommendations that need timely attention.
