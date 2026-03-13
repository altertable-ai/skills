import pytest
from skills_feedback.models import Labels, Vote
from skills_feedback.validation import parse_line_ranges, validate_labels, validate_skill_name


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("45-52", ["45-52"]),
        ("45-52,78-81", ["45-52", "78-81"]),
        ("78-78", ["78-78"]),
    ],
)
def test_parse_valid_ranges(input_str, expected):
    assert parse_line_ranges(input_str) == expected


@pytest.mark.parametrize(
    "input_str, match",
    [
        ("52-45", "start must be <= end"),
        ("-1-10", "must be positive"),
        ("abc-def", "must be positive"),
    ],
)
def test_parse_invalid_ranges(input_str, match):
    with pytest.raises(ValueError, match=match):
        parse_line_ranges(input_str)


LABEL_CONFIG = Labels(positive=["accurate"], negative=["outdated"])


@pytest.mark.parametrize(
    "vote, labels, expected_errors",
    [
        (Vote.UP, ["accurate"], 0),
        (Vote.UP, ["outdated"], 1),
        (Vote.DOWN, ["outdated"], 0),
        (Vote.UP, ["nonexistent"], 1),
        (Vote.UP, [], 0),
    ],
)
def test_validate_labels(vote, labels, expected_errors):
    assert len(validate_labels(vote, labels, LABEL_CONFIG)) == expected_errors


@pytest.mark.parametrize(
    "name, valid",
    [
        ("analyzing-charts", True),
        ("Analyzing-Charts", False),
        ("analyzing--charts", False),
        ("-analyzing", False),
    ],
)
def test_validate_skill_name(name, valid):
    errors = validate_skill_name(name)
    assert (len(errors) == 0) == valid
