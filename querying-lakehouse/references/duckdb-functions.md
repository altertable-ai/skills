# DuckDB Functions Reference

Comprehensive reference for DuckDB-specific functions used in the Lakehouse.

## Date and Time Functions

### Current Date/Time

| Function | Returns |
|----------|---------|
| `current_date` | Current date |
| `current_timestamp` | Current timestamp with timezone |
| `now()` | Alias for current_timestamp |
| `today()` | Alias for current_date |

### Date Arithmetic

```sql
-- Add intervals
date_add(date, INTERVAL n unit)
date + INTERVAL 'n unit'

-- Subtract intervals
date - INTERVAL 'n unit'

-- Difference between dates
date_diff('unit', start_date, end_date)
datediff('unit', start_date, end_date)  -- alias

-- Units: year, month, week, day, hour, minute, second
```

### Date Truncation

```sql
date_trunc('unit', timestamp)

-- Units: year, quarter, month, week, day, hour, minute, second
-- Examples:
date_trunc('month', '2024-03-15')  -- 2024-03-01
date_trunc('week', '2024-03-15')   -- 2024-03-11 (Monday)
```

### Date Parts

```sql
-- Extract components
year(date)
month(date)
day(date)
hour(timestamp)
minute(timestamp)
second(timestamp)
dayofweek(date)      -- 0=Sunday, 6=Saturday
dayofyear(date)
weekofyear(date)
quarter(date)

-- ISO week (Monday-based)
isodow(date)         -- 1=Monday, 7=Sunday

-- Using EXTRACT
EXTRACT(unit FROM timestamp)
```

### Date Formatting

```sql
strftime(timestamp, format)

-- Format codes:
-- %Y - 4-digit year
-- %m - 2-digit month
-- %d - 2-digit day
-- %H - 24-hour hour
-- %M - minute
-- %S - second
-- %j - day of year

-- Example:
strftime(timestamp, '%Y-%m-%d')  -- '2024-03-15'
```

### Date Parsing

```sql
strptime(string, format)

-- Example:
strptime('2024-03-15', '%Y-%m-%d')
```

## String Functions

### Basic Operations

```sql
-- Length
length(string)
char_length(string)

-- Case conversion
upper(string)
lower(string)
initcap(string)  -- Title Case

-- Trimming
trim(string)
ltrim(string)
rtrim(string)
trim(string, chars)  -- Remove specific chars

-- Padding
lpad(string, length, pad_char)
rpad(string, length, pad_char)
```

### Substring Operations

```sql
-- Extract substring
substring(string, start, length)
substr(string, start, length)
left(string, n)
right(string, n)

-- Find position
position(substring IN string)
strpos(string, substring)
instr(string, substring)
```

### Pattern Matching

```sql
-- LIKE patterns
string LIKE 'pattern%'
string ILIKE 'pattern%'  -- case insensitive

-- Regular expressions
regexp_matches(string, pattern)
regexp_extract(string, pattern)
regexp_replace(string, pattern, replacement)
regexp_split_to_array(string, pattern)
```

### String Manipulation

```sql
-- Concatenation
concat(string1, string2, ...)
string1 || string2

-- Replace
replace(string, old, new)

-- Split
string_split(string, delimiter)
split_part(string, delimiter, n)

-- Reverse
reverse(string)
```

## Numeric Functions

### Basic Math

```sql
abs(n)              -- Absolute value
ceil(n), ceiling(n) -- Round up
floor(n)            -- Round down
round(n, decimals)  -- Round to decimals
trunc(n, decimals)  -- Truncate to decimals
sign(n)             -- -1, 0, or 1
```

### Advanced Math

```sql
power(base, exp)    -- Exponentiation
sqrt(n)             -- Square root
log(n)              -- Natural log
log10(n)            -- Base-10 log
log2(n)             -- Base-2 log
exp(n)              -- e^n
ln(n)               -- Natural log (alias)
```

### Statistical

```sql
greatest(a, b, ...)  -- Maximum value
least(a, b, ...)     -- Minimum value
```

## Aggregate Functions

### Basic Aggregates

```sql
COUNT(*)              -- Count all rows
COUNT(column)         -- Count non-null
COUNT(DISTINCT col)   -- Count unique
SUM(column)
AVG(column)
MIN(column)
MAX(column)
```

### Statistical Aggregates

```sql
STDDEV(column)        -- Standard deviation
STDDEV_POP(column)    -- Population std dev
STDDEV_SAMP(column)   -- Sample std dev
VARIANCE(column)      -- Variance
VAR_POP(column)       -- Population variance
VAR_SAMP(column)      -- Sample variance
```

### Approximate Aggregates

```sql
APPROX_COUNT_DISTINCT(column)  -- Fast approximate unique count
```

### Array Aggregates

```sql
ARRAY_AGG(column)              -- Collect into array
STRING_AGG(column, delimiter)  -- Concatenate strings
LIST(column)                   -- DuckDB alias for ARRAY_AGG
```

### Conditional Aggregates

```sql
COUNT(*) FILTER (WHERE condition)
SUM(column) FILTER (WHERE condition)

-- Or using CASE
SUM(CASE WHEN condition THEN value ELSE 0 END)
COUNT(CASE WHEN condition THEN 1 END)
```

## Window Functions

### Ranking

```sql
ROW_NUMBER() OVER (...)   -- Unique sequential number
RANK() OVER (...)         -- Rank with gaps for ties
DENSE_RANK() OVER (...)   -- Rank without gaps
NTILE(n) OVER (...)       -- Divide into n buckets
PERCENT_RANK() OVER (...) -- Relative rank (0-1)
```

### Value Access

```sql
LAG(col, n, default) OVER (...)   -- Previous row value
LEAD(col, n, default) OVER (...)  -- Next row value
FIRST_VALUE(col) OVER (...)       -- First in window
LAST_VALUE(col) OVER (...)        -- Last in window
NTH_VALUE(col, n) OVER (...)      -- Nth value
```

### Window Frame

```sql
-- Syntax
function OVER (
  PARTITION BY columns
  ORDER BY columns
  ROWS/RANGE BETWEEN start AND end
)

-- Frame specifications
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
```

## JSON Functions

### Extraction

```sql
-- Arrow operators
json_col->'key'           -- Extract JSON value
json_col->>'key'          -- Extract as text
json_col->'arr'->0        -- Array element

-- Standard ducklake functions
json_extract(json, path)
json_extract_string(json, path)

-- Custom extension for schema-aware extraction
json_extract_string_property(table.properties, '$.key')
```

### json_extract_string_property

A custom ducklake extension for intelligent property extraction. Use this when you have tables where properties may exist as dedicated columns or in JSON:

```sql
-- Basic usage: extracts 'country' from JSON, or uses events.country column if it exists
SELECT json_extract_string_property(events.properties, '$.country') FROM events;

-- Works with nested paths
SELECT json_extract_string_property(events.properties, '$.settings.theme') FROM events;

-- Multiple properties in one query
SELECT
    json_extract_string_property(events.properties, '$.country') as country,
    json_extract_string_property(events.properties, '$.language') as language
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

### JSON Construction

```sql
to_json(value)
json_object(key, value, ...)
json_array(values...)
```

### JSON Querying

```sql
json_type(json)              -- Get type
json_array_length(json)      -- Array length
json_keys(json)              -- Object keys
json_contains(json, value)   -- Check containment
```

## Type Conversion

```sql
-- Cast syntax
CAST(value AS type)
value::type

-- Common types
::INTEGER, ::BIGINT
::FLOAT, ::DOUBLE
::VARCHAR, ::TEXT
::DATE, ::TIMESTAMP
::BOOLEAN
::JSON
```

## NULL Handling

```sql
COALESCE(val1, val2, ...)  -- First non-null
NULLIF(val1, val2)         -- NULL if equal
IFNULL(val, default)       -- Default if null
NVL(val, default)          -- Alias for IFNULL

-- NULL checks
val IS NULL
val IS NOT NULL
```

## Conditional Expressions

```sql
-- CASE expression
CASE
  WHEN condition1 THEN result1
  WHEN condition2 THEN result2
  ELSE default_result
END

-- Simple CASE
CASE column
  WHEN value1 THEN result1
  WHEN value2 THEN result2
  ELSE default_result
END

-- IIF (ternary)
IIF(condition, true_value, false_value)
```

## Metadata Tables

Use these to explore available tables and their structure before writing queries.

```sql
-- List all tables
SELECT table_name FROM duckdb_tables();

-- List all columns for a table
SELECT column_name, data_type FROM duckdb_columns() WHERE table_name = 'my_table';
```
