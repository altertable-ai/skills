from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel

SKILL_FILENAME: Final[str] = "SKILL.md"
MAX_CONTENT_CHARS: Final[int] = 8000
MAX_REFERENCE_CHARS: Final[int] = 2000
DEFAULT_MIN_SCORE: Final[int] = 70
MAX_RETRIES: Final[int] = 3
RETRY_DELAY: Final[float] = 1.0

SeverityLevel = Literal["critical", "major", "minor"]


class ScoreBreakdown(BaseModel):
    frontmatter: int = 0
    structure: int = 0
    content_quality: int = 0
    pitfalls: int = 0
    references: int = 0


class Issue(BaseModel):
    severity: SeverityLevel
    message: str


class ScoreResult(BaseModel):
    skill_name: str
    score: int
    breakdown: ScoreBreakdown
    issues: list[Issue] = []
    suggestions: list[str] = []
    judge_name: str = ""


class SkillContent(BaseModel):
    name: str
    content: str
    references: dict[str, str]
    line_count: int

    @classmethod
    def from_path(cls, skill_path: Path) -> SkillContent:
        skill_md = skill_path / SKILL_FILENAME
        if not skill_md.exists():
            raise FileNotFoundError(f"{SKILL_FILENAME} not found in {skill_path}")

        content = skill_md.read_text()

        references: dict[str, str] = {}
        ref_path = skill_path / "references"
        if ref_path.exists():
            for ref_file in ref_path.glob("*.md"):
                references[ref_file.name] = ref_file.read_text()

        return cls(
            name=skill_path.name,
            content=content,
            references=references,
            line_count=len(content.splitlines()),
        )
