"""URL Extraction from raw message text.

Member 3: Privacy, Cybersecurity and URL Analysis.

Extracts URLs using regex without making any network requests.
Handles both explicit (http/https) and bare domain URLs.
"""

from __future__ import annotations

import re
from typing import List
from urllib.parse import urlparse

# Matches http(s):// URLs and bare domain-like patterns (e.g. www.example.com/path)
_URL_PATTERN = re.compile(
    r"""
    (?:
        https?://                          # explicit scheme
        [^\s<>"'(){}\[\]]+                 # rest of URL
    )
    |
    (?:
        (?:www\.)                          # bare www. prefix
        [a-zA-Z0-9\-]+(?:\.[a-zA-Z]{2,})+ # domain
        (?:/[^\s<>"'(){}\[\]]*)?           # optional path
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

# Characters that commonly trail a URL in natural language
_TRAILING_JUNK = re.compile(r"[.,!?;:'\")]+$")


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from a raw message string.

    Args:
        text: Raw message text submitted by the user.

    Returns:
        List of unique URL strings found in the text, preserving order.
        Query strings and fragments are retained for analysis but
        the caller (analyzer) strips them before any output.
    """
    if not isinstance(text, str) or not text.strip():
        return []

    raw_matches = _URL_PATTERN.findall(text)
    seen: set[str] = set()
    urls: List[str] = []

    for match in raw_matches:
        # Strip trailing punctuation that is not part of the URL
        cleaned = _TRAILING_JUNK.sub("", match).strip()
        if not cleaned:
            continue

        # Normalise: add scheme for bare www. URLs so urlparse works correctly
        normalised = cleaned if cleaned.lower().startswith("http") else f"http://{cleaned}"

        try:
            parsed = urlparse(normalised)
            # Must have a non-empty netloc (host) to be a valid URL
            if not parsed.netloc:
                continue
        except ValueError:
            continue

        if normalised not in seen:
            seen.add(normalised)
            urls.append(normalised)

    return urls
