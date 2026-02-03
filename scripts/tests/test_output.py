import pytest
from scorer.models import Issue, ScoreBreakdown, ScoreResult
from scorer.output import format_cli, format_pr_comment


@pytest.fixture
def passing_result():
    return ScoreResult(
        skill_name="good-skill",
        score=85,
        breakdown=ScoreBreakdown(
            frontmatter=18, structure=22, content_quality=30, pitfalls=8, references=7
        ),
        issues=[],
        suggestions=["Consider adding more examples"],
        judge_name="gemini/gemini-flash-latest",
    )


@pytest.fixture
def failing_result():
    return ScoreResult(
        skill_name="bad-skill",
        score=55,
        breakdown=ScoreBreakdown(
            frontmatter=10, structure=15, content_quality=20, pitfalls=5, references=5
        ),
        issues=[
            Issue(severity="critical", message="Missing frontmatter"),
            Issue(severity="major", message="No Quick Start section"),
        ],
        suggestions=[],
        judge_name="gemini/gemini-flash-latest",
    )


def test_pr_comment_contains_header(passing_result, failing_result):
    # given
    results = [passing_result, failing_result]

    # when
    comment = format_pr_comment(results, min_score=70)

    # then
    assert "## Skill Quality Report" in comment


def test_pr_comment_contains_skill_table(passing_result, failing_result):
    # given
    results = [passing_result, failing_result]

    # when
    comment = format_pr_comment(results, min_score=70)

    # then
    assert "| Skill | Score | Status |" in comment
    assert "`good-skill`" in comment
    assert "`bad-skill`" in comment


def test_pr_comment_shows_pass_fail_indicators(passing_result, failing_result):
    # given
    results = [passing_result, failing_result]

    # when
    comment = format_pr_comment(results, min_score=70)

    # then
    assert ":white_check_mark:" in comment
    assert ":x:" in comment


def test_pr_comment_includes_issues(failing_result):
    # given
    results = [failing_result]

    # when
    comment = format_pr_comment(results, min_score=70)

    # then
    assert "Missing frontmatter" in comment


def test_cli_output_contains_skill_name(passing_result):
    # when
    output = format_cli(passing_result)

    # then
    assert "good-skill" in output


def test_cli_output_contains_score(passing_result):
    # when
    output = format_cli(passing_result)

    # then
    assert "85/100" in output


def test_cli_output_contains_breakdown_categories(passing_result):
    # when
    output = format_cli(passing_result)

    # then
    assert "frontmatter" in output
    assert "structure" in output


def test_cli_verbose_shows_suggestions(passing_result):
    # when
    output = format_cli(passing_result, verbose=True)

    # then
    assert "Consider adding more examples" in output


def test_cli_non_verbose_hides_suggestions(passing_result):
    # when
    output = format_cli(passing_result, verbose=False)

    # then
    assert "Consider adding more examples" not in output
