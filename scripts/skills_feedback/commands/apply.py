from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from skills_feedback.constants import SKILL_FILENAME
from skills_feedback.git import (
    git_checkout,
    git_checkout_new_branch,
    git_commit,
    git_current_branch,
    git_push,
    git_stage,
)
from skills_feedback.models import Config, Proposal, Rating, RatingsFile
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
    lines = [
        "## Summary",
        f"{proposal.type} skill: {proposal.reason}",
        "",
        "## Reason",
        proposal.reason,
        "",
        "## Feedback",
        f"Score: {score} ({up_count} up, {down_count} down)",
        "",
        "| Vote | Agent | Lines | Reason | Labels |",
        "|---|---|---|---|---|",
    ]
    for r in ratings:
        lines_str = ", ".join(r.lines) if r.lines else "whole file"
        labels_str = ", ".join(r.labels) if r.labels else "-"
        lines.append(f"| {r.vote} | {r.agent} | {lines_str} | {r.reason} | {labels_str} |")
    return "\n".join(lines)


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


def apply_thresholds(repo_root: Path, config: Config, *, dry_run: bool = False) -> int:
    fb = feedback_base(repo_root)
    if not fb.exists():
        print("No feedback data found.")
        return 0

    proposal_threshold = config.thresholds.proposal
    created = 0
    skipped = 0

    for feedback_dir in sorted(fb.iterdir()):
        if not feedback_dir.is_dir():
            continue

        skill_name = feedback_dir.name
        ppath = proposals_path(feedback_dir)
        proposals_file = load_proposals_file(ppath)
        if not proposals_file or not proposals_file.proposals:
            continue

        rpath = ratings_path(feedback_dir)
        ratings_file = load_ratings_file(rpath)
        score = ratings_file.compute_score() if ratings_file else 0
        ratings = ratings_file.ratings if ratings_file else []

        if score < proposal_threshold:
            skipped += 1
            continue

        for proposal in proposals_file.proposals:
            branch_name = f"feedback/{proposal.type}-{skill_name}-{proposal.id}"

            if dry_run:
                print(f"would create PR: {branch_name} (score: {score})")
                created += 1
                continue

            existing_pr = _check_existing_pr(repo_root, branch_name)
            if existing_pr:
                print(f"skipped: {skill_name} — PR already open: {existing_pr}")
                skipped += 1
                continue

            original_branch = git_current_branch(repo_root)

            try:
                git_checkout_new_branch(repo_root, branch_name)

                skill_dir = repo_root / skill_name
                if proposal.type == "add":
                    if not proposal.body:
                        print(f"skipped: {skill_name} — no body provided for add proposal")
                        git_checkout(repo_root, original_branch)
                        skipped += 1
                        continue
                    body_path = feedback_dir / proposal.body
                    skill_dir.mkdir(exist_ok=True)
                    (skill_dir / "references").mkdir(exist_ok=True)
                    shutil.copy2(body_path, skill_dir / SKILL_FILENAME)

                elif proposal.type == "modify":
                    if not proposal.body:
                        print(f"skipped: {skill_name} — no body provided for modify proposal")
                        git_checkout(repo_root, original_branch)
                        skipped += 1
                        continue
                    body_path = feedback_dir / proposal.body
                    shutil.copy2(body_path, skill_dir / SKILL_FILENAME)

                elif proposal.type == "remove":
                    if skill_dir.exists():
                        shutil.rmtree(skill_dir)

                proposals_file.proposals = [
                    p for p in proposals_file.proposals if p.id != proposal.id
                ]
                save_proposals_file(ppath, proposals_file)
                if proposal.body:
                    body_file = feedback_dir / proposal.body
                    if body_file.exists():
                        body_file.unlink()
                save_ratings_file(rpath, RatingsFile(skill=skill_name, ratings=[]))

                git_stage(repo_root, [ppath, rpath, skill_dir])
                git_commit(repo_root, f"skills-feedback: {proposal.type} {skill_name}")
                git_push(repo_root, branch_name)

                title = f"{proposal.type} skill: {skill_name}"
                pr_body = _build_pr_body(proposal, ratings, score)
                pr_url = _create_pr(repo_root, branch_name, title, pr_body, config.reviewer)

                if pr_url:
                    print(f"created: {pr_url}")
                    created += 1

            finally:
                current = git_current_branch(repo_root)
                if current != original_branch:
                    git_checkout(repo_root, original_branch)

    print(f"\nSummary: {created} PR(s) created, {skipped} skipped")
    return 0
