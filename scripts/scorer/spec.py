import sys
from urllib.request import urlopen

AGENT_SKILLS_SPEC_URLS: dict[str, str] = {
    "Agent Skills Specification": "https://agentskills.io/specification.md",
    "Best Practices for Skill Creators": "https://agentskills.io/skill-creation/best-practices.md",
    "Evaluating Skill Output Quality": "https://agentskills.io/skill-creation/evaluating-skills.md",
}

FETCH_TIMEOUT: float = 10.0

_cache: dict[str, str] = {}


class SpecUnavailableError(RuntimeError):
    """Raised when no specification document could be fetched."""


def _fetch_url(url: str, timeout: float = FETCH_TIMEOUT) -> str:
    with urlopen(url, timeout=timeout) as resp:  # nosec B310 - URLs are hardcoded constants
        return resp.read().decode()


def fetch_spec_context() -> str:
    """Fetch the Agent Skills spec, keeping whatever documents are reachable.

    Each document is fetched independently so one unreachable URL cannot discard the
    others. Scoring against a missing rubric would silently change what the gate means,
    so a total failure raises instead of degrading to a placeholder.
    """
    if "spec_context" in _cache:
        return _cache["spec_context"]

    sections: list[str] = []
    for title, url in AGENT_SKILLS_SPEC_URLS.items():
        try:
            sections.append(f"## {title}\n\n{_fetch_url(url)}")
        except Exception as e:
            print(f"Spec fetch failed for {title} ({e})", file=sys.stderr)

    if not sections:
        urls = ", ".join(AGENT_SKILLS_SPEC_URLS.values())
        raise SpecUnavailableError(f"No specification document could be fetched from {urls}")

    if len(sections) < len(AGENT_SKILLS_SPEC_URLS):
        print(
            f"Scoring against {len(sections)} of {len(AGENT_SKILLS_SPEC_URLS)} spec documents",
            file=sys.stderr,
        )

    result = "\n\n".join(sections)
    _cache["spec_context"] = result
    return result
