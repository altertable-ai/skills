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
    assert frontmatter["compatibility"] == "Requires the Altertable MCP server"
    assert frontmatter["metadata"] == {"author": "Altertable", "requires": "altertable-mcp"}
    description = frontmatter["description"].lower()
    assert all(term in description for term in ("chatgpt", "@data", "read-only"))


def test_chatgpt_data_skill_reuses_the_shared_query_procedure():
    _, body = _frontmatter(SKILL_DIR / "SKILL.md")

    assert "`query-altertable`" in body
    for duplicated_tool in ("initialize", "list_catalogs", "get_catalog", "validate_sql"):
        assert f"`{duplicated_tool}`" not in body

    body_lower = body.lower()
    required_boundaries = ("create", "update", "ingestion", "table-mutation")
    assert all(term in body_lower for term in required_boundaries)
    assert "ChatGPT owns the dashboard" in body
    assert "Do not call write or persistence tools" in body


def test_openai_metadata_exposes_the_read_only_mcp_dependency():
    metadata = yaml.safe_load((SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8"))

    assert metadata["interface"]["display_name"] == "Query Altertable with ChatGPT Data"
    assert metadata["policy"]["products"] == ["CHAT", "CODEX"]
    dependency = metadata["dependencies"]["tools"][0]
    assert dependency["type"] == "mcp"
    assert dependency["value"] == "altertable-mcp"
    assert dependency["transport"] == "streamable_http"
    assert dependency["url"].rstrip("/") == "https://mcp.altertable.ai/mcp"
