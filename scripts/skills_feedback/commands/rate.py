from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from skills_feedback.git import stage_and_commit
from skills_feedback.models import Config, Rating, RatingsFile, SkillsFeedbackError, Vote
from skills_feedback.output import print_confirmation, print_warning
from skills_feedback.storage import (
    ensure_feedback_dir,
    load_ratings_file,
    ratings_path,
    save_ratings_file,
    skill_exists,
)
from skills_feedback.validation import parse_line_ranges, validate_labels


def rate_skill(
    repo_root: Path,
    config: Config,
    name: str,
    vote: Vote,
    reason: str,
    lines: str | None,
    whole_file: bool,
    labels: list[str],
    agent: str,
    no_commit: bool,
) -> None:
    if not skill_exists(repo_root, name):
        raise SkillsFeedbackError("skill does not exist", skill=name)

    parsed_lines = None
    if not whole_file:
        if not lines:
            raise SkillsFeedbackError("either --lines or --whole-file is required", skill=name)
        try:
            parsed_lines = parse_line_ranges(lines)
        except ValueError as e:
            raise SkillsFeedbackError(str(e), skill=name) from e

    if labels:
        label_errors = validate_labels(vote, labels, config.labels)
        if label_errors:
            raise SkillsFeedbackError(label_errors[0], skill=name)

    feedback_dir = ensure_feedback_dir(repo_root, name)
    rpath = ratings_path(feedback_dir)
    ratings_file = load_ratings_file(rpath) or RatingsFile(skill=name, ratings=[])

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
    save_ratings_file(rpath, ratings_file)

    score = ratings_file.compute_score()
    if score <= config.thresholds.removal:
        print_warning(
            f"skill {name} has reached removal threshold "
            f"(score: {score}): consider running "
            f"`skills-feedback propose remove {name}`"
        )

    stage_and_commit(
        repo_root,
        [rpath],
        f"skills-feedback: rate {name}",
        no_commit=no_commit,
    )
    print_confirmation("rated", f"{name} {vote}")
