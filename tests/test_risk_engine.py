"""
Unit Tests for Risk Aggregation Engine
Member 4: Risk Aggregation, Warning Logic and System Integration
"""
import pytest
from backend.risk_engine import RiskAggregationEngine
from backend.schemas import OverallRiskLevel, MessagePrediction, URLRiskLevel


@pytest.fixture
def engine():
    return RiskAggregationEngine()


def test_clean_legitimate_message(engine):
    """Test 1: Legitimate message with no suspicious indicators produces LOW risk."""
    message = "Hi Grandma, dinner is ready at 7 PM. See you soon!"
    result = engine.aggregate_risk(
        message=message,
        ml_prediction=MessagePrediction.LEGITIMATE.value,
        ml_confidence=0.95,
        ml_triggers=[],
        ml_available=True,
        url_risk=URLRiskLevel.NO_URL.value,
        url_indicators=[],
        urls_found=[],
        url_available=True
    )

    assert result["overall_risk"] == OverallRiskLevel.LOW
    assert result["composite_score"] < 0.35
    assert len(result["risk_indicators"]) == 0


def test_high_confidence_scam_message(engine):
    """Test 2: High confidence scam prediction triggers HIGH risk escalation."""
    message = "URGENT: Your SBI account is suspended! Update KYC immediately."
    result = engine.aggregate_risk(
        message=message,
        ml_prediction=MessagePrediction.SCAM.value,
        ml_confidence=0.92,
        ml_triggers=["Urgent deadline pressure", "Bank impersonation"],
        ml_available=True,
        url_risk=URLRiskLevel.NO_URL.value,
        url_indicators=[],
        urls_found=[],
        url_available=True
    )

    assert result["overall_risk"] == OverallRiskLevel.HIGH
    assert result["composite_score"] >= 0.70
    assert "Urgent deadline pressure" in result["risk_indicators"]


def test_malicious_url_override(engine):
    """Test 3: Malicious URL escalates overall risk to HIGH even if text seems benign."""
    message = "Click here for account update: http://192.168.1.100/login"
    result = engine.aggregate_risk(
        message=message,
        ml_prediction=MessagePrediction.LEGITIMATE.value,
        ml_confidence=0.60,
        ml_triggers=[],
        ml_available=True,
        url_risk=URLRiskLevel.MALICIOUS.value,
        url_indicators=["Direct IP address used in link"],
        urls_found=["http://192.168.1.100/login"],
        url_available=True
    )

    assert result["overall_risk"] == OverallRiskLevel.HIGH
    assert result["composite_score"] >= 0.70


def test_otp_credential_theft_escalation(engine):
    """Test 4: OTP or password solicitation escalates to HIGH risk."""
    message = "Dear customer, your OTP is 948271. Share it with our executive to avoid account block."
    result = engine.aggregate_risk(
        message=message,
        ml_prediction=MessagePrediction.SUSPICIOUS.value,
        ml_confidence=0.65,
        ml_triggers=["Credential request"],
        ml_available=True,
        url_risk=URLRiskLevel.NO_URL.value,
        url_indicators=[],
        urls_found=[],
        url_available=True
    )

    assert result["overall_risk"] == OverallRiskLevel.HIGH
    assert any("OTP" in ind for ind in result["risk_indicators"])


def test_single_suspicious_indicator_yields_medium(engine):
    """Test 5: Single moderate indicator yields MEDIUM risk."""
    message = "Please check our seasonal discount at http://bit.ly/festive-deal"
    result = engine.aggregate_risk(
        message=message,
        ml_prediction=MessagePrediction.LEGITIMATE.value,
        ml_confidence=0.80,
        ml_triggers=[],
        ml_available=True,
        url_risk=URLRiskLevel.SUSPICIOUS.value,
        url_indicators=["Shortened link"],
        urls_found=["http://bit.ly/festive-deal"],
        url_available=True
    )

    assert result["overall_risk"] == OverallRiskLevel.MEDIUM
    assert 0.35 <= result["composite_score"] <= 0.70


def test_service_unavailability_fails_safe(engine):
    """Test 6: When ML or URL service is unavailable, message is NEVER classified as safe."""
    message = "Important update regarding your account at http://unknown-link.com"
    result = engine.aggregate_risk(
        message=message,
        ml_prediction=MessagePrediction.UNVERIFIED.value,
        ml_confidence=0.50,
        ml_triggers=[],
        ml_available=False,
        url_risk=URLRiskLevel.UNVERIFIED.value,
        url_indicators=[],
        urls_found=["http://unknown-link.com"],
        url_available=False
    )

    # Must be at least MEDIUM (fail-safe principle)
    assert result["overall_risk"] in [OverallRiskLevel.MEDIUM, OverallRiskLevel.HIGH]
    assert result["overall_risk"] != OverallRiskLevel.LOW
    assert any("unavailable" in ind for ind in result["risk_indicators"])
