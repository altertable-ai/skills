from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class Rating(BaseModel):
    vote: Literal["up", "down"]
    lines: list[str] | None
    reason: str
    labels: list[str]
    agent: str
    timestamp: str

    @property
    def score_value(self) -> int:
        return 1 if self.vote == "up" else -1


class RatingsFile(BaseModel):
    skill: str
    ratings: list[Rating]

    def compute_score(self) -> int:
        return sum(r.score_value for r in self.ratings)


class Proposal(BaseModel):
    id: str
    type: Literal["add", "modify", "remove"]
    reason: str
    lines: list[str] | None
    body: str | None
    proposed_by: str
    proposed_at: str


class ProposalsFile(BaseModel):
    skill: str
    proposals: list[Proposal]


class Config(BaseModel):
    thresholds: dict[str, int]
    reviewer: str
    labels: dict[str, list[str]]
