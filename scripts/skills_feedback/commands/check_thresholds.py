from __future__ import annotations

from pathlib import Path

from skills_feedback.constants import SKILL_FILENAME
from skills_feedback.models import Config
from skills_feedback.storage import (
    feedback_base,
    feedback_dir_for,
    load_proposals_file,
    load_ratings_file,
    proposals_path,
    ratings_path,
)


def _discover_skills(repo_root: Path) -> list[str]:
    skills = []
    for d in sorted(repo_root.iterdir()):
        if d.is_dir() and (d / SKILL_FILENAME).exists():
            skills.append(d.name)
    return skills


def _status_label(score: int, config: Config) -> str:
    if score <= config.thresholds.removal:
        return "REMOVAL SUGGESTED"
    if score < 0:
        return "below average"
    if score < config.thresholds.proposal:
        return "moderate"
    return "healthy"


def _proposal_summary(repo_root: Path, skill_name: str) -> str:
    fd = feedback_dir_for(repo_root, skill_name)
    proposals_file = load_proposals_file(proposals_path(fd))
    if not proposals_file or not proposals_file.proposals:
        return "-"
    counts: dict[str, int] = {}
    for p in proposals_file.proposals:
        counts[p.type] = counts.get(p.type, 0) + 1
    return ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))


def _classify_skill(
    repo_root: Path,
    skill_name: str,
    config: Config,
    rated: list[tuple[str, int, str, str]],
    unrated: list[str],
) -> None:
    fd = feedback_dir_for(repo_root, skill_name)
    ratings_file = load_ratings_file(ratings_path(fd))
    proposals = _proposal_summary(repo_root, skill_name)
    if ratings_file and ratings_file.ratings:
        score = ratings_file.compute_score()
        status = _status_label(score, config)
        rated.append((skill_name, score, status, proposals))
    elif proposals != "-":
        rated.append((skill_name, 0, "moderate", proposals))
    else:
        unrated.append(skill_name)


def _find_proposed_new(repo_root: Path, all_skills: list[str]) -> list[tuple[str, str]]:
    fb = feedback_base(repo_root)
    proposed_new: list[tuple[str, str]] = []
    if not fb.exists():
        return proposed_new
    for fd in sorted(fb.iterdir()):
        if fd.is_dir() and fd.name not in all_skills:
            proposals = _proposal_summary(repo_root, fd.name)
            if proposals != "-":
                proposed_new.append((fd.name, proposals))
    return proposed_new


def _print_rated(rated_skills: list[tuple[str, int, str, str]]) -> None:
    if not rated_skills:
        return
    print("SKILL RATINGS")
    print(f"{'Skill':<25}{'Score':<7}{'Status':<20}{'Proposals'}")
    for name, score, status, proposals in rated_skills:
        score_str = f"+{score}" if score > 0 else str(score)
        print(f"{name:<25}{score_str:<7}{status:<20}{proposals}")
    print()


def _print_proposed_new(proposed_new: list[tuple[str, str]]) -> None:
    if not proposed_new:
        return
    print("PROPOSED NEW SKILLS")
    for name, proposals in proposed_new:
        print(f"{name:<25}{'-':<7}{'-':<20}{proposals}")
    print()


def check_thresholds(repo_root: Path, config: Config) -> int:
    all_skills = _discover_skills(repo_root)
    rated_skills: list[tuple[str, int, str, str]] = []
    unrated_skills: list[str] = []

    for skill_name in all_skills:
        _classify_skill(repo_root, skill_name, config, rated_skills, unrated_skills)

    proposed_new = _find_proposed_new(repo_root, all_skills)

    _print_rated(rated_skills)
    if unrated_skills:
        print("UNRATED SKILLS")
        print(", ".join(unrated_skills))
        print()
    _print_proposed_new(proposed_new)

    return 0
