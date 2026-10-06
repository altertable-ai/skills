from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_hosted_app_creation_and_updates_submit_complete_registration():
    text = (ROOT / "skills/build-data-app/SKILL.md").read_text()
    for requirement in (
        "queries.json",
        "variables.json",
        "both `create_data_app` and `update_data_app`",
        "complete replacement",
        "same app revision",
        "empty collections",
        "existing source and registration",
        "integration blocker",
        "SQL",
        "docs/contract.md",
    ):
        assert requirement in text


def test_local_app_keeps_server_operations_without_registration():
    text = (ROOT / "skills/build-local-data-app/SKILL.md").read_text()
    assert "queries.json" not in text
    assert "variables.json" not in text
    assert "upstream instructions" in text
    assert "check inputs" in text
    assert "actual operations" in text
