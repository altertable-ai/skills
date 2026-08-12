---
name: explore-data
compatibility: Requires Altertable MCP server
description: "Inspects catalogs, schemas, tables, columns, semantic models, measures, and dimensions. Use to find what data exists or a table's columns. Reads metadata, runs no query."
metadata:
  author: altertable-ai
  requires: "altertable-mcp"
---

# Exploring Data

## Quick Start

To explore available data:
1. Call `initialize` before any other Altertable MCP tool
2. Use `list_catalogs` to see available Altertable databases and external catalogs
3. Use `get_catalog` for schemas, tables, columns, semantic measures, and dimensions
4. Narrow `get_catalog` with `schemas` or `tables` when a catalog is large

## When to Use This Skill

- User asks "what data do I have?"
- User wants to understand table structure
- Before writing queries to understand available columns
- When onboarding a new data source
- User asks about available catalogs, connections, or databases
- User needs to find semantic models, measures, dimensions, or table descriptions

## Core Workflow

### Step 1: Initialize Context

Call `initialize` first. It returns the current organization, environment, and relevant knowledge-entry context. Do not inspect or query data before initialization.

### Step 2: List Available Catalogs

Call `list_catalogs`. Each entry includes:

- `catalog_name` to pass into `get_catalog`
- display name and engine
- optional description

Catalogs can be Altertable-managed databases or external data sources such as Snowflake, BigQuery, Redshift, Postgres, MySQL, MariaDB, object-storage tables, and product analytics.

### Step 3: Get Catalog Schema

Call `get_catalog` for the catalog of interest:

- Schemas and tables
- Column names, data types, and nullability
- Semantic endorsement labels (`draft`, `verified`, `excluded`)
- Semantic dimensions, measures, and relations when available
- Note the catalog and schema names for query qualification (`catalog.schema.table`)

Use `level: overview` for broad discovery, `level: columns` for table shape, and `level: full` for semantic details. For wide catalogs, pass specific `schemas` or `tables`.

### Step 4: Explore Semantic Models

Semantic model details are included in `get_catalog`. Use them to discover pre-defined business logic:

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

### Built-in Catalogs

| Name | Purpose |
|------|---------|
| `product_analytics` | Product events, identities, web sessions, and pageviews when Product Analytics is enabled |
| `opentelemetry` | Logs and traces when OpenTelemetry is enabled |
| User-created catalogs | Managed lakehouse tables and connected external sources |

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

## Product Analytics Semantic Sources

The `product_analytics` catalog can include pre-defined semantic sources:

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
- Querying tables marked `excluded` from the semantic model
- Not checking semantic measures and dimensions that may already define the metrics needed

## Reference Files

- [Connection types detail](references/connection-types.md)
- [Schema patterns](references/schema-patterns.md)
