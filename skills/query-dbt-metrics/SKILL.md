---
name: query-dbt-metrics
compatibility: Requires Altertable sandbox tools, the metricflow-compile helper, and a deployment-target semantic manifest
description: "Discovers and queries dbt Semantic Layer metrics with native MetricFlow inside an Altertable sandbox. Use for saved metric queries, compatible dimension regrouping, ratios, or cumulative metrics defined in a dbt project."
metadata:
  author: Altertable
  requires: "altertable-mcp"
---

# Query dbt Metrics

Compile the deployed metric definition inside the sandbox, then execute its SQL with the sandbox's Altertable CLI credentials. Use `query-altertable` for questions that need ordinary SQL rather than a dbt metric definition.

## Get the Deployed Definitions

1. Check that `create_sandbox` and `run_sandbox_command` are available. This workflow requires enabled sandbox access; do not claim it works when those tools are unavailable.
2. Use the supplied artifact bucket and object key with `create_sandbox`. Inspect its live schema for the manifest inputs. If the artifact location is unknown, ask for it instead of guessing a bucket. A manifest already delivered in a cloned knowledge repository can also be selected explicitly.
3. Use `/workspace/semantic_manifest.json` for a bucket download, or the manifest path inside the returned repository clone. Deployment artifacts preserve the target's catalog and schema names. Do not run `dbt parse` in the sandbox or rewrite those names to make a query bind.
4. Run `metricflow-compile --help` and list the manifest's metrics and saved queries. Choose by descriptions and the requested population, period and output grain. A definition's presence does not establish endorsement, data freshness or a successful dbt build; check those separately when they matter.

Commands below run through `run_sandbox_command` in the created sandbox. The default manifest path is `/workspace/semantic_manifest.json`; use `--manifest PATH` for a repository artifact.

```bash
metricflow-compile --list
metricflow-compile --list-dimensions --metrics total_llm_cost avg_cost_per_session
```

Only use metric, saved-query and dimension names returned by discovery. The names in these examples illustrate a project; they are not universal Altertable metrics.

## Compile at the Requested Grain

Use a saved query when its metrics, dimensions and filters answer the question. Otherwise request compatible groupings from MetricFlow for the selected metrics and compile an ad hoc query.

```bash
metricflow-compile --saved-query agent_cost_overview > /workspace/metric.sql
```

For an ad hoc query, choose the time bounds from the question and copy the exact grouping names from discovery:

```bash
metricflow-compile \
  --metrics total_llm_cost avg_cost_per_session \
  --group-by metric_time__week chat__model \
  --start-date 2026-09-01 --end-date 2026-09-30 \
  > /workspace/metric.sql
```

Date inputs are inclusive; MetricFlow can expand them to complete periods at the requested grain. Read the effective bounds printed to stderr and report the period actually queried. If the question requires a partial period, use a native time-dimension filter and verify its result; do not silently present a full-week value as a two-day value.

Do not add guessed filters or derive a ratio by averaging returned ratios. For example, daily costs of 30 and 50 over 4 and 1 resolved findings yield daily ratios of 7.5 and 50. The monthly metric is 80 / 5 = 16; averaging the daily ratios gives the incorrect 28.75. Recompile the metric at month grain to obtain the monthly answer.

Let MetricFlow preserve cumulative windows, time-spine joins and offset history. Do not edit generated SQL to remove a join or trim an input period. If compilation rejects a metric or grouping, inspect discovery and the manifest source instead of approximating the definition with handwritten SQL.

## Execute and Verify

Compile successfully before executing. Keep the SQL in a file so a failed compile cannot become a partial query:

```bash
set -e
metricflow-compile --saved-query agent_cost_overview > /workspace/metric.sql
altertable --agent query -- "$(cat /workspace/metric.sql)" > /workspace/metric-result.json
```

Use `--` before the SQL argument: generated SQL can begin with a `--` comment that otherwise looks like a CLI option. Inspect both the command exit status and the result payload before reporting values. A result containing an `error` row is a failed query even if the CLI exits successfully.

The CLI already executes against the lakehouse using the sandbox's scoped principal; do not repeat the same query through `query_lakehouse` solely to claim validation. Compilation alone is not execution evidence.

Keep large results in workspace files and return a focused summary or subset. If `run_sandbox_command` reports truncation, inspect the saved file rather than treating stdout as the complete result. Surface missing relations, unavailable time-spine data and permission errors as execution failures, not zero-valued metrics.

Report the metric names, grouping, time bounds and observed values. Distinguish definition provenance from data freshness. Call `terminate_sandbox` when finished. Creating or changing dbt definitions, publishing views, or saving an Insight is a separate requested write.
