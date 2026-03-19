import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _run_score(*args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/score-skills.py", *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_validate_only_passes_for_valid_skill():
    result = _run_score("exploring-data", "--validate_only")

    assert result.returncode == 0
    assert "valid" in result.stdout.lower()


def test_validate_only_fails_for_invalid_skill():
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = Path(tmpdir) / "BAD_NAME"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("no frontmatter")

        result = _run_score(str(skill_dir), "--validate_only")

        assert result.returncode == 1


def test_validate_only_works_without_litellm():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("import sys; sys.modules['litellm'] = None\n")
        startup = f.name

    env = {**os.environ, "PYTHONSTARTUP": startup}
    result = _run_score("exploring-data", "--validate_only", env=env)

    assert result.returncode == 0, result.stderr
    assert "valid" in result.stdout.lower()
