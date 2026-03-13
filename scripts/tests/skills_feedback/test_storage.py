import pytest
from skills_feedback.constants import FEEDBACK_DIR_NAME, PROPOSALS_FILENAME, RATINGS_FILENAME
from skills_feedback.models import Proposal, ProposalsFile, ProposalType, Rating, RatingsFile, Vote
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
            Rating(vote=Vote.UP, lines=["1-5"], reason="good", labels=[], agent="a", timestamp="t"),
        ],
    )
    save_ratings_file(ratings_path(feedback_dir), ratings_file)

    loaded = load_ratings_file(ratings_path(feedback_dir))
    assert loaded is not None
    assert loaded.skill == "test-skill"
    assert len(loaded.ratings) == 1
    assert loaded.ratings[0].vote == "up"


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


@pytest.mark.parametrize(
    "func, expected_suffix",
    [
        (feedback_base, FEEDBACK_DIR_NAME),
        (lambda p: feedback_dir_for(p, "my-skill"), f"{FEEDBACK_DIR_NAME}/my-skill"),
        (ratings_path, RATINGS_FILENAME),
        (proposals_path, PROPOSALS_FILENAME),
    ],
)
def test_path_helpers(tmp_path, func, expected_suffix):
    assert func(tmp_path) == tmp_path / expected_suffix


@pytest.mark.parametrize("exists", [True, False])
def test_skill_exists(tmp_path, exists):
    if exists:
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")
    assert skill_exists(tmp_path, "my-skill") == exists


@pytest.mark.parametrize("filename", ["ratings.json", "proposals.json"])
def test_load_skips_malformed_json(tmp_path, filename):
    bad = tmp_path / filename
    bad.write_text("{invalid json")
    loader = load_ratings_file if "ratings" in filename else load_proposals_file
    assert loader(bad) is None


def test_load_ratings_missing_returns_none(tmp_path):
    assert load_ratings_file(tmp_path / "nonexistent.json") is None
