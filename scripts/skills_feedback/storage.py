from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import BaseModel, ValidationError

from skills_feedback.constants import (
    FEEDBACK_DIR_NAME,
    PROPOSALS_FILENAME,
    RATINGS_FILENAME,
    SKILL_FILENAME,
)
from skills_feedback.models import ProposalsFile, RatingsFile


def _load_json_model[T: BaseModel](path: Path, model: type[T]) -> T | None:
    if not path.exists():
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        return model.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"warning: skipping malformed {path}: {e}", file=sys.stderr)
        return None


def _save_json_model(path: Path, obj: BaseModel) -> None:
    with open(path, "w") as f:
        json.dump(obj.model_dump(), f, indent=2)
        f.write("\n")


class FeedbackStore:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.base = repo_root / FEEDBACK_DIR_NAME

    def skill_exists(self, name: str) -> bool:
        return (self.repo_root / name / SKILL_FILENAME).exists()

    def feedback_dir(self, skill_name: str) -> Path:
        return self.base / skill_name

    def ensure_dir(self, skill_name: str) -> Path:
        fd = self.feedback_dir(skill_name)
        fd.mkdir(parents=True, exist_ok=True)
        return fd

    def ratings_path(self, skill_name: str) -> Path:
        return self.feedback_dir(skill_name) / RATINGS_FILENAME

    def proposals_path(self, skill_name: str) -> Path:
        return self.feedback_dir(skill_name) / PROPOSALS_FILENAME

    def load_ratings(self, skill_name: str) -> RatingsFile | None:
        return _load_json_model(self.ratings_path(skill_name), RatingsFile)

    def save_ratings(self, skill_name: str, data: RatingsFile) -> None:
        _save_json_model(self.ratings_path(skill_name), data)

    def load_proposals(self, skill_name: str) -> ProposalsFile | None:
        return _load_json_model(self.proposals_path(skill_name), ProposalsFile)

    def save_proposals(self, skill_name: str, data: ProposalsFile) -> None:
        _save_json_model(self.proposals_path(skill_name), data)

    def skill_feedback_dirs(self) -> list[Path]:
        if not self.base.exists():
            return []
        return [fd for fd in sorted(self.base.iterdir()) if fd.is_dir()]
