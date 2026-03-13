from __future__ import annotations

from pathlib import Path

import yaml

from skills_feedback.constants import SKILLS_CONFIG_FILENAME
from skills_feedback.models import Config


def find_repo_root() -> Path:
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".git").exists():
            return parent
    return cwd


def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise FileNotFoundError(
            f"{config_path} not found: create it to configure thresholds and labels"
        )

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid config: expected a YAML mapping in {config_path}")

    return Config.model_validate(data)


def load_repo_config() -> tuple[Path, Config]:
    repo_root = find_repo_root()
    config = load_config(repo_root / SKILLS_CONFIG_FILENAME)
    return repo_root, config
