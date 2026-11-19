"""Tests for Access Control and Authorization Rules.

Member 2 (Cybersecurity & Privacy) test suite.
"""

from __future__ import annotations

import pytest
from security.access_control import (
    AccessDeniedError,
    derive_identity_from_token,
    enforce_resource_ownership,
    filter_user_profile,
    verify_action_consent,
)
from security.auth_rules import create_token, invalidate_token
from security.consent import ConsentPreferences

SAMPLE_SECRET = "access_control_test_secret_key_minimum_32_bytes_12345"


def test_derive_identity_from_valid_token():
    """Verify identity derivation extracts subject from valid token."""
    user_id = "user-alice-100"
    token = create_token(subject=user_id, secret_key=SAMPLE_SECRET)
    derived_id = derive_identity_from_token(token, SAMPLE_SECRET)
    assert derived_id == user_id


def test_derive_identity_from_invalid_token_fails():
    """Verify invalid or empty token raises AccessDeniedError."""
    with pytest.raises(AccessDeniedError, match="credentials not provided"):
        derive_identity_from_token("", SAMPLE_SECRET)

    with pytest.raises(AccessDeniedError, match="Invalid, expired, or revoked"):
        derive_identity_from_token("invalid.token.structure", SAMPLE_SECRET)


def test_derive_identity_from_revoked_token_fails():
    """Verify revoked/logged-out token raises AccessDeniedError."""
    user_id = "user-bob-200"
    token = create_token(subject=user_id, secret_key=SAMPLE_SECRET)
    invalidate_token(token)

    with pytest.raises(AccessDeniedError, match="Invalid, expired, or revoked"):
        derive_identity_from_token(token, SAMPLE_SECRET)


def test_resource_ownership_enforcement():
    """Verify that resource ownership checks pass for legitimate owner and block cross-user access."""
    owner_id = "user-alice-100"
    other_user_id = "user-mallory-666"

    # Legitimate owner
    assert enforce_resource_ownership(owner_id, owner_id) is True

    # Cross-user unauthorized access attempt
    with pytest.raises(AccessDeniedError, match="Unauthorized access"):
        enforce_resource_ownership(authenticated_user_id=other_user_id, resource_owner_id=owner_id)


def test_user_profile_filtering():
    """Verify that sensitive fields (password_hash) are stripped from public responses."""
    internal_doc = {
        "id": "user-123",
        "email": "senior@example.com",
        "password_hash": "$argon2id$v=19$m=65536,t=2,p=1$secret_hash",
        "full_name": "Senior User",
        "is_active": True,
        "internal_salt": "do_not_leak",
    }
    filtered = filter_user_profile(internal_doc)

    assert filtered["id"] == "user-123"
    assert filtered["email"] == "senior@example.com"
    assert filtered["full_name"] == "Senior User"
    assert filtered["is_active"] is True
    # CRITICAL: Verify secret fields are excluded
    assert "password_hash" not in filtered
    assert "internal_salt" not in filtered


def test_action_consent_verification():
    """Verify action gatekeeping enforces active consent."""
    prefs = ConsentPreferences(
        consent_message_analysis=True,
        consent_save_history=False,
        consent_analytics=False,
        consent_caregiver_sharing=False,
    )

    # Message analysis permitted
    allowed, _ = verify_action_consent(prefs, "message_analysis")
    assert allowed is True

    # Save history blocked without consent
    allowed, reason = verify_action_consent(prefs, "save_history")
    assert allowed is False
    assert "not granted" in reason

    # Caregiver sharing blocked without consent
    allowed, reason = verify_action_consent(prefs, "caregiver_sharing")
    assert allowed is False
    assert "not granted" in reason

    # Message analysis blocked if revoked
    revoked_prefs = ConsentPreferences(consent_message_analysis=False)
    allowed, reason = verify_action_consent(revoked_prefs, "message_analysis")
    assert allowed is False
    assert "withdrawn" in reason
