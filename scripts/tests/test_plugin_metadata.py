import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "altertable"
PLUGIN_SOURCE = "./plugins/altertable"

# The Claude directory only accepts these file types from organizations that aren't Verified.
DIRECTORY_ALLOWED_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
}
DIRECTORY_ALLOWED_NAMES = {"LICENSE"}


def shipped_files():
    tracked = subprocess.run(
        ["git", "ls-files", "--", PLUGIN.relative_to(ROOT).as_posix()],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    for name in tracked:
        path = ROOT / name
        if path.is_file():
            yield path


def shipped_text_files():
    for path in shipped_files():
        if path.suffix != ".png":
            yield path


def test_plugin_folder_ships_only_file_types_the_directory_accepts():
    offenders = [
        str(path.relative_to(ROOT))
        for path in shipped_files()
        if path.suffix.lower() not in DIRECTORY_ALLOWED_SUFFIXES
        and path.name not in DIRECTORY_ALLOWED_NAMES
    ]

    assert offenders == []


def test_plugin_folder_ships_no_executable_scripts():
    offenders = [
        str(path.relative_to(ROOT))
        for path in shipped_text_files()
        if path.read_bytes().startswith(b"#!")
    ]

    assert offenders == []


def test_plugins_share_the_skill_bundle_and_mcp_configuration():
    for path in (
        PLUGIN / ".claude-plugin" / "plugin.json",
        PLUGIN / ".codex-plugin" / "plugin.json",
        PLUGIN / ".cursor-plugin" / "plugin.json",
    ):
        metadata = json.loads(path.read_text(encoding="utf-8"))

        assert metadata["name"] == "altertable"
        assert metadata["skills"] == "./skills/"
        assert metadata["mcpServers"] == "./.mcp.json"


def test_plugin_manifest_assets_exist_inside_the_plugin_folder():
    claude = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    codex = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    cursor = json.loads((PLUGIN / ".cursor-plugin" / "plugin.json").read_text(encoding="utf-8"))

    assets = [
        claude["icon"],
        cursor["logo"],
        *(codex["interface"][key] for key in ("composerIcon", "composerIconDark", "logo")),
    ]
    for asset in assets:
        assert (PLUGIN / asset).resolve().is_file(), asset
        assert (PLUGIN / asset).resolve().is_relative_to(PLUGIN), asset


def test_marketplaces_point_to_the_plugin_folder():
    claude = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    cursor = json.loads((ROOT / ".cursor-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    codex = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )

    for marketplace in (claude, cursor, codex):
        assert marketplace["name"] == "altertable-ai"
        assert marketplace["plugins"][0]["name"] == "altertable"

    assert claude["plugins"][0]["source"] == PLUGIN_SOURCE
    assert cursor["plugins"][0]["source"] == PLUGIN_SOURCE
    assert codex["plugins"][0]["source"]["path"] == PLUGIN_SOURCE


def test_claude_plugin_metadata_keeps_the_current_findings_scope():
    metadata = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))

    assert metadata["name"] == "altertable"
    assert "findings" in metadata["description"].lower()
    assert "findings" in {keyword.lower() for keyword in metadata["keywords"]}


def test_claude_plugin_metadata_has_directory_listing_links():
    metadata = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))

    for field in ("privacyPolicyUrl", "termsOfServiceUrl", "documentationUrl", "supportUrl"):
        assert metadata[field].startswith("https://"), field


def test_codex_plugin_interface_has_listing_links():
    metadata = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))

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
        for path in (PLUGIN / "skills").rglob("*.md")
        if re.search(r"\$\{?ALTERTABLE_[A-Z_]+", path.read_text(encoding="utf-8"))
    ]

    assert offenders == []


def test_shared_mcp_configuration_uses_the_hosted_altertable_endpoint():
    mcp = json.loads((PLUGIN / ".mcp.json").read_text(encoding="utf-8"))

    assert mcp["mcpServers"]["altertable-mcp"]["url"].rstrip("/") == (
        "https://mcp.altertable.ai/mcp"
    )


def test_all_skills_have_readable_display_metadata_and_stable_ids():
    import yaml

    for skill_file in sorted((PLUGIN / "skills").glob("*/SKILL.md")):
        skill_dir = skill_file.parent
        frontmatter = yaml.safe_load(skill_file.read_text(encoding="utf-8").split("---", 2)[1])
        assert frontmatter["name"] == skill_dir.name

        metadata_file = skill_dir / "agents" / "openai.yaml"
        assert metadata_file.is_file(), f"{skill_dir.name} needs display metadata"
        interface = yaml.safe_load(metadata_file.read_text(encoding="utf-8"))["interface"]
        display_name = interface["display_name"]
        assert display_name[0].isupper(), skill_dir.name
        assert " " in display_name and "-" not in display_name, skill_dir.name
        assert 25 <= len(interface["short_description"]) <= 64, skill_dir.name
