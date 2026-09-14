import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "skills"

EXPECTED_SKILLS = {
    "analyze-product-behavior",
    "ask-altertable",
    "build-dashboards",
    "build-insights",
    "configure-tasks",
    "ingest-data",
    "instrument-product-analytics",
    "manage-knowledge",
    "query-altertable",
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


def test_generated_skill_inventories_match_the_skill_directories():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    readme_names = set(re.findall(r"\[([^]]+)\]\(skills/[^)]+/\)", readme))
    agent_names = set(re.findall(r"<name>([^<]+)</name>", agents))
    assert readme_names == EXPECTED_SKILLS
    assert agent_names == EXPECTED_SKILLS


def test_removed_discovery_concept_is_absent_from_shipped_content():
    checked_paths = [*SKILLS_DIR.rglob("*.md"), ROOT / "README.md", ROOT / "AGENTS.md"]

    occurrences = [
        path.relative_to(ROOT)
        for path in checked_paths
        if "discover" in path.read_text(encoding="utf-8").lower()
    ]

    assert occurrences == []


def test_internal_draft_workflows_are_absent_from_portable_content():
    checked_paths = [
        *SKILLS_DIR.rglob("*.md"),
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "templates" / "SKILL_TEMPLATE" / "SKILL.md",
    ]

    occurrences = [
        path.relative_to(ROOT)
        for path in checked_paths
        if "draft" in path.read_text(encoding="utf-8").lower()
    ]

    assert occurrences == []


def test_skill_entrypoints_stay_within_a_small_context_budget():
    oversized = {
        path.parent.name: len(path.read_text(encoding="utf-8").splitlines())
        for path in SKILLS_DIR.glob("*/SKILL.md")
        if len(path.read_text(encoding="utf-8").splitlines()) > 180
    }

    assert oversized == {}


def test_ask_altertable_is_the_fast_agent_delegation_path():
    body = _skill_body("ask-altertable")

    assert "`ask`" in body
    assert "`chat_id`" in body
    assert "default fast path" in body.lower()
    assert "Routing Table" not in body


def test_dashboard_skill_requires_an_explicit_altertable_destination():
    text = (SKILLS_DIR / "build-dashboards" / "SKILL.md").read_text(encoding="utf-8")
    _, raw_frontmatter, body = text.split("---", 2)
    description = yaml.safe_load(raw_frontmatter)["description"].lower()
    body = body.lower()

    assert "only when" in description
    assert "altertable" in description
    assert "generic" in description
    assert "client-native" in description
    assert "generic request" in body
    assert "does not imply altertable persistence" in body
    assert "client's native" in body
    assert "rendering convenience" in body


def test_dashboard_skill_keeps_copy_concise():
    body = _skill_body("build-dashboards").lower()

    assert "keep dashboard copy concise" in body
    assert "text widgets" in body


def test_shared_mcp_bootstrap_is_owned_by_the_platform_brief():
    platform = _skill_body("use-altertable")
    repeated_by = {
        path.parent.name
        for path in SKILLS_DIR.glob("*/SKILL.md")
        if path.parent.name != "use-altertable" and "`initialize`" in _skill_body(path.parent.name)
    }

    assert "`initialize`" in platform
    assert repeated_by == set()


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


def test_platform_brief_leads_with_the_primary_analysis_tools():
    surface = _skill_body("use-altertable").split("## Choose the Surface", 1)[1]
    surface = surface.split("## Current Documentation", 1)[0]

    assert "`ask`" in surface
    assert "`query_lakehouse`" in surface
    assert "MCP" not in surface


def test_skills_defer_evolving_argument_contracts_to_live_schemas():
    copied_arguments = {
        "analyze-product-behavior": ("`from`", "`to`", "`interval`"),
        "build-insights": (
            "`sql_definition`",
            "`sql_parameters`",
            "`x_axis_columns`",
            "`y_axis_columns`",
        ),
        "query-altertable": ("`catalog_name`", "`level: profile`"),
    }
    occurrences = {
        skill: argument
        for skill, arguments in copied_arguments.items()
        for argument in arguments
        if argument in _skill_body(skill)
    }

    assert occurrences == {}
    assert "live MCP schema" in _skill_body("build-insights")
    assert "live tool schema" in _skill_body("query-altertable")


def test_task_skill_models_findings_as_automation_output():
    body = _skill_body("configure-tasks")

    assert "Finding" in body
    assert "Notification" in body
    for target in ("insight", "dashboard", "connection", "database", "segment", "semantic model"):
        assert target in body.lower()
    for tool in ("list_tasks", "create_task", "update_task"):
        assert f"`{tool}`" in body


def test_ingestion_skill_covers_supported_ingestion_decisions():
    body = _skill_body("ingest-data")

    for operation in ("append", "upload", "upsert", "overwrite", "bucket", "external catalog"):
        assert operation in body.lower()
    assert "CLI" in body
    assert "HTTP API" in body


def test_query_skill_surfaces_altertable_specific_sql_capabilities():
    body = _skill_body("query-altertable")

    for capability in ("MATCH_RECOGNIZE", "SESSIONIZE", "time travel", "federated"):
        assert capability in body


def test_frontmatter_names_match_the_new_portfolio():
    for path in SKILLS_DIR.glob("*/SKILL.md"):
        _, raw_frontmatter, _ = path.read_text(encoding="utf-8").split("---", 2)
        frontmatter = yaml.safe_load(raw_frontmatter)
        assert frontmatter["name"] == path.parent.name


def test_readme_is_cross_platform_while_still_listing_the_ask_altertable_skill():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "skills-11-" in readme
    assert "[ask-altertable](skills/ask-altertable/)" in readme
    assert "/altertable:ask" not in readme
    assert "Quick Start with" not in readme
    assert "delegates questions to the Altertable Agent" in agents


def test_skill_template_prioritizes_non_obvious_context_over_boilerplate():
    template = (ROOT / "templates" / "SKILL_TEMPLATE" / "SKILL.md").read_text(encoding="utf-8")

    assert "name: <lowercase-hyphenated-name>" in template
    assert "non-obvious Altertable context" in template
    assert "Do not repeat shared MCP bootstrap" in template
    assert "live tool schema" in template
    assert "explicit user intent" in template


def test_cli_install_and_reference_links_are_available_where_needed():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    platform = _skill_body("use-altertable")
    ingestion = _skill_body("ingest-data")

    assert "curl -fsSL https://install.altertable.ai | sh" in readme
    assert CLI_DOCS_URL in readme
    assert CLI_REPOSITORY_URL in readme

    assert CLI_DOCS_URL in platform
    assert CLI_REPOSITORY_URL not in platform

    assert CLI_DOCS_URL in ingestion
    assert CLI_REPOSITORY_URL in ingestion
    assert "unless the user asks" in ingestion


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


def test_salvaged_platform_layers_have_a_current_owner():
    platform = _skill_body("use-altertable")
    behavior = _skill_body("analyze-product-behavior")
    insights = _skill_body("build-insights")
    tasks = _skill_body("configure-tasks")
    query = _skill_body("query-altertable")
    knowledge = _skill_body("manage-knowledge")

    for concept in ("DuckDB", "Catalogs", "Insights/Dashboards", "Tasks", "Findings/Notifications"):
        assert concept in platform
    for concept in ("web_sessions", "web_pageviews", "conversion window", "step timing"):
        assert concept in behavior
    assert "list_insights" in insights
    assert "view_insight" in insights
    for insight_kind in ("Funnel", "Retention", "Semantic", "SQL", "Segmentation"):
        assert insight_kind in insights
    for task_kind in ("AI analysis", "anomaly detection", "forecast"):
        assert task_kind in tasks
    assert "`monitor`" not in tasks
    assert "machine identifier" in query
    assert "external connection" in query.lower()
    assert "scoped by environment" in knowledge
    assert "importance, recency" in knowledge


def test_existing_insight_explanations_route_to_the_insight_skill():
    text = (SKILLS_DIR / "build-insights" / "SKILL.md").read_text(encoding="utf-8")
    _, raw_frontmatter, _ = text.split("---", 2)
    description = yaml.safe_load(raw_frontmatter)["description"].lower()

    assert "existing" in description
    assert "explain" in description
