"""Authentication Security Rules and Session Protection.

Member 2 (Cybersecurity & Privacy) module.
Provides:
1. Server-side password strength validation (elderly-accessible rules).
2. Anti-enumeration defense (generic error constants and timing equalizers).
3. In-memory sliding-window rate limiter for brute-force defense.
4. JWT token generation, signature decoding, and revocation blacklist.
5. Cryptographic CSRF token generation and constant-time verification.
"""

from __future__ import annotations

import hashlib
import hmac
import re
import time
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple
import jwt
from security.passwords import verify_password

# Standard anti-enumeration messages
GENERIC_LOGIN_ERROR = "Invalid email or password."
GENERIC_REGISTRATION_ERROR = (
    "Unable to register account with the provided details. Please check your credentials or log in."
)

# In-memory revocation cache for invalidated tokens (token_str -> expiration_timestamp)
_token_blacklist: Dict[str, float] = {}


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validate password complexity.

    Rules designed to balance security and usability for elderly users:
    - Minimum 8 characters.
    - Maximum 128 characters (prevents CPU exhaustion attacks).
    - Must contain at least one letter and at least one digit.
    """
    if not password or not isinstance(password, str):
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if len(password) > 128:
        return False, "Password must not exceed 128 characters."
    has_letter = bool(re.search(r"[A-Za-z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    if not (has_letter and has_digit):
        return False, "Password must contain both letters and numbers."
    return True, ""


def resist_timing_enumeration() -> None:
    """Execute a dummy password verification cycle to mitigate timing-based user enumeration.

    Ensures response time for non-existent accounts mirrors that of existing accounts.
    """
    verify_password(
        "dummy_password_timing_pad",
        "$argon2id$v=19$m=65536,t=2,p=1$c29tZXNhbHQ$R01Wb3JhZGl1bVNhbHQ",
    )


class SlidingWindowRateLimiter:
    """In-memory sliding-window rate limiter to mitigate credential stuffing and brute-force attacks."""

    def __init__(self) -> None:
        self._records: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> Tuple[bool, int]:
        """Check if request is permitted under rate limit.

        Args:
            key: Unique identifier (e.g. action + client IP).
            max_requests: Maximum allowed attempts in window.
            window_seconds: Sliding window duration in seconds.

        Returns:
            Tuple[bool, int]: (is_allowed, retry_after_seconds)
        """
        now = time.time()
        cutoff = now - window_seconds

        # Clean timestamps older than the sliding window
        valid_timestamps = [t for t in self._records[key] if t > cutoff]
        self._records[key] = valid_timestamps

        if len(valid_timestamps) >= max_requests:
            oldest_timestamp = valid_timestamps[0]
            retry_after = max(1, int(oldest_timestamp + window_seconds - now))
            return False, retry_after

        self._records[key].append(now)
        return True, 0

    def reset(self) -> None:
        """Clear all rate limit records (for testing or administrative resets)."""
        self._records.clear()


rate_limiter = SlidingWindowRateLimiter()


def create_token(
    subject: str,
    secret_key: str,
    expires_minutes: int = 60,
    claims: Optional[Dict[str, Any]] = None,
    algorithm: str = "HS256",
) -> str:
    """Issue a signed JWT access token."""
    if not secret_key or len(secret_key) < 32:
        raise ValueError("Secret key must be at least 32 bytes for secure HMAC-SHA256 signing.")

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)

    payload: Dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if claims:
        payload.update(claims)

    return jwt.encode(payload, secret_key, algorithm=algorithm)


def decode_token(
    token: str,
    secret_key: str,
    algorithm: str = "HS256",
) -> Optional[Dict[str, Any]]:
    """Decode and validate a signed JWT token, verifying signature, expiration, and blacklist status."""
    if not token or is_token_blacklisted(token):
        return None

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
            options={"require": ["sub", "exp", "iat"]},
        )
        return payload
    except jwt.PyJWTError:
        return None


def invalidate_token(token: str) -> None:
    """Add a token to the in-memory blacklist to support immediate revocation upon logout."""
    _purge_expired_tokens()
    try:
        unverified = jwt.decode(token, options={"verify_signature": False})
        exp = float(unverified.get("exp", time.time() + 3600))
    except Exception:
        exp = time.time() + 3600

    _token_blacklist[token] = exp


def is_token_blacklisted(token: str) -> bool:
    """Check if token is currently blacklisted/revoked."""
    _purge_expired_tokens()
    return token in _token_blacklist


def _purge_expired_tokens() -> None:
    """Remove naturally expired tokens from blacklist cache to prevent unbounded memory growth."""
    now = time.time()
    expired = [t for t, exp in _token_blacklist.items() if exp < now]
    for t in expired:
        _token_blacklist.pop(t, None)


def generate_csrf_token(session_id: str, csrf_secret: str) -> str:
    """Generate an HMAC-SHA256 CSRF token tied to a session identifier."""
    if not csrf_secret or len(csrf_secret) < 32:
        raise ValueError("CSRF secret key must be at least 32 bytes.")
    message = f"csrf:{session_id}".encode("utf-8")
    return hmac.new(csrf_secret.encode("utf-8"), message, hashlib.sha256).hexdigest()


def verify_csrf_token(token: str, session_id: str, csrf_secret: str) -> bool:
    """Verify CSRF token in constant time to prevent timing attacks."""
    if not token or not session_id or not csrf_secret:
        return False
    expected = generate_csrf_token(session_id, csrf_secret)
    return hmac.compare_digest(token, expected)
