from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

from pydantic import BaseModel, Field

SKILL_FILENAME: Final[str] = "SKILL.md"
SKILLS_DIR: Final[str] = "skills"
DEFAULT_MIN_SCORE: Final[int] = 70
# Tracks the newest Flash release, so scores can shift without a commit here.
# Gemini 3.x is optimized for default sampling, so judges.py sends no temperature.
DEFAULT_MODEL: Final[str] = "gemini/gemini-flash-latest"
MAX_RETRIES: Final[int] = 3
RETRY_DELAY: Final[float] = 1.0

VALID_REQUIRES: Final[frozenset[str]] = frozenset(
    {
        "altertable-mcp",
        "chronos",
        "python",
        "statsforecast",
        "statsmodels",
    }
)

SeverityLevel = Literal["critical", "major", "minor"]


class ScoreBreakdown(BaseModel):
    frontmatter: int = Field(default=0, ge=0, le=20)
    structure: int = Field(default=0, ge=0, le=25)
    content_quality: int = Field(default=0, ge=0, le=35)
    pitfalls: int = Field(default=0, ge=0, le=10)
    references: int = Field(default=0, ge=0, le=10)

    @property
    def total(self) -> int:
        return (
            self.frontmatter
            + self.structure
            + self.content_quality
            + self.pitfalls
            + self.references
        )


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
