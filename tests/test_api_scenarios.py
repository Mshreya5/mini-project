"""End to end scenarios required by the project brief."""

from __future__ import annotations

from app.core.models import ModuleState

from tests.conftest import (
    message_ok,
    module_failure,
    post_analyze,
    url_ok,
)


def test_legitimate_message_is_low_risk(build_client) -> None:
    client, _, _ = build_client(message_ok("LEGITIMATE", 0.04), url_ok("SAFE"))

    response = post_analyze(
        client, {"message": "Hi, I will bring the groceries at 6 pm as usual."}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["overall_risk"] == "LOW"
    assert body["status"] == "OK"
    assert body["message_prediction"] == "LEGITIMATE"
    assert body["url_risk"] == "NOT_APPLICABLE"
    assert body["risk_indicators"] == []
    assert body["warning"] == "No major suspicious activity was detected. Stay cautious."
    assert body["recommended_actions"]
    assert body["score"]["total"] == 0


def test_high_confidence_scam_with_otp_request_is_high_risk(build_client) -> None:
    client, _, _ = build_client(
        message_ok("SCAM", 0.94, ("urgency", "otp_request")), url_ok("SAFE")
    )

    response = post_analyze(
        client,
        {
            "message": (
                "URGENT: your account will be blocked today. Reply with the OTP "
                "sent to your phone to keep it active."
            )
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["overall_risk"] == "HIGH"
    assert body["url_risk"] == "NOT_APPLICABLE"
    assert "OVR-01" in body["score"]["applied_overrides"]
    assert any("Very high confidence" in item for item in body["risk_indicators"])
    assert any("OTP" in item for item in body["risk_indicators"])
    assert body["warning"].startswith("Warning!")
    assert any("Never share an OTP" in action for action in body["recommended_actions"])
    assert any("Do not transfer money" in action for action in body["recommended_actions"])


def test_message_with_suspicious_url_is_medium_risk(build_client) -> None:
    client, scam_client, url_client = build_client(
        message_ok("LEGITIMATE", 0.2),
        url_ok("SUSPICIOUS", ("shortened", "no_https")),
    )

    response = post_analyze(
        client,
        {"message": "Your parcel is held. Confirm here: http://bit.ly/parcel-due"},
    )

    body = response.json()
    assert response.status_code == 200
    assert body["overall_risk"] == "MEDIUM"
    assert body["status"] == "OK"
    assert body["url_risk"] == "SUSPICIOUS"
    assert body["analysed_url"] == "http://bit.ly/"
    assert any("shortened" in item.lower() for item in body["risk_indicators"])
    assert any("suspicious characteristics" in item for item in body["risk_indicators"])
    assert "Do not click the link." in " ".join(body["recommended_actions"])
    assert url_client.calls == ["http://bit.ly/parcel-due"]
    assert scam_client.calls and "parcel" in scam_client.calls[0]


def test_otp_request_with_link_escalates_to_high(build_client) -> None:
    client, _, _ = build_client(
        message_ok("LEGITIMATE", 0.55, ("otp_request",)), url_ok("SAFE")
    )

    response = post_analyze(
        client,
        {"message": "Share the verification code at https://verify-account.xyz/login"},
    )

    body = response.json()
    assert body["overall_risk"] == "HIGH"
    assert "OVR-03" in body["score"]["applied_overrides"]
    assert any("OTP is requested together" in item for item in body["risk_indicators"])


def test_message_without_url_skips_url_module(build_client) -> None:
    client, _, url_client = build_client(
        message_ok("LEGITIMATE", 0.05), module_failure(ModuleState.UNAVAILABLE)
    )

    response = post_analyze(client, {"message": "See you at the temple on Sunday."})

    body = response.json()
    assert body["url_risk"] == "NOT_APPLICABLE"
    assert body["status"] == "OK"
    url_status = next(
        item for item in body["module_status"] if item["name"] == "url_analyzer"
    )
    assert url_status["state"] == "SKIPPED"
    assert url_status["failed"] is False
    assert url_client.calls == []


def test_explicit_url_field_is_analysed_and_redacted(build_client) -> None:
    client, _, url_client = build_client(
        message_ok("LEGITIMATE", 0.1), url_ok("MALICIOUS")
    )

    response = post_analyze(
        client,
        {
            "message": "Please review the attached invoice.",
            "url": "https://bank-secure.login-verify.xyz/pay?token=abc123",
        },
    )

    body = response.json()
    assert url_client.calls == ["https://bank-secure.login-verify.xyz/pay?token=abc123"]
    assert body["analysed_url"] == "https://bank-secure.login-verify.xyz/"
    assert body["overall_risk"] == "HIGH"
    assert "OVR-02" in body["score"]["applied_overrides"]


def test_scam_module_timeout_never_returns_low(build_client) -> None:
    client, _, _ = build_client(
        module_failure(ModuleState.TIMEOUT, "scam_detector did not answer within 1s"),
        url_ok("SAFE"),
    )

    response = post_analyze(client, {"message": "Your refund is ready for collection."})

    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "DEGRADED"
    assert body["overall_risk"] == "MEDIUM"
    assert body["message_prediction"] == "UNKNOWN"
    assert any(
        "could not be checked for scam patterns" in item
        for item in body["risk_indicators"]
    )
    assert "could not finish" in body["warning"]
    failed = [item for item in body["module_status"] if item["failed"]]
    assert failed and failed[0]["state"] == "TIMEOUT"


def test_url_module_failure_never_returns_low(build_client) -> None:
    client, _, _ = build_client(
        message_ok("LEGITIMATE", 0.15),
        module_failure(ModuleState.HTTP_ERROR, "url_analyzer returned HTTP 503"),
    )

    response = post_analyze(
        client, {"message": "Open this link to reschedule: https://example.com/reschedule"}
    )

    body = response.json()
    assert body["overall_risk"] == "MEDIUM"
    assert body["status"] == "DEGRADED"
    assert body["url_risk"] == "UNKNOWN"
    assert any("Link safety could not be checked" in item for item in body["risk_indicators"])


def test_both_modules_failing_stays_degraded(build_client) -> None:
    client, _, _ = build_client(
        module_failure(ModuleState.UNAVAILABLE, "scam_detector is unreachable"),
        module_failure(ModuleState.UNAVAILABLE, "url_analyzer is unreachable"),
    )

    response = post_analyze(client, {"message": "Pay here now: https://pay-me.xyz/"})

    body = response.json()
    assert body["status"] == "DEGRADED"
    assert body["overall_risk"] in ("MEDIUM", "HIGH")
    assert body["message_prediction"] == "UNKNOWN"
    assert body["url_risk"] == "UNKNOWN"
    assert all(
        item["failed"] for item in body["module_status"] if item["name"] != "risk_engine"
    )


def test_empty_message_is_rejected(build_client) -> None:
    client, scam_client, _ = build_client(message_ok(), url_ok())

    response = post_analyze(client, {"message": "   "})

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "invalid_request"
    assert body["details"]
    assert scam_client.calls == []


def test_missing_message_field_is_rejected(build_client) -> None:
    client, _, _ = build_client(message_ok(), url_ok())

    response = client.post("/api/v1/analyze", json={"url": "https://example.com"})

    assert response.status_code == 422
    assert response.json()["error"] == "invalid_request"


def test_unsupported_url_scheme_is_rejected(build_client) -> None:
    client, _, _ = build_client(message_ok(), url_ok())

    response = post_analyze(
        client, {"message": "click here", "url": "ftp://example.com/file"}
    )

    assert response.status_code == 422
    assert "url" in {item["field"] for item in response.json()["details"]}


def test_health_and_risk_config_are_exposed(build_client) -> None:
    client, _, _ = build_client(message_ok(), url_ok())

    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    config = client.get("/api/v1/risk-config")
    payload = config.json()
    assert config.status_code == 200
    assert payload["thresholds"]["high"] > payload["thresholds"]["medium"]
    assert any(rule["id"] == "OVR-01" for rule in payload["overrides"])


def test_response_shape_matches_the_agreed_contract(build_client) -> None:
    client, _, _ = build_client(
        message_ok("SCAM", 0.91, ("bank_details",)), url_ok("SUSPICIOUS", ("lookalike",))
    )

    body = post_analyze(
        client,
        {"message": "Send your card details at https://secure-bankk.com/verify"},
    ).json()

    for field in (
        "overall_risk",
        "message_prediction",
        "url_risk",
        "risk_indicators",
        "warning",
        "recommended_actions",
    ):
        assert field in body
    assert body["overall_risk"] == "HIGH"
    assert 1 <= len(body["recommended_actions"]) <= 4
