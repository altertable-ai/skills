from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest
from scorer.spec import (
    AGENT_SKILLS_SPEC_URLS,
    SPEC_FALLBACK,
    _cache,
    _fetch_url,
    fetch_spec_context,
)


@pytest.fixture(autouse=True)
def clear_cache():
    _cache.clear()


@pytest.fixture()
def mock_urlopen():
    with patch("scorer.spec.urlopen") as mock:
        yield mock


def _mock_response(content: bytes) -> MagicMock:
    mock = MagicMock()
    mock.read.return_value = content
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


def test_fetch_url_returns_decoded_content(mock_urlopen):
    mock_urlopen.return_value = _mock_response(b"markdown content")

    result = _fetch_url("https://example.com/doc.md", timeout=5.0)

    assert result == "markdown content"
    mock_urlopen.assert_called_once_with("https://example.com/doc.md", timeout=5.0)


def test_fetch_spec_context_returns_concatenated_docs(mock_urlopen):
    mock_urlopen.return_value = _mock_response(b"doc body")

    result = fetch_spec_context()

    for title in AGENT_SKILLS_SPEC_URLS:
        assert f"## {title}" in result
    assert result.count("doc body") == len(AGENT_SKILLS_SPEC_URLS)


def test_fetch_spec_context_uses_cache_on_second_call(mock_urlopen):
    mock_urlopen.return_value = _mock_response(b"cached content")

    fetch_spec_context()
    fetch_spec_context()

    assert mock_urlopen.call_count == len(AGENT_SKILLS_SPEC_URLS)


def test_fetch_spec_context_falls_back_on_network_error(mock_urlopen):
    mock_urlopen.side_effect = URLError("connection failed")

    result = fetch_spec_context()

    assert result == SPEC_FALLBACK
