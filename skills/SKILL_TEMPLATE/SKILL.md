---
# Required fields
name: <lowercase-hyphenated-name>              # 1-64 chars, lowercase alphanumeric and hyphens, must match directory name
description: "<what it does and when to use it>" # 1-1024 chars, third-person, include trigger keywords

# Optional fields
license: <license-name>                        # e.g. "Apache-2.0" or "Proprietary. LICENSE.txt has complete terms"
compatibility: <environment requirements>      # 1-500 chars, only if skill has specific requirements
metadata:                                      # string keys to string values
  author: <author-name>
  version: "<semver>"
allowed-tools: <space-delimited tool list>     # e.g. "Bash(git:*) Bash(jq:*) Read" (experimental)
---

<!--
Frontmatter examples:

Minimal:
  name: exploring-data
  description: Explores data connections and schemas. Use when asked about tables, columns, or data types.

With optional fields:
  name: forecasting-timeseries
  description: Analyzes time series data for trends, anomalies, and forecasts. Use when detecting spikes or drops, predicting future values, or identifying anomalies in metrics over time.
  compatibility: Requires Python 3.12+, altertable-mcp, chronos, statsforecast, and statsmodels
  metadata:
    author: altertable-ai
    version: "1.0"
-->

# Your Skill Title

## Quick Start

<!-- 2-5 actionable lines showing immediate value -->

1. Step one
2. Step two
3. Step three

## When to Use This Skill

<!-- Bullet points with trigger conditions and keywords -->

- User wants to...
- User asks about...
- Keywords: "keyword1", "keyword2", "keyword3"

## Core Concepts

<!-- Build mental models, explain fundamentals -->

### Concept One

Description of the concept.

### Concept Two

Description of the concept.

## Workflow

<!-- Step-by-step procedures, progressive complexity -->

### Step 1: First Action

Explanation and example.

```language
code example
```

### Step 2: Second Action

Explanation and example.

## Examples

<!-- Concrete, real-world scenarios with code -->

### Example 1: Basic Usage

```language
concrete code example
```

### Example 2: Advanced Usage

```language
concrete code example
```

## Common Pitfalls

<!-- 5-10 specific mistakes with explanations -->

1. **Pitfall one** - Why it's wrong and how to avoid
2. **Pitfall two** - Why it's wrong and how to avoid
3. **Pitfall three** - Why it's wrong and how to avoid
4. **Pitfall four** - Why it's wrong and how to avoid
5. **Pitfall five** - Why it's wrong and how to avoid

## References

<!-- Links to detailed reference files -->

- [Reference topic](references/topic.md) - Description
