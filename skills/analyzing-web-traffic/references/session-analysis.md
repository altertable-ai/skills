# Session Analysis Reference

Deep dive into session-level web analytics.

## Session Fundamentals

### What is a Session?

A session represents a single visit to your website:
- Starts with first pageview
- Ends after 30 minutes of inactivity
- Groups all user actions during visit

### Session vs. User

| Concept | Description |
|---------|-------------|
| Session | One visit (user may have many) |
| User | One person (may have many sessions) |
| Pageview | One page load (many per session) |

## Session Metrics

### Volume Metrics

| Metric | Description |
|--------|-------------|
| Total Sessions | Count of all sessions |
| New Sessions | First-time visitor sessions |
| Returning Sessions | Repeat visitor sessions |

### Quality Metrics

| Metric | Description | Good Range |
|--------|-------------|------------|
| Avg Duration | Time on site | 2-5 minutes |
| Pages/Session | Depth | 2-4 pages |
| Bounce Rate | Single-page % | 30-50% |
| Engaged Rate | 2+ pages % | 50-70% |

## Session Analysis Patterns

### By Traffic Source

Compare session quality by acquisition:

```
Source          Sessions  Duration  Pages  Bounce
─────────────────────────────────────────────────
Organic Search   10,234    3:45     2.8    42%
Direct            5,678    2:15     2.1    55%
Social            3,456    1:30     1.5    68%
Email             2,345    4:20     3.2    35%
```

**Insights**:
- Email has best engagement
- Social has high bounce (wrong audience?)
- Organic good volume and quality

### By Device Type

Compare behavior across devices:

```
Device     Sessions  Duration  Pages  Bounce  CVR
────────────────────────────────────────────────
Desktop     8,000    4:00     3.0    40%    3.2%
Mobile      6,500    2:15     1.8    58%    1.8%
Tablet        800    3:30     2.5    45%    2.5%
```

**Insights**:
- Mobile has higher bounce (UX issue?)
- Mobile conversion much lower
- Consider mobile optimization

### By Landing Page

Evaluate entry points:

```
Landing Page       Sessions  Bounce  Avg Pages
───────────────────────────────────────────────
/home                5,000    45%      2.5
/blog/article-1      2,500    72%      1.3
/products            1,800    38%      3.2
/pricing               900    25%      4.1
```

**Insights**:
- Blog has high bounce (content seekers)
- Pricing page best engagement
- Home page performing well

## Bounce Rate Analysis

### Understanding Bounce Rate

Bounce = session with only one pageview

**Not always bad**:
- Blog readers may find answer
- Contact page visitors get info
- Single-page applications

**Usually concerning**:
- Product pages (want exploration)
- Landing pages (want conversion)
- Home page (want engagement)

### Bounce Rate Benchmarks

| Page Type | Typical Bounce |
|-----------|----------------|
| Blog/Content | 60-80% |
| Landing Page | 40-60% |
| Product Page | 30-50% |
| Home Page | 40-55% |
| Checkout | 20-30% |

### Reducing Bounce Rate

- Improve page load speed
- Match content to expectations
- Clear calls to action
- Related content suggestions
- Mobile optimization

## Session Duration Analysis

### Interpreting Duration

**Long sessions** (good):
- Engaged users
- Complex tasks
- Content consumption

**Short sessions** (investigate):
- Wrong traffic
- Poor UX
- Technical issues
- Quick tasks (may be OK)

### Duration Patterns

```
Duration      Sessions    %
──────────────────────────
0-10 sec       3,500    23%  ← Bounces
10-30 sec      2,200    15%  ← Quick exit
30s-3min       4,500    30%  ← Brief visit
3-10 min       3,200    21%  ← Engaged
10+ min        1,600    11%  ← Very engaged
```

## Session Flow Analysis

### Entry → Exit Patterns

Track common paths:

```
Entry           Exit              Sessions
──────────────────────────────────────────
/home        → /pricing           1,200
/blog        → /blog              2,500
/products    → /checkout            800
/landing     → /signup              450
```

### Conversion Paths

Identify paths that convert:

```
Path                                CVR
────────────────────────────────────────
home → products → cart → checkout   8.5%
products → cart → checkout          6.2%
blog → products → cart              4.1%
home → pricing → signup             3.8%
```

## Segmented Session Analysis

### New vs. Returning

```
            New Users    Returning
────────────────────────────────────
Sessions      8,000        7,000
Duration       2:30         4:15
Pages          2.1          3.5
Bounce         52%          38%
CVR            1.5%         4.2%
```

**Insight**: Returning users much more valuable

### Time-Based Segments

```
Time of Day   Sessions  Bounce  CVR
─────────────────────────────────────
Morning (6-12)  3,500    42%   2.8%
Afternoon       4,200    45%   2.5%
Evening (18-24) 5,800    48%   3.1%
Night (0-6)     1,500    55%   2.0%
```

### Day of Week

```
Day        Sessions  Bounce  Duration
──────────────────────────────────────
Monday       2,100    44%    3:20
Tuesday      2,300    42%    3:35
Wednesday    2,400    43%    3:25
Thursday     2,200    44%    3:30
Friday       2,000    46%    3:10
Saturday     1,800    52%    2:45
Sunday       1,700    54%    2:30
```

**Insight**: Weekday sessions more engaged
