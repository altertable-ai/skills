from __future__ import annotations

import json
from pathlib import Path

from skills_feedback.models import ProposalsFile, RatingsFile


def load_ratings_file(path: Path) -> RatingsFile | None:
    if not path.exists():
        return None
    with open(path) as f:
        data = json.load(f)
    return RatingsFile.model_validate(data)


def save_ratings_file(path: Path, ratings_file: RatingsFile) -> None:
    with open(path, "w") as f:
        json.dump(ratings_file.model_dump(), f, indent=2)
        f.write("\n")


def load_proposals_file(path: Path) -> ProposalsFile | None:
    if not path.exists():
        return None
    with open(path) as f:
        data = json.load(f)
    return ProposalsFile.model_validate(data)


def save_proposals_file(path: Path, proposals_file: ProposalsFile) -> None:
    with open(path, "w") as f:
        json.dump(proposals_file.model_dump(), f, indent=2)
        f.write("\n")


def ensure_feedback_dir(repo_root: Path, skill_name: str) -> Path:
    feedback_dir = repo_root / ".skills-feedback" / skill_name
    feedback_dir.mkdir(parents=True, exist_ok=True)
    return feedback_dir
