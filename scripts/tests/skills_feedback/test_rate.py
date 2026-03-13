import json

from skills_feedback.commands.rate import rate_skill
from skills_feedback.config import load_config
from skills_feedback.models import Vote


def test_rate_up_creates_rating(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote=Vote.UP,
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
    rating = data["ratings"][0]
    assert rating["vote"] == "up"


def test_rate_down_creates_rating(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote=Vote.DOWN,
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
        vote=Vote.UP,
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
    rating = data["ratings"][0]
    assert rating["lines"] is None


def test_rate_rejects_nonexistent_skill(repo):
    config = load_config(repo / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo,
        config=config,
        name="nonexistent",
        vote=Vote.UP,
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
        vote=Vote.UP,
        reason="test",
        lines="1-1",
        whole_file=False,
        labels=["outdated"],
        agent="test",
        no_commit=True,
    )
    assert result == 1


def test_rate_requires_lines_or_whole_file(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote=Vote.UP,
        reason="test",
        lines=None,
        whole_file=False,
        labels=[],
        agent="test",
        no_commit=True,
    )
    assert result == 1


def test_rate_rejects_invalid_line_range(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    result = rate_skill(
        repo_root=repo_with_skill,
        config=config,
        name="analyzing-charts",
        vote=Vote.UP,
        reason="test",
        lines="abc",
        whole_file=False,
        labels=[],
        agent="test",
        no_commit=True,
    )
    assert result == 1


def test_rate_shows_removal_warning(repo_with_skill, capsys):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    for _ in range(4):
        rate_skill(
            repo_root=repo_with_skill,
            config=config,
            name="analyzing-charts",
            vote=Vote.DOWN,
            reason="bad",
            lines=None,
            whole_file=True,
            labels=[],
            agent="test",
            no_commit=True,
        )
    captured = capsys.readouterr()
    assert "removal threshold" in captured.err
