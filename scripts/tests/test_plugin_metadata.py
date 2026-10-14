import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def shipped_text_files():
    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    for name in tracked:
        path = ROOT / name
        if path.suffix != ".png" and path.is_file():
            yield path


def test_plugins_share_the_skill_bundle_and_mcp_configuration():
    for path in (
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".codex-plugin" / "plugin.json",
        ROOT / ".cursor-plugin" / "plugin.json",
    ):
        metadata = json.loads(path.read_text(encoding="utf-8"))

        assert metadata["name"] == "altertable"
        assert metadata["skills"] == "./skills/"
        assert metadata["mcpServers"] == "./.mcp.json"


def test_claude_plugin_metadata_keeps_the_current_findings_scope():
    metadata = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))

    assert metadata["name"] == "altertable"
    assert "findings" in metadata["description"].lower()
    assert "findings" in {keyword.lower() for keyword in metadata["keywords"]}


def test_claude_plugin_metadata_has_directory_listing_links():
    metadata = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))

    for field in ("privacyPolicyUrl", "termsOfServiceUrl", "documentationUrl", "supportUrl"):
        assert metadata[field].startswith("https://"), field


def test_codex_plugin_interface_has_listing_links():
    metadata = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))

    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        assert metadata["interface"][field].startswith("https://"), field


def test_shipped_text_files_stay_under_the_directory_inspection_limit():
    oversized = [
        str(path.relative_to(ROOT))
        for path in shipped_text_files()
        if path.stat().st_size >= 256 * 1024
    ]

    assert oversized == []


def test_shipped_files_do_not_pipe_downloads_into_a_shell():
    piped_install = re.compile(r"\b(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b")

    offenders = [
        str(path.relative_to(ROOT))
        for path in shipped_text_files()
        if piped_install.search(path.read_text(encoding="utf-8", errors="ignore"))
    ]

    assert offenders == []


def test_skills_do_not_forward_environment_variables_to_altertable():
    offenders = [
        str(path.relative_to(ROOT))
        for path in (ROOT / "skills").rglob("*.md")
        if re.search(r"\$\{?ALTERTABLE_[A-Z_]+", path.read_text(encoding="utf-8"))
    ]

    assert offenders == []


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
