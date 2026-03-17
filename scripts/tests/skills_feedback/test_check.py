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


def test_check_thresholds_shows_unrated(repo_with_skill):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    output = check_thresholds(repo_with_skill, config)
    assert "UNRATED SKILLS" in output
    assert "analyzing-charts" in output


def test_check_thresholds_shows_rated_skill(repo_with_skill):
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
    output = check_thresholds(repo_with_skill, config)
    assert "analyzing-charts" in output
    assert "+2" in output


def test_check_thresholds_shows_proposal_summary(repo_with_skill):
    feedback_dir = repo_with_skill / ".skills-feedback" / "analyzing-charts"
    feedback_dir.mkdir(parents=True)
    (feedback_dir / "proposals.json").write_text(
        json.dumps(
            {
                "skill": "analyzing-charts",
                "proposals": [
                    {
                        "id": "modify-001",
                        "type": "modify",
                        "reason": "test",
                        "lines": ["1-5"],
                        "body": None,
                        "proposed_by": "test",
                        "proposed_at": "2026-01-01T00:00:00Z",
                    }
                ],
            }
        )
    )
    config = load_config(repo_with_skill / ".skills-config.yaml")
    output = check_thresholds(repo_with_skill, config)
    assert "1 modify" in output


def test_check_thresholds_shows_proposed_new(repo_with_skill):
    feedback_dir = repo_with_skill / ".skills-feedback" / "brand-new-skill"
    feedback_dir.mkdir(parents=True)
    (feedback_dir / "proposals.json").write_text(
        json.dumps(
            {
                "skill": "brand-new-skill",
                "proposals": [
                    {
                        "id": "add-001",
                        "type": "add",
                        "reason": "needed",
                        "lines": None,
                        "body": None,
                        "proposed_by": "test",
                        "proposed_at": "2026-01-01T00:00:00Z",
                    }
                ],
            }
        )
    )
    config = load_config(repo_with_skill / ".skills-config.yaml")
    output = check_thresholds(repo_with_skill, config)
    assert "PROPOSED NEW SKILLS" in output
    assert "brand-new-skill" in output


def test_check_thresholds_shows_removal_suggested(repo_with_skill):
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
        }
        for i in range(3)
    ]
    (feedback_dir / "ratings.json").write_text(
        json.dumps({"skill": "analyzing-charts", "ratings": ratings})
    )
    config = load_config(repo_with_skill / ".skills-config.yaml")
    output = check_thresholds(repo_with_skill, config)
    assert "REMOVAL SUGGESTED" in output
