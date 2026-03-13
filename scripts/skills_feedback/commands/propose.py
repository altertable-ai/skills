from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from skills_feedback.git import stage_and_commit
from skills_feedback.models import Proposal, ProposalsFile, ProposalType
from skills_feedback.output import print_confirmation, print_error
from skills_feedback.storage import (
    ensure_feedback_dir,
    load_proposals_file,
    proposals_path,
    save_proposals_file,
    skill_exists,
)
from skills_feedback.validation import parse_line_ranges, validate_skill_name


def _generate_id(proposal_type: str, agent: str, existing_ids: set[str]) -> tuple[str, str]:
    now = datetime.now(UTC)
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")
    base_id = f"{proposal_type}-{timestamp}-{agent}"
    proposal_id = base_id
    counter = 2
    while proposal_id in existing_ids:
        proposal_id = f"{base_id}-{counter}"
        counter += 1
    return proposal_id, now.isoformat()


def _copy_body(feedback_dir: Path, proposal_id: str, body: str) -> tuple[str, Path] | None:
    body_path = Path(body)
    if not body_path.exists():
        print_error("body", f"file not found: {body}")
        return None
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
) -> int:
    feedback_dir = ensure_feedback_dir(repo_root, name)
    ppath = proposals_path(feedback_dir)
    proposals_file = load_proposals_file(ppath) or ProposalsFile(skill=name, proposals=[])

    existing_ids = {p.id for p in proposals_file.proposals}
    proposal_id, timestamp = _generate_id(proposal_type, agent, existing_ids)

    body_ref = None
    changed_files: list[Path] = [ppath]
    if body:
        result = _copy_body(feedback_dir, proposal_id, body)
        if result is None:
            return 1
        body_ref, dest = result
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
    save_proposals_file(ppath, proposals_file)

    stage_and_commit(
        repo_root,
        changed_files,
        f"skills-feedback: propose {proposal_type} {name}",
        no_commit=no_commit,
    )
    print_confirmation("proposed", name, proposal_id)
    return 0


def propose_add(
    repo_root: Path,
    name: str,
    description: str,
    body: str | None,
    agent: str,
    no_commit: bool,
) -> int:
    name_errors = validate_skill_name(name)
    if name_errors:
        print_error(name, name_errors[0])
        return 1
    if skill_exists(repo_root, name):
        print_error(name, "skill already exists")
        return 1
    return _save_proposal(
        repo_root,
        name,
        ProposalType.ADD,
        description,
        agent,
        no_commit,
        body=body,
    )


def propose_modify(
    repo_root: Path,
    name: str,
    reason: str,
    lines: str,
    body: str | None,
    agent: str,
    no_commit: bool,
) -> int:
    if not skill_exists(repo_root, name):
        print_error(name, "skill does not exist")
        return 1
    try:
        parsed_lines = parse_line_ranges(lines)
    except ValueError as e:
        print_error(name, str(e))
        return 1
    return _save_proposal(
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
) -> int:
    if not skill_exists(repo_root, name):
        print_error(name, "skill does not exist")
        return 1
    return _save_proposal(repo_root, name, ProposalType.REMOVE, reason, agent, no_commit)
