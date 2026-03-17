from __future__ import annotations

import sys

import fire

from skills_feedback.commands.apply import apply_thresholds
from skills_feedback.commands.check_thresholds import check_thresholds as _check_thresholds
from skills_feedback.commands.propose import propose_add, propose_modify, propose_remove
from skills_feedback.commands.rate import rate_skill
from skills_feedback.config import load_repo_config
from skills_feedback.constants import ExitCode
from skills_feedback.models import SkillsFeedbackError, Vote


class Propose:
    """Propose a skill change (add, modify, or remove)."""

    def add(
        self,
        name: str,
        description: str,
        body: str | None = None,
        agent: str = "unknown",
        no_commit: bool = False,
    ) -> None:
        """Propose adding a new skill."""
        repo_root, _ = load_repo_config()
        propose_add(
            repo_root=repo_root,
            name=name,
            description=description,
            body=body,
            agent=agent,
            no_commit=no_commit,
        )

    def modify(
        self,
        name: str,
        reason: str,
        lines: str,
        body: str | None = None,
        agent: str = "unknown",
        no_commit: bool = False,
    ) -> None:
        """Propose modifying an existing skill."""
        repo_root, _ = load_repo_config()
        propose_modify(
            repo_root=repo_root,
            name=name,
            reason=reason,
            lines=lines,
            body=body,
            agent=agent,
            no_commit=no_commit,
        )

    def remove(
        self, name: str, reason: str, agent: str = "unknown", no_commit: bool = False
    ) -> None:
        """Propose removing an existing skill."""
        repo_root, _ = load_repo_config()
        propose_remove(
            repo_root=repo_root, name=name, reason=reason, agent=agent, no_commit=no_commit
        )


class SkillsFeedback:
    """Rate skills, propose changes, and check thresholds."""

    def __init__(self) -> None:
        self.propose = Propose()

    def rate(
        self,
        name: str,
        vote: Vote,
        reason: str,
        lines: str | None = None,
        whole_file: bool = False,
        labels: str | None = None,
        agent: str = "unknown",
        no_commit: bool = False,
    ) -> None:
        """Rate a skill up or down."""
        repo_root, config = load_repo_config()
        parsed_labels = [label.strip() for label in labels.split(",")] if labels else []
        rate_skill(
            repo_root=repo_root,
            config=config,
            name=name,
            vote=vote,
            reason=reason,
            lines=lines,
            whole_file=whole_file,
            labels=parsed_labels,
            agent=agent,
            no_commit=no_commit,
        )

    def check_thresholds(self) -> None:
        """Show skill ratings, status, and proposals dashboard."""
        repo_root, config = load_repo_config()
        print(_check_thresholds(repo_root, config))

    def apply(self, dry_run: bool = False) -> None:
        """Create PRs for proposals that have reached the score threshold."""
        repo_root, config = load_repo_config()
        apply_thresholds(repo_root, config, dry_run=dry_run)

    def version(self) -> None:
        """Print the skills-feedback version."""
        from skills_feedback import __version__

        print(__version__)


def main() -> None:
    try:
        fire.Fire(SkillsFeedback)
    except SkillsFeedbackError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(ExitCode.ERROR)


if __name__ == "__main__":
    main()
