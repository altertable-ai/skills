import sys
from urllib.request import urlopen

AGENT_SKILLS_SPEC_URLS: dict[str, str] = {
    "Agent Skills Specification": "https://agentskills.io/specification.md",
    "Best Practices for Skill Creators": "https://agentskills.io/skill-creation/best-practices.md",
    "Evaluating Skill Output Quality": "https://agentskills.io/skill-creation/evaluating-skills.md",
}

SPEC_FALLBACK: str = (
    "Evaluate against the Agent Skills specification at https://agentskills.io/specification.md"
)

FETCH_TIMEOUT: float = 10.0

_cache: dict[str, str] = {}


def _fetch_url(url: str, timeout: float = FETCH_TIMEOUT) -> str:
    with urlopen(url, timeout=timeout) as resp:  # nosec B310 - URLs are hardcoded constants
        return resp.read().decode()


def fetch_spec_context() -> str:
    """Fetch Agent Skills spec from agentskills.io, with fallback on failure."""
    if "spec_context" in _cache:
        return _cache["spec_context"]

    try:
        result = "\n\n".join(
            f"## {title}\n\n{_fetch_url(url)}" for title, url in AGENT_SKILLS_SPEC_URLS.items()
        )
    except Exception as e:
        print(f"Spec fetch failed ({e}), using fallback", file=sys.stderr)
        result = SPEC_FALLBACK

    _cache["spec_context"] = result
    return result
