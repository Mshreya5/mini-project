"""
Integration and End-to-End API Test Suite
Member 4: Risk Aggregation, Warning Logic and System Integration

Covers all 7 required evaluation scenarios:
1. Legitimate messages
2. Scam messages
3. Messages containing suspicious URLs
4. Messages containing OTP requests
5. Messages with no URLs
6. API failures and timeouts
7. Invalid inputs
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import requests

from backend.main import app
from backend.schemas import OverallRiskLevel

client = TestClient(app)


# ---------------- SCENARIO 1: Legitimate Message ----------------

def test_scenario_1_legitimate_message():
    """Scenario 1: Normal friendly message returns LOW risk."""
    payload = {
        "message": "Hi grandpa, dinner is ready at 7:30 PM. See you soon!",
        "sender": "+919876543210",
        "language": "English"
    }

    # Simulate Member 2 and Member 3 live responses
    with patch("backend.integrations.requests.post") as mock_post:
        # Member 2 returns LEGITIMATE
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "prediction": "LEGITIMATE",
            "confidence": 0.96,
            "detected_triggers": []
        }

        response = client.post("/api/v1/assess", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["overall_risk"] == "LOW"
        assert data["message_prediction"] == "LEGITIMATE"
        assert data["url_risk"] == "NO_URL"
        assert "No major suspicious activity" in data["warning"]
        assert len(data["recommended_actions"]) >= 2
        assert data["risk_score"] < 0.35


# ---------------- SCENARIO 2: Scam Message ----------------

def test_scenario_2_scam_message():
    """Scenario 2: High-urgency financial scam returns HIGH risk."""
    payload = {
        "message": "URGENT NOTICE: Your SBI netbanking account is suspended. Update KYC now or funds will be lost permanently.",
        "language": "English"
    }

    with patch("backend.integrations.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "prediction": "SCAM",
            "confidence": 0.94,
            "detected_triggers": ["Urgent deadline pressure", "Bank impersonation"]
        }

        response = client.post("/api/v1/assess", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["overall_risk"] == "HIGH"
        assert data["message_prediction"] == "SCAM"
        assert "fraudulent" in data["warning"].lower() or "warning!" in data["warning"].lower()
        assert len(data["risk_indicators"]) >= 2
        assert data["risk_score"] >= 0.70


# ---------------- SCENARIO 3: Message Containing Suspicious URL ----------------

def test_scenario_3_message_with_suspicious_url():
    """Scenario 3: Message containing a shortened or suspicious link."""
    payload = {
        "message": "Claim your free Rs 5000 Diwali gift card right now at http://bit.ly/claim-diwali-gift-2026",
        "language": "English"
    }

    def mock_requests_post(url, *args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                if "predict" in url:
                    return {
                        "prediction": "SCAM",
                        "confidence": 0.85,
                        "detected_triggers": ["Unsolicited prize lure"]
                    }
                else:
                    return {
                        "urls_found": ["http://bit.ly/claim-diwali-gift-2026"],
                        "url_risk": "SUSPICIOUS",
                        "indicators": ["Masked/Shortened URL hiding destination"],
                        "privacy_redacted": True
                    }
        return MockResponse()

    with patch("backend.integrations.requests.post", side_effect=mock_requests_post):
        response = client.post("/api/v1/assess", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["overall_risk"] == "HIGH"
        assert data["url_risk"] == "SUSPICIOUS"
        assert any("link" in a.lower() for a in data["recommended_actions"])
        assert any("url" in ind.lower() or "shortened" in ind.lower() for ind in data["risk_indicators"])


# ---------------- SCENARIO 4: Message Containing OTP Request ----------------

def test_scenario_4_message_with_otp_request():
    """Scenario 4: Request asking for OTP / verification code returns HIGH risk."""
    payload = {
        "message": "Bank officer alert: Your verification code is 492019. Tell this code to our caller to prevent card blockage.",
        "language": "English"
    }

    with patch("backend.integrations.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "prediction": "SCAM",
            "confidence": 0.88,
            "detected_triggers": ["OTP harvesting", "Authority impersonation"]
        }

        response = client.post("/api/v1/assess", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["overall_risk"] == "HIGH"
        assert any("otp" in ind.lower() for ind in data["risk_indicators"])
        assert any("otp" in a.lower() for a in data["recommended_actions"])


# ---------------- SCENARIO 5: Message With No URLs ----------------

def test_scenario_5_message_with_no_urls():
    """Scenario 5: Message with no URLs handles url_risk gracefully as NO_URL."""
    payload = {
        "message": "Auntie, please transfer 2000 rupees to my GPay number urgently. My car broke down.",
        "language": "English"
    }

    with patch("backend.integrations.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "prediction": "SUSPICIOUS",
            "confidence": 0.65,
            "detected_triggers": ["Financial pressure"]
        }

        response = client.post("/api/v1/assess", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["url_risk"] == "NO_URL"
        assert data["overall_risk"] in ["MEDIUM", "HIGH"]
        assert any("transfer" in a.lower() or "money" in a.lower() for a in data["recommended_actions"])


# ---------------- SCENARIO 6: API Failures and Timeouts (Fail-Safe) ----------------

def test_scenario_6_api_failure_and_timeout_resilience():
    """
    Scenario 6: If Member 2 or Member 3 APIs fail or time out,
    the system MUST NOT classify the message as safe.
    """
    payload = {
        "message": "Notice regarding your pending electricity bill at http://power-pay-bill.com",
        "language": "English"
    }

    with patch("backend.integrations.requests.post", side_effect=requests.exceptions.Timeout("API Timeout")):
        response = client.post("/api/v1/assess", json=payload)
        assert response.status_code == 200
        data = response.json()

        # Must fail safe: NOT LOW RISK!
        assert data["overall_risk"] != "LOW"
        assert data["overall_risk"] in ["MEDIUM", "HIGH"]
        assert data["message_prediction"] == "UNVERIFIED"
        assert data["url_risk"] == "UNVERIFIED"
        assert data["module_status"]["ml_service"] == "OFFLINE_FALLBACK"
        assert data["module_status"]["url_service"] == "OFFLINE_FALLBACK"
        assert any("offline" in ind.lower() or "unreachable" in ind.lower() for ind in data["risk_indicators"])


# ---------------- SCENARIO 7: Invalid Input Handling ----------------

def test_scenario_7_invalid_input_empty_message():
    """Scenario 7a: Empty message rejected with 422 Unprocessable Entity."""
    response = client.post("/api/v1/assess", json={"message": ""})
    assert response.status_code == 422


def test_scenario_7_invalid_input_whitespace_only():
    """Scenario 7b: Whitespace only message rejected with 422."""
    response = client.post("/api/v1/assess", json={"message": "    \n\t  "})
    assert response.status_code == 422


def test_scenario_7_invalid_input_missing_field():
    """Scenario 7c: Missing message field rejected with 422."""
    response = client.post("/api/v1/assess", json={"sender": "+919999999999"})
    assert response.status_code == 422


# ---------------- Response Contract Verification ----------------

def test_response_schema_exact_match():
    """Verifies all required keys in the final JSON response."""
    payload = {
        "message": "Hello, is this the correct address?",
        "language": "English"
    }

    with patch("backend.integrations.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "prediction": "LEGITIMATE",
            "confidence": 0.95,
            "detected_triggers": []
        }

        response = client.post("/api/v1/assess", json=payload)
        assert response.status_code == 200
        data = response.json()

        required_fields = [
            "overall_risk",
            "message_prediction",
            "url_risk",
            "risk_indicators",
            "warning",
            "recommended_actions",
            "risk_score",
            "module_status",
            "timestamp"
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
