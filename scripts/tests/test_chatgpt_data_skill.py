from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "skills" / "query-with-chatgpt-data"


def _frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    _, raw_frontmatter, body = text.split("---", 2)
    return yaml.safe_load(raw_frontmatter), body


def test_chatgpt_data_skill_has_narrow_activation_metadata():
    frontmatter, _ = _frontmatter(SKILL_DIR / "SKILL.md")

    assert frontmatter["name"] == "query-with-chatgpt-data"
    description = frontmatter["description"]
    assert description.startswith("Use when")
    assert "ChatGPT Work" in description
    assert "@Data" in description
    assert "ordinary Altertable analysis" in description


def test_chatgpt_data_skill_defines_read_only_tool_sequence():
    _, body = _frontmatter(SKILL_DIR / "SKILL.md")

    positions = [
        body.index(f"`{tool}`")
        for tool in ("initialize", "list_catalogs", "get_catalog", "query_lakehouse")
    ]
    assert positions == sorted(positions)
    assert "`validate_sql`" in body
    assert "ChatGPT owns the dashboard" in body
    assert "Do not call write or persistence tools" in body


def test_openai_metadata_exposes_skill_in_chat_and_codex():
    metadata = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8"))

    assert metadata["interface"]["display_name"] == "Query Altertable with ChatGPT Data"
    assert metadata["policy"] == {
        "products": ["CHAT", "CODEX"],
        "allow_implicit_invocation": True,
    }
    assert metadata["dependencies"]["tools"] == [
        {
            "type": "mcp",
            "value": "altertable-mcp",
            "description": "Inspect and query the governed Altertable lakehouse",
            "transport": "streamable_http",
            "url": "https://mcp.altertable.ai/mcp",
        }
    ]


def test_ask_delegates_to_the_altertable_agent_instead_of_routing_skills():
    ask = (ROOT / "skills" / "ask" / "SKILL.md").read_text(encoding="utf-8")

    assert "`ask`" in ask
    assert "`chat_id`" in ask
    assert "Routing Table" not in ask


def test_cursor_plugin_uses_shared_mcp_endpoint():
    plugin = yaml.safe_load((ROOT / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8"))
    marketplace = yaml.safe_load(
        (ROOT / ".cursor-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    mcp = yaml.safe_load((ROOT / ".mcp.json").read_text(encoding="utf-8"))

    assert plugin["name"] == "altertable"
    assert plugin["displayName"] == "Altertable"
    assert plugin["mcpServers"] == "./.mcp.json"
    assert marketplace["name"] == "altertable-ai"
    assert marketplace["plugins"][0]["name"] == "altertable"
    assert mcp["mcpServers"]["altertable-mcp"]["url"] == "https://mcp.altertable.ai/mcp"
