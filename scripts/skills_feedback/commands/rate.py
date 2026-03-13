from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from skills_feedback.git import stage_and_commit
from skills_feedback.models import Config, Rating, RatingsFile
from skills_feedback.output import print_confirmation, print_error, print_warning
from skills_feedback.storage import ensure_feedback_dir, load_ratings_file, save_ratings_file
from skills_feedback.validation import parse_line_ranges, validate_labels


def rate_skill(
    repo_root: Path,
    config: Config,
    name: str,
    vote: Literal["up", "down"],
    reason: str,
    lines: str | None,
    whole_file: bool,
    labels: list[str],
    agent: str,
    no_commit: bool,
) -> int:
    if not (repo_root / name / "SKILL.md").exists():
        print_error(name, "skill does not exist")
        return 1

    parsed_lines = None
    if not whole_file:
        if not lines:
            print_error(name, "either --lines or --whole-file is required")
            return 1
        try:
            parsed_lines = parse_line_ranges(lines)
        except ValueError as e:
            print_error(name, str(e))
            return 1

    if labels:
        label_errors = validate_labels(vote, labels, config.labels)
        if label_errors:
            print_error(name, label_errors[0])
            return 1

    feedback_dir = ensure_feedback_dir(repo_root, name)
    ratings_path = feedback_dir / "ratings.json"
    ratings_file = load_ratings_file(ratings_path) or RatingsFile(skill=name, ratings=[])

    now = datetime.now(UTC)
    rating = Rating(
        vote=vote,
        lines=parsed_lines,
        reason=reason,
        labels=labels,
        agent=agent,
        timestamp=now.isoformat(),
    )
    ratings_file.ratings.append(rating)
    save_ratings_file(ratings_path, ratings_file)

    score = ratings_file.compute_score()
    removal_threshold = config.thresholds.get("removal", -3)
    if score <= removal_threshold:
        print_warning(
            f"skill {name} has reached removal threshold "
            f"(score: {score}) — consider running "
            f"`skills-feedback propose remove {name}`"
        )

    stage_and_commit(
        repo_root,
        [ratings_path],
        f"skills-feedback: rate {name}",
        no_commit=no_commit,
    )
    print_confirmation("rated", f"{name} {vote}")
    return 0
