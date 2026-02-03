from typing import Final

from .models import DEFAULT_MIN_SCORE, ScoreResult

MAX_PR_ISSUES: Final[int] = 5
MAX_CLI_ISSUES: Final[int] = 10
MAX_SUGGESTIONS: Final[int] = 3
PROGRESS_BAR_WIDTH: Final[int] = 10
SEPARATOR_WIDTH: Final[int] = 50

CATEGORY_MAX_SCORES: Final[dict[str, int]] = {
    "frontmatter": 20,
    "structure": 25,
    "content_quality": 35,
    "pitfalls": 10,
    "references": 10,
}

SEVERITY_ICONS: Final[dict[str, str]] = {
    "critical": "X",
    "major": "!",
    "minor": "-",
}

SEVERITY_ICONS_GITHUB: Final[dict[str, str]] = {
    "critical": ":red_circle:",
    "major": ":orange_circle:",
    "minor": ":yellow_circle:",
}


def format_pr_comment(results: list[ScoreResult], min_score: int = DEFAULT_MIN_SCORE) -> str:
    lines = ["## Skill Quality Report", ""]
    lines.append("| Skill | Score | Status |")
    lines.append("|-------|-------|--------|")

    for result in results:
        status = ":white_check_mark:" if result.score >= min_score else ":x:"
        lines.append(f"| `{result.skill_name}` | **{result.score}**/100 | {status} |")

    lines.append("")

    for result in results:
        if result.issues:
            lines.append(f"<details><summary>{result.skill_name} issues</summary>")
            lines.append("")
            for issue in result.issues[:MAX_PR_ISSUES]:
                icon = SEVERITY_ICONS_GITHUB.get(issue.severity, "")
                lines.append(f"- {icon} {issue.message}")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    judge_name = results[0].judge_name if results else "N/A"
    lines.append(f"*Threshold: {min_score} | Judge: {judge_name}*")

    return "\n".join(lines)


def format_cli(result: ScoreResult, verbose: bool = False) -> str:
    lines = [
        f"{'=' * SEPARATOR_WIDTH}",
        f"Skill: {result.skill_name}",
        f"Score: {result.score}/100",
        f"Judge: {result.judge_name}",
        "",
        "Breakdown:",
    ]

    for category, max_points in CATEGORY_MAX_SCORES.items():
        points = getattr(result.breakdown, category, 0)
        filled = int(points / max_points * PROGRESS_BAR_WIDTH)
        bar = "#" * filled + "-" * (PROGRESS_BAR_WIDTH - filled)
        lines.append(f"  {category:18} [{bar}] {points}/{max_points}")

    if result.issues:
        lines.append("")
        lines.append("Issues:")
        for issue in result.issues[:MAX_CLI_ISSUES]:
            icon = SEVERITY_ICONS.get(issue.severity, "-")
            lines.append(f"  [{icon}] {issue.message}")

    if verbose and result.suggestions:
        lines.append("")
        lines.append("Suggestions:")
        for suggestion in result.suggestions[:MAX_SUGGESTIONS]:
            lines.append(f"  * {suggestion}")

    return "\n".join(lines)
