"""Adapter for Member 3's URL analysis API.

Contract (see docs/contracts.md):

    POST <URL_API_URL>   {"url": "https://..."}
    -> 200 {"url_risk": "SAFE" | "SUSPICIOUS" | "MALICIOUS",
            "flags": ["shortened", "ip_address", "lookalike", "no_https"],
            "score": 0.0-1.0}

All URL reputation work stays in Member 3's module. This adapter only maps their
verdict and flags onto the shared indicator vocabulary.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.clients.base import JsonApiClient
from app.clients.parsing import (
    as_bool,
    as_confidence,
    as_text_list,
    first_present,
    normalise_token,
)
from app.core.models import (
    ModuleState,
    URL_MALICIOUS,
    URL_SAFE,
    URL_SUSPICIOUS,
    URL_UNKNOWN,
    RemoteCallResult,
    UrlAnalysis,
)
from app.settings import Settings

_LEVEL_KEYS = (
    "url_risk",
    "risk_level",
    "risk",
    "verdict",
    "classification",
    "level",
    "label",
)
_FLAG_KEYS = (
    "flags",
    "reasons",
    "indicators",
    "signals",
    "red_flags",
    "findings",
    "issues",
)

_MALICIOUS_LABELS = {
    "malicious",
    "phishing",
    "dangerous",
    "danger",
    "unsafe",
    "critical",
    "high",
    "high_risk",
    "blacklisted",
    "malware",
}
_SUSPICIOUS_LABELS = {
    "suspicious",
    "warning",
    "medium",
    "moderate",
    "risky",
    "potentially_suspicious",
    "unverified",
}
_SAFE_LABELS = {"safe", "clean", "benign", "low", "ok", "legitimate", "trusted", "whitelisted"}


def normalise_level(value: Any) -> str:
    """Map a member's verdict onto SAFE / SUSPICIOUS / MALICIOUS / UNKNOWN."""
    token = normalise_token(value if isinstance(value, str) else str(value))
    if token in _MALICIOUS_LABELS:
        return URL_MALICIOUS
    if token in _SUSPICIOUS_LABELS:
        return URL_SUSPICIOUS
    if token in _SAFE_LABELS:
        return URL_SAFE
    return URL_UNKNOWN


def parse_url_payload(payload: Mapping[str, Any], url: str) -> UrlAnalysis | None:
    results = payload.get("results")
    if isinstance(results, list):
        if not results:
            return UrlAnalysis(level=URL_SAFE, flags=(), url=url, score=0.0)
        first = results[0]
        if isinstance(first, dict):
            raw_suspicious = first.get("suspicious", False)
            risk_score = int(first.get("risk_score", 0))
            raw_risk_level = str(first.get("risk_level", "")).upper()
            indicators_text = " ".join(str(i).lower() for i in first.get("risk_indicators", []))

            if (
                raw_risk_level == "HIGH"
                or risk_score >= 2
                or "ip address" in indicators_text
                or "brand impersonation" in indicators_text
                or "deceptive keywords" in indicators_text
            ):
                raw_level = URL_MALICIOUS
            elif raw_risk_level == "MEDIUM" or raw_suspicious or risk_score >= 1:
                raw_level = URL_SUSPICIOUS
            else:
                raw_level = URL_SAFE

            flags = []
            for ind in first.get("risk_indicators", []):
                ind_lower = str(ind).lower()
                if "ip address" in ind_lower:
                    flags.append("ip_address")
                elif "shortener" in ind_lower:
                    flags.append("shortened")
                elif "brand impersonation" in ind_lower or "homoglyph" in ind_lower or "subdomain" in ind_lower or "deceptive keywords" in ind_lower:
                    flags.append("lookalike")
                elif "top-level domain" in ind_lower:
                    flags.append("suspicious_tld")
                elif "path keywords" in ind_lower:
                    flags.append("phishing_keywords")
                elif "redirect" in ind_lower:
                    flags.append("redirect")
                elif "at symbol" in ind_lower:
                    flags.append("lookalike")
                elif "unencrypted" in ind_lower or "http" in ind_lower:
                    flags.append("no_https")

            parsed_url = str(first.get("url", url))
            if parsed_url.startswith("http://") and "no_https" not in flags:
                flags.append("no_https")

            return UrlAnalysis(
                level=raw_level,
                flags=tuple(flags),
                url=url,
                score=min(1.0, round(risk_score * 0.25, 4)),
            )

    raw_level = first_present(payload, _LEVEL_KEYS)

    flags = list(as_text_list(first_present(payload, _FLAG_KEYS)))

    if as_bool(first_present(payload, ("is_shortened", "shortened", "uses_shortener"))) and (
        "shortened" not in flags
    ):
        flags.append("shortened")
    if as_bool(first_present(payload, ("is_ip_address", "ip_address", "uses_ip"))) and (
        "ip_address" not in flags
    ):
        flags.append("ip_address")
    if as_bool(first_present(payload, ("lookalike", "is_lookalike", "typosquatting"))) and (
        "lookalike" not in flags
    ):
        flags.append("lookalike")
    https = as_bool(first_present(payload, ("is_https", "https", "has_https")))
    if https is False and "no_https" not in flags:
        flags.append("no_https")

    if raw_level is None:
        if as_bool(first_present(payload, ("is_malicious", "malicious"))) is True:
            raw_level = URL_MALICIOUS
        elif as_bool(first_present(payload, ("is_suspicious", "suspicious"))) is True:
            raw_level = URL_SUSPICIOUS
        elif as_bool(first_present(payload, ("is_safe", "safe"))) is True:
            raw_level = URL_SAFE

    if raw_level is None:
        return None

    level = normalise_level(raw_level)
    if level == URL_UNKNOWN:
        return None

    return UrlAnalysis(
        level=level,
        flags=tuple(flags),
        url=url,
        score=as_confidence(first_present(payload, ("score", "risk_score", "confidence"))),
    )


class UrlAnalyzerClient:
    """Calls Member 3's URL endpoint and normalises the response."""

    module_name = "url_analyzer"

    def __init__(self, settings: Settings, session: Any | None = None) -> None:
        self._http = JsonApiClient(
            name=self.module_name,
            endpoint=settings.url_api_url,
            timeout_seconds=settings.request_timeout_seconds,
            max_retries=settings.max_retries,
            session=session,
        )

    def analyze(self, url: str) -> RemoteCallResult[UrlAnalysis]:
        result = self._http.post({"message": url, "url": url, "consent_given": True})
        if result.state is not ModuleState.OK or result.data is None:
            return RemoteCallResult(
                state=result.state,
                detail=result.detail,
                latency_ms=result.latency_ms,
            )

        analysis = parse_url_payload(result.data, url)
        if analysis is None:
            return RemoteCallResult(
                state=ModuleState.INVALID_RESPONSE,
                detail="URL analysis response did not contain a recognised risk level",
                latency_ms=result.latency_ms,
            )

        return RemoteCallResult(
            state=ModuleState.OK, data=analysis, latency_ms=result.latency_ms
        )
