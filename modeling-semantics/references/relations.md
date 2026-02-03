# Relations Reference

Complete guide to defining relations between semantic sources.

## Relation Definition

```yaml
relations:
  - source: target_source_slug  # Required: slug of related source
    foreign_key: column_name    # Required: FK column in this source
```

## Basic Relations

### One-to-Many

When this source has many records per related record:

```yaml
# In orders source
relations:
  - source: users
    foreign_key: user_id
```

Meaning: Each order belongs to one user; each user can have many orders.

### Many-to-One

Same as above, just from the perspective of the "many" side.

## Join Path Resolution

When querying across sources, the system automatically finds the shortest path.

### Direct Relation

```
orders ──user_id──> users
```

Query on orders with user dimensions uses direct join.

### Indirect Relation

```
order_items ──order_id──> orders ──user_id──> users
```

Query on order_items with user dimensions joins through orders.

### Dijkstra's Algorithm

The system uses shortest-path algorithm to:
1. Find all possible paths between sources
2. Select the path with fewest joins
3. Generate optimal JOIN clause

## Relation Patterns

### User Reference

Most common pattern - referencing user/identity:

```yaml
# In events source
relations:
  - source: identities
    foreign_key: user_id
```

### Parent-Child

Hierarchical data:

```yaml
# In order_items source
relations:
  - source: orders
    foreign_key: order_id

# In orders source
relations:
  - source: users
    foreign_key: user_id
```

### Multiple Relations

A source can have multiple relations:

```yaml
# In orders source
relations:
  - source: users
    foreign_key: user_id
  - source: products
    foreign_key: product_id
  - source: shipping_addresses
    foreign_key: shipping_address_id
```

### Self-Referential

For hierarchical data within same table:

```yaml
# In employees source
relations:
  - source: employees
    foreign_key: manager_id
```

## Built-in Source Relations

The `events` source relates to:

```yaml
relations:
  - source: identities
    foreign_key: user_id
```

This allows querying events with identity dimensions.

## Join Behavior

### Inner vs Outer Joins

By default, relations use LEFT JOIN:
- All records from the primary source are included
- Related records are joined when available
- NULL values appear when no match exists

### Null Handling

When a foreign key is NULL:
- The join still works (LEFT JOIN)
- Related dimensions return NULL
- Consider filtering if needed

## Common Patterns

### Events to Users

```yaml
# events source
relations:
  - source: identities
    foreign_key: user_id
```

Query: "Count of events by user country"
- Groups events by identity.country dimension

### Orders to Multiple Sources

```yaml
# orders source
relations:
  - source: users
    foreign_key: user_id
  - source: products
    foreign_key: product_id
  - source: stores
    foreign_key: store_id
```

Query: "Revenue by product category and store region"
- Joins orders → products for category
- Joins orders → stores for region

### Transitive Relations

```yaml
# order_items source
relations:
  - source: orders
    foreign_key: order_id

# orders source
relations:
  - source: users
    foreign_key: user_id
```

Query on order_items with user dimensions:
- Automatically joins: order_items → orders → users

## Troubleshooting

### No Join Path Found

If queries fail with "no join path":
1. Check that both sources exist
2. Verify relation is defined
3. Check foreign key column exists
4. Ensure source slugs match exactly

### Ambiguous Paths

If multiple paths exist:
- System chooses shortest
- Consider restructuring if wrong path chosen
- May need intermediate sources

### Performance Issues

For slow queries with many joins:
1. Consider denormalizing
2. Add direct relations where possible
3. Check indexes on foreign keys

## Best Practices

### Naming Foreign Keys

- Use consistent naming: `user_id`, `order_id`
- Match the related source name
- Avoid ambiguous names like `id` or `ref`

### Documentation

- Document the relationship meaning
- Note any business rules
- Explain cardinality

### Bidirectional Relations

Only define relation on one side:
- Define on the "many" side
- The "one" side doesn't need explicit relation

### Testing Relations

1. Query using dimensions from related source
2. Verify correct records are joined
3. Check NULL handling for missing relations
