from __future__ import annotations

from pydantic import BaseModel, Field

from skills_feedback.commands.apply import apply_thresholds
from skills_feedback.commands.check_thresholds import check_thresholds
from skills_feedback.commands.propose import propose_add, propose_modify, propose_remove
from skills_feedback.commands.rate import rate_skill
from skills_feedback.config import load_repo_config
from skills_feedback.models import SkillsFeedbackError, Vote


class RateRequest(BaseModel):
    """Rate a skill up or down to express quality feedback."""

    name: str = Field(description="Skill name to rate (e.g., 'analyzing-charts')")
    vote: Vote = Field(description="Vote direction")
    reason: str = Field(description="Why you are rating this way")
    lines: str | None = Field(default=None, description="Line ranges (e.g., '45-52,78-81')")
    whole_file: bool = Field(
        default=False, description="Rate the entire file instead of specific lines"
    )
    labels: list[str] = Field(
        default_factory=list, description="Quality labels (e.g., ['accurate', 'helpful'])"
    )
    agent: str = Field(default="unknown", description="Identity of the agent rating")
    no_commit: bool = Field(default=False, description="Stage changes but do not commit")


class ProposeAddRequest(BaseModel):
    """Propose adding a new skill to the repository."""

    name: str = Field(description="Skill name (lowercase, hyphen-separated)")
    description: str = Field(description="Why this skill should exist")
    body: str | None = Field(
        default=None, description="Path to a SKILL.md file for the proposed skill"
    )
    agent: str = Field(default="unknown", description="Identity of the agent making the proposal")
    no_commit: bool = Field(default=False, description="Stage changes but do not commit")


class ProposeModifyRequest(BaseModel):
    """Propose modifying an existing skill."""

    name: str = Field(description="Skill name to modify")
    reason: str = Field(description="Why this change is needed")
    lines: str = Field(description="Line ranges to modify (e.g., '45-52,78-81')")
    body: str | None = Field(default=None, description="Path to a modified SKILL.md file")
    agent: str = Field(default="unknown", description="Identity of the agent making the proposal")
    no_commit: bool = Field(default=False, description="Stage changes but do not commit")


class ProposeRemoveRequest(BaseModel):
    """Propose removing an existing skill."""

    name: str = Field(description="Skill name to remove")
    reason: str = Field(description="Why this skill should be removed")
    agent: str = Field(default="unknown", description="Identity of the agent making the proposal")
    no_commit: bool = Field(default=False, description="Stage changes but do not commit")


class ApplyRequest(BaseModel):
    """Create PRs for proposals that reached the score threshold."""

    dry_run: bool = Field(default=False, description="Show what would happen without creating PRs")


def _load():
    return load_repo_config()


def rate(request: RateRequest) -> None:
    """Rate a skill up or down to express quality feedback."""
    repo_root, config = _load()
    result = rate_skill(
        repo_root=repo_root,
        config=config,
        name=request.name,
        vote=request.vote,
        reason=request.reason,
        lines=request.lines,
        whole_file=request.whole_file,
        labels=request.labels,
        agent=request.agent,
        no_commit=request.no_commit,
    )
    if result != 0:
        raise SkillsFeedbackError("rate failed", skill=request.name)


def propose_add_skill(request: ProposeAddRequest) -> None:
    """Propose adding a new skill to the repository."""
    repo_root, _ = _load()
    result = propose_add(
        repo_root=repo_root,
        name=request.name,
        description=request.description,
        body=request.body,
        agent=request.agent,
        no_commit=request.no_commit,
    )
    if result != 0:
        raise SkillsFeedbackError("propose add failed", skill=request.name)


def propose_modify_skill(request: ProposeModifyRequest) -> None:
    """Propose modifying an existing skill."""
    repo_root, _ = _load()
    result = propose_modify(
        repo_root=repo_root,
        name=request.name,
        reason=request.reason,
        lines=request.lines,
        body=request.body,
        agent=request.agent,
        no_commit=request.no_commit,
    )
    if result != 0:
        raise SkillsFeedbackError("propose modify failed", skill=request.name)


def propose_remove_skill(request: ProposeRemoveRequest) -> None:
    """Propose removing an existing skill."""
    repo_root, _ = _load()
    result = propose_remove(
        repo_root=repo_root,
        name=request.name,
        reason=request.reason,
        agent=request.agent,
        no_commit=request.no_commit,
    )
    if result != 0:
        raise SkillsFeedbackError("propose remove failed", skill=request.name)


def apply(request: ApplyRequest | None = None) -> None:
    """Create PRs for proposals that reached the score threshold."""
    repo_root, config = _load()
    dry_run = request.dry_run if request else False
    result = apply_thresholds(repo_root, config, dry_run=dry_run)
    if result != 0:
        raise SkillsFeedbackError("apply failed")


def check() -> None:
    """Show skill ratings, status, and proposals dashboard."""
    repo_root, config = _load()
    result = check_thresholds(repo_root, config)
    if result != 0:
        raise SkillsFeedbackError("check-thresholds failed")
