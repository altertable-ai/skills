import json

import pytest
from skills_feedback.commands.propose import _copy_body, propose_add, propose_modify, propose_remove
from skills_feedback.models import SkillsFeedbackError


def test_propose_add_creates_proposal(repo):
    propose_add(
        repo_root=repo,
        name="testing-skills",
        description="A new testing skill",
        body=None,
        agent="claude-code",
        no_commit=True,
    )
    proposals_path = repo / ".skills-feedback" / "testing-skills" / "proposals.json"
    assert proposals_path.exists()
    data = json.loads(proposals_path.read_text())
    assert data["skill"] == "testing-skills"
    assert len(data["proposals"]) == 1
    assert data["proposals"][0]["type"] == "add"
    assert data["proposals"][0]["reason"] == "A new testing skill"


def test_propose_add_rejects_existing_skill(repo):
    skill_dir = repo / "testing-skills"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: testing-skills\ndescription: test\n---\n# Test")
    with pytest.raises(SkillsFeedbackError, match="already exists"):
        propose_add(
            repo_root=repo,
            name="testing-skills",
            description="dup",
            body=None,
            agent="test",
            no_commit=True,
        )


def test_propose_add_rejects_invalid_name(repo):
    with pytest.raises(SkillsFeedbackError):
        propose_add(
            repo_root=repo,
            name="Invalid-Name",
            description="test",
            body=None,
            agent="test",
            no_commit=True,
        )


def test_propose_modify_creates_proposal(repo_with_skill):
    propose_modify(
        repo_root=repo_with_skill,
        name="analyzing-charts",
        reason="Missing empty dataset guidance",
        lines="78-78",
        body=None,
        agent="claude-code",
        no_commit=True,
    )
    proposals_path = repo_with_skill / ".skills-feedback" / "analyzing-charts" / "proposals.json"
    data = json.loads(proposals_path.read_text())
    assert data["proposals"][0]["type"] == "modify"
    assert data["proposals"][0]["lines"] == ["78-78"]


def test_propose_modify_rejects_nonexistent_skill(repo):
    with pytest.raises(SkillsFeedbackError, match="does not exist"):
        propose_modify(
            repo_root=repo,
            name="nonexistent",
            reason="test",
            lines="1-1",
            body=None,
            agent="test",
            no_commit=True,
        )


def test_propose_add_with_body(repo, tmp_path):
    body_file = tmp_path / "new-skill.md"
    body_file.write_text("---\nname: new-skill\ndescription: test\n---\n# New Skill")
    propose_add(
        repo_root=repo,
        name="new-skill",
        description="A new skill with body",
        body=str(body_file),
        agent="test",
        no_commit=True,
    )
    bodies_dir = repo / ".skills-feedback" / "new-skill" / "bodies"
    assert bodies_dir.exists()
    body_files = list(bodies_dir.iterdir())
    assert len(body_files) == 1
    assert "New Skill" in body_files[0].read_text()


def test_propose_modify_with_body(repo_with_skill, tmp_path):
    body_file = tmp_path / "updated.md"
    body_file.write_text("---\nname: analyzing-charts\ndescription: updated\n---\n# Updated")
    propose_modify(
        repo_root=repo_with_skill,
        name="analyzing-charts",
        reason="section rewrite",
        lines="1-5",
        body=str(body_file),
        agent="test",
        no_commit=True,
    )
    bodies_dir = repo_with_skill / ".skills-feedback" / "analyzing-charts" / "bodies"
    assert bodies_dir.exists()


def test_propose_modify_rejects_invalid_lines(repo_with_skill):
    with pytest.raises(SkillsFeedbackError):
        propose_modify(
            repo_root=repo_with_skill,
            name="analyzing-charts",
            reason="test",
            lines="invalid",
            body=None,
            agent="test",
            no_commit=True,
        )


def test_propose_remove_creates_proposal(repo):
    skill_dir = repo / "exploring-data"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: exploring-data\ndescription: test\n---\n# Test")
    propose_remove(
        repo_root=repo,
        name="exploring-data",
        reason="Superseded by querying-lakehouse",
        agent="claude-code",
        no_commit=True,
    )
    proposals_path = repo / ".skills-feedback" / "exploring-data" / "proposals.json"
    data = json.loads(proposals_path.read_text())
    assert data["proposals"][0]["type"] == "remove"


def test_copy_body_raises_for_missing_file(tmp_path):
    with pytest.raises(SkillsFeedbackError, match="not found"):
        _copy_body(tmp_path, "test-id", "/no/such/file.md")
