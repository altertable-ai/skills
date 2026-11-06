import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"


def _body(skill: str) -> str:
    text = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
    return text.split("---", 2)[2]


def _sql_blocks(body: str) -> list[str]:
    return re.findall(r"```sql\n(.*?)```", body, flags=re.DOTALL)


def test_query_skill_treats_a_truncated_result_as_a_preview_not_a_page_to_fetch():
    body = _body("query-altertable")

    assert "repeat the same statement with the returned offset" not in body
    assert "preview, not the population" in body
    assert "aggregate, narrow, or project instead of paging" in body


def test_query_skill_routes_full_exports_to_the_cli_instead_of_the_conversation():
    body = _body("query-altertable")

    assert "count(*)" in body
    assert "altertable query --format csv --output" in body


def test_opentelemetry_examples_project_columns_on_wide_tables():
    blocks = _sql_blocks(_body("investigate-opentelemetry"))

    assert blocks
    assert not [block for block in blocks if re.search(r"SELECT\s+\*", block, flags=re.IGNORECASE)]
    assert any("GROUP BY" in block for block in blocks)
