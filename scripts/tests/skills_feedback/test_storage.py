import pytest
from skills_feedback.constants import FEEDBACK_DIR_NAME, RATINGS_FILENAME
from skills_feedback.models import Proposal, ProposalsFile, ProposalType, Rating, RatingsFile, Vote
from skills_feedback.storage import FeedbackStore


def test_save_and_load_ratings(tmp_path):
    store = FeedbackStore(tmp_path)
    store.ensure_dir("test-skill")
    ratings_file = RatingsFile(
        skill="test-skill",
        ratings=[
            Rating(vote=Vote.UP, lines=["1-5"], reason="good", labels=[], agent="a", timestamp="t"),
        ],
    )
    store.save_ratings("test-skill", ratings_file)

    loaded = store.load_ratings("test-skill")
    assert loaded is not None
    assert loaded.skill == "test-skill"
    assert len(loaded.ratings) == 1
    assert loaded.ratings[0].vote == "up"


def test_save_and_load_proposals(tmp_path):
    store = FeedbackStore(tmp_path)
    store.ensure_dir("test-skill")
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
    store.save_proposals("test-skill", proposals_file)

    loaded = store.load_proposals("test-skill")
    assert loaded is not None
    assert loaded.skill == "test-skill"
    assert len(loaded.proposals) == 1


def test_ensure_dir_creates_directories(tmp_path):
    store = FeedbackStore(tmp_path)
    path = store.ensure_dir("test-skill")
    assert path.exists()
    assert path.is_dir()
    assert path == tmp_path / FEEDBACK_DIR_NAME / "test-skill"


def test_ensure_dir_idempotent(tmp_path):
    store = FeedbackStore(tmp_path)
    path1 = store.ensure_dir("test-skill")
    path2 = store.ensure_dir("test-skill")
    assert path1 == path2


@pytest.mark.parametrize(
    "func_name, expected_suffix",
    [
        ("feedback_dir", f"{FEEDBACK_DIR_NAME}/my-skill"),
        ("ratings_path", f"{FEEDBACK_DIR_NAME}/my-skill/{RATINGS_FILENAME}"),
    ],
)
def test_path_helpers(tmp_path, func_name, expected_suffix):
    store = FeedbackStore(tmp_path)
    assert getattr(store, func_name)("my-skill") == tmp_path / expected_suffix


@pytest.mark.parametrize("exists", [True, False])
def test_skill_exists(tmp_path, exists):
    store = FeedbackStore(tmp_path)
    if exists:
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Test")
    assert store.skill_exists("my-skill") == exists


def test_load_ratings_missing_returns_none(tmp_path):
    store = FeedbackStore(tmp_path)
    assert store.load_ratings("nonexistent") is None


@pytest.mark.parametrize("filename", ["ratings.json", "proposals.json"])
def test_load_skips_malformed_json(tmp_path, filename):
    feedback_dir = tmp_path / FEEDBACK_DIR_NAME / "bad-skill"
    feedback_dir.mkdir(parents=True)
    (feedback_dir / filename).write_text("{invalid json")
    store = FeedbackStore(tmp_path)
    loader = store.load_ratings if "ratings" in filename else store.load_proposals
    assert loader("bad-skill") is None


def test_skill_feedback_dirs(tmp_path):
    store = FeedbackStore(tmp_path)
    assert store.skill_feedback_dirs() == []

    base = tmp_path / FEEDBACK_DIR_NAME
    base.mkdir()
    (base / "skill-a").mkdir()
    (base / "skill-b").mkdir()
    dirs = store.skill_feedback_dirs()
    assert len(dirs) == 2
    assert dirs[0].name == "skill-a"
