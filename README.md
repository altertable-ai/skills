# Skills

A collection of skills for AI agents.


## Skills

| Skill | Description |
|-------|-------------|
| `evaluating-skills` | Evaluate and review skill quality |
| `exploring-data` | Explore data connections and schemas |
| `querying-lakehouse` | Write and execute DuckDB SQL queries |
| `modeling-semantics` | Create semantic models |
| `creating-insights` | Create discoveries with insights |
| `deciding-actions` | Decision matrices for insight types |
| `analyzing-charts` | Interpret chart data |
| `analyzing-web-traffic` | Analyze web analytics |
| `building-segments` | Create user segments |
| `analyzing-funnels` | Analyze conversion funnels |
| `configuring-watchers` | Set up monitoring agents |
| `managing-discoveries` | Handle discovery approval workflow |
| `using-memory` | Store and retrieve agent memories |
| `understanding-platform` | Understand Altertable platform |
| `tracking-events` | Work with product analytics events |
| `integrating-external` | Connect to external MCP servers |

## Scoring development

```bash
uv sync
uv run pre-commit install
uv run pytest scripts/tests/
```

### Validate a Skill

```bash
uv run skills validate ./skill-name
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Sources

- [Agent Skills Specification](https://agentskills.io/specification)
