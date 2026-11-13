"""Unit tests for the aggregation mechanism itself."""

from __future__ import annotations

import pytest

from app.core.models import Indicator
from app.core.risk_engine import RiskEngine, highest_level


def indicator(config, indicator_id: str) -> Indicator:
    resolved = config.resolve(indicator_id)
    assert resolved is not None
    return resolved


def assess(config, indicators, **overrides):
    engine = RiskEngine(config)
    context = {
        "prediction": "LEGITIMATE",
        "confidence": 0.1,
        "url_level": "NOT_APPLICABLE",
        "has_link": False,
    }
    context.update(overrides)
    return engine.assess(indicators, **context)


def test_no_indicators_is_low(risk_config) -> None:
    result = assess(risk_config, [])

    assert result.level == "LOW"
    assert result.score == 0


def test_single_medium_indicator_stays_low(risk_config) -> None:
    result = assess(risk_config, [indicator(risk_config, "URGENCY_PRESSURE")])

    assert result.score == risk_config.severity_points["MEDIUM"]
    assert result.level == "LOW"


def test_two_medium_indicators_reach_medium(risk_config) -> None:
    indicators = [
        indicator(risk_config, "URGENCY_PRESSURE"),
        indicator(risk_config, "IMPERSONATION"),
    ]

    result = assess(risk_config, indicators)

    assert result.level == "MEDIUM"


def test_per_module_cap_prevents_one_module_dominating(risk_config) -> None:
    indicators = [
        indicator(risk_config, "SCAM_PREDICTION"),
        indicator(risk_config, "OTP_REQUEST"),
        indicator(risk_config, "PAYMENT_REQUEST"),
        indicator(risk_config, "BANK_DETAILS_REQUEST"),
    ]

    result = assess(risk_config, indicators)

    assert result.raw_score == risk_config.severity_points["HIGH"] * 4
    assert result.score == risk_config.module_caps["message"]
    assert "message" in result.capped_sources


def test_decisive_indicators_add_no_points(risk_config) -> None:
    result = assess(
        risk_config,
        [indicator(risk_config, "MALICIOUS_URL")],
        url_level="MALICIOUS",
        has_link=True,
    )

    assert result.level == "HIGH"
    assert result.score == 0
    assert "OVR-02" in result.overrides
    assert all(
        contribution.indicator_id != "MALICIOUS_URL" for contribution in result.contributions
    )


def test_high_confidence_scam_override_needs_both_prediction_and_confidence(risk_config) -> None:
    below = assess(
        risk_config,
        [indicator(risk_config, "SCAM_PREDICTION")],
        prediction="SCAM",
        confidence=0.7,
    )
    above = assess(
        risk_config,
        [indicator(risk_config, "SCAM_PREDICTION")],
        prediction="SCAM",
        confidence=0.85,
    )

    assert "OVR-01" not in below.overrides
    assert below.level == "MEDIUM"
    assert "OVR-01" in above.overrides
    assert above.level == "HIGH"


def test_otp_with_link_override_requires_a_link(risk_config) -> None:
    without_link = assess(
        risk_config,
        [indicator(risk_config, "OTP_REQUEST")],
        has_link=False,
    )
    with_link = assess(
        risk_config,
        [indicator(risk_config, "OTP_REQUEST")],
        has_link=True,
        url_level="SAFE",
    )

    assert without_link.level == "MEDIUM"
    assert with_link.level == "HIGH"
    assert "OVR-03" in with_link.overrides
    assert any(item.id == "OTP_REQUEST_WITH_LINK" for item in with_link.indicators)


def test_degraded_floor_raises_low_to_medium(risk_config) -> None:
    result = assess(
        risk_config,
        [indicator(risk_config, "MESSAGE_ANALYSIS_UNAVAILABLE")],
        floor=risk_config.degraded_floor,
        degraded=True,
    )

    assert result.level == "MEDIUM"
    assert result.degraded is True


def test_degraded_reason_does_not_contradict_final_level(risk_config) -> None:
    """The audit trail must explain the returned level, not the pre-floor one."""
    result = assess(
        risk_config,
        [indicator(risk_config, "MESSAGE_ANALYSIS_UNAVAILABLE")],
        floor=risk_config.degraded_floor,
        degraded=True,
    )

    assert result.level == "MEDIUM"
    # The score sentence is about points only; the floor must be explained too,
    # otherwise the audit trail ends on "...maps to LOW" for a MEDIUM answer.
    assert any("raised to MEDIUM" in reason for reason in result.reasons)
    assert "raised to" in result.reasons[-1]


def test_threshold_boundaries_are_inclusive(risk_config) -> None:
    medium_threshold = risk_config.thresholds["medium"]
    high_threshold = risk_config.thresholds["high"]
    engine = RiskEngine(risk_config)

    assert engine._level_for_score(medium_threshold - 1) == "LOW"
    assert engine._level_for_score(medium_threshold) == "MEDIUM"
    assert engine._level_for_score(high_threshold - 1) == "MEDIUM"
    assert engine._level_for_score(high_threshold) == "HIGH"


@pytest.mark.parametrize(
    ("levels", "expected"),
    [
        (("LOW", "MEDIUM"), "MEDIUM"),
        (("HIGH", "MEDIUM"), "HIGH"),
        (("LOW", None), "LOW"),
        ((None, None), "LOW"),
    ],
)
def test_highest_level(levels, expected) -> None:
    assert highest_level(*levels) == expected
