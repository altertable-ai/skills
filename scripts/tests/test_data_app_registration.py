from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_hosted_app_creation_and_updates_submit_complete_registration():
    text = (ROOT / "skills/build-data-app/SKILL.md").read_text()
    for requirement in (
        "queries.json",
        "variables.json",
        "variable list",
        "both `create_data_app` and `update_data_app`",
        "complete replacement",
        "same app revision",
        "SQL",
        "docs/contract.md",
    ):
        assert requirement in text


def test_local_app_workflow_uses_the_hosted_query_contract():
    text = (ROOT / "skills/build-local-data-app/SKILL.md").read_text()
    for requirement in (
        "variable list",
        "`query(id, values)`",
        "queries.json",
        "variables.json",
        "CLI proxy",
        "iframe",
        "postMessage",
    ):
        assert requirement in text
