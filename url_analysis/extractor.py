from __future__ import annotations

import re
from typing import List
from urllib.parse import urlparse

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

_TRAILING_JUNK = re.compile(r"[.,!?;:'\")]+$")


def extract_urls(text: str) -> List[str]:
    """Extract all URLs from a raw message string."""
    if not isinstance(text, str) or not text.strip():
        return []

    raw_matches = _URL_PATTERN.findall(text)
    seen: set[str] = set()
    urls: List[str] = []

    for match in raw_matches:
        cleaned = _TRAILING_JUNK.sub("", match).strip()
        if not cleaned:
            continue

        normalised = cleaned if cleaned.lower().startswith("http") else f"http://{cleaned}"

        try:
            parsed = urlparse(normalised)
            if not parsed.netloc:
                continue
        except ValueError:
            continue

        if normalised not in seen:
            seen.add(normalised)
            urls.append(normalised)

    return urls
