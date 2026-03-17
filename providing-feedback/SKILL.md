---
name: providing-feedback
compatibility: Cursor, VS Code, Claude Code, Altertable
description: "Rates skills and proposes changes using the skills-feedback CLI. Use when evaluating skill quality, suggesting improvements, proposing new skills, or when a skill feels outdated, inaccurate, or missing."
---

# Providing Feedback on Skills

## When to Use This Skill

- After using a skill that gave good or bad guidance
- When a skill contains outdated or inaccurate information
- When a skill is missing coverage for a common scenario
- When you want to propose a new skill or remove an obsolete one
- Keywords: "feedback", "rate", "propose", "skill quality", "outdated skill"

## Why Feedback Matters

Skills are shared knowledge between agents. Without feedback, bad skills persist and good skills get no signal. The feedback loop is what keeps the skill library accurate and useful over time.

When you use a skill and it works well, rating it up tells other agents they can trust it. When a skill misleads you, rating it down prevents other agents from making the same mistake. Every vote counts: a single downvote with a clear reason can start a chain that fixes a broken skill for every agent.

## How It Works

### Ratings

Agents vote up or down on skills they use. Each vote is +1 or -1. Votes accumulate per skill into a score.

A rating includes:
- **Vote direction**: up (skill helped) or down (skill misled)
- **Reason**: a specific explanation, not just "good" or "bad"
- **Scope**: either the whole file or specific line ranges
- **Labels**: constrained vocabulary tags that categorize the feedback

**Positive** (for upvotes): `accurate`, `well-structured`, `helpful`, `good-examples`

**Negative** (for downvotes): `outdated`, `inaccurate`, `incomplete`, `wrong-examples`, `poorly-structured`

Labels help categorize feedback but do not affect the score.

### Proposals

When you identify a concrete change needed, you file a proposal:
- **Add**: propose a new skill that does not exist yet
- **Modify**: propose changes to specific lines of an existing skill
- **Remove**: propose removing a skill that is obsolete or superseded

Proposals can include a body file with the replacement content.

### Consensus and Automation

Ratings accumulate per skill. When enough agents agree, proposals qualify for automatic PR creation:

- **Add/Modify proposals**: qualify when skill score >= 3 (positive consensus)
- **Remove proposals**: qualify when skill score <= -3 (negative consensus)

When a skill's score hits the removal threshold, the CLI warns agents to consider a removal proposal. When proposals reach consensus, `skills-feedback apply` creates PRs with the full ratings table in the PR body for human review.

## Best Practices

- **Rate after using a skill, not before**: your experience is the signal
- **Be specific in reasons**: "SQL examples use deprecated syntax on lines 45-52" is actionable, "needs improvement" is not
- **Use the right labels**: positive labels for upvotes, negative labels for downvotes
- **Always identify yourself**: the `--agent` flag lets other agents see who contributed
- **One concern per proposal**: a modify proposal should address one issue, not rewrite the entire skill
- **Propose removal only when superseded**: if a skill is just weak, propose modify instead

## Examples

### Rating a skill after using it

You used `analyzing-charts` and the examples were accurate:

```
$ skills-feedback rate --name analyzing-charts --vote up --reason "chart type examples matched actual API response" --whole-file --labels accurate --agent claude-code
rated: analyzing-charts up
```

### Rating specific lines that misled you

Lines 45-52 in `exploring-data` showed deprecated SQL syntax:

```
$ skills-feedback rate --name exploring-data --vote down --reason "SQL examples use deprecated UNNEST syntax" --lines "45-52" --labels outdated --agent claude-code
rated: exploring-data down
```

### Checking the dashboard

```
$ skills-feedback check-thresholds
SKILL RATINGS
Skill                    Score  Status              Proposals
analyzing-charts         +4     healthy             -
exploring-data           -3     REMOVAL SUGGESTED   1 remove

UNRATED SKILLS
building-segments, configuring-watchers
```

### Previewing what apply would do

```
$ skills-feedback apply --dry-run
would create PR: feedback/remove-exploring-data-remove-20260317T100000Z-claude-code (score: -3)

Summary: 1 PR(s) created, 0 skipped
```

## Troubleshooting

- **"skill does not exist"**: check the skill name matches a directory with a `SKILL.md` file
- **"Label X is not allowed for Y votes"**: positive labels are only for upvotes, negative labels only for downvotes
- **"either --lines or --whole-file is required"**: you must specify a scope when rating
- **"not a git repository"**: `apply` requires a git repo with an `origin` remote
- **"gh CLI not found"**: `apply` requires the [GitHub CLI](https://cli.github.com/) to create PRs

## Workflow

1. **Use a skill** in your work
2. **Rate it** based on your experience (up if it helped, down if it misled)
3. **Propose a change** if you identified a concrete improvement
4. **Check the dashboard** to see which skills need attention
5. **Apply** when proposals reach consensus to create PRs

## Common Pitfalls

1. **Rating without a reason**: the reason is what makes the vote useful to others
2. **Using wrong labels for vote direction**: positive labels on downvotes get rejected
3. **Proposing add for an existing skill**: use modify instead
4. **Vague proposal reasons**: other agents need to understand and vote on your proposal
5. **Forgetting scope**: specify lines for targeted feedback, or use whole-file for general quality

## References

- [CLI usage](references/cli-usage.md) - Commands, options, and installation
