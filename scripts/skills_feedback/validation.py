from __future__ import annotations

import re

from skills_feedback.models import Labels

SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_line_ranges(lines_str: str) -> list[str]:
    """Parse comma-separated line ranges like '45-52,78-81'."""
    ranges = []
    for part in lines_str.split(","):
        part = part.strip()
        if "-" not in part:
            raise ValueError(f"Invalid range format '{part}': must be start-end")
        segments = part.split("-", 1)
        try:
            start = int(segments[0])
            end = int(segments[1])
        except ValueError:
            raise ValueError(f"Line range values must be positive integers, got '{part}'")
        if start <= 0 or end <= 0:
            raise ValueError(f"Line range values must be positive integers, got '{part}'")
        if start > end:
            raise ValueError(f"Invalid range '{part}': start must be <= end")
        ranges.append(part)
    return ranges


def validate_labels(vote: str, labels: list[str], label_config: Labels) -> list[str]:
    """Validate that labels are allowed for the given vote direction."""
    if not labels:
        return []
    allowed = set(label_config.positive if vote == "up" else label_config.negative)
    return [
        f"Label '{label}' is not allowed for '{vote}' votes. Allowed: {sorted(allowed)}"
        for label in labels
        if label not in allowed
    ]


def validate_skill_name(name: str) -> list[str]:
    """Validate a skill name matches the required pattern."""
    if not SKILL_NAME_PATTERN.match(name):
        return [f"Skill name '{name}' must be lowercase alphanumeric with single hyphens"]
    return []
