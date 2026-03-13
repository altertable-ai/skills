from __future__ import annotations

from pathlib import Path

import yaml

from skills_feedback.models import Config


def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise FileNotFoundError(
            f"{config_path} not found — create it to configure thresholds and labels"
        )

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid config: expected a YAML mapping in {config_path}")
    if "thresholds" not in data:
        raise ValueError(f"Missing required field 'thresholds' in {config_path}")
    if "labels" not in data:
        raise ValueError(f"Missing required field 'labels' in {config_path}")

    return Config(
        thresholds=data["thresholds"],
        reviewer=data.get("reviewer", ""),
        labels=data["labels"],
    )
