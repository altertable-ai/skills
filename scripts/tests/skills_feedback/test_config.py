import pytest
from skills_feedback.config import load_config


def test_load_config_valid(tmp_path):
    config_file = tmp_path / ".skills-config.yaml"
    config_file.write_text(
        "thresholds:\n  proposal: 3\n  removal: -3\n"
        "reviewer: fvaleye\n"
        "labels:\n  positive:\n    - accurate\n  negative:\n    - outdated\n"
    )
    config = load_config(config_file)
    assert config.thresholds.proposal == 3
    assert config.reviewer == "fvaleye"
    assert "accurate" in config.labels.positive


def test_load_config_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match="not found"):
        load_config(tmp_path / "nonexistent.yaml")


def test_load_config_defaults_when_minimal(tmp_path):
    config_file = tmp_path / ".skills-config.yaml"
    config_file.write_text("reviewer: fvaleye\n")
    config = load_config(config_file)
    assert config.thresholds.proposal == 3
    assert config.thresholds.removal == -3
    assert config.labels.positive == []


def test_load_config_invalid_yaml(tmp_path):
    config_file = tmp_path / ".skills-config.yaml"
    config_file.write_text("not a mapping")
    with pytest.raises(ValueError, match="expected a YAML mapping"):
        load_config(config_file)
