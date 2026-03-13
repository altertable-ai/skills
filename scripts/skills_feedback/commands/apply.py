from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from skills_feedback.constants import SKILL_FILENAME
from skills_feedback.git import (
    git_checkout,
    git_checkout_new_branch,
    git_commit,
    git_current_branch,
    git_push,
    git_stage,
    is_git_repo,
)
from skills_feedback.models import (
    Config,
    Proposal,
    ProposalsFile,
    ProposalType,
    Rating,
    RatingsFile,
    Vote,
)
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


@dataclass
class QualifiedSkill:
    name: str
    feedback_dir: Path
    proposals_file: ProposalsFile
    proposal: Proposal
    ppath: Path
    rpath: Path
    score: int
    ratings: list[Rating]

    @property
    def branch_name(self) -> str:
        return f"feedback/{self.proposal.type}-{self.name}-{self.proposal.id}"


def _qualifies(proposal: Proposal, score: int, config: Config) -> bool:
    if proposal.type == ProposalType.REMOVE:
        return score <= config.thresholds.removal
    return score >= config.thresholds.proposal


def _evaluate_feedback_dir(feedback_dir: Path, config: Config) -> QualifiedSkill | None:
    ppath = proposals_path(feedback_dir)
    proposals_file = load_proposals_file(ppath)
    if not proposals_file or not proposals_file.proposals:
        return None

    rpath = ratings_path(feedback_dir)
    ratings_file = load_ratings_file(rpath)
    score = ratings_file.compute_score() if ratings_file else 0
    ratings = ratings_file.ratings if ratings_file else []

    proposal = next((p for p in proposals_file.proposals if _qualifies(p, score, config)), None)
    if not proposal:
        return None

    return QualifiedSkill(
        name=feedback_dir.name,
        feedback_dir=feedback_dir,
        proposals_file=proposals_file,
        proposal=proposal,
        ppath=ppath,
        rpath=rpath,
        score=score,
        ratings=ratings,
    )


def _collect_qualifying(repo_root: Path, config: Config) -> list[QualifiedSkill]:
    fb = feedback_base(repo_root)
    if not fb.exists():
        return []
    results = []
    for fd in sorted(fb.iterdir()):
        if not fd.is_dir():
            continue
        skill = _evaluate_feedback_dir(fd, config)
        if skill:
            results.append(skill)
    return results


def _apply_proposal(proposal: Proposal, feedback_dir: Path, skill_dir: Path) -> str | None:
    """Apply proposal to skill directory. Returns error message on skip, None on success."""
    if proposal.type == ProposalType.REMOVE:
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        return None
    if not proposal.body:
        return f"no body provided for {proposal.type} proposal"
    body_path = feedback_dir / proposal.body
    if proposal.type == ProposalType.ADD:
        skill_dir.mkdir(exist_ok=True)
        (skill_dir / "references").mkdir(exist_ok=True)
    shutil.copy2(body_path, skill_dir / SKILL_FILENAME)
    return None


def _cleanup(skill: QualifiedSkill) -> None:
    proposal = skill.proposal
    skill.proposals_file.proposals = [
        p for p in skill.proposals_file.proposals if p.id != proposal.id
    ]
    save_proposals_file(skill.ppath, skill.proposals_file)
    if proposal.body:
        body_file = skill.feedback_dir / proposal.body
        if body_file.exists():
            body_file.unlink()
    save_ratings_file(skill.rpath, RatingsFile(skill=skill.name, ratings=[]))


def _process(repo_root: Path, config: Config, skill: QualifiedSkill) -> bool:
    proposal = skill.proposal

    if _check_existing_pr(repo_root, skill.branch_name):
        print(f"skipped: {skill.name}:PR already open")
        return False

    original_branch = git_current_branch(repo_root)
    try:
        git_checkout_new_branch(repo_root, skill.branch_name)

        error = _apply_proposal(proposal, skill.feedback_dir, repo_root / skill.name)
        if error:
            print(f"skipped: {skill.name}:{error}")
            git_checkout(repo_root, original_branch)
            return False

        _cleanup(skill)
        git_stage(repo_root, [skill.ppath, skill.rpath, repo_root / skill.name])
        git_commit(repo_root, f"skills-feedback: {proposal.type} {skill.name}")
        git_push(repo_root, skill.branch_name)

        pr_body = _build_pr_body(proposal, skill.ratings, skill.score)
        pr_url = _create_pr(
            repo_root,
            skill.branch_name,
            f"{proposal.type} skill: {skill.name}",
            pr_body,
            config.reviewer,
        )
        if pr_url:
            print(f"created: {pr_url}")
            return True
        return False
    finally:
        current = git_current_branch(repo_root)
        if current != original_branch:
            git_checkout(repo_root, original_branch)


def apply_thresholds(repo_root: Path, config: Config, *, dry_run: bool = False) -> int:
    if not dry_run and not is_git_repo(repo_root):
        print_error("apply", "not a git repository")
        return 1

    qualifying = _collect_qualifying(repo_root, config)
    if not qualifying:
        print("No feedback data found.")
        return 0

    created = 0
    skipped = 0
    for skill in qualifying:
        if dry_run:
            print(f"would create PR: {skill.branch_name} (score: {skill.score})")
            created += 1
        elif _process(repo_root, config, skill):
            created += 1
        else:
            skipped += 1

    print(f"\nSummary: {created} PR(s) created, {skipped} skipped")
    return 0


def _ratings_table(ratings: list[Rating]) -> str:
    if not ratings:
        return ""
    lines = [
        "| Vote | Agent | Lines | Reason | Labels |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in ratings:
        rating_lines = ", ".join(r.lines) if r.lines else "-"
        labels = ", ".join(r.labels) if r.labels else "-"
        lines.append(f"| {r.vote} | {r.agent} | {rating_lines} | {r.reason} | {labels} |")
    return "\n".join(lines)


def _build_pr_body(proposal: Proposal, ratings: list[Rating], score: int) -> str:
    up_count = sum(1 for r in ratings if r.vote == Vote.UP)
    down_count = sum(1 for r in ratings if r.vote == Vote.DOWN)
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
        _ratings_table(ratings),
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
        print_warning("gh CLI not found:cannot check for existing PRs")
        return None


def _create_pr(cwd: Path, branch_name: str, title: str, body: str, reviewer: str) -> str | None:
    try:
        cmd = ["gh", "pr", "create", "--head", branch_name, "--title", title, "--body", body]
        if reviewer:
            cmd += ["--reviewer", reviewer]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            return result.stdout.strip()
        print_error("pr", result.stderr.strip())
        return None
    except FileNotFoundError:
        print_error("apply", "gh CLI not found:install gh and authenticate")
        return None
