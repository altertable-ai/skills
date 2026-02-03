# Versioning Reference

Guide to version control in the platform.

## Versioned Resources

### What's Versioned

| Resource | Versioned | Notes |
|----------|-----------|-------|
| Semantic Sources | Yes | Full version control |
| Dimensions | Yes | Part of source |
| Measures | Yes | Part of source |
| Relations | Yes | Part of source |
| Dashboards | Partial | Configuration versioned |
| Charts | Partial | Definition versioned |

### What's Not Versioned

| Resource | Versioning |
|----------|------------|
| Connections | No (config only) |
| Raw data | No (external) |
| Memories | No (temporal) |
| Discoveries | No (immutable once created) |

## Version States

### Draft

**Definition:** Work in progress version

**Characteristics:**
- Not active
- Can be modified
- Not queryable
- Exists alongside published

**Operations:**
- Create changes
- Save progress
- Preview results
- Discard if needed

### Published

**Definition:** Active, live version

**Characteristics:**
- Currently active
- Read-only
- Queryable
- Powers all operations

**Operations:**
- Query against
- Create discoveries from
- Base for new drafts

### Archived

**Definition:** Previous version, retained for history

**Characteristics:**
- Not active
- Read-only
- Historical reference
- Can be restored

**Operations:**
- View history
- Compare with current
- Restore if needed

## Version Lifecycle

```
[no version] → draft → published → archived
                 ↑         │
                 └─────────┘ (new draft from published)
```

### Create Draft

Starting a new version:

1. From scratch (new resource)
2. From published (modify existing)
3. From archived (restore old)

### Publish Draft

Making a version active:

1. Validate changes
2. Review impact
3. Publish
4. Previous published → archived

### Archive

When new version publishes:
- Old published becomes archived
- Timestamp recorded
- Remains accessible
- Can be restored

## Version Operations

### Creating Versions

```yaml
operation: create_draft
source: existing_published  # or "new" or archived_id
```

### Comparing Versions

Compare between:
- Draft vs Published
- Published vs Archived
- Any two versions

Comparison shows:
- Added elements
- Removed elements
- Modified elements
- Unchanged elements

### Restoring Versions

From archived to draft:
1. Select archived version
2. Create draft from it
3. Review/modify
4. Publish when ready

## Semantic Source Versioning

### What's Versioned

Full source definition:
- All dimensions
- All measures
- All relations
- Configuration

### Version Structure

```yaml
version:
  id: version_123
  state: published
  created_at: 2024-01-15T10:00:00Z
  published_at: 2024-01-15T12:00:00Z
  created_by: user_123
  content:
    dimensions: [...]
    measures: [...]
    relations: [...]
```

### Breaking Changes

Watch for:
- Removed dimensions
- Renamed dimensions
- Changed data types
- Modified relations

Impact:
- Charts may break
- Segments may fail
- Queries may error

## Version Best Practices

### Before Publishing

1. **Validate syntax**
   - All references resolve
   - Types are correct
   - Relations are valid

2. **Test queries**
   - Run sample queries
   - Check performance
   - Verify results

3. **Review impact**
   - What depends on this?
   - Who will be affected?
   - Any breaking changes?

### After Publishing

1. **Monitor**
   - Watch for errors
   - Check query performance
   - Listen for feedback

2. **Document**
   - What changed
   - Why it changed
   - Who approved

3. **Be ready to rollback**
   - Know the restore process
   - Have archived version
   - Quick response plan

## Version History

### Tracking Changes

Each version records:
- Who created it
- When created
- What changed
- Why (commit message)

### Audit Trail

Full history shows:
- All versions ever published
- Who made changes
- When changes occurred
- Change descriptions

### Viewing History

```
Version 3 (current) - Jan 15 - "Added revenue dimension"
Version 2 (archived) - Jan 10 - "Fixed date formatting"
Version 1 (archived) - Jan 5 - "Initial model"
```

## Branching (Future)

### Concept

Multiple draft versions:
- Feature branches
- Experiment branches
- Team branches

### Merge

Combining branches:
- Resolve conflicts
- Test combined
- Publish merged

## Common Pitfalls

- Publishing without testing
- Ignoring breaking changes
- Not documenting changes
- Losing version history
- No rollback plan
