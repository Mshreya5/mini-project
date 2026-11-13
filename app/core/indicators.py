"""Translation of module outputs into the indicator catalogue.

Member 2 reports a prediction with an optional set of signal tokens. Member 3
reports a URL verdict with optional flags. Neither vocabulary is hard coded
here: both are mapped to rule-set indicator ids through ``config/risk_config.json``
so a new token from either member is a config change, not a code change.
"""

from __future__ import annotations

from app.core.models import (
    PREDICTION_SCAM,
    URL_MALICIOUS,
    URL_SUSPICIOUS,
    Indicator,
    MessageAnalysis,
    UrlAnalysis,
)
from app.settings import RiskConfig


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def message_indicator_ids(
    config: RiskConfig, message: MessageAnalysis
) -> list[str]:
    """Indicators implied by Member 2's prediction and signal tokens."""
    ids: list[str] = []
    threshold = config.scam_confidence["prediction_threshold"]
    high_confidence = config.scam_confidence["high_confidence"]
    confidence = message.confidence

    if message.prediction == PREDICTION_SCAM and (
        confidence is None or confidence >= threshold
    ):
        ids.append("SCAM_PREDICTION")

    if (
        message.prediction == PREDICTION_SCAM
        and confidence is not None
        and confidence >= high_confidence
    ):
        ids.append("HIGH_CONFIDENCE_SCAM")

    for signal in message.signals:
        mapped = config.signal_map.get(signal)
        if mapped and mapped in config.indicators:
            ids.append(mapped)

    return _unique(ids)


def url_indicator_ids(config: RiskConfig, url: UrlAnalysis | None) -> list[str]:
    """Indicators implied by Member 3's verdict and flags."""
    if url is None:
        return []

    ids: list[str] = []
    if url.level == URL_MALICIOUS:
        ids.append("MALICIOUS_URL")
    elif url.level == URL_SUSPICIOUS:
        ids.append("SUSPICIOUS_URL")

    for flag in url.flags:
        mapped = config.url_flag_map.get(flag)
        if mapped and mapped in config.indicators:
            ids.append(mapped)

    return _unique(ids)


def build_indicators(
    config: RiskConfig,
    *,
    message: MessageAnalysis | None = None,
    url: UrlAnalysis | None = None,
    message_unavailable: bool = False,
    url_unavailable: bool = False,
) -> list[Indicator]:
    """Full indicator list for one analysis, before override rules are applied."""
    ids: list[str] = []

    if message_unavailable:
        ids.append("MESSAGE_ANALYSIS_UNAVAILABLE")
    elif message is not None:
        ids.extend(message_indicator_ids(config, message))

    if url_unavailable:
        ids.append("URL_ANALYSIS_UNAVAILABLE")
    elif url is not None:
        ids.extend(url_indicator_ids(config, url))

    indicators: list[Indicator] = []
    for indicator_id in _unique(ids):
        indicator = config.resolve(indicator_id)
        if indicator is not None:
            indicators.append(indicator)
    return indicators
