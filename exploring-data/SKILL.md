---
name: exploring-data
compatibility: Requires Altertable MCP server
description: Explores data connections and schemas to understand available tables, columns, and data types. Use when the user asks about data structure, available tables, what data exists, or wants to understand their data sources before querying.
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Exploring Data

## Quick Start

To explore available data:
1. List all connections to see available data sources
2. Get connection details to see schemas and tables
3. Explore semantic models for pre-defined metrics

## When to Use This Skill

- User asks "what data do I have?"
- User wants to understand table structure
- Before writing queries to understand available columns
- When onboarding a new data source
- User asks about available connections or databases

## Core Workflow

### Step 1: List Available Connections

Start by listing all connections to see what data sources are available:
- Each connection has a name, engine type, and slug
- Connections can be data warehouses (Snowflake, BigQuery) or databases (PostgreSQL, MySQL)
- Built-in connections include `altertable` (platform data) and `sample-data`

### Step 2: Get Connection Schema

For each connection of interest:
- Retrieve the full schema including catalogs, schemas, and tables
- Each table includes column names, data types, and nullability
- Note the catalog and schema names for query qualification

### Step 3: Explore Semantic Models

Semantic models provide pre-defined business logic:
- Dimensions (categorical attributes for grouping)
- Measures (aggregations like count, sum, average)
- Relations (join paths between sources)

## Connection Types

### Data Warehouses

| Engine | Description |
|--------|-------------|
| Snowflake | Cloud data warehouse with catalogs and schemas |
| BigQuery | Google's serverless data warehouse |
| Redshift | AWS data warehouse |

### Databases

| Engine | Description |
|--------|-------------|
| PostgreSQL | Open-source relational database |
| MySQL / MariaDB | Popular relational databases |
| Clickhouse | Column-oriented OLAP database |

### Built-in Connections

| Name | Purpose |
|------|---------|
| `altertable` | Platform data (events, identities, pageviews) |
| `sample-data` | Demo data for testing and learning |

## Understanding Schemas

### Table Qualification

Tables are referenced using three-part names:
```
catalog.schema.table
```

Example:
```sql
SELECT * FROM my_warehouse.public.users LIMIT 10
```

### Column Data Types

Common types across engines:
- `VARCHAR`, `TEXT`, `STRING` - Text data
- `INTEGER`, `BIGINT`, `INT64` - Whole numbers
- `FLOAT`, `DOUBLE`, `NUMERIC` - Decimal numbers
- `BOOLEAN` - True/false values
- `TIMESTAMP`, `DATETIME` - Date and time
- `DATE` - Date only
- `JSON`, `VARIANT` - Semi-structured data

## Built-in Semantic Sources

The `altertable` connection includes pre-defined semantic sources:

| Source | Description |
|--------|-------------|
| `events` | Product analytics events with properties |
| `identities` | User identity information |
| `pageviews` | Web page view events |
| `sessions` | Web session aggregations |
| `identity-overrides` | Identity resolution rules |

## Common Patterns

### Discovering Table Purpose

Look for clues in:
- Table names (e.g., `users`, `orders`, `events`)
- Column names (e.g., `created_at`, `user_id`, `amount`)
- Data types (timestamps indicate time-series data)

### Identifying Primary Keys

Look for columns named:
- `id`, `uuid`, `pk`
- `{table_name}_id` (e.g., `user_id` in `users` table)

### Finding Relationships

Look for foreign key patterns:
- `{other_table}_id` columns
- Matching column names across tables
- Semantic model relations

## Common Pitfalls

- Assuming table names without checking the schema first
- Forgetting to qualify tables with catalog.schema
- Missing that some tables may be views or materialized views
- Not checking for semantic models that may already define the metrics needed

## Reference Files

- [Connection types detail](references/connection-types.md)
- [Schema patterns](references/schema-patterns.md)
