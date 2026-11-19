from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from ai_module.api.main import app as ai_app
from url_analysis.api import app as url_app
from app.main import create_app
from app.settings import Settings, get_risk_config
from app.clients.scam_detector import ScamDetectorClient
from app.clients.url_analyzer import UrlAnalyzerClient


@pytest.fixture(scope="module")
def integrated_client():
    ai_client = TestClient(ai_app, base_url="http://127.0.0.1:8001")
    url_client_session = TestClient(url_app, base_url="http://127.0.0.1:8002")

    settings = Settings(
        scam_api_url="http://127.0.0.1:8001/predict",
        url_api_url="http://127.0.0.1:8002/analyze-url",
        request_timeout_seconds=2.0,
        max_retries=0,
    )
    config = get_risk_config()

    scam_client = ScamDetectorClient(settings, session=ai_client)
    url_client = UrlAnalyzerClient(settings, session=url_client_session)

    app = create_app(
        settings=settings,
        config=config,
        scam_client=scam_client,
        url_client=url_client,
    )
    return TestClient(app)


def test_scenario_1_normal_legitimate_message(integrated_client):
    resp = integrated_client.post(
        "/api/v1/analyze",
        json={"message": "Hi grandpa, I am coming over for dinner at 7 pm tonight."},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_risk"] == "LOW"
    assert data["message_prediction"] == "LEGITIMATE"
    assert data["url_risk"] == "NOT_APPLICABLE"
    assert data["status"] == "OK"
    assert "No major suspicious activity" in data["warning"]


def test_scenario_2_scam_message_without_url(integrated_client):
    resp = integrated_client.post(
        "/api/v1/analyze",
        json={
            "message": "Congratulations! You have won a cash lottery prize of 50000. Claim your reward immediately."
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_risk"] in ("MEDIUM", "HIGH")
    assert data["message_prediction"] == "SCAM"
    assert data["url_risk"] == "NOT_APPLICABLE"
    assert any("prize" in ind.lower() or "scam" in ind.lower() for ind in data["risk_indicators"])


def test_scenario_3_legitimate_message_with_safe_url(integrated_client):
    resp = integrated_client.post(
        "/api/v1/analyze",
        json={
            "message": "Read the morning news updates at https://www.google.com/news when you have time."
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_risk"] == "LOW"
    assert data["url_risk"] == "SAFE"
    assert data["message_prediction"] == "LEGITIMATE"


def test_scenario_4_scam_message_with_suspicious_url(integrated_client):
    resp = integrated_client.post(
        "/api/v1/analyze",
        json={
            "message": "URGENT: Your account is locked. Verify at http://192.168.1.1/login or bit.ly/unlock"
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_risk"] == "HIGH"
    assert data["url_risk"] in ("SUSPICIOUS", "MALICIOUS")
    assert data["analysed_url"] is not None


def test_scenario_5_otp_request(integrated_client):
    resp = integrated_client.post(
        "/api/v1/analyze",
        json={
            "message": "Dear customer, share the OTP sent to your mobile with the bank manager to cancel transaction."
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_risk"] in ("MEDIUM", "HIGH")
    assert any("otp" in ind.lower() for ind in data["risk_indicators"])
    assert any("otp" in act.lower() for act in data["recommended_actions"])


def test_scenario_6_urgent_payment_threat_suspension(integrated_client):
    resp = integrated_client.post(
        "/api/v1/analyze",
        json={
            "message": "FINAL NOTICE: Your electricity connection will be suspended. Pay immediately via transfer."
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_risk"] in ("MEDIUM", "HIGH")
    assert any("payment" in ind.lower() or "threat" in ind.lower() for ind in data["risk_indicators"])


def test_scenario_7_invalid_or_empty_input(integrated_client):
    resp = integrated_client.post("/api/v1/analyze", json={"message": "   "})
    assert resp.status_code == 422
    data = resp.json()
    assert data["error"] == "invalid_request"


def test_scenario_8_borderline_message(integrated_client):
    resp = integrated_client.post(
        "/api/v1/analyze",
        json={"message": "Can you check if you received the document I sent earlier?"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["overall_risk"] == "LOW"
    assert data["status"] == "OK"


def test_scenario_9_url_service_unavailable():
    class BrokenUrlSession:
        def post(self, url, **kwargs):
            import httpx
            return httpx.Response(503, text="Service Unavailable", request=httpx.Request("POST", url))

    ai_client = TestClient(ai_app, base_url="http://127.0.0.1:8001")

    settings = Settings(
        scam_api_url="http://127.0.0.1:8001/predict",
        url_api_url="http://127.0.0.1:8002/analyze-url",
        request_timeout_seconds=0.5,
        max_retries=0,
    )
    config = get_risk_config()
    scam_client = ScamDetectorClient(settings, session=ai_client)
    url_client = UrlAnalyzerClient(settings, session=BrokenUrlSession())

    app = create_app(
        settings=settings,
        config=config,
        scam_client=scam_client,
        url_client=url_client,
    )
    client = TestClient(app)

    resp = client.post("/api/v1/analyze", json={"message": "Please review this link: https://example.com/doc"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "DEGRADED"
    assert data["overall_risk"] != "LOW"
    assert data["url_risk"] == "UNKNOWN"


def test_scenario_10_ai_ml_service_unavailable():
    class BrokenScamSession:
        def post(self, url, **kwargs):
            import httpx
            return httpx.Response(500, text="Internal Server Error", request=httpx.Request("POST", url))

    url_client_session = TestClient(url_app, base_url="http://127.0.0.1:8002")

    settings = Settings(
        scam_api_url="http://127.0.0.1:8001/predict",
        url_api_url="http://127.0.0.1:8002/analyze-url",
        request_timeout_seconds=0.5,
        max_retries=0,
    )
    config = get_risk_config()
    scam_client = ScamDetectorClient(settings, session=BrokenScamSession())
    url_client = UrlAnalyzerClient(settings, session=url_client_session)

    app = create_app(
        settings=settings,
        config=config,
        scam_client=scam_client,
        url_client=url_client,
    )
    client = TestClient(app)

    resp = client.post("/api/v1/analyze", json={"message": "Hello, how are you doing today?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "DEGRADED"
    assert data["overall_risk"] != "LOW"
    assert data["message_prediction"] == "UNKNOWN"
