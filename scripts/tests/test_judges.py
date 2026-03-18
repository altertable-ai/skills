import pytest
from scorer.judges import _build_evaluation_prompt
from scorer.models import SkillContent

SPEC_CONTEXT = "## Agent Skills Specification\nSpec content here"


@pytest.fixture()
def skill():
    return SkillContent(name="test-skill", content="# Test\nBody", references={}, line_count=2)


@pytest.mark.parametrize(
    "expected",
    [
        "Spec content here",
        "Agent Skills Specification",
        "test-skill",
    ],
)
def test_build_evaluation_prompt_includes_spec_and_skill(skill, expected):
    result = _build_evaluation_prompt(skill, spec_context=SPEC_CONTEXT)

    assert expected in result


def test_build_evaluation_prompt_shows_none_without_references(skill):
    result = _build_evaluation_prompt(skill, spec_context=SPEC_CONTEXT)

    assert "None" in result


def test_build_evaluation_prompt_includes_reference_content():
    skill = SkillContent(
        name="test-skill",
        content="# Test",
        references={"guide.md": "guide content"},
        line_count=1,
    )

    result = _build_evaluation_prompt(skill, spec_context=SPEC_CONTEXT)

    assert "guide.md" in result
    assert "guide content" in result
