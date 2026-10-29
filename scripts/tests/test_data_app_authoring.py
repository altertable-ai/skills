"""Portfolio boundaries shared by hosted and local authoring workflows."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_both_runtimes_route_to_the_same_composition_guidance():
    hosted = ROOT / "skills/build-data-app/SKILL.md"
    local = ROOT / "skills/build-local-data-app/SKILL.md"
    reference = ROOT / "skills/build-data-app/references/composition.md"
    assert reference.is_file()
    assert "references/composition.md" in hosted.read_text()
    assert "../build-data-app/references/composition.md" in local.read_text()


def test_backend_section_contracts_remain_available():
    skill = (ROOT / "skills/build-data-app/SKILL.md").read_text()
    for section in ("Finding documents", "Metric illustrations", "Charting semantic metrics"):
        assert f"## {section}\n" in skill


def test_metric_queries_can_be_extended_without_redefining_the_metric():
    skill = (ROOT / "skills/build-data-app/SKILL.md").read_text()
    assert "keep its query and dimension members unchanged" not in skill
    assert "DIMENSIONS" in skill and "WHERE" in skill
