#!/usr/bin/env bash
# Regenerates the <available_skills> block in AGENTS.md from SKILL.md frontmatters.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_FILE="$ROOT/AGENTS.md"
TMPFILE=$(mktemp)

# Build the XML block
{
  echo "<available_skills>"
  for skill_file in "$ROOT"/*/SKILL.md; do
    dir="$(basename "$(dirname "$skill_file")")"
    [ "$dir" = "SKILL_TEMPLATE" ] && continue

    name=""
    description=""
    in_frontmatter=false

    while IFS= read -r line; do
      if [ "$line" = "---" ]; then
        if $in_frontmatter; then break; fi
        in_frontmatter=true
        continue
      fi
      if $in_frontmatter; then
        case "$line" in
          name:*) name="${line#name: }" ;;
          description:*) description="${line#description: }" ;;
        esac
      fi
    done < "$skill_file"

    # Strip surrounding quotes
    description="${description#\"}"
    description="${description%\"}"

    echo "  <skill>"
    echo "    <name>$name</name>"
    echo "    <description>$description</description>"
    echo "  </skill>"
  done
  echo "</available_skills>"
} > "$TMPFILE"

# Replace section: remove from "## Available Skills" up to (but not including) the next "## " heading
awk -v blockfile="$TMPFILE" '
  /^## Available Skills/ {
    print "## Available Skills"
    print ""
    while ((getline line < blockfile) > 0) print line
    print ""
    skip = 1
    next
  }
  skip && /^## / { skip = 0 }
  !skip { print }
' "$AGENTS_FILE" > "$AGENTS_FILE.tmp"

mv "$AGENTS_FILE.tmp" "$AGENTS_FILE"
rm -f "$TMPFILE"

count=$(grep -c '<skill>' "$AGENTS_FILE")
echo "Updated AGENTS.md with $count skills"
