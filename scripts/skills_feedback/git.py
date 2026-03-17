from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        capture_output=True,
        text=True,
        check=check,
        cwd=cwd,
    )


def is_git_repo(cwd: Path) -> bool:
    return _run(cwd, "git", "rev-parse", "--is-inside-work-tree", check=False).returncode == 0


def git_stage(cwd: Path, files: list[Path]) -> None:
    _run(cwd, "git", "add", "-f", *[str(f) for f in files])


def git_commit(cwd: Path, message: str) -> None:
    _run(cwd, "git", "commit", "-m", message)


def stage_and_commit(
    cwd: Path,
    files: list[Path],
    message: str,
    *,
    no_commit: bool = False,
) -> None:
    if not is_git_repo(cwd):
        print("warning: not a git repository, skipping commit", file=sys.stderr)
        return
    if no_commit:
        return
    git_stage(cwd, files)
    git_commit(cwd, message)


def git_checkout_new_branch(cwd: Path, branch_name: str, base: str = "main") -> None:
    _run(cwd, "git", "checkout", "-b", branch_name, base)


def git_push(cwd: Path, branch_name: str) -> None:
    _run(cwd, "git", "push", "-u", "origin", branch_name)


def git_current_branch(cwd: Path) -> str:
    return _run(cwd, "git", "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def git_checkout(cwd: Path, branch_name: str) -> None:
    _run(cwd, "git", "checkout", branch_name)
