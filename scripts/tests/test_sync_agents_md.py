import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parent.parent / "sync-agents-md.py"


@pytest.fixture(scope="module")
def sync():
    spec = importlib.util.spec_from_file_location("sync_agents_md", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_skills_table_uses_the_first_sentence(sync):
    # given
    skills = [("query-lakehouse", "Runs DuckDB SQL. Use when a question needs a query.")]

    # when
    table = sync.build_skills_table(skills)

    # then
    assert "| [query-lakehouse](skills/query-lakehouse/) | Runs DuckDB SQL |" in table
    assert "Use when" not in table


def test_build_skills_table_escapes_pipes_so_rows_stay_intact(sync):
    # given
    skills = [("explore-data", "Inspects tables | views. Use to find data.")]

    # when
    table = sync.build_skills_table(skills)

    # then
    assert r"Inspects tables \| views" in table
    assert len(table.splitlines()) == 3
