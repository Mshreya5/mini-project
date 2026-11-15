"""URL discovery and normalisation.

Deciding whether a message contains a link is plumbing, not scam classification,
so it lives here instead of duplicating work owned by Member 2 or Member 3.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

_URL_PATTERN = re.compile(
    r"""(?xi)
    (?:
        https?://[^\s<>"'\)\]]+
        |
        www\.[^\s<>"'\)\]]+
        |
        [a-z0-9][a-z0-9\-]*(?:\.[a-z0-9\-]+)*\.
        (?:com|net|org|in|co|info|xyz|top|site|online|link|click|shop|icu|biz|live|app|bank)
        (?:/[^\s<>"'\)\]]*)?
    )
    """
)


def extract_urls(text: str) -> list[str]:
    """Return every URL-looking substring in ``text``, in order of appearance."""
    seen: set[str] = set()
    found: list[str] = []
    for match in _URL_PATTERN.finditer(text or ""):
        candidate = match.group(0).rstrip(".,;:!?")
        if candidate.lower() not in seen:
            seen.add(candidate.lower())
            found.append(candidate)
    return found


def extract_first_url(text: str) -> str | None:
    urls = extract_urls(text)
    return urls[0] if urls else None


def normalise_url(raw: str) -> str | None:
    """Make a user supplied URL absolute and reject non http(s) schemes."""
    candidate = (raw or "").strip()
    if not candidate or any(character.isspace() for character in candidate):
        return None

    explicit_scheme = re.match(r"^([a-zA-Z][a-zA-Z0-9+.\-]*)://", candidate)
    if explicit_scheme:
        if explicit_scheme.group(1).lower() not in ("http", "https"):
            return None
    else:
        # Catches ``javascript:`` / ``data:`` style values. A colon followed by a
        # digit is a port, not a scheme.
        colon_scheme = re.match(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):(?![0-9])", candidate)
        if colon_scheme and colon_scheme.group(1).lower() not in ("http", "https"):
            return None
        candidate = f"https://{candidate}"

    parsed = urlparse(candidate)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None
    return candidate


def redact_url(url: str) -> str:
    """Keep the host for display, drop query strings that may hold identifiers."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.hostname or parsed.netloc}/" if parsed.hostname else url
