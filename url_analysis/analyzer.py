from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List
from urllib.parse import urlparse

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
    # Indian banking & digital services
    "sbi", "yono", "hdfc", "icici", "axis", "pnb", "bankofbaroda",
    "kotak", "canara", "unionbank", "paytm", "phonepe", "gpay",
    "bhim", "aadhaar", "uidai", "incometax", "epfo",
]

_OFFICIAL_BRAND_DOMAINS = {
    "google": ("google.com", "google.co.in", "google.in"),
    "sbi": ("sbi.co.in", "onlinesbi.sbi", "onlinesbi.com"),
    "yono": ("onlinesbi.sbi", "sbi.co.in"),
    "hdfc": ("hdfcbank.com", "hdfc.com"),
    "icici": ("icicibank.com", "icicibank.co.in"),
    "axis": ("axisbank.com", "axisbank.co.in"),
    "kotak": ("kotak.com", "kotakbank.com"),
    "pnb": ("pnbindia.in", "pnb.bank.in"),
    "paytm": ("paytm.com", "paytmbank.com"),
    "phonepe": ("phonepe.com",),
    "gpay": ("google.com",),
    "bhim": ("bhimupi.org.in", "npci.org.in"),
    "aadhaar": ("uidai.gov.in",),
    "uidai": ("uidai.gov.in",),
    "incometax": ("incometax.gov.in", "incometaxindia.gov.in"),
    "epfo": ("epfindia.gov.in",),
    "amazon": ("amazon.com", "amazon.in", "amazon.co.uk"),
    "apple": ("apple.com",),
    "microsoft": ("microsoft.com", "live.com"),
    "netflix": ("netflix.com",),
    "facebook": ("facebook.com",),
    "instagram": ("instagram.com",),
    "whatsapp": ("whatsapp.com",),
    "twitter": ("twitter.com", "x.com"),
    "linkedin": ("linkedin.com",),
    "paypal": ("paypal.com",),
    "bankofamerica": ("bankofamerica.com",),
    "chase": ("chase.com",),
    "wellsfargo": ("wellsfargo.com",),
    "citibank": ("citibank.com", "citi.com"),
    "hsbc": ("hsbc.com", "hsbc.co.in"),
    "ebay": ("ebay.com", "ebay.in"),
    "dropbox": ("dropbox.com",),
    "icloud": ("icloud.com", "apple.com"),
    "outlook": ("outlook.com", "live.com", "microsoft.com"),
    "yahoo": ("yahoo.com",),
}

_HOMOGLYPH_PATTERN = re.compile(r"[0-9]")

_SUSPICIOUS_TLDS = frozenset(
    [
        "xyz", "top", "club", "work", "click", "link", "gq", "ml", "cf", "tk", "pw", "zip", "mov",
        "online", "site", "live", "icu", "buzz", "rest", "app", "bid", "vip", "monster", "fit", "surf", "casa"
    ]
)

_SUSPICIOUS_PATH_PATTERNS = re.compile(
    r"(?i)(login|signin|verify|verification|account|update|confirm|secure|banking|password|credential|suspend|kyc|otp|pan|aadhaar|claim|prize|lottery|winner|reward|cash|bill|cutoff|download|apk)",
)

_SUSPICIOUS_DOMAIN_KEYWORDS = re.compile(
    r"(?i)(prize|lottery|winner|reward|claim|bonus|cashback|kyc|pan|aadhaar|otp|banking|verify|verification|security|account-update|reactivate|suspend|cutoff|bill-pay|free-gift|lucky-draw)"
)

_SUBDOMAIN_THRESHOLD = 3


@dataclass
class AnalysisResult:
    url: str
    url_found: bool
    suspicious: bool
    risk_score: int
    risk_indicators: List[str] = field(default_factory=list)
    explanation: str = ""
    risk_level: str = "LOW"


def _check_ip_based(host: str) -> str | None:
    """Detect IP address used directly as host."""
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
    host_no_digits = _HOMOGLYPH_PATTERN.sub("", host_lower)

    for brand in _KNOWN_BRANDS:
        valid_domains = _OFFICIAL_BRAND_DOMAINS.get(brand, (f"{brand}.com",))
        is_official = any(host_lower == d or host_lower.endswith("." + d) for d in valid_domains)
        if is_official:
            continue

        if brand in host_lower:
            return f"Possible brand impersonation: '{brand}' in domain"

        if brand in host_no_digits and brand not in host_lower:
            return f"Possible homoglyph substitution targeting '{brand}'"

    return None


def _check_suspicious_domain_keywords(host: str) -> str | None:
    """Detect high-risk scam or financial fraud terms embedded in domain names."""
    host_lower = host.lower()
    if any(host_lower == d or host_lower.endswith("." + d) for d in ("wikipedia.org", "google.com", "gov.in", "nic.in")):
        return None
    if _SUSPICIOUS_DOMAIN_KEYWORDS.search(host_lower):
        return "Deceptive keywords in domain (prize/lottery/kyc/verify/bank)"
    return None


def _check_no_https(url: str) -> str | None:
    """Detect unencrypted HTTP connection on public websites."""
    u_lower = url.lower()
    if u_lower.startswith("http://"):
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if host not in ("localhost", "127.0.0.1"):
            return "Unencrypted connection (HTTP instead of HTTPS)"
    return None


def _check_excessive_subdomains(host: str) -> str | None:
    """Detect unusually deep subdomain structures."""
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
    tail = url[8:]
    if "http" in tail.lower():
        return "Embedded redirect URL detected"
    return None


def _check_at_symbol(url: str) -> str | None:
    """Detect @ symbol in URL used to spoof the displayed host."""
    parsed = urlparse(url)
    if "@" in (parsed.netloc or ""):
        return "@ symbol in URL (host spoofing technique)"
    return None


def _strip_query_for_output(url: str) -> str:
    """Return URL with query string and fragment removed for privacy-safe output."""
    parsed = urlparse(url)
    return parsed._replace(query="", fragment="").geturl()


def analyze_url(url: str) -> AnalysisResult:
    """Run all structural risk indicator checks against a single URL."""
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
            risk_level="LOW",
        )

    host = parsed.netloc or ""
    path = parsed.path or ""
    indicators: List[str] = []

    for check_fn, arg in [
        (_check_ip_based, host),
        (_check_shortener, host),
        (_check_suspicious_tld, host),
        (_check_misspelled_brand, host),
        (_check_suspicious_domain_keywords, host),
        (_check_excessive_subdomains, host),
        (_check_suspicious_path, path),
        (_check_no_https, url),
        (_check_long_url, url),
        (_check_multiple_redirects, url),
        (_check_at_symbol, url),
    ]:
        result = check_fn(arg)
        if result:
            indicators.append(result)

    risk_score = len(indicators)
    suspicious = risk_score >= 2

    is_high_risk = (
        any("IP address" in ind for ind in indicators)
        or any("brand impersonation" in ind.lower() for ind in indicators)
        or any("homoglyph" in ind.lower() for ind in indicators)
        or any("@ symbol" in ind.lower() for ind in indicators)
        or (any("deceptive keywords" in ind.lower() for ind in indicators) and risk_score >= 2)
        or risk_score >= 3
    )

    if is_high_risk:
        risk_level = "HIGH"
    elif suspicious or risk_score >= 1:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if risk_level == "LOW":
        explanation = "No suspicious characteristics were detected in this URL. The link appears legitimate."
    elif risk_level == "MEDIUM":
        explanation = (
            f"This link has characteristics requiring caution ({', '.join(indicators)}). "
            "Verify the destination before opening."
        )
    else:
        explanation = (
            f"High-risk indicators detected ({', '.join(indicators)}). "
            "This link shows patterns commonly associated with phishing or financial scams. Do not enter passwords or credentials."
        )

    return AnalysisResult(
        url=_strip_query_for_output(url),
        url_found=True,
        suspicious=suspicious,
        risk_score=risk_score,
        risk_indicators=indicators,
        explanation=explanation,
        risk_level=risk_level,
    )
