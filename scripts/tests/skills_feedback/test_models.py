from skills_feedback.models import Config, Proposal, ProposalsFile, Rating, RatingsFile


def test_rating_up_vote():
    rating = Rating(
        vote="up",
        lines=["45-52"],
        reason="Good content",
        labels=["accurate"],
        agent="claude-code",
        timestamp="2026-03-13T10:30:00Z",
    )
    assert rating.vote == "up"
    assert rating.score_value == 1


def test_rating_down_vote():
    rating = Rating(
        vote="down",
        lines=["78-78"],
        reason="Incomplete",
        labels=["incomplete"],
        agent="crewai",
        timestamp="2026-03-13T10:30:00Z",
    )
    assert rating.score_value == -1


def test_rating_whole_file_lines_null():
    rating = Rating(
        vote="up",
        lines=None,
        reason="Overall good",
        labels=[],
        agent="claude-code",
        timestamp="2026-03-13T10:30:00Z",
    )
    assert rating.lines is None


def test_ratings_file_compute_score():
    ratings_file = RatingsFile(
        skill="test-skill",
        ratings=[
            Rating(vote="up", lines=None, reason="good", labels=[], agent="a", timestamp="t1"),
            Rating(vote="up", lines=None, reason="good", labels=[], agent="b", timestamp="t2"),
            Rating(vote="down", lines=None, reason="bad", labels=[], agent="c", timestamp="t3"),
        ],
    )
    assert ratings_file.compute_score() == 1


def test_ratings_file_empty_score():
    ratings_file = RatingsFile(skill="test-skill", ratings=[])
    assert ratings_file.compute_score() == 0


def test_proposal_id_format():
    proposal = Proposal(
        id="add-20260313T100000Z-claude-code",
        type="add",
        reason="New skill needed",
        lines=None,
        body=None,
        proposed_by="claude-code",
        proposed_at="2026-03-13T10:00:00Z",
    )
    assert proposal.id == "add-20260313T100000Z-claude-code"
    assert proposal.type == "add"


def test_proposals_file_append():
    pf = ProposalsFile(skill="test", proposals=[])
    proposal = Proposal(
        id="add-20260313T100000Z-claude-code",
        type="add",
        reason="test",
        lines=None,
        body=None,
        proposed_by="claude-code",
        proposed_at="2026-03-13T10:00:00Z",
    )
    pf.proposals.append(proposal)
    assert len(pf.proposals) == 1


def test_config_defaults():
    config = Config(
        thresholds={"proposal": 3, "removal": -3},
        reviewer="fvaleye",
        labels={"positive": ["accurate"], "negative": ["outdated"]},
    )
    assert config.thresholds["proposal"] == 3
    assert config.reviewer == "fvaleye"
