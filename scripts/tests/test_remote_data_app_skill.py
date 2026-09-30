import json
import re
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
    assert "`build-local-data-app`" in body
    assert remote["metadata"]["requires"] == "altertable-mcp"


def test_remote_source_contract_is_single_file_with_restricted_imports():
    _, body = _skill("build-remote-data-app")

    assert "`index.ts`" in body
    assert "`index_tsx`" in body
    imports = set(re.findall(r"`(@altertable/[^`]+|react[^`]*)`", body))
    assert imports == {"@altertable/data-app", "react", "react-dom"}
    assert "https://github.com/altertable-ai/data-app" in body


def test_remote_workflow_separates_validation_from_persistence():
    _, body = _skill("build-remote-data-app")

    assert "`validate_data_app`" in body
    assert "errors" in body
    for tool in ("create_data_app", "update_data_app", "delete_data_app"):
        assert f"`{tool}`" in body
    assert body.index("`validate_data_app`") < body.index("`create_data_app`")
    assert body.index("`validate_data_app`") < body.index("`update_data_app`")
    assert "slug" in body and "url" in body


def test_remote_entrypoint_states_the_cli_boundary_once():
    _, body = _skill("build-remote-data-app")

    assert len(re.findall(r"\bCLI\b", body)) == 1


def test_plugin_descriptions_advertise_remote_data_apps_consistently():
    for directory in (".claude-plugin", ".codex-plugin", ".cursor-plugin"):
        metadata = json.loads((ROOT / directory / "plugin.json").read_text(encoding="utf-8"))
        assert "remote data apps" in metadata["description"]
    for directory in (".claude-plugin", ".cursor-plugin"):
        metadata = json.loads((ROOT / directory / "marketplace.json").read_text(encoding="utf-8"))
        assert "remote data apps" in metadata["metadata"]["description"]
        assert "remote data apps" in metadata["plugins"][0]["description"]
