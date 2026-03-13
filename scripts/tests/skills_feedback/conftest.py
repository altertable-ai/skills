import subprocess

import pytest


@pytest.fixture
def repo(tmp_path):
    """Create an isolated git repo with skills-feedback config.

    Each test gets its own tmp_path, making this safe for pytest-xdist parallel execution.
    """
    subprocess.run(["git", "init", str(tmp_path)], capture_output=True, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.com"], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "config", "user.name", "T"], capture_output=True, cwd=tmp_path)
    config = tmp_path / ".skills-config.yaml"
    config.write_text(
        "thresholds:\n  proposal: 3\n  removal: -3\n"
        "reviewer: test\n"
        "labels:\n  positive:\n    - accurate\n    - helpful\n"
        "  negative:\n    - outdated\n    - incomplete\n"
    )
    subprocess.run(["git", "add", "."], capture_output=True, cwd=tmp_path)
    subprocess.run(["git", "commit", "-m", "init"], capture_output=True, cwd=tmp_path)
    return tmp_path


@pytest.fixture
def repo_with_skill(repo):
    """Git repo with an existing analyzing-charts skill directory."""
    skill_dir = repo / "analyzing-charts"
    skill_dir.mkdir()
    skill_content = "---\nname: analyzing-charts\ndescription: test\n---\n# Test\n"
    (skill_dir / "SKILL.md").write_text(skill_content * 10)
    subprocess.run(["git", "add", "."], capture_output=True, cwd=repo)
    subprocess.run(["git", "commit", "-m", "add skill"], capture_output=True, cwd=repo)
    return repo
