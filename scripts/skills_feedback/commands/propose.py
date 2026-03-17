from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from skills_feedback.git import stage_and_commit
from skills_feedback.models import Proposal, ProposalsFile, ProposalType, SkillsFeedbackError
from skills_feedback.output import print_confirmation
from skills_feedback.storage import FeedbackStore
from skills_feedback.validation import parse_line_ranges, validate_skill_name


def _generate_id(proposal_type: str, agent: str) -> tuple[str, str]:
    now = datetime.now(UTC)
    short_id = str(uuid4())
    return f"{proposal_type}-{short_id}-{agent}", now.isoformat()


def _copy_body(feedback_dir: Path, proposal_id: str, body: str) -> tuple[str, Path]:
    body_path = Path(body)
    if not body_path.exists():
        raise SkillsFeedbackError(f"body file not found: {body}")
    bodies_dir = feedback_dir / "bodies"
    bodies_dir.mkdir(exist_ok=True)
    dest = bodies_dir / f"{proposal_id}.md"
    dest.write_text(body_path.read_text())
    return f"bodies/{proposal_id}.md", dest


def _save_proposal(
    repo_root: Path,
    name: str,
    proposal_type: ProposalType,
    reason: str,
    agent: str,
    no_commit: bool,
    *,
    lines: list[str] | None = None,
    body: str | None = None,
) -> None:
    store = FeedbackStore(repo_root)
    feedback_dir = store.ensure_dir(name)
    proposals_file = store.load_proposals(name) or ProposalsFile(skill=name, proposals=[])

    proposal_id, timestamp = _generate_id(proposal_type, agent)

    body_ref = None
    changed_files: list[Path] = [store.proposals_path(name)]
    if body:
        body_ref, dest = _copy_body(feedback_dir, proposal_id, body)
        changed_files.append(dest)

    proposal = Proposal(
        id=proposal_id,
        type=proposal_type,
        reason=reason,
        lines=lines,
        body=body_ref,
        proposed_by=agent,
        proposed_at=timestamp,
    )
    proposals_file.proposals.append(proposal)
    store.save_proposals(name, proposals_file)

    stage_and_commit(
        repo_root,
        changed_files,
        f"skills-feedback: propose {proposal_type} {name}",
        no_commit=no_commit,
    )
    print_confirmation("proposed", name, proposal_id)


def propose_add(
    repo_root: Path,
    name: str,
    description: str,
    body: str | None,
    agent: str,
    no_commit: bool,
) -> None:
    name_errors = validate_skill_name(name)
    if name_errors:
        raise SkillsFeedbackError(name_errors[0], skill=name)
    store = FeedbackStore(repo_root)
    if store.skill_exists(name):
        raise SkillsFeedbackError("skill already exists", skill=name)
    _save_proposal(repo_root, name, ProposalType.ADD, description, agent, no_commit, body=body)


def propose_modify(
    repo_root: Path,
    name: str,
    reason: str,
    lines: str,
    body: str | None,
    agent: str,
    no_commit: bool,
) -> None:
    store = FeedbackStore(repo_root)
    if not store.skill_exists(name):
        raise SkillsFeedbackError("skill does not exist", skill=name)
    try:
        parsed_lines = parse_line_ranges(lines)
    except ValueError as e:
        raise SkillsFeedbackError(str(e), skill=name) from e
    _save_proposal(
        repo_root,
        name,
        ProposalType.MODIFY,
        reason,
        agent,
        no_commit,
        lines=parsed_lines,
        body=body,
    )


def propose_remove(
    repo_root: Path,
    name: str,
    reason: str,
    agent: str,
    no_commit: bool,
) -> None:
    store = FeedbackStore(repo_root)
    if not store.skill_exists(name):
        raise SkillsFeedbackError("skill does not exist", skill=name)
    _save_proposal(repo_root, name, ProposalType.REMOVE, reason, agent, no_commit)
