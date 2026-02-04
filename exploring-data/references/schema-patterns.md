# Schema Patterns Reference

Common patterns for understanding and navigating data schemas.

## Identifying Table Types

### Fact Tables

Contain measurements and metrics, typically:
- Large number of rows
- Foreign keys to dimension tables
- Numeric columns for metrics
- Timestamp columns for time-series

Common names:
- `events`, `transactions`, `orders`, `logs`
- `fact_*` prefix (e.g., `fact_sales`)

### Dimension Tables

Contain descriptive attributes:
- Relatively static data
- Primary key referenced by fact tables
- Text and categorical columns

Common names:
- `users`, `products`, `customers`, `locations`
- `dim_*` prefix (e.g., `dim_customer`)

### Bridge/Junction Tables

Connect many-to-many relationships:
- Two foreign key columns
- Optional attributes about the relationship

Common names:
- `user_roles`, `order_items`, `product_categories`
- Often named `{table1}_{table2}`

## Column Naming Patterns

### Primary Keys

| Pattern | Example |
|---------|---------|
| `id` | `id` |
| `{table}_id` | `user_id` |
| `uuid` | `uuid` |
| `pk` | `pk` |

### Foreign Keys

| Pattern | Example |
|---------|---------|
| `{referenced_table}_id` | `user_id`, `order_id` |
| `fk_{table}` | `fk_customer` |

### Timestamps

| Pattern | Purpose |
|---------|---------|
| `created_at` | Record creation time |
| `updated_at` | Last modification time |
| `deleted_at` | Soft delete timestamp |
| `timestamp` | Event occurrence time |
| `{action}_at` | Specific action time (e.g., `shipped_at`) |

### Status/State

| Pattern | Purpose |
|---------|---------|
| `status` | Current state as string |
| `state` | Current state as string |
| `is_{condition}` | Boolean flag (e.g., `is_active`) |
| `has_{feature}` | Boolean flag (e.g., `has_subscription`) |

### Amounts/Metrics

| Pattern | Purpose |
|---------|---------|
| `amount` | Monetary value |
| `total` | Aggregated value |
| `count` | Quantity |
| `{metric}_cents` | Money in cents (e.g., `price_cents`) |

## Data Type Patterns

### Identifying Time-Series Data

Look for:
- `TIMESTAMP` or `DATETIME` columns
- Columns named `*_at`, `*_date`, `*_time`
- High row counts with continuous timestamps

### Identifying Categorical Data

Look for:
- `VARCHAR` or `TEXT` with limited unique values
- `ENUM` types
- Columns named `type`, `category`, `status`, `kind`

### Identifying JSON/Semi-Structured

Look for:
- `JSON`, `JSONB`, `VARIANT` types
- Columns named `properties`, `metadata`, `attributes`, `extra`
- Columns named `data`, `payload`, `context`

## Schema Organization Patterns

### Environment-Based

```
database
├── production
│   └── tables
├── staging
│   └── tables
└── development
    └── tables
```

### Domain-Based

```
database
├── sales
│   ├── orders
│   └── customers
├── marketing
│   ├── campaigns
│   └── leads
└── product
    ├── events
    └── users
```

### Layer-Based (Data Warehouse)

```
database
├── raw          # Source data as-is
├── staging      # Cleaned and validated
├── marts        # Business-ready aggregations
└── analytics    # Ad-hoc analysis
```

## Relationship Discovery

### One-to-Many

Look for:
- Foreign key in the "many" table
- Primary key in the "one" table

Example:
```
users (one)          orders (many)
├── id ←─────────────┤ user_id
└── name             └── amount
```

### Many-to-Many

Look for:
- Junction table with two foreign keys
- Optional attributes on the relationship

Example:
```
users           user_roles        roles
├── id ←────────┤ user_id         ├── id
└── name        ├── role_id ──────→ └── name
                └── granted_at
```

### Self-Referential

Look for:
- Foreign key referencing same table
- Common for hierarchies

Example:
```
employees
├── id
├── name
└── manager_id → employees.id
```

## Event Data Patterns

### Standard Event Schema

```
events
├── id              # Unique event ID
├── timestamp       # When event occurred
├── event           # Type of event
├── user_id         # Who triggered it
├── properties      # JSON of event-specific data
└── context         # JSON of contextual data
```

### Common Event Properties

| Property | Purpose |
|----------|---------|
| `page_url` | Current page |
| `referrer` | Previous page |
| `device_type` | Mobile/desktop/tablet |
| `browser` | User agent info |
| `session_id` | Session identifier |
| `campaign` | Marketing attribution |

## Soft Delete Patterns

### Timestamp-Based

```sql
-- Active records only
SELECT * FROM users WHERE deleted_at IS NULL

-- Include deleted
SELECT * FROM users
```

### Boolean-Based

```sql
-- Active records only
SELECT * FROM users WHERE is_deleted = false
```

### Status-Based

```sql
-- Active records only
SELECT * FROM users WHERE status != 'deleted'
```
