"""Tests for URL Analysis API endpoints.

Member 3: Privacy, Cybersecurity and URL Analysis.
"""

from __future__ import annotations

from fastapi.testclient import TestClient
from app import app

client = TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# /analyze-url
# ---------------------------------------------------------------------------

def test_analyze_clean_message_no_urls():
    resp = client.post("/analyze-url", json={"message": "Hello, how are you?", "consent_given": True})
    assert resp.status_code == 200
    data = resp.json()
    assert data["urls_found"] is False
    assert data["url_count"] == 0
    assert data["results"] == []


def test_analyze_message_with_suspicious_url():
    resp = client.post(
        "/analyze-url",
        json={"message": "Click here: http://192.168.1.1/login/verify", "consent_given": True},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["urls_found"] is True
    assert data["url_count"] == 1
    result = data["results"][0]
    assert result["suspicious"] is True
    assert len(result["risk_indicators"]) >= 2


def test_analyze_message_with_clean_url():
    resp = client.post(
        "/analyze-url",
        json={"message": "Read the news at https://www.bbc.co.uk/news", "consent_given": True},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["urls_found"] is True
    result = data["results"][0]
    assert result["suspicious"] is False


def test_consent_denied_returns_403():
    resp = client.post(
        "/analyze-url",
        json={"message": "https://example.com", "consent_given": False},
    )
    assert resp.status_code == 403


def test_blank_message_returns_422():
    resp = client.post("/analyze-url", json={"message": "   ", "consent_given": True})
    assert resp.status_code == 422


def test_missing_message_field_returns_422():
    resp = client.post("/analyze-url", json={"consent_given": True})
    assert resp.status_code == 422


def test_response_never_contains_raw_message():
    """Raw message text must never appear in the API response."""
    secret_text = "URGENT WIN PRIZE secret_marker_xyz"
    resp = client.post(
        "/analyze-url",
        json={"message": f"{secret_text} https://prize-win.xyz/claim", "consent_given": True},
    )
    assert resp.status_code == 200
    assert "secret_marker_xyz" not in resp.text


def test_query_string_not_in_response():
    """Query parameters must be stripped from URLs in the response."""
    resp = client.post(
        "/analyze-url",
        json={"message": "https://example.com/page?token=supersecret", "consent_given": True},
    )
    assert resp.status_code == 200
    assert "supersecret" not in resp.text


def test_privacy_note_present_in_response():
    resp = client.post("/analyze-url", json={"message": "https://example.com", "consent_given": True})
    assert resp.status_code == 200
    assert "privacy_note" in resp.json()


def test_multiple_urls_all_analysed():
    resp = client.post(
        "/analyze-url",
        json={
            "message": "Visit https://bit.ly/abc or https://www.google.com",
            "consent_given": True,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["url_count"] == 2


# ---------------------------------------------------------------------------
# /privacy-info
# ---------------------------------------------------------------------------

def test_privacy_info_returns_all_fields():
    resp = client.get("/privacy-info")
    assert resp.status_code == 200
    data = resp.json()
    assert "what_is_processed" in data
    assert "why_it_is_processed" in data
    assert "how_data_is_protected" in data
    assert "data_retention" in data
    assert isinstance(data["how_data_is_protected"], list)
    assert len(data["how_data_is_protected"]) >= 3


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

def test_health_check():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
