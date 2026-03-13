from __future__ import annotations

from pathlib import Path

from skills_feedback.models import Config
from skills_feedback.storage import load_proposals_file, load_ratings_file


def _discover_skills(repo_root: Path) -> list[str]:
    skills = []
    for d in sorted(repo_root.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            skills.append(d.name)
    return skills


def _status_label(score: int, config: Config) -> str:
    proposal_threshold = config.thresholds.get("proposal", 3)
    removal_threshold = config.thresholds.get("removal", -3)
    if score <= removal_threshold:
        return "REMOVAL SUGGESTED"
    if score < 0:
        return "below average"
    if score < proposal_threshold:
        return "moderate"
    return "healthy"


def _proposal_summary(repo_root: Path, skill_name: str) -> str:
    feedback_dir = repo_root / ".skills-feedback" / skill_name
    proposals_file = load_proposals_file(feedback_dir / "proposals.json")
    if not proposals_file or not proposals_file.proposals:
        return "-"
    counts: dict[str, int] = {}
    for p in proposals_file.proposals:
        counts[p.type] = counts.get(p.type, 0) + 1
    return ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))


def check_thresholds(repo_root: Path, config: Config) -> int:
    all_skills = _discover_skills(repo_root)
    feedback_base = repo_root / ".skills-feedback"

    rated_skills: list[tuple[str, int, str, str]] = []
    unrated_skills: list[str] = []
    proposed_new: list[tuple[str, str]] = []

    for skill_name in all_skills:
        feedback_dir = feedback_base / skill_name
        ratings_file = load_ratings_file(feedback_dir / "ratings.json")
        proposals = _proposal_summary(repo_root, skill_name)
        if ratings_file and ratings_file.ratings:
            score = ratings_file.compute_score()
            status = _status_label(score, config)
            rated_skills.append((skill_name, score, status, proposals))
        else:
            if proposals != "-":
                rated_skills.append((skill_name, 0, "moderate", proposals))
            else:
                unrated_skills.append(skill_name)

    if feedback_base.exists():
        for feedback_dir in sorted(feedback_base.iterdir()):
            if feedback_dir.is_dir() and feedback_dir.name not in all_skills:
                proposals = _proposal_summary(repo_root, feedback_dir.name)
                if proposals != "-":
                    proposed_new.append((feedback_dir.name, proposals))

    if rated_skills:
        print("SKILL RATINGS")
        print(f"{'Skill':<25}{'Score':<7}{'Status':<20}{'Proposals'}")
        for name, score, status, proposals in rated_skills:
            score_str = f"+{score}" if score > 0 else str(score)
            print(f"{name:<25}{score_str:<7}{status:<20}{proposals}")
        print()

    if unrated_skills:
        print("UNRATED SKILLS")
        print(", ".join(unrated_skills))
        print()

    if proposed_new:
        print("PROPOSED NEW SKILLS")
        for name, proposals in proposed_new:
            print(f"{name:<25}{'-':<7}{'-':<20}{proposals}")
        print()

    return 0
