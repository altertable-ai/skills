#!/usr/bin/env python3
import re
from html import escape
from pathlib import Path
from typing import Any

import yaml
from scorer.models import SKILLS_DIR as _SKILLS_DIR_NAME
from scorer.models import VALID_REQUIRES

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / _SKILLS_DIR_NAME
AGENTS_FILE = ROOT / "AGENTS.md"
README_FILE = ROOT / "README.md"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.+?)\n---", re.DOTALL)
AVAILABLE_SKILLS_SECTION_RE = re.compile(r"(## Available Skills\n)\n.*?(?=\n## |\Z)", re.DOTALL)


def parse_frontmatter(skill_file: Path) -> dict[str, Any]:
    text = skill_file.read_text(encoding="utf-8")
    frontmatter_match = FRONTMATTER_RE.match(text)
    if not frontmatter_match:
        return {}
    parsed = yaml.safe_load(frontmatter_match.group(1))
    return parsed if isinstance(parsed, dict) else {}


def collect_skills(skills_dir: Path) -> list[tuple[str, str]]:
    skills: list[tuple[str, str]] = []
    seen_names: set[str] = set()
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        fm = parse_frontmatter(skill_file)
        name = fm.get("name", "")
        description = fm.get("description", "")
        if name:
            if name in seen_names:
                raise RuntimeError(f"Duplicate skill name in frontmatter: {name} ({skill_file})")
            seen_names.add(name)
            requires_raw = fm.get("metadata", {}).get("requires", "")
            requires = (
                {r.strip() for r in requires_raw.split(",") if r.strip()} if requires_raw else set()
            )
            invalid = requires - VALID_REQUIRES
            if invalid:
                raise RuntimeError(
                    f"Invalid metadata.requires in {skill_file}: {invalid}. "
                    f"Valid values: {sorted(VALID_REQUIRES)}"
                )
            skills.append((name, description))

    return skills


def build_skills_xml(skills: list[tuple[str, str]]) -> str:
    lines = ["<available_skills>"]
    for name, description in skills:
        lines.append("  <skill>")
        lines.append(f"    <name>{escape(name)}</name>")
        lines.append(f"    <description>{escape(description)}</description>")
        lines.append("  </skill>")
    lines.append("</available_skills>")
    return "\n".join(lines)


def build_skills_table(skills: list[tuple[str, str]]) -> str:
    lines = ["| Skill | Description |", "| ----- | ----------- |"]
    for name, description in skills:
        summary = description.split(". ")[0].rstrip(".").replace("|", r"\|")
        lines.append(f"| [{name}](skills/{name}/) | {summary} |")
    return "\n".join(lines)


def update_available_skills(target: Path, block: str) -> None:
    content = target.read_text(encoding="utf-8")
    # Replace from "## Available Skills" up to the next "## " heading
    if not AVAILABLE_SKILLS_SECTION_RE.search(content):
        raise RuntimeError(f"{target.name} has no '## Available Skills' section — cannot update")
    new_content = AVAILABLE_SKILLS_SECTION_RE.sub(rf"\1\n{block}\n", content)
    if new_content != content:
        target.write_text(new_content, encoding="utf-8")


def main() -> None:
    skills = collect_skills(SKILLS_DIR)
    update_available_skills(AGENTS_FILE, build_skills_xml(skills))
    update_available_skills(README_FILE, build_skills_table(skills))
    print(f"Updated AGENTS.md and README.md with {len(skills)} skills")


if __name__ == "__main__":
    main()
