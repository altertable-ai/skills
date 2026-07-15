# Altertable DuckDB Functions Reference

Custom DuckDB extensions available in the Altertable Lakehouse.

## json_extract_string_property

A custom extension for performant property extraction. Use this when you have tables where properties may exist as dedicated columns or in JSON.

```sql
-- Basic usage: extracts 'country' from JSON, or uses events.country column if it exists
SELECT json_extract_string_property(events.properties_bucketed, '$.country') FROM events;

-- Works with nested paths
SELECT json_extract_string_property(events.properties_bucketed, '$.settings.theme') FROM events;

-- Multiple properties in one query
SELECT
    json_extract_string_property(events.properties_bucketed, '$.country') as country,
    json_extract_string_property(events.properties_bucketed, '$.language') as language
FROM events;
```

**Benefits:**
- Zero overhead when column exists (uses direct column reference)
- Automatic VARCHAR casting for non-string columns
- Supports bucketed STRUCT storage (a-z, _ buckets)
- Enables schema evolution without query changes

**Constraints:**
- The JSON path must be a constant string literal
- Always returns VARCHAR
