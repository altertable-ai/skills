import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _skill(name: str) -> tuple[dict, str]:
    text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
    _, frontmatter, body = text.split("---", 2)
    return yaml.safe_load(frontmatter), body


def test_remote_apps_have_an_mcp_only_route_distinct_from_local_apps():
    remote, body = _skill("build-remote-data-app")
    local, _ = _skill("build-local-data-app")

    assert remote["compatibility"] == "Requires the Altertable MCP server"
    assert "remote" in remote["description"].lower()
    assert "local" in local["description"].lower()
    assert "local app" in local["description"].lower()
    assert "no local coding environment or Altertable CLI" in body


def test_remote_source_contract_is_single_file_with_restricted_imports():
    _, body = _skill("build-remote-data-app")

    assert "`index.ts`" in body
    assert "`index_tsx`" in body
    assert "only `@altertable/data-app`, `react`, and `react-dom`" in body
    assert "https://github.com/altertable-ai/data-app" in body
    assert "Do not invent runtime exports" in body


def test_remote_workflow_separates_validation_from_persistence():
    _, body = _skill("build-remote-data-app")

    assert "`validate_data_app`" in body
    assert "`errors` is empty" in body
    assert "without saving" in body
    for tool in ("create_data_app", "update_data_app", "delete_data_app"):
        assert f"`{tool}`" in body
    assert "existing slug" in body
    assert "explicit deletion request" in body
    assert "does not prove" in body


def test_plugin_descriptions_advertise_remote_data_apps_consistently():
    for directory in (".claude-plugin", ".codex-plugin", ".cursor-plugin"):
        metadata = json.loads((ROOT / directory / "plugin.json").read_text(encoding="utf-8"))
        assert "remote data apps" in metadata["description"]
    for directory in (".claude-plugin", ".cursor-plugin"):
        metadata = json.loads((ROOT / directory / "marketplace.json").read_text(encoding="utf-8"))
        assert "remote data apps" in metadata["metadata"]["description"]
        assert "remote data apps" in metadata["plugins"][0]["description"]
