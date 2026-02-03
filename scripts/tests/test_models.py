import tempfile
from pathlib import Path

import pytest
from scorer.models import Issue, ScoreBreakdown, ScoreResult, SkillContent


def test_issue_stores_severity_and_message():
    # given / when
    issue = Issue(severity="critical", message="Missing frontmatter")

    # then
    assert issue.severity == "critical"
    assert issue.message == "Missing frontmatter"


def test_issue_model_dump_returns_dict():
    # given
    issue = Issue(severity="major", message="Bad name")

    # when
    result = issue.model_dump()

    # then
    assert result == {"severity": "major", "message": "Bad name"}


def test_score_breakdown_model_dump_includes_all_fields():
    # given
    breakdown = ScoreBreakdown(frontmatter=10)

    # when
    result = breakdown.model_dump()

    # then
    assert result["frontmatter"] == 10
    assert result["structure"] == 0


def test_score_result_model_dump_includes_all_fields():
    # given
    result = ScoreResult(
        skill_name="test-skill",
        score=85,
        breakdown=ScoreBreakdown(frontmatter=18),
        issues=[Issue(severity="minor", message="test issue")],
        suggestions=["improve X"],
        judge_name="gemini/gemini-flash-latest",
    )

    # when
    data = result.model_dump()

    # then
    assert data["skill_name"] == "test-skill"
    assert data["score"] == 85
    assert data["judge_name"] == "gemini/gemini-flash-latest"
    assert len(data["issues"]) == 1


def test_skill_content_from_path_loads_skill():
    # given
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = Path(tmpdir) / "testing-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Testing Skill\n\nContent here.\n")

        # when
        skill = SkillContent.from_path(skill_dir)

        # then
        assert skill.name == "testing-skill"
        assert skill.line_count == 3


def test_skill_content_from_path_raises_when_missing():
    # given
    with tempfile.TemporaryDirectory() as tmpdir:
        missing_path = Path(tmpdir) / "missing"

        # when / then
        with pytest.raises(FileNotFoundError):
            SkillContent.from_path(missing_path)
