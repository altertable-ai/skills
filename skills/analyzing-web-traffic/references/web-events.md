# Web Events Reference

Understanding web analytics events tracked in Altertable.

## Core Event Types

### Pageview

Triggered when a page loads.

**Key Properties**:
| Property | Description |
|----------|-------------|
| `page_url` | Full URL of the page |
| `page_path` | Path portion (e.g., /products/item) |
| `page_title` | HTML title tag |
| `referrer` | Previous page URL |
| `referrer_host` | Previous page domain |

### Session Start

Triggered when a new session begins.

**Key Properties**:
| Property | Description |
|----------|-------------|
| `session_id` | Unique session identifier |
| `landing_page` | First page of session |
| `traffic_source` | Attribution source |
| `utm_source` | UTM source parameter |
| `utm_medium` | UTM medium parameter |
| `utm_campaign` | UTM campaign parameter |

### Session End

Triggered when session concludes (timeout or explicit).

**Key Properties**:
| Property | Description |
|----------|-------------|
| `session_id` | Session identifier |
| `exit_page` | Last page viewed |
| `session_duration` | Total time in seconds |
| `pages_viewed` | Count of pageviews |

## Device & Browser Properties

Available on all web events:

| Property | Description | Examples |
|----------|-------------|----------|
| `device_type` | Device category | mobile, desktop, tablet |
| `browser` | Browser name | Chrome, Safari, Firefox |
| `browser_version` | Browser version | 120.0.0 |
| `os` | Operating system | iOS, Windows, Android |
| `os_version` | OS version | 17.0, 11 |
| `screen_width` | Screen width in pixels | 1920, 390 |
| `screen_height` | Screen height in pixels | 1080, 844 |

## Geographic Properties

| Property | Description |
|----------|-------------|
| `country` | Country code (ISO) |
| `region` | State/province |
| `city` | City name |
| `timezone` | User timezone |
| `language` | Browser language |

## UTM Parameters

For campaign tracking:

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `utm_source` | Traffic source | google, newsletter |
| `utm_medium` | Marketing medium | cpc, email, social |
| `utm_campaign` | Campaign name | spring_sale |
| `utm_term` | Paid keywords | running+shoes |
| `utm_content` | Ad variation | banner_v2 |

## Session Definition

### Session Rules

A session groups events from one user visit:

1. **Timeout**: 30 minutes of inactivity ends session
2. **Day boundary**: New day starts new session
3. **Source change**: New traffic source starts new session

### Session Metrics

| Metric | Calculation |
|--------|-------------|
| Session Duration | Last event - First event |
| Pageviews | Count of pageview events |
| Bounce | Session with single pageview |
| Engaged | Session with 2+ pageviews |

## Common Event Patterns

### Basic Page Tracking

```
pageview (page_path: /home)
pageview (page_path: /products)
pageview (page_path: /products/item-1)
```

### Bounced Session

```
session_start (landing_page: /blog/article)
pageview (page_path: /blog/article)
session_end (pages_viewed: 1)  // Bounce
```

### Engaged Session

```
session_start (landing_page: /home)
pageview (page_path: /home)
pageview (page_path: /pricing)
pageview (page_path: /signup)
session_end (pages_viewed: 3)  // Engaged
```

## Traffic Source Classification

### Direct Traffic

- No referrer
- Typed URL
- Bookmarks
- Some app links

### Organic Search

- Referrer from search engine
- No utm_medium=cpc
- Google, Bing, DuckDuckGo, etc.

### Paid Search

- Referrer from search engine
- utm_medium=cpc or ppc
- Google Ads, Bing Ads

### Social

- Referrer from social platforms
- Facebook, Twitter, LinkedIn, etc.
- May include utm_medium=social

### Referral

- Referrer from other websites
- Not search or social
- Blogs, news sites, partners

### Email

- utm_medium=email
- Or referrer from email service

## Analysis Queries

### Pageviews by Day

Group pageviews by date to see traffic trends.

### Sessions by Source

Group sessions by traffic_source for acquisition analysis.

### Device Breakdown

Group by device_type to understand audience.

### Top Pages

Group pageviews by page_path, sort by count descending.

### Bounce Rate by Page

Calculate single-pageview sessions per landing page.
