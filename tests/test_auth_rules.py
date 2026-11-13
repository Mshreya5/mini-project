"""Tests for Authentication Rules, Rate Limiting, and Tokens.

Member 2 (Cybersecurity & Privacy) test suite.
"""

from __future__ import annotations

import time
import pytest
from security.auth_rules import (
    GENERIC_LOGIN_ERROR,
    GENERIC_REGISTRATION_ERROR,
    create_token,
    decode_token,
    generate_csrf_token,
    invalidate_token,
    is_token_blacklisted,
    rate_limiter,
    resist_timing_enumeration,
    validate_password_strength,
    verify_csrf_token,
)

SAMPLE_SECRET = "a_very_secure_test_secret_key_minimum_32_bytes_long_12345"
SAMPLE_CSRF_SECRET = "csrf_secret_key_minimum_32_bytes_long_67890"


def test_password_strength_validation():
    """Verify password strength validation rules."""
    # Valid password
    valid, msg = validate_password_strength("StrongPass123!")
    assert valid is True
    assert msg == ""

    # Too short (< 8 chars)
    valid, msg = validate_password_strength("Short1!")
    assert valid is False
    assert "at least 8 characters" in msg

    # No digits
    valid, msg = validate_password_strength("NoDigitsHere!")
    assert valid is False
    assert "both letters and numbers" in msg

    # No letters
    valid, msg = validate_password_strength("1234567890!")
    assert valid is False
    assert "both letters and numbers" in msg

    # Exceeding 128 characters
    valid, msg = validate_password_strength("A1" * 65)
    assert valid is False
    assert "must not exceed 128 characters" in msg

    # Empty
    valid, msg = validate_password_strength("")
    assert valid is False


def test_anti_enumeration_constants_and_timing():
    """Verify anti-enumeration error consistency and timing resistance padding."""
    assert GENERIC_LOGIN_ERROR == "Invalid email or password."
    assert "Unable to register account" in GENERIC_REGISTRATION_ERROR
    # Ensure timing padding executes without raising errors
    resist_timing_enumeration()


def test_sliding_window_rate_limiter():
    """Verify sliding-window rate limiting behavior."""
    rate_limiter.reset()
    key = "login:test_ip_127.0.0.1"

    # Allow up to 3 requests
    for _ in range(3):
        allowed, retry_after = rate_limiter.is_allowed(key, max_requests=3, window_seconds=60)
        assert allowed is True
        assert retry_after == 0

    # 4th request must be rejected
    blocked, retry_after = rate_limiter.is_allowed(key, max_requests=3, window_seconds=60)
    assert blocked is False
    assert retry_after > 0

    # Reset clears records
    rate_limiter.reset()
    allowed_again, _ = rate_limiter.is_allowed(key, max_requests=3, window_seconds=60)
    assert allowed_again is True


def test_jwt_issuance_and_decoding():
    """Verify token generation, signature validation, and claims parsing."""
    user_id = "user-uuid-12345"
    token = create_token(
        subject=user_id,
        secret_key=SAMPLE_SECRET,
        expires_minutes=30,
        claims={"role": "user"},
    )
    assert isinstance(token, str)

    # Decode with matching key
    payload = decode_token(token, SAMPLE_SECRET)
    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["role"] == "user"

    # Decoding with wrong key fails
    wrong_key = "different_secret_key_minimum_32_bytes_long_11111"
    assert decode_token(token, wrong_key) is None


def test_token_invalidation_and_blacklist():
    """Verify token revocation upon logout."""
    token = create_token(subject="user-uuid-logout", secret_key=SAMPLE_SECRET)
    assert decode_token(token, SAMPLE_SECRET) is not None
    assert is_token_blacklisted(token) is False

    # Invalidate token
    invalidate_token(token)
    assert is_token_blacklisted(token) is True
    # Decoding revoked token must return None
    assert decode_token(token, SAMPLE_SECRET) is None


def test_csrf_token_generation_and_constant_time_verification():
    """Verify CSRF token generation and tampering resistance."""
    session_id = "session-elderly-777"
    csrf = generate_csrf_token(session_id, SAMPLE_CSRF_SECRET)
    assert isinstance(csrf, str)
    assert len(csrf) == 64  # SHA256 hex digest length

    # Valid verification
    assert verify_csrf_token(csrf, session_id, SAMPLE_CSRF_SECRET) is True

    # Tampered token
    tampered_csrf = csrf[:-4] + "ffff"
    assert verify_csrf_token(tampered_csrf, session_id, SAMPLE_CSRF_SECRET) is False

    # Mismatched session
    assert verify_csrf_token(csrf, "different-session-999", SAMPLE_CSRF_SECRET) is False
