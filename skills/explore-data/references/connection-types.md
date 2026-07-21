# Connection Types Reference

Use `list_catalogs` as the source of truth for the connections available in the current environment. The supported set can include:

- Warehouses: Snowflake, BigQuery, and Redshift
- Databases: PostgreSQL, MySQL, MariaDB, and Supabase
- Lakehouse and object storage: DuckDB, bucket tables, Iceberg tables, R2 catalogs, S3 Tables, and AWS Glue

Do not infer connection configuration fields from this skill. Connection configuration belongs to the current Altertable UI and API contract.

## Explore a Connection

1. Call `list_catalogs` and copy the returned `catalog_name`.
2. Call `get_catalog` with that exact name.
3. Use the returned schemas, tables, columns, semantic models, and relations.
4. Qualify tables as `catalog.schema.table` when querying.

## Query Dialect

`query_lakehouse` and `validate_sql` accept DuckDB SQL for every connected source. Do not copy Snowflake, BigQuery, MySQL, or Redshift-specific syntax into lakehouse queries.

```sql
SELECT *
FROM my_catalog.public.users
WHERE created_at >= CURRENT_DATE - INTERVAL 7 DAY
LIMIT 100
```

Validate unfamiliar syntax with `validate_sql` before executing it.
