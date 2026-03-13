import json

from skills_feedback.commands.propose import _copy_body, propose_add, propose_modify, propose_remove


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
    proposal = data["proposals"][0]
    assert proposal["type"] == "add"
    assert proposal["reason"] == "A new testing skill"


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
    proposal = data["proposals"][0]
    assert proposal["type"] == "modify"
    assert proposal["lines"] == ["78-78"]


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


def test_propose_add_with_body(repo, tmp_path):
    body_file = tmp_path / "new-skill.md"
    body_file.write_text("---\nname: new-skill\ndescription: test\n---\n# New Skill")
    result = propose_add(
        repo_root=repo,
        name="new-skill",
        description="A new skill with body",
        body=str(body_file),
        agent="test",
        no_commit=True,
    )
    assert result == 0
    bodies_dir = repo / ".skills-feedback" / "new-skill" / "bodies"
    assert bodies_dir.exists()
    body_files = list(bodies_dir.iterdir())
    assert len(body_files) == 1
    assert "New Skill" in body_files[0].read_text()


def test_propose_modify_with_body(repo_with_skill, tmp_path):
    body_file = tmp_path / "updated.md"
    body_file.write_text("---\nname: analyzing-charts\ndescription: updated\n---\n# Updated")
    result = propose_modify(
        repo_root=repo_with_skill,
        name="analyzing-charts",
        reason="section rewrite",
        lines="1-5",
        body=str(body_file),
        agent="test",
        no_commit=True,
    )
    assert result == 0
    bodies_dir = repo_with_skill / ".skills-feedback" / "analyzing-charts" / "bodies"
    assert bodies_dir.exists()


def test_propose_modify_rejects_invalid_lines(repo_with_skill):
    result = propose_modify(
        repo_root=repo_with_skill,
        name="analyzing-charts",
        reason="test",
        lines="invalid",
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
    proposal = data["proposals"][0]
    assert proposal["type"] == "remove"


def test_copy_body_returns_none_for_missing_file(tmp_path):
    result = _copy_body(tmp_path, "test-id", "/no/such/file.md")
    assert result is None
