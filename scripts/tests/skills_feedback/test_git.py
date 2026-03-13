import subprocess

from skills_feedback.git import git_commit, git_stage, is_git_repo


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
