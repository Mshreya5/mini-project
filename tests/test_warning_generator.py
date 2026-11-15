"""
Unit Tests for Elderly Warning and Action Generator
Member 4: Risk Aggregation, Warning Logic and System Integration
"""
from backend.warning_generator import WarningGenerator
from backend.schemas import OverallRiskLevel


def test_warning_generation_all_levels():
    """Verifies clear, non-intimidating warnings across all risk levels."""
    low_warn = WarningGenerator.generate_warning(OverallRiskLevel.LOW, [], "English")
    med_warn = WarningGenerator.generate_warning(OverallRiskLevel.MEDIUM, ["Suspicious element"], "English")
    high_warn = WarningGenerator.generate_warning(OverallRiskLevel.HIGH, ["Scam detected"], "English")

    assert "No major suspicious activity" in low_warn
    assert "Verify the sender" in med_warn
    assert "fraudulent" in high_warn or "Warning!" in high_warn


def test_multilingual_warnings():
    """Verifies warning generation in Hindi and Kannada."""
    hindi_warn = WarningGenerator.generate_warning(OverallRiskLevel.HIGH, [], "Hindi")
    kannada_warn = WarningGenerator.generate_warning(OverallRiskLevel.HIGH, [], "Kannada")

    assert "चेतावनी" in hindi_warn
    assert "ಎಚ್ಚರಿಕೆ" in kannada_warn


def test_recommended_actions_tailored():
    """Verifies tailored actions for URLs, OTPs, and financial pressure."""
    actions = WarningGenerator.generate_recommended_actions(
        overall_risk=OverallRiskLevel.HIGH,
        risk_indicators=["Urgent payment request", "Request for confidential OTP", "Suspicious URL"],
        has_url=True,
        language="English"
    )

    actions_text = " ".join(actions)
    assert any("link" in a.lower() for a in actions)
    assert any("otp" in a.lower() for a in actions)
    assert any("transfer" in a.lower() or "money" in a.lower() for a in actions)
    assert len(actions) >= 2


def test_recommended_actions_for_clean_message():
    """Low risk messages still receive gentle safety reminders."""
    actions = WarningGenerator.generate_recommended_actions(
        overall_risk=OverallRiskLevel.LOW,
        risk_indicators=[],
        has_url=False,
        language="English"
    )

    assert len(actions) >= 2
