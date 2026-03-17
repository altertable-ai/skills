# CLI Usage Reference

## Commands

### Rate a skill

```bash
skills-feedback rate --name <skill> --vote up|down --reason "..." --whole-file --agent <you>
skills-feedback rate --name <skill> --vote up|down --reason "..." --lines "45-52" --labels <label> --agent <you>
```

### Propose changes

```bash
skills-feedback propose add --name <skill> --description "..." --body <path> --agent <you>
skills-feedback propose modify --name <skill> --reason "..." --lines "45-52" --body <path> --agent <you>
skills-feedback propose remove --name <skill> --reason "..." --agent <you>
```

### Check dashboard

```bash
skills-feedback check-thresholds
```

### Apply qualifying proposals

```bash
skills-feedback apply --dry-run
skills-feedback apply
```

## Options

| Flag | Description |
| --- | --- |
| `--name` | Skill name (lowercase, hyphen-separated) |
| `--vote` | `up` or `down` |
| `--reason` | Why you are rating or proposing |
| `--lines` | Line ranges (e.g., `45-52,78-81`) |
| `--whole-file` | Rate the entire skill file |
| `--labels` | Quality label from config |
| `--body` | Path to a SKILL.md file |
| `--agent` | Your agent identity |
| `--no-commit` | Stage changes without committing |
| `--dry-run` | Preview without creating PRs |

## Installation

```bash
pip install "altertable-skills @ git+https://github.com/altertable-ai/skills.git"
```

Requires a `.skills-config.yaml` in the repo root. See [AGENTS.md](../../AGENTS.md) for full configuration.
