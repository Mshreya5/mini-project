"""Member 2: Cybersecurity and Privacy Module Interface.

Provides reusable security and privacy logic for Member 4's backend integration:
- Argon2id password hashing and constant-time verification (`security.passwords`)
- Authentication validation, sliding-window rate limiting, and JWT tokens (`security.auth_rules`)
- Granular consent management and elderly transparency notices (`security.consent`)
- Privacy-preserving log sanitization and payload limits (`security.privacy`)
- Token identity derivation and resource ownership access control (`security.access_control`)
"""

from security.access_control import (
    AccessDeniedError,
    derive_identity_from_token,
    enforce_resource_ownership,
    filter_user_profile,
    verify_action_consent,
)
from security.auth_rules import (
    GENERIC_LOGIN_ERROR,
    GENERIC_REGISTRATION_ERROR,
    SlidingWindowRateLimiter,
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
from security.consent import (
    ConsentAuditEntry,
    ConsentPreferences,
    ConsentRecord,
    can_process_message,
    can_save_history,
    can_share_caregiver,
    create_default_consent,
    get_elderly_transparency_notices,
    record_consent_update,
)
from security.passwords import hash_password, needs_rehash, verify_password
from security.privacy import (
    MAX_MESSAGE_PAYLOAD_BYTES,
    SensitiveDataRedactingFilter,
    prepare_history_record,
    sanitize_text,
    setup_secure_logging,
    validate_payload_size,
)

__all__ = [
    # Passwords
    "hash_password",
    "verify_password",
    "needs_rehash",
    # Auth Rules
    "validate_password_strength",
    "resist_timing_enumeration",
    "SlidingWindowRateLimiter",
    "rate_limiter",
    "create_token",
    "decode_token",
    "invalidate_token",
    "is_token_blacklisted",
    "generate_csrf_token",
    "verify_csrf_token",
    "GENERIC_LOGIN_ERROR",
    "GENERIC_REGISTRATION_ERROR",
    # Consent
    "ConsentPreferences",
    "ConsentRecord",
    "ConsentAuditEntry",
    "create_default_consent",
    "record_consent_update",
    "get_elderly_transparency_notices",
    "can_process_message",
    "can_save_history",
    "can_share_caregiver",
    # Privacy
    "sanitize_text",
    "SensitiveDataRedactingFilter",
    "setup_secure_logging",
    "validate_payload_size",
    "prepare_history_record",
    "MAX_MESSAGE_PAYLOAD_BYTES",
    # Access Control
    "AccessDeniedError",
    "derive_identity_from_token",
    "enforce_resource_ownership",
    "filter_user_profile",
    "verify_action_consent",
]
