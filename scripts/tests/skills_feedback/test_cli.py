import pytest
from skills_feedback.cli import Propose, SkillsFeedback
from skills_feedback.config import find_repo_root, load_config
from skills_feedback.models import Vote


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
        propose = Propose()
        with pytest.raises(SystemExit) as exc_info:
            propose.add(
                name="new-skill",
                description="test skill",
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 0

    def test_add_rejects_invalid_name(self):
        propose = Propose()
        with pytest.raises(SystemExit) as exc_info:
            propose.add(
                name="Invalid",
                description="test",
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 1


@pytest.mark.usefixtures("_patch_cli_load")
class TestProposeModify:
    def test_modify_success(self):
        propose = Propose()
        with pytest.raises(SystemExit) as exc_info:
            propose.modify(
                name="analyzing-charts",
                reason="update needed",
                lines="1-5",
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 0

    def test_modify_rejects_nonexistent(self):
        propose = Propose()
        with pytest.raises(SystemExit) as exc_info:
            propose.modify(
                name="nonexistent",
                reason="test",
                lines="1-1",
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 1


@pytest.mark.usefixtures("_patch_cli_load")
class TestProposeRemove:
    def test_remove_success(self):
        propose = Propose()
        with pytest.raises(SystemExit) as exc_info:
            propose.remove(
                name="analyzing-charts",
                reason="superseded",
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 0

    def test_remove_rejects_nonexistent(self):
        propose = Propose()
        with pytest.raises(SystemExit) as exc_info:
            propose.remove(
                name="nonexistent",
                reason="test",
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 1


@pytest.mark.usefixtures("_patch_cli_load")
class TestSkillsFeedbackRate:
    def test_rate_success(self):
        sf = SkillsFeedback()
        with pytest.raises(SystemExit) as exc_info:
            sf.rate(
                name="analyzing-charts",
                vote=Vote.UP,
                reason="good",
                whole_file=True,
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 0

    def test_rate_with_labels_csv(self):
        sf = SkillsFeedback()
        with pytest.raises(SystemExit) as exc_info:
            sf.rate(
                name="analyzing-charts",
                vote=Vote.UP,
                reason="good",
                whole_file=True,
                labels="accurate,helpful",
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 0

    def test_rate_rejects_nonexistent(self):
        sf = SkillsFeedback()
        with pytest.raises(SystemExit) as exc_info:
            sf.rate(
                name="nonexistent",
                vote=Vote.UP,
                reason="test",
                whole_file=True,
                agent="test",
                no_commit=True,
            )
        assert exc_info.value.code == 1


@pytest.mark.usefixtures("_patch_cli_load_bare")
class TestSkillsFeedbackCheckThresholds:
    def test_check_thresholds_success(self):
        sf = SkillsFeedback()
        with pytest.raises(SystemExit) as exc_info:
            sf.check_thresholds()
        assert exc_info.value.code == 0


@pytest.mark.usefixtures("_patch_cli_load_bare")
class TestSkillsFeedbackApply:
    def test_apply_dry_run(self):
        sf = SkillsFeedback()
        with pytest.raises(SystemExit) as exc_info:
            sf.apply(dry_run=True)
        assert exc_info.value.code == 0
