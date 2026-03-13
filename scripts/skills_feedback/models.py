from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class ProposalType(StrEnum):
    ADD = "add"
    MODIFY = "modify"
    REMOVE = "remove"


class Rating(BaseModel):
    """A single up/down vote on a skill."""

    vote: Literal["up", "down"]
    lines: list[str] | None
    reason: str
    labels: list[str] = Field(default_factory=list)
    agent: str
    timestamp: str

    @property
    def score_value(self) -> int:
        """Return +1 for up votes, -1 for down votes."""
        return 1 if self.vote == "up" else -1


class RatingsFile(BaseModel):
    """Per-skill ratings storage."""

    skill: str
    ratings: list[Rating] = Field(default_factory=list)

    def compute_score(self) -> int:
        """Compute the aggregate score from all ratings."""
        return sum(r.score_value for r in self.ratings)


class Proposal(BaseModel):
    """A proposed skill change (add, modify, or remove)."""

    id: str
    type: ProposalType
    reason: str
    lines: list[str] | None = None
    body: str | None = None
    proposed_by: str
    proposed_at: str


class ProposalsFile(BaseModel):
    """Per-skill proposals storage."""

    skill: str
    proposals: list[Proposal] = Field(default_factory=list)


class Thresholds(BaseModel):
    """Score thresholds for actions."""

    proposal: int = 3
    removal: int = -3


class Labels(BaseModel):
    """Label sets for positive and negative votes."""

    positive: list[str] = Field(default_factory=list)
    negative: list[str] = Field(default_factory=list)


class Config(BaseModel):
    """Configuration loaded from .skills-config.yaml."""

    thresholds: Thresholds = Field(default_factory=Thresholds)
    reviewer: str = ""
    labels: Labels = Field(default_factory=Labels)
