import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_plugins_share_the_skill_bundle_and_mcp_configuration():
    for path in (ROOT / ".codex-plugin" / "plugin.json", ROOT / ".cursor-plugin" / "plugin.json"):
        metadata = json.loads(path.read_text(encoding="utf-8"))

        assert metadata["name"] == "altertable"
        assert metadata["skills"] == "./skills/"
        assert metadata["mcpServers"] == "./.mcp.json"


def test_claude_plugin_metadata_keeps_the_current_findings_scope():
    metadata = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))

    assert metadata["name"] == "altertable"
    assert "findings" in metadata["description"].lower()
    assert "findings" in {keyword.lower() for keyword in metadata["keywords"]}


def test_cursor_marketplace_points_to_the_root_plugin():
    marketplace = json.loads(
        (ROOT / ".cursor-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )

    assert marketplace["name"] == "altertable-ai"
    assert marketplace["plugins"][0]["name"] == "altertable"
    assert marketplace["plugins"][0]["source"] == "./"


def test_shared_mcp_configuration_uses_the_hosted_altertable_endpoint():
    mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))

    assert mcp["mcpServers"]["altertable-mcp"]["url"].rstrip("/") == (
        "https://mcp.altertable.ai/mcp"
    )
