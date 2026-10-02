from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_hosted_app_creation_and_updates_submit_complete_registration():
    text = (ROOT / "skills/build-data-app/SKILL.md").read_text()
    for requirement in (
        "getDataAppRegistration()",
        "`queries` and `variables`",
        "both `create_data_app` and `update_data_app`",
        "complete replacement",
        "same app revision",
        "docs/contract.md",
    ):
        assert requirement in text


def test_local_app_workflow_preserves_statement_execution():
    text = (ROOT / "skills/build-local-data-app/SKILL.md").read_text()
    assert "arbitrary SQL statements" in text
    assert "registration" in text
