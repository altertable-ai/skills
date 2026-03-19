---
name: analyzing-web-traffic
compatibility: Requires Altertable MCP server
description: Analyzes web analytics data to identify traffic patterns and user behavior trends. Use when asked about pageviews, sessions, web metrics, traffic sources, or user behavior on websites.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Analyzing Web Traffic

## Quick Start

To analyze web traffic:
1. Query pageview and session data via the Altertable MCP server
2. Compare the current period against a previous period (WoW, MoM, or YoY)
3. Segment by traffic source, device, geography, or page
4. Surface anomalies, trends, and actionable findings

## When to Use This Skill

- User asks about website traffic, pageviews, or sessions
- Investigating traffic spikes, drops, or trends
- Comparing traffic across time periods or segments
- Evaluating traffic source mix or user engagement

## Analysis Workflow

### Step 1: Determine Scope and Time Frame

Ask the user (or infer from context):
- **Period**: What date range to analyze (default to last 7 days if unspecified)
- **Comparison**: What to compare against (previous period of equal length)
- **Focus**: Overall traffic, a specific source, a specific page, or a segment

### Step 2: Query Traffic Data

Use the Altertable MCP server to fetch web analytics data. The primary tool returns the top 50 pages by pageviews, visitors, and sessions grouped by week, with breakdowns by URL, referrer, country, UTM source/campaign, device, and device type.

For deeper analysis, complement with SQL queries against the lakehouse to compute:
- **Volume**: pageviews, sessions, unique visitors
- **Engagement**: bounce rate, pages per session, avg session duration
- **Acquisition**: traffic by source/medium, referrer breakdown

Always pull both the current period and the comparison period so you can compute deltas.

### Step 3: Segment the Data

Break down by at least one dimension to find where changes originate:
- **Traffic source**: organic, paid, direct, social, referral, email
- **Device type**: desktop, mobile, tablet
- **Geography**: country, region
- **Page or section**: top pages, landing pages, exit pages

When a top-level metric moves, drill into segments to isolate which segment drove the change.

### Step 4: Identify Patterns and Anomalies

Look for:
- **Trends**: sustained directional movement across multiple periods
- **Anomalies**: single-period spikes or drops that break the pattern
- **Shifts in mix**: a source growing as a share even if total traffic is flat

Quantify every observation with absolute numbers and percentage change.

### Step 5: Summarize and Recommend

Present findings with:
- The metric, its value, and the delta vs. the comparison period
- Which segment is responsible for the change
- A hypothesis for why (site changes, seasonality, campaigns)
- A suggested next step or action when applicable

## Time Period Comparison Guide

| Comparison | When to Use |
|------------|-------------|
| WoW (week-over-week) | Short-term monitoring, recent changes |
| MoM (month-over-month) | Growth tracking, campaign evaluation |
| YoY (year-over-year) | Seasonal businesses, long-term trends |

Always compare equal-length periods. When comparing WoW, align on the same day of week. When comparing MoM, account for differing month lengths.

## Segmentation Priorities

When the user does not specify a segment, default to this order:
1. **Traffic source** -- most common driver of traffic changes
2. **Device type** -- surfaces mobile vs. desktop divergence
3. **Top pages** -- pinpoints content driving volume shifts

Only add geography or other dimensions if the first pass does not explain the change.

## Common Pitfalls

- **Reporting totals without comparison**: always include a delta to a prior period so the user can gauge significance
- **Ignoring seasonality**: a WoW drop on a holiday week is expected, not alarming -- flag it rather than over-interpreting
- **Mixing up pageviews and sessions**: these measure different things; present both when discussing volume
- **Not drilling into segments**: a flat total can hide offsetting gains and losses across sources or pages
- **Presenting numbers without context**: raw counts are meaningless without comparison, percentage change, or benchmarks
- **Forgetting to check for tracking issues**: sudden drops to zero or impossible spikes often indicate instrumentation problems, not real traffic changes

## Reference Files

- [Web events reference](references/web-events.md)
- [Session analysis](references/session-analysis.md)
- [Trend comparison](references/trend-comparison.md)
