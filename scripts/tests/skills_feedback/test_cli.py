import pytest
from skills_feedback.cli import Propose, SkillsFeedback
from skills_feedback.config import find_repo_root, load_config
from skills_feedback.models import SkillsFeedbackError, Vote


@pytest.fixture
def _patch_cli_load(repo_with_skill, monkeypatch):
    config = load_config(repo_with_skill / ".skills-config.yaml")
    monkeypatch.setattr("skills_feedback.cli.load_repo_config", lambda: (repo_with_skill, config))


@pytest.fixture
def _patch_cli_load_bare(repo, monkeypatch):
    config = load_config(repo / ".skills-config.yaml")
    monkeypatch.setattr("skills_feedback.cli.load_repo_config", lambda: (repo, config))


class TestFindRepoRoot:
    def test_finds_git_root(self, repo, monkeypatch):
        monkeypatch.chdir(repo)
        root = find_repo_root()
        assert (root / ".git").exists()

    def test_returns_cwd_when_no_git(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        root = find_repo_root()
        assert root == tmp_path


@pytest.mark.usefixtures("_patch_cli_load")
class TestProposeAdd:
    def test_add_success(self):
        Propose().add(name="new-skill", description="test skill", agent="test", no_commit=True)

    def test_add_rejects_invalid_name(self):
        with pytest.raises(SkillsFeedbackError):
            Propose().add(name="Invalid", description="test", agent="test", no_commit=True)


@pytest.mark.usefixtures("_patch_cli_load")
class TestProposeModify:
    def test_modify_success(self):
        Propose().modify(
            name="analyzing-charts",
            reason="update needed",
            lines="1-5",
            agent="test",
            no_commit=True,
        )

    def test_modify_rejects_nonexistent(self):
        with pytest.raises(SkillsFeedbackError):
            Propose().modify(
                name="nonexistent",
                reason="test",
                lines="1-1",
                agent="test",
                no_commit=True,
            )


@pytest.mark.usefixtures("_patch_cli_load")
class TestProposeRemove:
    def test_remove_success(self):
        Propose().remove(name="analyzing-charts", reason="superseded", agent="test", no_commit=True)

    def test_remove_rejects_nonexistent(self):
        with pytest.raises(SkillsFeedbackError):
            Propose().remove(name="nonexistent", reason="test", agent="test", no_commit=True)


@pytest.mark.usefixtures("_patch_cli_load")
class TestSkillsFeedbackRate:
    def test_rate_success(self):
        SkillsFeedback().rate(
            name="analyzing-charts",
            vote=Vote.UP,
            reason="good",
            whole_file=True,
            agent="test",
            no_commit=True,
        )

    def test_rate_with_labels_csv(self):
        SkillsFeedback().rate(
            name="analyzing-charts",
            vote=Vote.UP,
            reason="good",
            whole_file=True,
            labels="accurate,helpful",
            agent="test",
            no_commit=True,
        )

    def test_rate_rejects_nonexistent(self):
        with pytest.raises(SkillsFeedbackError):
            SkillsFeedback().rate(
                name="nonexistent",
                vote=Vote.UP,
                reason="test",
                whole_file=True,
                agent="test",
                no_commit=True,
            )


@pytest.mark.usefixtures("_patch_cli_load_bare")
class TestSkillsFeedbackCheckThresholds:
    def test_check_thresholds_success(self):
        SkillsFeedback().check_thresholds()


@pytest.mark.usefixtures("_patch_cli_load_bare")
class TestSkillsFeedbackApply:
    def test_apply_dry_run(self):
        SkillsFeedback().apply(dry_run=True)
