"""Tests for Privacy-Preserving Logging and Data Handling.

Member 2 (Cybersecurity & Privacy) test suite.
"""

from __future__ import annotations

import logging
from security.privacy import (
    MAX_MESSAGE_PAYLOAD_BYTES,
    SensitiveDataRedactingFilter,
    prepare_history_record,
    sanitize_text,
    validate_payload_size,
)


def test_sanitize_text_redacts_credentials_and_tokens():
    """Verify that passwords and authorization tokens are redacted."""
    payload = '{"username": "elderly_user", "password": "MySuperSecret123!"}'
    cleaned = sanitize_text(payload)
    assert "MySuperSecret123!" not in cleaned
    assert "[REDACTED_SECRET]" in cleaned

    bearer_string = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy.sig"
    cleaned_bearer = sanitize_text(bearer_string)
    assert "eyJhbGci" not in cleaned_bearer
    assert "[REDACTED_TOKEN]" in cleaned_bearer


def test_sanitize_text_redacts_banking_cards_and_otp():
    """Verify that credit card numbers and OTP codes are redacted."""
    card_log = "Payment processed with card number 4111 2222 3333 4444 on gateway"
    cleaned_card = sanitize_text(card_log)
    assert "4111 2222 3333 4444" not in cleaned_card
    assert "[REDACTED_CARD_NUMBER]" in cleaned_card

    otp_log = "Sent verification OTP: 739102 to mobile"
    cleaned_otp = sanitize_text(otp_log)
    assert "739102" not in cleaned_otp
    assert "[REDACTED_OTP]" in cleaned_otp


def test_sanitize_text_redacts_phone_numbers_and_message_content():
    """Verify phone numbers and raw message contents in logs are sanitized."""
    phone_log = "User contact phone is +1-800-555-0199"
    cleaned_phone = sanitize_text(phone_log)
    assert "+1-800-555-0199" not in cleaned_phone
    assert "[REDACTED_PHONE]" in cleaned_phone

    raw_msg_log = '{"message": "Urgent: Your account is suspended! Send $500 gift card immediately"}'
    cleaned_msg = sanitize_text(raw_msg_log)
    assert "Send $500 gift card" not in cleaned_msg
    assert "[MESSAGE_CONTENT_NOT_LOGGED_FOR_PRIVACY]" in cleaned_msg


def test_redacting_logger_filter():
    """Verify that logging.Filter intercepts and sanitizes record messages."""
    test_logger = logging.getLogger("test_redaction_logger")
    test_logger.setLevel(logging.INFO)
    test_filter = SensitiveDataRedactingFilter()
    test_logger.addFilter(test_filter)

    class CapturingHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records = []

        def emit(self, record):
            self.records.append(record.getMessage())

    handler = CapturingHandler()
    test_logger.addHandler(handler)

    test_logger.info("User login attempt with password=%s", "RawSecretPassword123")

    assert len(handler.records) == 1
    emitted = handler.records[0]
    assert "RawSecretPassword123" not in emitted
    assert "[REDACTED_SECRET]" in emitted


def test_payload_size_validation():
    """Verify payload size constraint enforcement."""
    # Within 64 KiB
    valid, msg = validate_payload_size(1024)
    assert valid is True
    assert msg == ""

    # Exceeding 64 KiB
    invalid, msg = validate_payload_size(MAX_MESSAGE_PAYLOAD_BYTES + 500)
    assert invalid is False
    assert "exceeds limit" in msg


def test_history_record_contains_zero_raw_message_text():
    """Verify Privacy by Design: history record stores ONLY risk metadata, never raw message text."""
    sample_text = "URGENT: Win 1,000,000 USD! Click http://phish-scam.xyz right now!"
    record = prepare_history_record(
        user_id="user-999",
        message_type="sms",
        risk_level="high",
        risk_score=0.92,
    )

    assert record["user_id"] == "user-999"
    assert record["message_type"] == "sms"
    assert record["risk_level"] == "high"
    assert record["risk_score"] == 0.92
    assert "created_at" in record

    # CRITICAL: Confirm raw text does NOT exist anywhere in the record
    assert "content" not in record
    assert "text" not in record
    assert sample_text not in str(record)
