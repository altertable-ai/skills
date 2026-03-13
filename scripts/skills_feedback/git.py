from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def is_git_repo(cwd: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.returncode == 0


def git_stage(cwd: Path, files: list[Path]) -> None:
    subprocess.run(
        ["git", "add", *[str(f) for f in files]],
        check=True,
        capture_output=True,
        cwd=cwd,
    )


def git_commit(cwd: Path, message: str) -> None:
    subprocess.run(
        ["git", "commit", "-m", message],
        check=True,
        capture_output=True,
        cwd=cwd,
    )


def stage_and_commit(
    cwd: Path, files: list[Path], message: str, *, no_commit: bool = False
) -> None:
    if not is_git_repo(cwd):
        print("warning: not a git repository, skipping commit", file=sys.stderr)
        return
    git_stage(cwd, files)
    if not no_commit:
        git_commit(cwd, message)


def git_checkout_new_branch(cwd: Path, branch_name: str, base: str = "main") -> None:
    subprocess.run(
        ["git", "checkout", "-b", branch_name, base],
        check=True,
        capture_output=True,
        cwd=cwd,
    )


def git_push(cwd: Path, branch_name: str) -> None:
    subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        check=True,
        capture_output=True,
        cwd=cwd,
    )


def git_current_branch(cwd: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
        cwd=cwd,
    )
    return result.stdout.strip()


def git_checkout(cwd: Path, branch_name: str) -> None:
    subprocess.run(
        ["git", "checkout", branch_name],
        check=True,
        capture_output=True,
        cwd=cwd,
    )
