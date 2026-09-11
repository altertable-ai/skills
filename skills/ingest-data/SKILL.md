---
name: ingest-data
description: "Loads data into Altertable through the CLI, HTTP API, DataFrame tooling, object storage, or generated pipelines. Use for file upload, append, upsert, overwrite, bucket synchronization, or deciding between ingestion and an external catalog."
metadata:
  author: Altertable
---

# Ingest Data

Choose the ingestion path based on where the data lives, whether it must be copied, and how the workflow will run. Read current instructions with `search_docs` when the Altertable MCP server is available; otherwise use [Ingest data](https://altertable.ai/docs/ingest-data).

## Choose the Path

| Situation | Preferred path |
| --- | --- |
| Local CSV, JSON, or Parquet file | CLI `upload` |
| Event-style JSON object or batch | CLI or HTTP `append` |
| File matched to existing rows by primary key | CLI or HTTP `upsert` |
| Pandas, Polars, or Ibis data already in memory | DataFrame integration through DuckDB |
| Files continuously arriving in object storage | Bucket synchronizer |
| Repeatable extraction and loading from a source | Generated or maintained dlt pipeline |
| Existing database, warehouse, or object catalog should stay in place | External catalog; query it without copying |

Prefer the Altertable CLI for terminal scripts and CI because profiles handle authentication and `--agent` provides structured output. See the [CLI guide](https://altertable.ai/docs/developer-tooling/cli) for installation and authentication, and the [CLI repository](https://github.com/altertable-ai/altertable-cli) for releases and the complete command contract. Do not install the CLI unless the user asks; if it is unavailable, provide the installation link or choose another supported surface.

Prefer the HTTP API for application-controlled ingestion. Use an SDK when it already handles retries, batching, and the relevant data structure.

## Write Semantics

- `append` adds records and can create or evolve an event-style destination according to the current API behavior.
- `upload --mode create` creates a destination from a file.
- `upload --mode append` adds file rows to an existing table.
- `upload --mode overwrite` replaces table contents; use it only when replacement is explicit.
- `upsert` matches existing rows by the supplied primary key and requires a stable, unique key.

Inspect the current CLI help or API schema before constructing a request. Do not guess flags, payload limits, supported formats, or asynchronous behavior from an old example.

## Workflow

1. Confirm the organization, environment, destination `catalog.schema.table`, source format, expected row count, and desired write semantics.
2. Inspect the existing destination schema when it exists. Check names, types, nullability, primary-key suitability, and column ordering behavior.
3. Decide whether federation through an external catalog is preferable to copying the data.
4. Execute the smallest bounded write. Never expose credentials in commands, logs, or chat.
5. For asynchronous append, upload, upsert, synchronization, or pipeline work, poll the returned job or task identifier until terminal state.
6. Verify row counts, schema, representative non-sensitive values, and duplicate behavior with a bounded query.

When generating a dlt workflow, use the documented `generate_dlt_pipeline` tool if available, inspect its output, request secrets through the platform's secret flow, and test against a non-production destination first.

## Guardrails

- Do not infer overwrite intent from “refresh,” “reload,” or a filename collision.
- Do not use mutable business attributes as an upsert key.
- Do not load sensitive fields merely because they exist in the source.
- Keep large writes in batches that fit current transaction and memory limits.
- Preserve source timestamps and stable identifiers needed for idempotency.
- Report partial or rejected rows rather than treating an accepted job as verified data.
