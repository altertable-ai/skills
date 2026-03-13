import json

from skills_feedback.commands.propose import propose_add, propose_modify, propose_remove


def test_propose_add_creates_proposal(repo):
    result = propose_add(
        repo_root=repo,
        name="testing-skills",
        description="A new testing skill",
        body=None,
        agent="claude-code",
        no_commit=True,
    )
    assert result == 0
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
    result = propose_add(
        repo_root=repo,
        name="testing-skills",
        description="dup",
        body=None,
        agent="test",
        no_commit=True,
    )
    assert result == 1


def test_propose_add_rejects_invalid_name(repo):
    result = propose_add(
        repo_root=repo,
        name="Invalid-Name",
        description="test",
        body=None,
        agent="test",
        no_commit=True,
    )
    assert result == 1


def test_propose_modify_creates_proposal(repo_with_skill):
    result = propose_modify(
        repo_root=repo_with_skill,
        name="analyzing-charts",
        reason="Missing empty dataset guidance",
        lines="78-78",
        body=None,
        agent="claude-code",
        no_commit=True,
    )
    assert result == 0
    proposals_path = repo_with_skill / ".skills-feedback" / "analyzing-charts" / "proposals.json"
    data = json.loads(proposals_path.read_text())
    assert data["proposals"][0]["type"] == "modify"
    assert data["proposals"][0]["lines"] == ["78-78"]


def test_propose_modify_rejects_nonexistent_skill(repo):
    result = propose_modify(
        repo_root=repo,
        name="nonexistent",
        reason="test",
        lines="1-1",
        body=None,
        agent="test",
        no_commit=True,
    )
    assert result == 1


def test_propose_remove_creates_proposal(repo):
    skill_dir = repo / "exploring-data"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: exploring-data\ndescription: test\n---\n# Test")

    result = propose_remove(
        repo_root=repo,
        name="exploring-data",
        reason="Superseded by querying-lakehouse",
        agent="claude-code",
        no_commit=True,
    )
    assert result == 0
    proposals_path = repo / ".skills-feedback" / "exploring-data" / "proposals.json"
    data = json.loads(proposals_path.read_text())
    assert data["proposals"][0]["type"] == "remove"
