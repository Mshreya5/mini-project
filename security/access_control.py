"""Access Control and Authorization Rules.

Member 2 (Cybersecurity & Privacy) module.
Enforces:
1. Derivation of user identity exclusively from cryptographically verified tokens.
2. Complete rejection of client-supplied user IDs as proof of ownership.
3. Cross-user isolation rules (preventing User A from reading User B's records).
4. Response data filtering (guaranteeing password hashes and secrets never leak).
5. Granular consent permission gatekeeping before protected actions.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple
from security.auth_rules import decode_token
from security.consent import ConsentPreferences


class AccessDeniedError(Exception):
    """Raised when an unauthenticated or unauthorized access attempt is detected."""


def derive_identity_from_token(token: str, secret_key: str) -> str:
    """Derive user identity strictly from verified token claims.

    Args:
        token: Signed JWT access token.
        secret_key: Cryptographic HMAC key.

    Returns:
        str: Authenticated user ID (token 'sub' claim).

    Raises:
        AccessDeniedError: If token is missing, expired, revoked, or signature invalid.
    """
    if not token:
        raise AccessDeniedError("Authentication credentials not provided.")

    payload = decode_token(token, secret_key)
    if not payload:
        raise AccessDeniedError("Invalid, expired, or revoked authentication credentials.")

    user_id = payload.get("sub")
    if not user_id:
        raise AccessDeniedError("Malformed token credentials.")

    return str(user_id)


def enforce_resource_ownership(authenticated_user_id: str, resource_owner_id: str) -> bool:
    """Verify that the authenticated user is the legitimate owner of the requested resource.

    Args:
        authenticated_user_id: Identity derived from verified session token.
        resource_owner_id: Stored owner user_id of the database record.

    Returns:
        bool: True if ownership is valid.

    Raises:
        AccessDeniedError: If attempting to access another user's record.
    """
    if not authenticated_user_id or not resource_owner_id:
        raise AccessDeniedError("Ownership verification failed: missing identity parameters.")

    if str(authenticated_user_id) != str(resource_owner_id):
        raise AccessDeniedError("Unauthorized access: you do not have permission to access this record.")

    return True


def filter_user_profile(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Filter internal user document to guarantee sensitive security fields are never exposed.

    Guarantees:
    - password_hash, salts, and secret keys are stripped.
    """
    safe_fields = {"id", "email", "full_name", "is_active", "created_at"}
    return {k: v for k, v in user_data.items() if k in safe_fields and k != "password_hash"}


def verify_action_consent(
    preferences: ConsentPreferences,
    purpose: str,
) -> Tuple[bool, str]:
    """Gatekeeper enforcing that an action is backed by active, unrevoked consent.

    Args:
        preferences: Active consent choices of the authenticated user.
        purpose: Target processing purpose.

    Returns:
        Tuple[bool, str]: (is_permitted, denial_reason)
    """
    if purpose == "message_analysis":
        if not preferences.consent_message_analysis:
            return False, "Message analysis consent has been withdrawn. Enable it in privacy settings."
        return True, ""

    if purpose == "save_history":
        if not preferences.consent_save_history:
            return False, "History saving consent is not granted. Message results will not be saved."
        return True, ""

    if purpose == "analytics":
        if not preferences.consent_analytics:
            return False, "Threat analytics consent is not granted."
        return True, ""

    if purpose == "caregiver_sharing":
        if not preferences.consent_caregiver_sharing:
            return False, "Caregiver sharing consent is not granted or feature is pending team approval."
        return True, ""

    return False, f"Unknown processing purpose: {purpose}"
