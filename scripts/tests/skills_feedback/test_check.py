import json

from skills_feedback.commands.check_thresholds import _discover_skills, check_thresholds
from skills_feedback.config import load_config


def test_discover_skills(repo_with_skill):
    skills = _discover_skills(repo_with_skill)
    assert "analyzing-charts" in skills


def test_discover_skills_ignores_non_skill_dirs(repo_with_skill):
    (repo_with_skill / "scripts").mkdir()
    skills = _discover_skills(repo_with_skill)
    assert "scripts" not in skills


def test_check_thresholds_shows_unrated(repo_with_skill, capsys):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    check_thresholds(repo_with_skill, config)
    captured = capsys.readouterr()
    assert "UNRATED SKILLS" in captured.out
    assert "analyzing-charts" in captured.out


def test_check_thresholds_shows_rated_skill(repo_with_skill, capsys):
    feedback_dir = repo_with_skill / ".skills-feedback" / "analyzing-charts"
    feedback_dir.mkdir(parents=True)
    rating = {"lines": None, "reason": "good", "labels": [], "timestamp": "t"}
    (feedback_dir / "ratings.json").write_text(
        json.dumps(
            {
                "skill": "analyzing-charts",
                "ratings": [
                    {**rating, "vote": "up", "agent": "a"},
                    {**rating, "vote": "up", "agent": "b"},
                ],
            }
        )
    )
    config = load_config(repo_with_skill / ".skills-config.yaml")
    check_thresholds(repo_with_skill, config)
    captured = capsys.readouterr()
    assert "analyzing-charts" in captured.out
    assert "+2" in captured.out


def test_check_thresholds_shows_removal_suggested(repo_with_skill, capsys):
    feedback_dir = repo_with_skill / ".skills-feedback" / "analyzing-charts"
    feedback_dir.mkdir(parents=True)
    ratings = [
        {
            "vote": "down",
            "lines": None,
            "reason": "bad",
            "labels": [],
            "agent": f"a{i}",
            "timestamp": "t",
        }  # noqa: E501
        for i in range(3)
    ]
    (feedback_dir / "ratings.json").write_text(
        json.dumps(
            {
                "skill": "analyzing-charts",
                "ratings": ratings,
            }
        )
    )
    config = load_config(repo_with_skill / ".skills-config.yaml")
    check_thresholds(repo_with_skill, config)
    captured = capsys.readouterr()
    assert "REMOVAL SUGGESTED" in captured.out
