from __future__ import annotations


def parse_line_ranges(lines_str: str) -> list[str]:
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


def validate_labels(vote: str, labels: list[str], label_config: dict[str, list[str]]) -> list[str]:
    if not labels:
        return []
    errors = []
    allowed_key = "positive" if vote == "up" else "negative"
    allowed = set(label_config.get(allowed_key, []))
    for label in labels:
        if label not in allowed:
            errors.append(
                f"Label '{label}' is not allowed for '{vote}' votes. Allowed: {sorted(allowed)}"
            )
    return errors


def validate_skill_name(name: str) -> list[str]:
    errors = []
    if name != name.lower():
        errors.append(f"Skill name '{name}' must be lowercase")
    if name.startswith("-") or name.endswith("-"):
        errors.append("Skill name cannot start or end with a hyphen")
    if "--" in name:
        errors.append("Skill name cannot contain consecutive hyphens")
    if not all(c.isalnum() or c == "-" for c in name):
        errors.append(f"Skill name '{name}' contains invalid characters")
    return errors
