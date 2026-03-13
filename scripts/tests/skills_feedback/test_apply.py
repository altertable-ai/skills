import json
import subprocess

from skills_feedback.commands.apply import (
    QualifiedSkill,
    _apply_proposal,
    _build_pr_body,
    _check_existing_pr,
    _cleanup,
    _collect_qualifying,
    _create_pr,
    apply_thresholds,
)
from skills_feedback.config import load_config
from skills_feedback.constants import SKILL_FILENAME
from skills_feedback.models import (
    Proposal,
    ProposalsFile,
    ProposalType,
    Rating,
    Vote,
)


def test_build_pr_body():
    proposal = Proposal(
        id="remove-20260313T100000Z-claude-code",
        type=ProposalType.REMOVE,
        reason="Superseded by querying-lakehouse",
        lines=None,
        body=None,
        proposed_by="claude-code",
        proposed_at="2026-03-13T10:00:00Z",
    )
    ratings = [
        Rating(
            vote=Vote.UP,
            lines=["78-78"],
            reason="Redundant",
            labels=["outdated"],
            agent="claude-code",
            timestamp="t1",
        ),
        Rating(
            vote=Vote.DOWN,
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
    subprocess.run(["git", "config", "commit.gpgsign", "false"], capture_output=True, cwd=tmp_path)

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
                        "vote": "down",
                        "lines": None,
                        "reason": "outdated",
                        "labels": [],
                        "agent": "a",
                        "timestamp": "t1",
                    },
                    {
                        "vote": "down",
                        "lines": None,
                        "reason": "superseded",
                        "labels": [],
                        "agent": "b",
                        "timestamp": "t2",
                    },
                    {
                        "vote": "down",
                        "lines": None,
                        "reason": "redundant",
                        "labels": [],
                        "agent": "c",
                        "timestamp": "t3",
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
    assert result is None


def test_create_pr_includes_reviewer_when_set(tmp_path):
    result = _create_pr(tmp_path, "test-branch", "title", "body", "fvaleye")
    assert result is None


def test_apply_add_copies_body_to_skill_dir(tmp_path):
    feedback_dir = tmp_path / "feedback"
    feedback_dir.mkdir()
    body_content = "---\nname: new-skill\n---\n# New Skill"
    (feedback_dir / "body.md").write_text(body_content)

    skill_dir = tmp_path / "new-skill"
    proposal = Proposal(
        id="add-001",
        type=ProposalType.ADD,
        reason="test",
        lines=None,
        body="body.md",
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    _apply_proposal(proposal, feedback_dir, skill_dir)
    assert (skill_dir / SKILL_FILENAME).read_text() == body_content
    assert (skill_dir / "references").is_dir()


def test_apply_add_returns_error_without_body(tmp_path):
    proposal = Proposal(
        id="add-001",
        type=ProposalType.ADD,
        reason="test",
        lines=None,
        body=None,
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    error = _apply_proposal(proposal, tmp_path, tmp_path / "skill")
    assert error and "no body" in error


def test_apply_modify_copies_body(tmp_path):
    feedback_dir = tmp_path / "feedback"
    feedback_dir.mkdir()
    (feedback_dir / "updated.md").write_text("# Updated")

    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (skill_dir / SKILL_FILENAME).write_text("# Original")

    proposal = Proposal(
        id="modify-001",
        type=ProposalType.MODIFY,
        reason="test",
        lines=["1-5"],
        body="updated.md",
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    _apply_proposal(proposal, feedback_dir, skill_dir)
    assert (skill_dir / SKILL_FILENAME).read_text() == "# Updated"


def test_apply_modify_returns_error_without_body(tmp_path):
    proposal = Proposal(
        id="modify-001",
        type=ProposalType.MODIFY,
        reason="test",
        lines=["1-5"],
        body=None,
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    error = _apply_proposal(proposal, tmp_path, tmp_path / "skill")
    assert error and "no body" in error


def test_apply_remove_deletes_skill_dir(tmp_path):
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / SKILL_FILENAME).write_text("# Test")
    proposal = Proposal(
        id="remove-001",
        type=ProposalType.REMOVE,
        reason="test",
        lines=None,
        body=None,
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    _apply_proposal(proposal, tmp_path, skill_dir)
    assert not skill_dir.exists()


def test_apply_remove_noop_when_missing(tmp_path):
    skill_dir = tmp_path / "nonexistent"
    proposal = Proposal(
        id="remove-001",
        type=ProposalType.REMOVE,
        reason="test",
        lines=None,
        body=None,
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    _apply_proposal(proposal, tmp_path, skill_dir)
    assert not skill_dir.exists()


def test_cleanup_removes_entry_and_resets_ratings(tmp_path):
    feedback_dir = tmp_path / "feedback"
    feedback_dir.mkdir()
    ppath = feedback_dir / "proposals.json"
    rpath = feedback_dir / "ratings.json"
    rpath.write_text(json.dumps({"skill": "test", "ratings": []}))

    proposal = Proposal(
        id="remove-001",
        type=ProposalType.REMOVE,
        reason="test",
        lines=None,
        body=None,
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    proposals_file = ProposalsFile(skill="test", proposals=[proposal])
    skill = QualifiedSkill(
        name="test",
        feedback_dir=feedback_dir,
        proposals_file=proposals_file,
        proposal=proposal,
        ppath=ppath,
        rpath=rpath,
        score=0,
        ratings=[],
    )

    _cleanup(skill)

    loaded_proposals = json.loads(ppath.read_text())
    assert len(loaded_proposals["proposals"]) == 0
    loaded_ratings = json.loads(rpath.read_text())
    assert len(loaded_ratings["ratings"]) == 0


def test_cleanup_deletes_body_file(tmp_path):
    feedback_dir = tmp_path / "feedback"
    feedback_dir.mkdir()
    body_file = feedback_dir / "body.md"
    body_file.write_text("content")
    ppath = feedback_dir / "proposals.json"
    rpath = feedback_dir / "ratings.json"

    proposal = Proposal(
        id="add-001",
        type=ProposalType.ADD,
        reason="test",
        lines=None,
        body="body.md",
        proposed_by="test",
        proposed_at="2026-01-01T00:00:00Z",
    )
    proposals_file = ProposalsFile(skill="test", proposals=[proposal])
    skill = QualifiedSkill(
        name="test",
        feedback_dir=feedback_dir,
        proposals_file=proposals_file,
        proposal=proposal,
        ppath=ppath,
        rpath=rpath,
        score=0,
        ratings=[],
    )

    _cleanup(skill)
    assert not body_file.exists()


def test_check_existing_pr_returns_none_without_gh(tmp_path):
    result = _check_existing_pr(tmp_path, "nonexistent-branch")
    assert result is None


def test_collect_qualifying_empty_when_no_feedback(tmp_path):
    config_file = _setup_qualifying_repo(tmp_path, threshold=999)
    config_file.write_text(
        "thresholds:\n  proposal: 999\n  removal: -999\n"
        "reviewer: test\n"
        "labels:\n  positive: [accurate]\n  negative: [outdated]\n"
    )
    config = load_config(config_file)
    assert _collect_qualifying(tmp_path, config) == []


def test_collect_qualifying_returns_matching(tmp_path):
    config_file = _setup_qualifying_repo(tmp_path)
    config = load_config(config_file)
    result = _collect_qualifying(tmp_path, config)
    assert len(result) == 1
    assert result[0].name == "exploring-data"
    assert result[0].score == -3
    assert result[0].proposal.type == ProposalType.REMOVE


def test_collect_qualifying_skips_remove_with_positive_score(tmp_path):
    config_file = _setup_qualifying_repo(tmp_path, threshold=2)
    config = load_config(config_file)
    feedback_dir = tmp_path / ".skills-feedback" / "exploring-data"
    (feedback_dir / "ratings.json").write_text(
        json.dumps(
            {
                "skill": "exploring-data",
                "ratings": [
                    {
                        "vote": "up",
                        "lines": None,
                        "reason": "good",
                        "labels": [],
                        "agent": "a",
                        "timestamp": "t1",
                    },
                    {
                        "vote": "up",
                        "lines": None,
                        "reason": "good",
                        "labels": [],
                        "agent": "b",
                        "timestamp": "t2",
                    },
                ],
            }
        )
    )
    subprocess.run(["git", "add", "."], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "commit", "-m", "update"], capture_output=True, cwd=tmp_path)
    assert _collect_qualifying(tmp_path, config) == []
