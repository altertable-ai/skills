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

Web analytics focuses on:
1. **Traffic volume**: Pageviews, sessions, visitors
2. **Traffic sources**: Where users come from
3. **User behavior**: What users do on site
4. **Performance**: Bounce rate, time on site

## When to Use This Skill

- User asks about website traffic
- Analyzing pageview patterns
- Understanding traffic sources
- Evaluating user engagement
- Comparing time periods (WoW, MoM)

## Key Metrics

### Volume Metrics

| Metric | Description |
|--------|-------------|
| Pageviews | Total page loads |
| Sessions | User visit sequences |
| Unique Visitors | Distinct users |
| Pages/Session | Engagement depth |

### Engagement Metrics

| Metric | Description |
|--------|-------------|
| Bounce Rate | Single-page sessions % |
| Avg Session Duration | Time spent per session |
| Pages per Session | Pages viewed per visit |
| Exit Rate | Sessions ending on page % |

### Acquisition Metrics

| Metric | Description |
|--------|-------------|
| Traffic by Source | Where users come from |
| Referrer Analysis | Which sites send traffic |
| Campaign Performance | Marketing channel results |

## Analysis Workflow

### Step 1: Set Time Frame

- Define analysis period
- Choose comparison period
- Consider seasonality

### Step 2: Get Overview

- Total traffic volume
- Key metric trends
- Any obvious anomalies

### Step 3: Segment Analysis

- By traffic source
- By device type
- By geography
- By page/section

### Step 4: Identify Patterns

- Trends (up/down/flat)
- Seasonality (weekly, monthly)
- Anomalies (spikes, drops)

### Step 5: Interpret and Recommend

- Explain what's happening
- Suggest actions
- Flag concerns

## Traffic Source Analysis

### Source Categories

| Source | Examples |
|--------|----------|
| Direct | Typed URL, bookmarks |
| Organic Search | Google, Bing (non-paid) |
| Paid Search | Google Ads, Bing Ads |
| Social | Facebook, Twitter, LinkedIn |
| Referral | Other websites |
| Email | Email campaigns |

### Key Questions

- Which sources drive most traffic?
- Which sources have best engagement?
- Are source proportions changing?
- Which sources convert best?

## Time-Based Analysis

### Week-over-Week (WoW)

Compare to same day last week:
- Accounts for weekly patterns
- Good for recent trends
- Watch for holidays

### Month-over-Month (MoM)

Compare to same period last month:
- Accounts for monthly patterns
- Good for growth tracking
- Watch for calendar effects

### Year-over-Year (YoY)

Compare to same period last year:
- Accounts for seasonality
- Good for long-term trends
- Watch for major changes

## Page Analysis

### Top Pages

Identify most visited pages:
- Landing pages
- Popular content
- Key conversion pages

### Entry Pages

Where sessions start:
- First impression pages
- SEO landing pages
- Campaign destinations

### Exit Pages

Where sessions end:
- Natural endpoints (thank you)
- Problem areas (high unexpected exit)
- Conversion endpoints

## User Behavior Patterns

### Engaged Users

- Multiple pages per session
- Longer session duration
- Return visits
- Conversion actions

### Bouncing Users

- Single page sessions
- Very short duration
- No subsequent visits
- Consider: wrong traffic or poor experience

### Journey Patterns

Common paths through site:
- Landing → Content → Conversion
- Search → Product → Cart → Checkout
- Blog → Product → Exit

## Trend Interpretation

### Growing Traffic

Positive signals:
- Content is resonating
- SEO improvements working
- Marketing effective

Verify:
- Quality of traffic (engagement)
- Source sustainability
- Conversion rates maintained

### Declining Traffic

Investigate:
- Technical issues
- Algorithm changes
- Competitive pressure
- Seasonal effects

Check:
- Specific sources affected
- Specific pages affected
- Timing of decline

### Flat Traffic

Consider:
- Is this expected?
- Market saturation?
- Missed opportunities?
- Need new initiatives?

## Common Pitfalls

- Ignoring seasonality in comparisons
- Looking at pageviews without sessions
- Not segmenting by source
- Missing bot traffic
- Confusing correlation with causation
- Not considering site changes

## Reference Files

- [Web events reference](references/web-events.md)
- [Session analysis](references/session-analysis.md)
- [Trend comparison](references/trend-comparison.md)
