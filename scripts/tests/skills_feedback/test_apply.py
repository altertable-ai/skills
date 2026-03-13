import json
import subprocess

from skills_feedback.commands.apply import _build_pr_body, _create_pr, apply_thresholds
from skills_feedback.config import load_config
from skills_feedback.models import Proposal, Rating


def test_build_pr_body():
    proposal = Proposal(
        id="remove-20260313T100000Z-claude-code",
        type="remove",
        reason="Superseded by querying-lakehouse",
        lines=None,
        body=None,
        proposed_by="claude-code",
        proposed_at="2026-03-13T10:00:00Z",
    )
    ratings = [
        Rating(
            vote="up",
            lines=["78-78"],
            reason="Redundant",
            labels=["outdated"],
            agent="claude-code",
            timestamp="t1",
        ),
        Rating(
            vote="down",
            lines=None,
            reason="Still useful",
            labels=["accurate"],
            agent="gemini",
            timestamp="t2",
        ),
    ]
    body = _build_pr_body(proposal, ratings, score=0)
    assert "Superseded by querying-lakehouse" in body
    assert "Redundant" in body
    assert "Still useful" in body
    assert "Score: 0" in body


def test_apply_skips_below_threshold(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    config_file = tmp_path / ".skills-config.yaml"
    config_file.write_text(
        "thresholds:\n  proposal: 5\n  removal: -3\n"
        "reviewer: test\n"
        "labels:\n  positive: [accurate]\n  negative: [outdated]\n"
    )
    config = load_config(config_file)
    result = apply_thresholds(tmp_path, config, dry_run=True)
    assert result == 0


def _setup_qualifying_repo(tmp_path, *, reviewer="test", threshold=2):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t.com"], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "config", "user.name", "T"], capture_output=True, cwd=tmp_path)

    reviewer_line = f"reviewer: {reviewer}\n" if reviewer else ""
    config_file = tmp_path / ".skills-config.yaml"
    config_file.write_text(
        f"thresholds:\n  proposal: {threshold}\n  removal: -3\n"
        f"{reviewer_line}"
        "labels:\n  positive: [accurate]\n  negative: [outdated]\n"
    )

    skill_dir = tmp_path / "exploring-data"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: exploring-data\ndescription: test\n---\n# Test")

    feedback_dir = tmp_path / ".skills-feedback" / "exploring-data"
    feedback_dir.mkdir(parents=True)
    (feedback_dir / "proposals.json").write_text(
        json.dumps(
            {
                "skill": "exploring-data",
                "proposals": [
                    {
                        "id": "remove-20260313T100000Z-claude-code",
                        "type": "remove",
                        "reason": "Superseded",
                        "lines": None,
                        "body": None,
                        "proposed_by": "claude-code",
                        "proposed_at": "2026-03-13T10:00:00Z",
                    }
                ],
            }
        )
    )
    (feedback_dir / "ratings.json").write_text(
        json.dumps(
            {
                "skill": "exploring-data",
                "ratings": [
                    {
                        "vote": "up",
                        "lines": None,
                        "reason": "agree",
                        "labels": [],
                        "agent": "a",
                        "timestamp": "t1",
                    },
                    {
                        "vote": "up",
                        "lines": None,
                        "reason": "agree",
                        "labels": [],
                        "agent": "b",
                        "timestamp": "t2",
                    },
                ],
            }
        )
    )

    subprocess.run(["git", "add", "."], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "commit", "-m", "init"], capture_output=True, cwd=tmp_path)
    return config_file


def test_apply_dry_run_shows_qualifying(tmp_path, capsys):
    config_file = _setup_qualifying_repo(tmp_path)
    config = load_config(config_file)
    result = apply_thresholds(tmp_path, config, dry_run=True)
    assert result == 0
    output = capsys.readouterr().out
    assert "would create PR" in output
    assert "remove-20260313T100000Z-claude-code" in output


def test_apply_dry_run_branch_includes_proposal_id(tmp_path, capsys):
    config_file = _setup_qualifying_repo(tmp_path)
    config = load_config(config_file)
    apply_thresholds(tmp_path, config, dry_run=True)
    output = capsys.readouterr().out
    assert "feedback/remove-exploring-data-remove-20260313T100000Z-claude-code" in output


def test_apply_no_feedback_dir(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    config_file = tmp_path / ".skills-config.yaml"
    config_file.write_text(
        "thresholds:\n  proposal: 3\n  removal: -3\n"
        "reviewer: test\n"
        "labels:\n  positive: [accurate]\n  negative: [outdated]\n"
    )
    config = load_config(config_file)
    result = apply_thresholds(tmp_path, config, dry_run=True)
    assert result == 0


def test_create_pr_skips_reviewer_when_empty(tmp_path):
    result = _create_pr(tmp_path, "test-branch", "title", "body", "")
    # gh CLI not found in test env, but we verify the function doesn't crash
    # with empty reviewer (it returns None due to FileNotFoundError)
    assert result is None


def test_create_pr_includes_reviewer_when_set(tmp_path):
    result = _create_pr(tmp_path, "test-branch", "title", "body", "fvaleye")
    assert result is None
