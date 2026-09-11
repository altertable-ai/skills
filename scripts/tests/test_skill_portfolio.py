from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"

EXPECTED_SKILLS = {
    "analyze-product-behavior",
    "ask",
    "build-dashboards",
    "build-insights",
    "configure-tasks",
    "ingest-data",
    "instrument-product-analytics",
    "manage-knowledge",
    "query-lakehouse",
    "query-with-chatgpt-data",
    "use-altertable",
}

CLI_DOCS_URL = "https://altertable.ai/docs/developer-tooling/cli"
CLI_REPOSITORY_URL = "https://github.com/altertable-ai/altertable-cli"


def _skill_body(name: str) -> str:
    text = (SKILLS_DIR / name / "SKILL.md").read_text(encoding="utf-8")
    _, _, body = text.split("---", 2)
    return body


def test_shipped_portfolio_contains_only_platform_workflows():
    actual = {path.parent.name for path in SKILLS_DIR.glob("*/SKILL.md")}

    assert actual == EXPECTED_SKILLS


def test_removed_discovery_concept_is_absent_from_shipped_content():
    checked_paths = [*SKILLS_DIR.rglob("*.md"), ROOT / "README.md", ROOT / "AGENTS.md"]

    occurrences = [
        path.relative_to(ROOT)
        for path in checked_paths
        if "discover" in path.read_text(encoding="utf-8").lower()
    ]

    assert occurrences == []


def test_skill_entrypoints_stay_within_a_small_context_budget():
    oversized = {
        path.parent.name: len(path.read_text(encoding="utf-8").splitlines())
        for path in SKILLS_DIR.glob("*/SKILL.md")
        if len(path.read_text(encoding="utf-8").splitlines()) > 180
    }

    assert oversized == {}


def test_ask_is_the_fast_agent_delegation_path():
    body = _skill_body("ask")

    assert body.index("`initialize`") < body.index("`ask`")
    assert "`chat_id`" in body
    assert "default fast path" in body.lower()
    assert "Routing Table" not in body


def test_platform_brief_contains_altertable_operating_invariants():
    body = _skill_body("use-altertable")

    for required in (
        "`initialize`",
        "`list_catalogs`",
        "`get_catalog`",
        "DuckDB",
        "`catalog.schema.table`",
        "`search_docs`",
        "read-only",
        "read-write",
    ):
        assert required in body


def test_insight_skill_uses_current_sql_definition_contract():
    body = _skill_body("build-insights")

    assert "`sql_definition`" in body
    assert "`sql_parameters`" in body
    assert "`sql_statement`" not in body


def test_task_skill_models_findings_as_automation_output():
    body = _skill_body("configure-tasks")

    assert "Finding" in body
    assert "Notification" in body
    for target in ("insight", "dashboard", "connection", "database", "segment", "semantic model"):
        assert target in body.lower()
    for tool in ("list_tasks", "draft_task", "create_task", "update_task"):
        assert f"`{tool}`" in body


def test_ingestion_skill_covers_supported_ingestion_decisions():
    body = _skill_body("ingest-data")

    for operation in ("append", "upload", "upsert", "overwrite", "bucket", "external catalog"):
        assert operation in body.lower()
    assert "CLI" in body
    assert "HTTP API" in body


def test_query_skill_surfaces_altertable_specific_sql_capabilities():
    body = _skill_body("query-lakehouse")

    for capability in ("MATCH_RECOGNIZE", "SESSIONIZE", "time travel", "federated"):
        assert capability in body


def test_frontmatter_names_match_the_new_portfolio():
    for path in SKILLS_DIR.glob("*/SKILL.md"):
        _, raw_frontmatter, _ = path.read_text(encoding="utf-8").split("---", 2)
        frontmatter = yaml.safe_load(raw_frontmatter)
        assert frontmatter["name"] == path.parent.name


def test_readme_is_cross_platform_while_still_listing_the_ask_skill():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "skills-11-" in readme
    assert "[ask](skills/ask/)" in readme
    assert "/altertable:ask" not in readme
    assert "Quick Start with" not in readme
    assert "delegates questions to the Altertable Agent" in agents


def test_skill_template_prioritizes_non_obvious_context_over_boilerplate():
    template = (ROOT / "templates" / "SKILL_TEMPLATE" / "SKILL.md").read_text(encoding="utf-8")

    assert "non-obvious" in template
    assert "Build mental models, explain fundamentals" not in template
    assert "5-10 specific mistakes" not in template
    assert "forecast-timeseries" not in template


def test_contributor_guidance_prioritizes_platform_specific_context():
    guidance = "\n".join(
        (ROOT / name).read_text(encoding="utf-8") for name in ("AGENTS.md", "CONTRIBUTING.md")
    )

    assert "non-obvious" in guidance
    assert "live tool" in guidance
    assert "5-10 mistakes" not in guidance
    assert "Quick Start" not in guidance


def test_skill_scorer_does_not_reward_unnecessary_boilerplate_or_references():
    scorer = (ROOT / "scripts" / "scorer" / "judges.py").read_text(encoding="utf-8")

    assert "Do not reward generic tutorials" in scorer
    assert "References are optional" in scorer
    assert "Common pitfalls" not in scorer


def test_plugin_manifests_describe_the_current_platform_scope():
    manifests = [
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".codex-plugin" / "plugin.json",
        ROOT / ".cursor-plugin" / "plugin.json",
    ]

    for path in manifests:
        content = path.read_text(encoding="utf-8").lower()
        assert "ingestion" in content
        assert "automation" in content
        assert "product-analytics" in content
        assert "findings" in content


def test_cli_install_and_reference_links_are_available_where_needed():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    platform = _skill_body("use-altertable")
    ingestion = _skill_body("ingest-data")

    assert "## Optional Altertable CLI" in readme
    assert "curl -fsSL https://install.altertable.ai | sh" in readme
    assert "does not install the CLI" in readme
    assert CLI_DOCS_URL in readme
    assert CLI_REPOSITORY_URL in readme

    assert CLI_DOCS_URL in platform
    assert CLI_REPOSITORY_URL not in platform

    assert CLI_DOCS_URL in ingestion
    assert CLI_REPOSITORY_URL in ingestion
    assert "Do not install the CLI unless the user asks" in ingestion


def test_agents_guide_documents_the_current_repository_workflow():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    for required in (
        "https://altertable.ai/docs/llms-full.txt",
        "templates/SKILL_TEMPLATE",
        ".codex-plugin/plugin.json",
        "scripts/sync-agents-md.py",
        "generated from skill frontmatter",
        "uv run pre-commit run --all-files",
        "does not install the Altertable CLI",
    ):
        assert required in agents

    assert "### SKILL.md Format" not in agents
