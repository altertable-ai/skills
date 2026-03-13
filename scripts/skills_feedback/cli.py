from __future__ import annotations

import argparse
import sys
from pathlib import Path

from skills_feedback.commands.apply import apply_thresholds
from skills_feedback.commands.check_thresholds import check_thresholds
from skills_feedback.commands.propose import propose_add, propose_modify, propose_remove
from skills_feedback.commands.rate import rate_skill
from skills_feedback.config import load_config


def _find_repo_root() -> Path:
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".git").exists():
            return parent
    return cwd


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="skills-feedback",
        description="Rate skills, propose changes, and check thresholds.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # propose
    propose_parser = subparsers.add_parser("propose", help="Propose a skill change")
    propose_sub = propose_parser.add_subparsers(dest="propose_command")

    # propose add
    add_parser = propose_sub.add_parser("add", help="Propose a new skill")
    add_parser.add_argument("name", help="Skill name")
    add_parser.add_argument("--description", required=True, help="Why this skill should exist")
    add_parser.add_argument("--body", help="Path to SKILL.md file")
    add_parser.add_argument("--agent", default="unknown", help="Agent identity")
    add_parser.add_argument("--no-commit", action="store_true", help="Stage but do not commit")

    # propose modify
    modify_parser = propose_sub.add_parser("modify", help="Propose a skill modification")
    modify_parser.add_argument("name", help="Skill name")
    modify_parser.add_argument("--reason", required=True, help="Why this change is needed")
    modify_parser.add_argument("--lines", required=True, help="Line ranges (e.g., 45-52,78-81)")
    modify_parser.add_argument("--body", help="Path to modified SKILL.md file")
    modify_parser.add_argument("--agent", default="unknown", help="Agent identity")
    modify_parser.add_argument("--no-commit", action="store_true", help="Stage but do not commit")

    # propose remove
    remove_parser = propose_sub.add_parser("remove", help="Propose a skill removal")
    remove_parser.add_argument("name", help="Skill name")
    remove_parser.add_argument("--reason", required=True, help="Why this skill should be removed")
    remove_parser.add_argument("--agent", default="unknown", help="Agent identity")
    remove_parser.add_argument("--no-commit", action="store_true", help="Stage but do not commit")

    # rate
    rate_parser = subparsers.add_parser("rate", help="Rate a skill")
    rate_parser.add_argument("name", help="Skill name")
    rate_parser.add_argument("vote", choices=["up", "down"], help="Vote direction")
    rate_parser.add_argument("--reason", required=True, help="Why you are rating this way")
    lines_group = rate_parser.add_mutually_exclusive_group(required=True)
    lines_group.add_argument("--lines", help="Line ranges (e.g., 45-52,78-81)")
    lines_group.add_argument("--whole-file", action="store_true", help="Rate the whole file")
    rate_parser.add_argument("--labels", help="Comma-separated labels")
    rate_parser.add_argument("--agent", default="unknown", help="Agent identity")
    rate_parser.add_argument("--no-commit", action="store_true", help="Stage but do not commit")

    # check-thresholds
    subparsers.add_parser("check-thresholds", help="Show skill ratings and proposals")

    # apply
    apply_parser = subparsers.add_parser("apply", help="Create PRs for qualifying proposals")
    apply_parser.add_argument("--dry-run", action="store_true", help="Show what would happen")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    repo_root = _find_repo_root()
    config_path = repo_root / ".skills-config.yaml"

    if args.command == "propose":
        if args.propose_command is None:
            propose_parser.print_help()
            sys.exit(0)

        config = load_config(config_path)

        if args.propose_command == "add":
            sys.exit(
                propose_add(
                    repo_root=repo_root,
                    name=args.name,
                    description=args.description,
                    body=args.body,
                    agent=args.agent,
                    no_commit=args.no_commit,
                )
            )
        elif args.propose_command == "modify":
            sys.exit(
                propose_modify(
                    repo_root=repo_root,
                    name=args.name,
                    reason=args.reason,
                    lines=args.lines,
                    body=args.body,
                    agent=args.agent,
                    no_commit=args.no_commit,
                )
            )
        elif args.propose_command == "remove":
            sys.exit(
                propose_remove(
                    repo_root=repo_root,
                    name=args.name,
                    reason=args.reason,
                    agent=args.agent,
                    no_commit=args.no_commit,
                )
            )

    elif args.command == "rate":
        config = load_config(config_path)
        labels = [label.strip() for label in args.labels.split(",")] if args.labels else []
        sys.exit(
            rate_skill(
                repo_root=repo_root,
                config=config,
                name=args.name,
                vote=args.vote,
                reason=args.reason,
                lines=args.lines,
                whole_file=args.whole_file,
                labels=labels,
                agent=args.agent,
                no_commit=args.no_commit,
            )
        )

    elif args.command == "check-thresholds":
        config = load_config(config_path)
        sys.exit(check_thresholds(repo_root, config))

    elif args.command == "apply":
        config = load_config(config_path)
        sys.exit(apply_thresholds(repo_root, config, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
