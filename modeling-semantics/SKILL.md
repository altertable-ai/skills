---
name: modeling-semantics
compatibility: Altertable
description: Creates and maintains semantic models with dimensions, measures, and relations. Use when defining business metrics, creating reusable data models, setting up the semantic layer, or when users ask about dimensions and measures.
---

# Modeling Semantics

## Quick Start

A semantic source defines:
- **Dimensions**: Categorical attributes for grouping (e.g., country, product_type)
- **Measures**: Aggregations for metrics (e.g., count of users, sum of revenue)
- **Relations**: Join paths to other sources

## When to Use This Skill

- Creating reusable business metrics
- Defining how tables relate to each other
- Setting up dimensions for segmentation
- Building a semantic layer over raw data
- User asks about metrics, dimensions, or measures

## Core Concepts

### Semantic Source

A semantic source is a virtual layer on top of a database table that defines:
1. Which columns are dimensions (for grouping)
2. Which columns are measures (for aggregating)
3. How this source relates to other sources

### Source Structure

```yaml
source:
  table: catalog.schema.table_name
  slug: unique-source-name
  description: Human-readable description
  dimensions:
    - name: dimension_name
      type: String
      sql: column_name
  measures:
    - name: measure_name
      kind: Count
      sql: column_name
  relations:
    - source: other-source
      foreign_key: other_id
```

## Dimension Types

| Type | Description | Examples |
|------|-------------|----------|
| `String` | Text values | country, status, name |
| `Integer` | Whole numbers | age, quantity, year |
| `Float` | Decimal numbers | score, rating |
| `Boolean` | True/false | is_active, has_subscription |
| `Timestamp` | Date and time | created_at, updated_at |
| `Date` | Date only | birth_date, order_date |
| `UUID` | Unique identifiers | id, user_id |
| `JSON` | Semi-structured | properties, metadata |

### Timestamp Breakdowns

Timestamp dimensions can be broken down into:
- `Hour` - Group by hour of day
- `Day` - Group by calendar day
- `Week` - Group by week (Monday start)
- `Month` - Group by calendar month
- `Quarter` - Group by quarter
- `Year` - Group by year

## Measure Kinds

| Kind | Description | SQL Example |
|------|-------------|-------------|
| `Count` | Count all rows | `COUNT(*)` |
| `CountDistinct` | Count unique values | `COUNT(DISTINCT column)` |
| `Sum` | Sum of values | `SUM(column)` |
| `Average` | Mean of values | `AVG(column)` |
| `Min` | Minimum value | `MIN(column)` |
| `Max` | Maximum value | `MAX(column)` |
| `Expression` | Custom SQL | Any valid SQL expression |

### Expression Measures

For complex calculations:

```yaml
measures:
  - name: conversion_rate
    kind: Expression
    sql: "COUNT(DISTINCT CASE WHEN converted THEN user_id END)::FLOAT / NULLIF(COUNT(DISTINCT user_id), 0)"
```

## Relations

Relations define how sources connect for joins.

### Basic Relation

```yaml
relations:
  - source: users
    foreign_key: user_id
```

This means: "This source has a `user_id` column that references the `users` source"

### Relation Properties

- `source`: Slug of the related source
- `foreign_key`: Column in this source that references the other

### Join Path Resolution

When querying across sources, the system uses Dijkstra's algorithm to find the shortest join path.

## Built-in Sources

Altertable provides pre-defined semantic sources:

| Source | Table | Purpose |
|--------|-------|---------|
| `events` | Product analytics events | Event tracking |
| `identities` | User identities | User information |
| `pageviews` | Web page views | Web analytics |
| `sessions` | Web sessions | Session-level metrics |
| `identity-overrides` | Identity rules | ID resolution |

## Workflow

### Step 1: Identify the Table

Determine which database table to model:
- Check connection schemas
- Understand table structure
- Identify primary key

### Step 2: Define Dimensions

For each column that can be used for grouping:
- Assign appropriate type
- Add description
- Consider timestamp breakdowns

### Step 3: Define Measures

For each metric needed:
- Choose appropriate kind
- Write SQL expression if needed
- Add description

### Step 4: Define Relations

For each foreign key:
- Identify the related source
- Specify the foreign key column

## Common Patterns

### User Events Source

```yaml
dimensions:
  - name: event
    type: String
    description: Type of event
  - name: timestamp
    type: Timestamp
    description: When event occurred
  - name: user_id
    type: UUID
    description: User who triggered event

measures:
  - name: event_count
    kind: Count
    description: Total number of events
  - name: unique_users
    kind: CountDistinct
    sql: user_id
    description: Unique users

relations:
  - source: identities
    foreign_key: user_id
```

### Orders Source

```yaml
dimensions:
  - name: order_date
    type: Date
  - name: status
    type: String
  - name: customer_id
    type: UUID

measures:
  - name: order_count
    kind: Count
  - name: total_revenue
    kind: Sum
    sql: amount
  - name: average_order_value
    kind: Average
    sql: amount
```

## Common Pitfalls

- Forgetting to add relations for foreign keys
- Using wrong dimension type (e.g., String for dates)
- Creating measures without proper NULL handling
- Not considering timestamp breakdown options
- Missing descriptions that help users understand metrics

## Reference Files

- [Dimensions reference](references/dimensions.md)
- [Measures reference](references/measures.md)
- [Relations reference](references/relations.md)
- [Built-in sources](references/built-in-sources.md)
