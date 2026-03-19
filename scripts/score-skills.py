import asyncio
import json
import sys
from pathlib import Path

import fire
from skills_cli.cli import validate as validate_skill

SKILL_FILENAME = "SKILL.md"


def score(
    *paths: str,
    min_score: int = 70,
    json_output: bool = False,
    pr_comment: bool = False,
    scan_all: bool = False,
    verbose: bool = False,
    validate_only: bool = False,
    model: str | None = None,
) -> None:
    """Score skills using LLM judge.

    Args:
        paths: Skill directories to score
        min_score: Minimum passing score (default: 70)
        json_output: Output raw JSON
        pr_comment: Output GitHub PR comment format
        scan_all: Score all skills in directory
        verbose: Show suggestions
        validate_only: Run validation only, no LLM scoring
        model: LLM model (default: gemini/gemini-3.1-pro-preview)
    """
    skill_paths: list[Path] = []
    for path_str in paths:
        skill_path = Path(path_str)
        if scan_all and skill_path.is_dir():
            for subdir in sorted(skill_path.iterdir()):
                is_valid = (
                    subdir.is_dir()
                    and (subdir / SKILL_FILENAME).exists()
                    and subdir.name != "SKILL_TEMPLATE"
                )
                if is_valid:
                    skill_paths.append(subdir)
        elif skill_path.is_dir() and (skill_path / SKILL_FILENAME).exists():
            skill_paths.append(skill_path)

    if not skill_paths:
        print("No valid skill directories found", file=sys.stderr)
        sys.exit(1)

    validation_failed = False
    for skill_path in skill_paths:
        errors = validate_skill(skill_path)
        if errors:
            validation_failed = True
            print(f"Validation failed: {skill_path.name}", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)

    if validate_only:
        if not validation_failed:
            print("All skills valid!")
        sys.exit(1 if validation_failed else 0)

    if validation_failed:
        print("Skipping LLM scoring due to validation errors", file=sys.stderr)
        sys.exit(1)

    from scorer import fetch_spec_context, format_cli, format_pr_comment, score_batch

    try:
        spec_context = fetch_spec_context()
    except Exception as e:
        print(f"Error fetching spec: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        results = asyncio.run(score_batch(skill_paths, spec_context, model))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps([result.model_dump() for result in results], indent=2))
    elif pr_comment:
        print(format_pr_comment(results, min_score))
    else:
        for result in results:
            print(format_cli(result, verbose))
            print()

    passed = all(result.score >= min_score for result in results)
    sys.exit(0 if passed else 1)


def main():
    fire.Fire(score)


if __name__ == "__main__":
    main()
