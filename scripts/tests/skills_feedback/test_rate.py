import json

from skills_feedback.commands.rate import rate_skill
from skills_feedback.config import load_config


def test_rate_up_creates_rating(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote="up",
        reason="Good content",
        lines="45-52",
        whole_file=False,
        labels=[],
        agent="claude-code",
        no_commit=True,
    )
    assert result == 0
    ratings_path = repo_with_skill / ".skills-feedback" / "analyzing-charts" / "ratings.json"
    data = json.loads(ratings_path.read_text())
    assert data["ratings"][0]["vote"] == "up"


def test_rate_down_creates_rating(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote="down",
        reason="Missing content",
        lines="78-78",
        whole_file=False,
        labels=["incomplete"],
        agent="test",
        no_commit=True,
    )
    assert result == 0


def test_rate_whole_file(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote="up",
        reason="Overall good",
        lines=None,
        whole_file=True,
        labels=[],
        agent="test",
        no_commit=True,
    )
    assert result == 0
    ratings_path = repo_with_skill / ".skills-feedback" / "analyzing-charts" / "ratings.json"
    data = json.loads(ratings_path.read_text())
    assert data["ratings"][0]["lines"] is None


def test_rate_rejects_nonexistent_skill(repo):
    config = load_config(repo / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo,
        config=config,
        name="nonexistent",
        vote="up",
        reason="test",
        lines="1-1",
        whole_file=False,
        labels=[],
        agent="test",
        no_commit=True,
    )
    assert result == 1


def test_rate_rejects_invalid_label(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote="up",
        reason="test",
        lines="1-1",
        whole_file=False,
        labels=["outdated"],
        agent="test",
        no_commit=True,
    )
    assert result == 1
