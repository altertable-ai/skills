# Connection Types Reference

Detailed information about each supported connection type in Altertable.

## Snowflake

Cloud-native data warehouse with separate compute and storage.

### Connection Properties
- `account` - Snowflake account identifier
- `warehouse` - Virtual warehouse for compute
- `database` - Default database
- `schema` - Default schema
- `role` - Snowflake role for access control

### Schema Structure
```
account
└── database (catalog)
    └── schema
        └── table
```

### Special Features
- Time travel queries
- Zero-copy cloning
- Semi-structured data (VARIANT type)
- Automatic clustering

### Example Query
```sql
SELECT * FROM my_db.my_schema.users
WHERE created_at > DATEADD(day, -7, CURRENT_DATE())
```

## BigQuery

Google Cloud's serverless, highly scalable data warehouse.

### Connection Properties
- `project_id` - GCP project identifier
- `dataset` - Default dataset (equivalent to schema)
- `location` - Data location (US, EU, etc.)

### Schema Structure
```
project
└── dataset (schema)
    └── table
```

### Special Features
- Nested and repeated fields (STRUCT, ARRAY)
- Partitioned tables
- Federated queries
- ML built-in (BQML)

### Example Query
```sql
SELECT * FROM `project.dataset.users`
WHERE created_at > DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
```

## PostgreSQL

Open-source relational database, widely used for transactional workloads.

### Connection Properties
- `host` - Database server hostname
- `port` - Connection port (default: 5432)
- `database` - Database name
- `schema` - Default schema (default: public)

### Schema Structure
```
database
└── schema (default: public)
    └── table
```

### Special Features
- JSONB for semi-structured data
- Full-text search
- Extensions (PostGIS, pg_trgm)
- Materialized views

### Example Query
```sql
SELECT * FROM public.users
WHERE created_at > NOW() - INTERVAL '7 days'
```

## Clickhouse

Column-oriented OLAP database optimized for analytics.

### Connection Properties
- `host` - Server hostname
- `port` - HTTP port (default: 8123) or native (9000)
- `database` - Database name

### Schema Structure
```
database
└── table
```

### Special Features
- Extremely fast aggregations
- Materialized views for real-time aggregation
- Distributed queries
- Approximate functions (uniq, quantile)

### Example Query
```sql
SELECT * FROM users
WHERE created_at > today() - 7
```

## MySQL / MariaDB

Popular relational databases for web applications.

### Connection Properties
- `host` - Database server hostname
- `port` - Connection port (default: 3306)
- `database` - Database name

### Schema Structure
```
database
└── table
```

### Example Query
```sql
SELECT * FROM users
WHERE created_at > DATE_SUB(NOW(), INTERVAL 7 DAY)
```

## Redshift

AWS data warehouse based on PostgreSQL.

### Connection Properties
- `host` - Cluster endpoint
- `port` - Connection port (default: 5439)
- `database` - Database name
- `schema` - Default schema

### Special Features
- Distribution styles (KEY, ALL, EVEN)
- Sort keys for query optimization
- Spectrum for S3 queries
- Concurrency scaling

### Example Query
```sql
SELECT * FROM schema.users
WHERE created_at > DATEADD(day, -7, GETDATE())
```

## Supabase

PostgreSQL-based backend-as-a-service.

### Connection Properties
- `host` - Supabase project URL
- `port` - Connection port (default: 5432)
- `database` - Database name (default: postgres)

### Special Features
- Real-time subscriptions
- Row-level security
- Auth integration
- Storage integration

Uses standard PostgreSQL syntax.
