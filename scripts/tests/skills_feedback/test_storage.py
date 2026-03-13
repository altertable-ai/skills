from skills_feedback.models import Proposal, ProposalsFile, Rating, RatingsFile
from skills_feedback.storage import (
    ensure_feedback_dir,
    load_proposals_file,
    load_ratings_file,
    save_proposals_file,
    save_ratings_file,
)


def test_save_and_load_ratings(tmp_path):
    feedback_dir = tmp_path / ".skills-feedback" / "test-skill"
    feedback_dir.mkdir(parents=True)

    ratings_file = RatingsFile(
        skill="test-skill",
        ratings=[
            Rating(vote="up", lines=["1-5"], reason="good", labels=[], agent="a", timestamp="t"),
        ],
    )
    save_ratings_file(feedback_dir / "ratings.json", ratings_file)

    loaded = load_ratings_file(feedback_dir / "ratings.json")
    assert loaded is not None
    assert loaded.skill == "test-skill"
    assert len(loaded.ratings) == 1
    assert loaded.ratings[0].vote == "up"


def test_load_ratings_missing_returns_empty(tmp_path):
    result = load_ratings_file(tmp_path / "nonexistent.json")
    assert result is None


def test_save_and_load_proposals(tmp_path):
    feedback_dir = tmp_path / ".skills-feedback" / "test-skill"
    feedback_dir.mkdir(parents=True)

    proposals_file = ProposalsFile(
        skill="test-skill",
        proposals=[
            Proposal(
                id="add-20260313T100000Z-test",
                type="add",
                reason="test",
                lines=None,
                body=None,
                proposed_by="test",
                proposed_at="2026-03-13T10:00:00Z",
            ),
        ],
    )
    save_proposals_file(feedback_dir / "proposals.json", proposals_file)

    loaded = load_proposals_file(feedback_dir / "proposals.json")
    assert loaded is not None
    assert loaded.skill == "test-skill"
    assert len(loaded.proposals) == 1


def test_ensure_feedback_dir_creates_directories(tmp_path):
    path = ensure_feedback_dir(tmp_path, "test-skill")
    assert path.exists()
    assert path.is_dir()
    assert path == tmp_path / ".skills-feedback" / "test-skill"


def test_ensure_feedback_dir_idempotent(tmp_path):
    path1 = ensure_feedback_dir(tmp_path, "test-skill")
    path2 = ensure_feedback_dir(tmp_path, "test-skill")
    assert path1 == path2
