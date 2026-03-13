from skills_feedback.constants import FEEDBACK_DIR_NAME, PROPOSALS_FILENAME, RATINGS_FILENAME
from skills_feedback.models import Proposal, ProposalsFile, ProposalType, Rating, RatingsFile
from skills_feedback.storage import (
    ensure_feedback_dir,
    feedback_base,
    feedback_dir_for,
    load_proposals_file,
    load_ratings_file,
    proposals_path,
    ratings_path,
    save_proposals_file,
    save_ratings_file,
    skill_exists,
)


def test_save_and_load_ratings(tmp_path):
    feedback_dir = tmp_path / FEEDBACK_DIR_NAME / "test-skill"
    feedback_dir.mkdir(parents=True)

    ratings_file = RatingsFile(
        skill="test-skill",
        ratings=[
            Rating(vote="up", lines=["1-5"], reason="good", labels=[], agent="a", timestamp="t"),
        ],
    )
    save_ratings_file(ratings_path(feedback_dir), ratings_file)

    loaded = load_ratings_file(ratings_path(feedback_dir))
    assert loaded is not None
    assert loaded.skill == "test-skill"
    assert len(loaded.ratings) == 1
    assert loaded.ratings[0].vote == "up"


def test_load_ratings_missing_returns_empty(tmp_path):
    result = load_ratings_file(tmp_path / "nonexistent.json")
    assert result is None


def test_save_and_load_proposals(tmp_path):
    feedback_dir = tmp_path / FEEDBACK_DIR_NAME / "test-skill"
    feedback_dir.mkdir(parents=True)

    proposals_file = ProposalsFile(
        skill="test-skill",
        proposals=[
            Proposal(
                id="add-20260313T100000Z-test",
                type=ProposalType.ADD,
                reason="test",
                lines=None,
                body=None,
                proposed_by="test",
                proposed_at="2026-03-13T10:00:00Z",
            ),
        ],
    )
    save_proposals_file(proposals_path(feedback_dir), proposals_file)

    loaded = load_proposals_file(proposals_path(feedback_dir))
    assert loaded is not None
    assert loaded.skill == "test-skill"
    assert len(loaded.proposals) == 1


def test_ensure_feedback_dir_creates_directories(tmp_path):
    path = ensure_feedback_dir(tmp_path, "test-skill")
    assert path.exists()
    assert path.is_dir()
    assert path == tmp_path / FEEDBACK_DIR_NAME / "test-skill"


def test_ensure_feedback_dir_idempotent(tmp_path):
    path1 = ensure_feedback_dir(tmp_path, "test-skill")
    path2 = ensure_feedback_dir(tmp_path, "test-skill")
    assert path1 == path2


def test_feedback_dir_for_returns_correct_path(tmp_path):
    result = feedback_dir_for(tmp_path, "my-skill")
    assert result == tmp_path / FEEDBACK_DIR_NAME / "my-skill"


def test_feedback_base_returns_correct_path(tmp_path):
    result = feedback_base(tmp_path)
    assert result == tmp_path / FEEDBACK_DIR_NAME


def test_ratings_path_returns_correct_filename(tmp_path):
    result = ratings_path(tmp_path)
    assert result == tmp_path / RATINGS_FILENAME


def test_proposals_path_returns_correct_filename(tmp_path):
    result = proposals_path(tmp_path)
    assert result == tmp_path / PROPOSALS_FILENAME


def test_skill_exists_true(tmp_path):
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# Test")
    assert skill_exists(tmp_path, "my-skill")


def test_skill_exists_false(tmp_path):
    assert not skill_exists(tmp_path, "nonexistent")
