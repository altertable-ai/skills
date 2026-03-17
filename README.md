# Skills

[![CI](https://github.com/altertable-ai/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/altertable-ai/skills/actions/workflows/ci.yml)

A collection of skills for AI agents following the [Agent Skills Specification](https://agentskills.io/specification).

## Getting Started

```bash
# Install pre-commit hooks
uv run pre-commit install

# Validate a skill
uv run skills validate ./skill-name

# Run tests
uv run pytest scripts/tests/
```

## Skills Feedback CLI

AI agents can rate skills, propose changes, and create PRs when consensus is reached.

### Install

```bash
# From the repo (requires git)
pip install "altertable-skills @ git+https://github.com/altertable-ai/skills.git"

# From a release tag
pip install "altertable-skills @ git+https://github.com/altertable-ai/skills.git@v0.1.0"
```

### Setup

Create a `.skills-config.yaml` in your repo root:

```yaml
thresholds:
  proposal: 3
  removal: -3
reviewer: your-github-username
labels:
  positive: [accurate, helpful]
  negative: [outdated, inaccurate]
```

### Usage

```bash
# Rate a skill
skills-feedback rate --name analyzing-charts --vote up --reason "clear examples" --whole-file --agent my-agent

# Propose a change
skills-feedback propose modify --name analyzing-charts --reason "outdated section" --lines "45-52" --agent my-agent

# Check the dashboard
skills-feedback check-thresholds

# Create PRs for qualifying proposals
skills-feedback apply --dry-run
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Sources

- [Agent Skills Specification](https://agentskills.io/specification)
