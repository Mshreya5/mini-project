"""Unit tests for warning and action generation."""

from __future__ import annotations

from app.core.warnings import build_actions, build_warning, describe_indicators


def indicators(config, *ids):
    resolved = [config.resolve(indicator_id) for indicator_id in ids]
    return [item for item in resolved if item is not None]


def test_warning_text_per_level(risk_config) -> None:
    assert build_warning(risk_config, "LOW") == risk_config.warnings["LOW"]
    assert "Verify the sender" in build_warning(risk_config, "MEDIUM")
    assert build_warning(risk_config, "HIGH").startswith("Warning!")


def test_degraded_warning_is_different_and_honest(risk_config) -> None:
    normal = build_warning(risk_config, "MEDIUM")
    degraded = build_warning(risk_config, "MEDIUM", degraded=True)

    assert degraded != normal
    assert "could not finish" in degraded


def test_actions_are_prioritised_deduplicated_and_capped(risk_config) -> None:
    actions = build_actions(
        risk_config,
        "HIGH",
        indicators(risk_config, "MALICIOUS_URL", "OTP_REQUEST", "PAYMENT_REQUEST"),
    )

    assert len(actions) <= risk_config.max_actions
    assert len(actions) == len(set(actions))
    assert actions[0] == risk_config.actions["NEVER_SHARE_OTP"]
    assert any("Do not click the link" in action for action in actions)


def test_low_risk_gets_one_gentle_action(risk_config) -> None:
    actions = build_actions(risk_config, "LOW", [])

    assert actions == [risk_config.actions["KEEP_CAUTIOUS"]]


def test_actions_follow_the_indicators_that_fired(risk_config) -> None:
    actions = build_actions(
        risk_config, "MEDIUM", indicators(risk_config, "SHORTENED_URL")
    )

    assert risk_config.actions["DO_NOT_CLICK_LINK"] in actions


def test_describe_indicators_returns_unique_labels(risk_config) -> None:
    labels = describe_indicators(
        indicators(risk_config, "OTP_REQUEST", "OTP_REQUEST", "URGENCY_PRESSURE")
    )

    assert labels == [
        risk_config.indicators["OTP_REQUEST"].label,
        risk_config.indicators["URGENCY_PRESSURE"].label,
    ]
