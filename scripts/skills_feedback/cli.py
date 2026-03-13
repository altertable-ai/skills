from __future__ import annotations

import sys

import fire

from skills_feedback.commands.apply import apply_thresholds
from skills_feedback.commands.check_thresholds import check_thresholds as _check_thresholds
from skills_feedback.commands.propose import propose_add, propose_modify, propose_remove
from skills_feedback.commands.rate import rate_skill
from skills_feedback.config import load_repo_config
from skills_feedback.models import Vote


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
        """Propose adding a new skill.

        Args:
            name: Skill name (lowercase, hyphen-separated).
            description: Why this skill should exist.
            body: Path to a SKILL.md file for the proposed skill.
            agent: Identity of the agent making the proposal.
            no_commit: Stage changes but do not commit.
        """
        repo_root, _ = load_repo_config()
        sys.exit(
            propose_add(
                repo_root=repo_root,
                name=name,
                description=description,
                body=body,
                agent=agent,
                no_commit=no_commit,
            )
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
        """Propose modifying an existing skill.

        Args:
            name: Skill name to modify.
            reason: Why this change is needed.
            lines: Line ranges to modify (e.g., '45-52,78-81').
            body: Path to a modified SKILL.md file.
            agent: Identity of the agent making the proposal.
            no_commit: Stage changes but do not commit.
        """
        repo_root, _ = load_repo_config()
        sys.exit(
            propose_modify(
                repo_root=repo_root,
                name=name,
                reason=reason,
                lines=lines,
                body=body,
                agent=agent,
                no_commit=no_commit,
            )
        )

    def remove(
        self,
        name: str,
        reason: str,
        agent: str = "unknown",
        no_commit: bool = False,
    ) -> None:
        """Propose removing an existing skill.

        Args:
            name: Skill name to remove.
            reason: Why this skill should be removed.
            agent: Identity of the agent making the proposal.
            no_commit: Stage changes but do not commit.
        """
        repo_root, _ = load_repo_config()
        sys.exit(
            propose_remove(
                repo_root=repo_root,
                name=name,
                reason=reason,
                agent=agent,
                no_commit=no_commit,
            )
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
        """Rate a skill up or down.

        Args:
            name: Skill name to rate.
            vote: Vote direction ('up' or 'down').
            reason: Why you are rating this way.
            lines: Line ranges (e.g., '45-52,78-81'). Required unless whole_file is set.
            whole_file: Rate the entire file instead of specific lines.
            labels: Comma-separated labels (e.g., 'accurate,helpful').
            agent: Identity of the agent rating.
            no_commit: Stage changes but do not commit.
        """
        repo_root, config = load_repo_config()
        parsed_labels = [label.strip() for label in labels.split(",")] if labels else []
        sys.exit(
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
        )

    def check_thresholds(self) -> None:
        """Show skill ratings, status, and proposals dashboard."""
        repo_root, config = load_repo_config()
        sys.exit(_check_thresholds(repo_root, config))

    def apply(self, dry_run: bool = False) -> None:
        """Create PRs for proposals that have reached the score threshold.

        Args:
            dry_run: Show what would happen without creating PRs.
        """
        repo_root, config = load_repo_config()
        sys.exit(apply_thresholds(repo_root, config, dry_run=dry_run))

    def version(self) -> None:
        """Print the skills-feedback version."""
        from skills_feedback import __version__

        print(__version__)


def main() -> None:
    """Entry point for the skills-feedback CLI."""
    fire.Fire(SkillsFeedback)


if __name__ == "__main__":
    main()
