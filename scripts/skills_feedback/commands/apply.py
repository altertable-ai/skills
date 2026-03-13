from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from py_markdown_table.markdown_table import markdown_table

from skills_feedback.constants import SKILL_FILENAME
from skills_feedback.git import (
    git_checkout,
    git_checkout_new_branch,
    git_commit,
    git_current_branch,
    git_push,
    git_stage,
)
from skills_feedback.models import Config, Proposal, ProposalType, Rating, RatingsFile
from skills_feedback.output import print_error, print_warning
from skills_feedback.storage import (
    feedback_base,
    load_proposals_file,
    load_ratings_file,
    proposals_path,
    ratings_path,
    save_proposals_file,
    save_ratings_file,
)


def _build_pr_body(proposal: Proposal, ratings: list[Rating], score: int) -> str:
    up_count = sum(1 for r in ratings if r.vote == "up")
    down_count = sum(1 for r in ratings if r.vote == "down")

    table_data = [
        {
            "Vote": r.vote,
            "Agent": r.agent,
            "Lines": ", ".join(r.lines) if r.lines else "whole file",
            "Reason": r.reason,
            "Labels": ", ".join(r.labels) if r.labels else "-",
        }
        for r in ratings
    ]
    table_md = markdown_table(table_data).get_markdown() if table_data else ""

    sections = [
        "## Summary",
        f"{proposal.type} skill: {proposal.reason}",
        "",
        "## Reason",
        proposal.reason,
        "",
        "## Feedback",
        f"Score: {score} ({up_count} up, {down_count} down)",
        "",
        table_md,
    ]
    return "\n".join(sections)


def _check_existing_pr(cwd: Path, branch_name: str) -> str | None:
    try:
        result = subprocess.run(
            [
                "gh",
                "pr",
                "list",
                "--head",
                branch_name,
                "--state",
                "open",
                "--json",
                "url",
                "--jq",
                ".[0].url",
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        url = result.stdout.strip()
        return url if url else None
    except FileNotFoundError:
        print_warning("gh CLI not found — cannot check for existing PRs")
        return None


def _create_pr(cwd: Path, branch_name: str, title: str, body: str, reviewer: str) -> str | None:
    try:
        cmd = [
            "gh",
            "pr",
            "create",
            "--head",
            branch_name,
            "--title",
            title,
            "--body",
            body,
        ]
        if reviewer:
            cmd += ["--reviewer", reviewer]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        print_error("pr", result.stderr.strip())
        return None
    except FileNotFoundError:
        print_error("apply", "gh CLI not found — install gh and authenticate")
        return None


class _SkipProposal(Exception):
    pass


def _apply_add(proposal: Proposal, feedback_dir: Path, skill_dir: Path) -> None:
    if not proposal.body:
        raise _SkipProposal("no body provided for add proposal")
    body_path = feedback_dir / proposal.body
    skill_dir.mkdir(exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    shutil.copy2(body_path, skill_dir / SKILL_FILENAME)


def _apply_modify(proposal: Proposal, feedback_dir: Path, skill_dir: Path) -> None:
    if not proposal.body:
        raise _SkipProposal("no body provided for modify proposal")
    body_path = feedback_dir / proposal.body
    shutil.copy2(body_path, skill_dir / SKILL_FILENAME)


def _apply_remove(skill_dir: Path) -> None:
    if skill_dir.exists():
        shutil.rmtree(skill_dir)


_PROPOSAL_HANDLERS = {
    ProposalType.ADD: _apply_add,
    ProposalType.MODIFY: _apply_modify,
}


def _apply_proposal(proposal: Proposal, feedback_dir: Path, skill_dir: Path) -> None:
    if proposal.type == ProposalType.REMOVE:
        _apply_remove(skill_dir)
    else:
        handler = _PROPOSAL_HANDLERS[proposal.type]
        handler(proposal, feedback_dir, skill_dir)


def _cleanup_proposal(
    proposals_file,
    proposal: Proposal,
    ppath: Path,
    rpath: Path,
    feedback_dir: Path,
    skill_name: str,
) -> None:
    proposals_file.proposals = [p for p in proposals_file.proposals if p.id != proposal.id]
    save_proposals_file(ppath, proposals_file)
    if proposal.body:
        body_file = feedback_dir / proposal.body
        if body_file.exists():
            body_file.unlink()
    save_ratings_file(rpath, RatingsFile(skill=skill_name, ratings=[]))


@dataclass
class _ApplyResult:
    created: int = 0
    skipped: int = 0


def _collect_qualifying_skills(repo_root: Path, config: Config) -> list[dict]:
    fb = feedback_base(repo_root)
    if not fb.exists():
        return []

    qualifying = []
    for feedback_dir in sorted(fb.iterdir()):
        if not feedback_dir.is_dir():
            continue

        ppath = proposals_path(feedback_dir)
        proposals_file = load_proposals_file(ppath)
        if not proposals_file or not proposals_file.proposals:
            continue

        rpath = ratings_path(feedback_dir)
        ratings_file = load_ratings_file(rpath)
        score = ratings_file.compute_score() if ratings_file else 0
        ratings = ratings_file.ratings if ratings_file else []

        if score < config.thresholds.proposal:
            continue

        qualifying.append(
            {
                "feedback_dir": feedback_dir,
                "skill_name": feedback_dir.name,
                "proposals_file": proposals_file,
                "ppath": ppath,
                "rpath": rpath,
                "score": score,
                "ratings": ratings,
            }
        )
    return qualifying


def _process_proposal(
    repo_root: Path, config: Config, skill: dict, proposal: Proposal, result: _ApplyResult
) -> None:
    skill_name = skill["skill_name"]
    feedback_dir = skill["feedback_dir"]
    branch_name = f"feedback/{proposal.type}-{skill_name}-{proposal.id}"

    existing_pr = _check_existing_pr(repo_root, branch_name)
    if existing_pr:
        print(f"skipped: {skill_name} — PR already open: {existing_pr}")
        result.skipped += 1
        return

    original_branch = git_current_branch(repo_root)
    try:
        git_checkout_new_branch(repo_root, branch_name)
        skill_dir = repo_root / skill_name

        try:
            _apply_proposal(proposal, feedback_dir, skill_dir)
        except _SkipProposal as e:
            print(f"skipped: {skill_name} — {e}")
            git_checkout(repo_root, original_branch)
            result.skipped += 1
            return

        _cleanup_proposal(
            skill["proposals_file"],
            proposal,
            skill["ppath"],
            skill["rpath"],
            feedback_dir,
            skill_name,
        )

        git_stage(repo_root, [skill["ppath"], skill["rpath"], skill_dir])
        git_commit(repo_root, f"skills-feedback: {proposal.type} {skill_name}")
        git_push(repo_root, branch_name)

        pr_body = _build_pr_body(proposal, skill["ratings"], skill["score"])
        pr_url = _create_pr(
            repo_root, branch_name, f"{proposal.type} skill: {skill_name}", pr_body, config.reviewer
        )
        if pr_url:
            print(f"created: {pr_url}")
            result.created += 1
    finally:
        current = git_current_branch(repo_root)
        if current != original_branch:
            git_checkout(repo_root, original_branch)


def apply_thresholds(repo_root: Path, config: Config, *, dry_run: bool = False) -> int:
    qualifying = _collect_qualifying_skills(repo_root, config)
    if not qualifying:
        print("No feedback data found.")
        return 0

    result = _ApplyResult()

    for skill in qualifying:
        for proposal in skill["proposals_file"].proposals:
            branch_name = f"feedback/{proposal.type}-{skill['skill_name']}-{proposal.id}"
            if dry_run:
                print(f"would create PR: {branch_name} (score: {skill['score']})")
                result.created += 1
            else:
                _process_proposal(repo_root, config, skill, proposal, result)

    print(f"\nSummary: {result.created} PR(s) created, {result.skipped} skipped")
    return 0
