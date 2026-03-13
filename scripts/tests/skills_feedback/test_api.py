import pytest
from skills_feedback.api import (
    ApplyRequest,
    ProposeAddRequest,
    ProposeModifyRequest,
    ProposeRemoveRequest,
    RateRequest,
    SkillsFeedbackError,
    apply,
    check,
    propose_add_skill,
    propose_modify_skill,
    propose_remove_skill,
    rate,
)
from skills_feedback.config import load_config
from skills_feedback.models import Vote


@pytest.fixture
def _patch_load(repo_with_skill, monkeypatch):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    monkeypatch.setattr("skills_feedback.api._load", lambda: (repo_with_skill, config))


@pytest.fixture
def _patch_load_bare(repo, monkeypatch):
    config = load_config(repo / ".skills-config.yaml")
    monkeypatch.setattr("skills_feedback.api._load", lambda: (repo, config))


@pytest.mark.usefixtures("_patch_load")
class TestRate:
    def test_rate_success(self):
        request = RateRequest(
            name="analyzing-charts",
            vote=Vote.UP,
            reason="good content",
            whole_file=True,
            agent="test",
            no_commit=True,
        )
        rate(request)

    def test_rate_raises_on_nonexistent_skill(self):
        request = RateRequest(
            name="nonexistent",
            vote=Vote.UP,
            reason="test",
            whole_file=True,
            agent="test",
            no_commit=True,
        )
        with pytest.raises(SkillsFeedbackError, match="rate failed"):
            rate(request)


@pytest.mark.usefixtures("_patch_load_bare")
class TestProposeAdd:
    def test_propose_add_skill_success(self):
        request = ProposeAddRequest(
            name="new-skill",
            description="A new skill",
            agent="test",
            no_commit=True,
        )
        propose_add_skill(request)

    def test_propose_add_skill_raises_on_invalid_name(self):
        request = ProposeAddRequest(
            name="Invalid-Name",
            description="test",
            agent="test",
            no_commit=True,
        )
        with pytest.raises(SkillsFeedbackError, match="propose add failed"):
            propose_add_skill(request)


@pytest.mark.usefixtures("_patch_load")
class TestProposeModify:
    def test_propose_modify_skill_success(self):
        request = ProposeModifyRequest(
            name="analyzing-charts",
            reason="needs update",
            lines="1-5",
            agent="test",
            no_commit=True,
        )
        propose_modify_skill(request)

    def test_propose_modify_skill_raises_on_nonexistent(self):
        request = ProposeModifyRequest(
            name="nonexistent",
            reason="test",
            lines="1-1",
            agent="test",
            no_commit=True,
        )
        with pytest.raises(SkillsFeedbackError, match="propose modify failed"):
            propose_modify_skill(request)


@pytest.mark.usefixtures("_patch_load")
class TestProposeRemove:
    def test_propose_remove_skill_success(self):
        request = ProposeRemoveRequest(
            name="analyzing-charts",
            reason="superseded",
            agent="test",
            no_commit=True,
        )
        propose_remove_skill(request)

    def test_propose_remove_skill_raises_on_nonexistent(self):
        request = ProposeRemoveRequest(
            name="nonexistent",
            reason="test",
            agent="test",
            no_commit=True,
        )
        with pytest.raises(SkillsFeedbackError, match="propose remove failed"):
            propose_remove_skill(request)


@pytest.mark.usefixtures("_patch_load_bare")
class TestApply:
    def test_apply_dry_run_success(self):
        apply(ApplyRequest(dry_run=True))

    def test_apply_default_request_none(self):
        apply(None)


@pytest.mark.usefixtures("_patch_load_bare")
class TestCheck:
    def test_check_success(self):
        check()
