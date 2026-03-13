from __future__ import annotations

import json
from pathlib import Path

from skills_feedback.constants import (
    FEEDBACK_DIR_NAME,
    PROPOSALS_FILENAME,
    RATINGS_FILENAME,
    SKILL_FILENAME,
)
from skills_feedback.models import ProposalsFile, RatingsFile


def skill_exists(repo_root: Path, name: str) -> bool:
    return (repo_root / name / SKILL_FILENAME).exists()


def feedback_dir_for(repo_root: Path, skill_name: str) -> Path:
    return repo_root / FEEDBACK_DIR_NAME / skill_name


def feedback_base(repo_root: Path) -> Path:
    return repo_root / FEEDBACK_DIR_NAME


def ratings_path(feedback_dir: Path) -> Path:
    return feedback_dir / RATINGS_FILENAME


def proposals_path(feedback_dir: Path) -> Path:
    return feedback_dir / PROPOSALS_FILENAME


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
    fd = feedback_dir_for(repo_root, skill_name)
    fd.mkdir(parents=True, exist_ok=True)
    return fd
