#!/usr/bin/env python3
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_FILE = ROOT / "AGENTS.md"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.+?)\n---", re.DOTALL)
AVAILABLE_SKILLS_SECTION_RE = re.compile(r"(## Available Skills\n)\n.*?(?=\n## |\Z)", re.DOTALL)


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        if value:
            fields[key.strip()] = value.strip().strip('"')
    return fields


def build_skills_xml(root: Path) -> str:
    skills: list[tuple[str, str]] = []
    seen_names: set[str] = set()
    for skill_file in sorted(root.glob("*/SKILL.md")):
        if skill_file.parent.name == "SKILL_TEMPLATE":
            continue
        fm = parse_frontmatter(skill_file)
        name = fm.get("name", "")
        description = fm.get("description", "")
        if name:
            if name in seen_names:
                raise RuntimeError(f"Duplicate skill name in frontmatter: {name} ({skill_file})")
            seen_names.add(name)
            skills.append((name, description))

    lines = ["<available_skills>"]
    for name, description in skills:
        lines.append("  <skill>")
        lines.append(f"    <name>{escape(name)}</name>")
        lines.append(f"    <description>{escape(description)}</description>")
        lines.append("  </skill>")
    lines.append("</available_skills>")
    return "\n".join(lines)


def update_agents_md(agents_file: Path, skills_xml: str) -> None:
    content = agents_file.read_text(encoding="utf-8")
    # Replace from "## Available Skills" up to the next "## " heading
    replacement = rf"\1\n{skills_xml}\n"
    if not AVAILABLE_SKILLS_SECTION_RE.search(content):
        raise RuntimeError("AGENTS.md has no '## Available Skills' section — cannot update")
    new_content = AVAILABLE_SKILLS_SECTION_RE.sub(replacement, content)
    if new_content != content:
        agents_file.write_text(new_content, encoding="utf-8")


def main() -> None:
    skills_xml = build_skills_xml(ROOT)
    update_agents_md(AGENTS_FILE, skills_xml)
    count = skills_xml.count("<skill>")
    print(f"Updated AGENTS.md with {count} skills")


if __name__ == "__main__":
    main()
