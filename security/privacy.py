"""Privacy-Preserving Data Handling and Redaction Rules.

Member 2 (Cybersecurity & Privacy) module.
Enforces Privacy by Design:
1. Scrubbing of PII, passwords, tokens, OTPs, cards, and raw message text from application logs.
2. In-memory processing rules ensuring original messages are discarded after analysis.
3. Payload size constraints (64 KiB) to prevent memory exhaustion DoS.
4. History metadata sanitization guaranteeing raw text is never persisted.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

MAX_MESSAGE_PAYLOAD_BYTES = 65536  # 64 KiB limit

# High-performance regular expression patterns for sensitive data redaction
REDACTION_PATTERNS = [
    # Passwords in JSON / query params / key-value format (quoted or unquoted)
    (
        re.compile(r'(?i)(["\']?(?:password|pwd|pass|secret|csrf_token)["\']?\s*[:=]\s*["\']?)([^"\'\s&,;{}]+)(["\']?)'),
        r"\g<1>[REDACTED_SECRET]\g<3>",
    ),
    # Authorization header / Bearer tokens / JWT format
    (
        re.compile(r'(?i)(Bearer\s+)[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_.+/=]*'),
        r"\g<1>[REDACTED_TOKEN]",
    ),
    # Credit Card Numbers (13 to 19 digits with optional hyphens or spaces)
    (
        re.compile(r'\b(?:\d[ -]*?){13,19}\b'),
        r"[REDACTED_CARD_NUMBER]",
    ),
    # OTP / 2FA Verification Codes
    (
        re.compile(r'(?i)\b(?:otp|one[- ]time[- ]passcode|pin|verification[- ]code)\s*[:=]?\s*(\d{4,8})\b'),
        r"[REDACTED_OTP]",
    ),
    # Email addresses (partially mask to preserve diagnostic ability: a***@domain.com)
    (
        re.compile(r'\b([A-Za-z0-9._%+-])[A-Za-z0-9._%+-]*(@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b'),
        r"\g<1>***\g<2>",
    ),
    # Phone numbers (international and local formats)
    (
        re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'),
        r"[REDACTED_PHONE]",
    ),
    # Raw message content in JSON payload logging
    (
        re.compile(r'(?i)(["\']?(?:message|content|text|sms_body)["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])'),
        r"\g<1>[MESSAGE_CONTENT_NOT_LOGGED_FOR_PRIVACY]\g<3>",
    ),
]


def sanitize_text(text: str) -> str:
    """Sanitize any arbitrary string, scrubbing all sensitive personal information."""
    if not isinstance(text, str):
        text = str(text)

    sanitized = text
    for pattern, replacement in REDACTION_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized


class SensitiveDataRedactingFilter(logging.Filter):
    """Logging filter that scrubs sensitive PII, credentials, and message text from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            # Format msg with args first so pattern matching catches formatted credentials
            formatted = record.getMessage()
            record.msg = sanitize_text(formatted)
            record.args = ()
        except Exception:
            if isinstance(record.msg, str):
                record.msg = sanitize_text(record.msg)
        return True


def setup_secure_logging() -> None:
    """Configure root logger with privacy-preserving redaction filter."""
    redacting_filter = SensitiveDataRedactingFilter()
    root_logger = logging.getLogger()
    if not any(isinstance(f, SensitiveDataRedactingFilter) for f in root_logger.filters):
        root_logger.addFilter(redacting_filter)


def validate_payload_size(content_length_bytes: Optional[int]) -> Tuple[bool, str]:
    """Validate incoming payload size against maximum permitted threshold (64 KiB)."""
    if content_length_bytes is None:
        return True, ""
    if content_length_bytes > MAX_MESSAGE_PAYLOAD_BYTES:
        return False, f"Request payload ({content_length_bytes} bytes) exceeds limit of {MAX_MESSAGE_PAYLOAD_BYTES} bytes."
    return True, ""


def prepare_history_record(
    user_id: str,
    message_type: str,
    risk_level: str,
    risk_score: float,
) -> Dict[str, Any]:
    """Generate a privacy-compliant analysis history record.

    Guarantees Privacy by Design:
    - Retains ONLY risk metadata for the user's dashboard.
    - Raw SMS or email text is NEVER included in this record.
    """
    return {
        "user_id": str(user_id),
        "message_type": str(message_type).lower(),
        "risk_level": str(risk_level).lower(),
        "risk_score": round(float(risk_score), 4),
        "created_at": datetime.now(timezone.utc),
    }
