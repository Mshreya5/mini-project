"""Structural and lexical URL risk indicator analysis.

Member 3: Privacy, Cybersecurity and URL Analysis.

All checks are purely structural — no HTTP requests are made.
A URL is flagged suspicious only when 2 or more indicators fire,
avoiding false positives from a single ambiguous signal.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

_SHORTENER_HOSTS = frozenset(
    [
        "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
        "buff.ly", "adf.ly", "short.link", "rebrand.ly", "cutt.ly",
        "tiny.cc", "shorte.st", "clck.ru", "bl.ink", "shorturl.at",
    ]
)

_KNOWN_BRANDS = [
    "paypal", "amazon", "google", "microsoft", "apple", "netflix",
    "facebook", "instagram", "whatsapp", "twitter", "linkedin",
    "bankofamerica", "chase", "wellsfargo", "citibank", "hsbc",
    "ebay", "dropbox", "icloud", "outlook", "yahoo",
]

# Common typosquatting substitutions: l→1, o→0, etc.
_HOMOGLYPH_PATTERN = re.compile(r"[0-9]")

# Suspicious TLDs frequently abused in phishing
_SUSPICIOUS_TLDS = frozenset(
    ["xyz", "top", "club", "work", "click", "link", "gq", "ml", "cf", "tk", "pw", "zip", "mov"]
)

# Patterns that suggest credential harvesting or redirect abuse
_SUSPICIOUS_PATH_PATTERNS = re.compile(
    r"(?i)(login|signin|verify|account|update|confirm|secure|banking|password|credential|suspend)",
)

# Excessive subdomains: more than 3 labels before the registered domain
_SUBDOMAIN_THRESHOLD = 3


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class AnalysisResult:
    url: str
    url_found: bool
    suspicious: bool
    risk_score: int
    risk_indicators: List[str] = field(default_factory=list)
    explanation: str = ""


# ---------------------------------------------------------------------------
# Individual indicator checks
# ---------------------------------------------------------------------------

def _check_ip_based(host: str) -> str | None:
    """Detect IP address used directly as host (e.g. http://192.168.1.1/login)."""
    ipv4 = re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}(:\d+)?", host)
    ipv6 = host.startswith("[")
    if ipv4 or ipv6:
        return "IP address used instead of domain name"
    return None


def _check_shortener(host: str) -> str | None:
    """Detect known URL shortening services."""
    bare = host.lower().lstrip("www.")
    if bare in _SHORTENER_HOSTS:
        return "URL shortener detected"
    return None


def _check_suspicious_tld(host: str) -> str | None:
    """Detect use of TLDs commonly abused in phishing campaigns."""
    parts = host.lower().split(".")
    tld = parts[-1] if parts else ""
    if tld in _SUSPICIOUS_TLDS:
        return f"Suspicious top-level domain (.{tld})"
    return None


def _check_misspelled_brand(host: str) -> str | None:
    """Detect misspelled or homoglyph-substituted brand names in the domain."""
    host_lower = host.lower()
    # Strip digits for homoglyph comparison
    host_no_digits = _HOMOGLYPH_PATTERN.sub("", host_lower)

    for brand in _KNOWN_BRANDS:
        # Exact brand present but domain is NOT the legitimate brand domain
        legitimate_domain = f"{brand}.com"
        if brand in host_lower and not host_lower.endswith(legitimate_domain):
            return f"Possible brand impersonation: '{brand}' in domain"

        # Homoglyph: digits removed version matches brand (e.g. paypa1 → paypal)
        if brand in host_no_digits and brand not in host_lower:
            return f"Possible homoglyph substitution targeting '{brand}'"

    return None


def _check_excessive_subdomains(host: str) -> str | None:
    """Detect unusually deep subdomain structures."""
    # Remove port if present
    bare_host = host.split(":")[0]
    labels = bare_host.split(".")
    if len(labels) > _SUBDOMAIN_THRESHOLD:
        return f"Unusual subdomain depth ({len(labels)} labels)"
    return None


def _check_suspicious_path(path: str) -> str | None:
    """Detect credential-harvesting keywords in the URL path."""
    if _SUSPICIOUS_PATH_PATTERNS.search(path):
        return "Suspicious path keywords (login/verify/account/secure)"
    return None


def _check_long_url(url: str) -> str | None:
    """Detect excessively long URLs used to obscure the true destination."""
    if len(url) > 200:
        return "Unusually long URL (may obscure destination)"
    return None


def _check_multiple_redirects(url: str) -> str | None:
    """Detect URL-within-URL redirect patterns."""
    # Count occurrences of http in the URL after the scheme
    tail = url[8:]  # skip 'https://'
    if "http" in tail.lower():
        return "Embedded redirect URL detected"
    return None


def _check_at_symbol(url: str) -> str | None:
    """Detect @ symbol in URL used to spoof the displayed host."""
    parsed = urlparse(url)
    if "@" in (parsed.netloc or ""):
        return "@ symbol in URL (host spoofing technique)"
    return None


# ---------------------------------------------------------------------------
# Public analysis function
# ---------------------------------------------------------------------------

def _strip_query_for_output(url: str) -> str:
    """Return URL with query string and fragment removed for privacy-safe output."""
    parsed = urlparse(url)
    return parsed._replace(query="", fragment="").geturl()


def analyze_url(url: str) -> AnalysisResult:
    """Run all structural risk indicator checks against a single URL.

    No network requests are made. Analysis is purely lexical/structural.

    Args:
        url: A normalised URL string (must include scheme).

    Returns:
        AnalysisResult with indicators and a suspicious flag.
        suspicious=True only when risk_score >= 2.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return AnalysisResult(
            url=url,
            url_found=True,
            suspicious=False,
            risk_score=0,
            risk_indicators=["Malformed URL — could not parse"],
            explanation="The URL could not be parsed and was not analysed further.",
        )

    host = parsed.netloc or ""
    path = parsed.path or ""
    indicators: List[str] = []

    for check_fn, arg in [
        (_check_ip_based, host),
        (_check_shortener, host),
        (_check_suspicious_tld, host),
        (_check_misspelled_brand, host),
        (_check_excessive_subdomains, host),
        (_check_suspicious_path, path),
        (_check_long_url, url),
        (_check_multiple_redirects, url),
        (_check_at_symbol, url),
    ]:
        result = check_fn(arg)
        if result:
            indicators.append(result)

    risk_score = len(indicators)
    # Require at least 2 indicators before marking suspicious
    suspicious = risk_score >= 2

    if not indicators:
        explanation = "No suspicious characteristics were detected in this URL."
    elif not suspicious:
        explanation = (
            f"One potential indicator was noted ({indicators[0]}), "
            "but a single signal is insufficient to classify this URL as suspicious."
        )
    else:
        explanation = (
            f"The URL contains {risk_score} characteristics commonly associated with "
            "phishing or scam links. Exercise caution before clicking."
        )

    return AnalysisResult(
        url=_strip_query_for_output(url),
        url_found=True,
        suspicious=suspicious,
        risk_score=risk_score,
        risk_indicators=indicators,
        explanation=explanation,
    )
