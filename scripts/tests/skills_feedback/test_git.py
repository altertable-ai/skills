import subprocess

from skills_feedback.git import (
    git_checkout,
    git_checkout_new_branch,
    git_commit,
    git_current_branch,
    git_stage,
    is_git_repo,
    stage_and_commit,
)


def _init_repo(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t.com"], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "config", "user.name", "T"], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], capture_output=True, cwd=tmp_path)
    (tmp_path / "init.txt").write_text("init")
    subprocess.run(["git", "add", "."], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "commit", "-m", "init"], capture_output=True, cwd=tmp_path)


def test_is_git_repo_true(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    assert is_git_repo(tmp_path) is True


def test_is_git_repo_false(tmp_path):
    assert is_git_repo(tmp_path) is False


def test_git_stage_calls_git_add(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")

    git_stage(tmp_path, [test_file])

    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert "test.txt" in result.stdout


def test_git_commit_creates_commit(tmp_path):
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        capture_output=True,
        cwd=tmp_path,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        capture_output=True,
        cwd=tmp_path,
    )
    subprocess.run(
        ["git", "config", "commit.gpgsign", "false"],
        capture_output=True,
        cwd=tmp_path,
    )
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello")
    git_stage(tmp_path, [test_file])

    git_commit(tmp_path, "test commit")

    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert "test commit" in result.stdout


def test_git_checkout_new_branch(tmp_path):
    _init_repo(tmp_path)
    git_checkout_new_branch(tmp_path, "feature-branch", base="HEAD")
    assert git_current_branch(tmp_path) == "feature-branch"


def test_git_current_branch(tmp_path):
    _init_repo(tmp_path)
    branch = git_current_branch(tmp_path)
    assert branch in ("main", "master")


def test_git_checkout(tmp_path):
    _init_repo(tmp_path)
    original = git_current_branch(tmp_path)
    git_checkout_new_branch(tmp_path, "other-branch", base="HEAD")
    assert git_current_branch(tmp_path) == "other-branch"
    git_checkout(tmp_path, original)
    assert git_current_branch(tmp_path) == original


def test_stage_and_commit_creates_commit(tmp_path):
    _init_repo(tmp_path)
    test_file = tmp_path / "new.txt"
    test_file.write_text("content")

    stage_and_commit(tmp_path, [test_file], "staged commit")

    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert "staged commit" in result.stdout


def test_stage_and_commit_no_commit_flag(tmp_path):
    _init_repo(tmp_path)
    test_file = tmp_path / "staged.txt"
    test_file.write_text("content")

    stage_and_commit(tmp_path, [test_file], "should not commit", no_commit=True)

    result = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert "should not commit" not in result.stdout
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )
    assert "staged.txt" not in staged.stdout


def test_stage_and_commit_skips_when_not_git(tmp_path, capsys):
    test_file = tmp_path / "file.txt"
    test_file.write_text("content")

    stage_and_commit(tmp_path, [test_file], "should skip")

    captured = capsys.readouterr()
    assert "not a git repository" in captured.err
