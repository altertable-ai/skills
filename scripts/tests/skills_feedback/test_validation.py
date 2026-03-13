import pytest
from skills_feedback.models import Labels
from skills_feedback.validation import parse_line_ranges, validate_labels, validate_skill_name


def test_parse_single_range():
    assert parse_line_ranges("45-52") == ["45-52"]


def test_parse_multiple_ranges():
    assert parse_line_ranges("45-52,78-81") == ["45-52", "78-81"]


def test_parse_single_line():
    assert parse_line_ranges("78-78") == ["78-78"]


def test_parse_invalid_range_start_greater_than_end():
    with pytest.raises(ValueError, match="start must be <= end"):
        parse_line_ranges("52-45")


def test_parse_invalid_range_negative():
    with pytest.raises(ValueError, match="must be positive"):
        parse_line_ranges("-1-10")


def test_parse_invalid_range_non_numeric():
    with pytest.raises(ValueError, match="must be positive"):
        parse_line_ranges("abc-def")


LABEL_CONFIG = Labels(positive=["accurate"], negative=["outdated"])


def test_validate_labels_up_with_positive():
    errors = validate_labels("up", ["accurate"], LABEL_CONFIG)
    assert errors == []


def test_validate_labels_up_with_negative_rejects():
    errors = validate_labels("up", ["outdated"], LABEL_CONFIG)
    assert len(errors) == 1


def test_validate_labels_down_with_negative():
    errors = validate_labels("down", ["outdated"], LABEL_CONFIG)
    assert errors == []


def test_validate_labels_unknown_label():
    errors = validate_labels("up", ["nonexistent"], LABEL_CONFIG)
    assert len(errors) == 1


def test_validate_labels_empty_is_ok():
    errors = validate_labels("up", [], LABEL_CONFIG)
    assert errors == []


def test_validate_skill_name_valid():
    assert validate_skill_name("analyzing-charts") == []


def test_validate_skill_name_uppercase_rejected():
    errors = validate_skill_name("Analyzing-Charts")
    assert len(errors) > 0


def test_validate_skill_name_consecutive_hyphens():
    errors = validate_skill_name("analyzing--charts")
    assert len(errors) > 0


def test_validate_skill_name_starts_with_hyphen():
    errors = validate_skill_name("-analyzing")
    assert len(errors) > 0
