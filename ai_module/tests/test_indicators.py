import pytest
from ai_module.src.warning_indicators import (
    WarningIndicatorDetector,
    detect_detailed_indicators,
    detect_suspicious_indicators,
)


@pytest.fixture
def detector():
    return WarningIndicatorDetector()


def test_urgent_payment_indicator(detector):
    msg = "Please transfer money immediately to settle your overdue parcel fee."
    indicators = detector.extract_indicators(msg)
    assert "Urgent payment request" in indicators

    msg_crypto = "Pay with bitcoin or buy google play card now."
    assert "Urgent payment request" in detector.extract_indicators(msg_crypto)


def test_otp_request_indicator(detector):
    msg = "Please reply with your OTP to confirm your security code."
    indicators = detector.extract_indicators(msg)
    assert "OTP request" in indicators


def test_fake_lottery_prize_indicator(detector):
    msg = "Congratulations! You have been selected as the lottery winner of £5000 cash. Claim your prize!"
    indicators = detector.extract_indicators(msg)
    assert "Fake lottery or prize" in indicators


def test_bank_impersonation_indicator(detector):
    msg = "Barclays Bank Alert: Unauthorized activity detected on your debit card. Contact fraud team."
    indicators = detector.extract_indicators(msg)
    assert "Bank impersonation" in indicators


def test_suspicious_account_verification_indicator(detector):
    msg = "Click here to verify your account credentials and update your profile."
    indicators = detector.extract_indicators(msg)
    assert "Suspicious account verification" in indicators


def test_threatening_account_suspension_indicator(detector):
    msg = "Final warning: Your account has been suspended due to security risks. Act within 24 hours."
    indicators = detector.extract_indicators(msg)
    assert "Threatening account suspension" in indicators


def test_suspicious_link_indicator(detector):
    msg1 = "Verify here: https://secure-bank-login.xyz/verify"
    assert "Suspicious link" in detector.extract_indicators(msg1)

    msg2 = "Check details at bit.ly/3xyz45"
    assert "Suspicious link" in detector.extract_indicators(msg2)


def test_benign_messages_do_not_trigger_false_indicators(detector):
    msg_school = "Grandma, I won a prize at school today for reading books!"
    ind_school = detector.extract_indicators(msg_school)
    assert "OTP request" not in ind_school
    assert "Urgent payment request" not in ind_school

    msg_bank = "We are having a picnic near the river bank."
    ind_bank = detector.extract_indicators(msg_bank)
    assert len(ind_bank) == 0

    msg_family = "Hi Mum, when are you arriving tomorrow? Let me know if you need anything."
    assert len(detector.extract_indicators(msg_family)) == 0


def test_empty_or_none_handling(detector):
    assert detector.extract_indicators("") == []
    assert detector.extract_indicators("   ") == []
    assert detector.extract_indicators(None) == []
