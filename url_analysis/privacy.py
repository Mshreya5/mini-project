"""Privacy protection layer for URL analysis.

Member 3: Privacy, Cybersecurity and URL Analysis.

Responsibilities:
- Consent enforcement before any message processing.
- Input validation and payload size guard.
- Message sanitization: strips PII before passing text to extractor.
- Ensures no raw message text is logged or stored.
"""

from __future__ import annotations

import re
from typing import Tuple

MAX_MESSAGE_BYTES = 65536  # 64 KiB — consistent with Member 2's privacy module

# Patterns to strip obvious PII from message text before URL extraction.
# We only need to remove PII; URLs must be preserved for analysis.
_PII_PATTERNS = [
    # Phone numbers
    re.compile(r"\b(?:\+?\d{1,3}[.\-\s]?)?\(?\d{3}\)?[.\-\s]?\d{3}[.\-\s]?\d{4}\b"),
    # Credit card numbers (13–19 digits with optional separators)
    re.compile(r"\b(?:\d[ \-]?){13,19}\b"),
    # Email addresses
    re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
]

_PII_PLACEHOLDER = "[REDACTED]"


def check_consent(consent_given: bool) -> Tuple[bool, str]:
    """Verify that the user has given consent for message analysis.

    Args:
        consent_given: Boolean flag from the request payload.

    Returns:
        Tuple[bool, str]: (is_permitted, denial_reason)
    """
    if not consent_given:
        return False, (
            "Message analysis requires your consent. "
            "Please enable safety analysis in your privacy settings."
        )
    return True, ""


def validate_message(message: str) -> Tuple[bool, str]:
    """Validate message type, length, and encoding.

    Args:
        message: Raw message string from the request.

    Returns:
        Tuple[bool, str]: (is_valid, error_detail)
    """
    if not isinstance(message, str):
        return False, "Message must be a text string."
    if not message.strip():
        return False, "Message must not be blank."
    byte_length = len(message.encode("utf-8"))
    if byte_length > MAX_MESSAGE_BYTES:
        return False, f"Message exceeds maximum allowed size of {MAX_MESSAGE_BYTES} bytes."
    return True, ""


def sanitize_message_for_extraction(message: str) -> str:
    """Strip PII from message text while preserving URLs for extraction.

    Phone numbers, email addresses, and card numbers are replaced with
    [REDACTED] so they are never passed downstream or logged.
    URLs are intentionally preserved because they are the analysis target.

    Args:
        message: Raw message text.

    Returns:
        Sanitized message string safe to pass to the URL extractor.
    """
    sanitized = message
    for pattern in _PII_PATTERNS:
        sanitized = pattern.sub(_PII_PLACEHOLDER, sanitized)
    return sanitized


def get_privacy_info() -> dict:
    """Return structured plain-language privacy disclosure for the /privacy-info endpoint."""
    return {
        "what_is_processed": (
            "When you submit a message for safety checking, the text is temporarily "
            "held in server memory solely to extract and analyse any web links (URLs) it contains."
        ),
        "why_it_is_processed": (
            "URLs are checked for structural characteristics associated with phishing and scam links "
            "(e.g. IP-based addresses, URL shorteners, misspelled brand names) "
            "to help protect you from online fraud."
        ),
        "how_data_is_protected": [
            "Your message is processed entirely in memory — it is never written to a database or log file.",
            "Personal information (phone numbers, email addresses, card numbers) is removed from the "
            "message before any URL extraction takes place.",
            "Query strings are stripped from URLs before they appear in any API response.",
            "No third-party services or external HTTP requests are used during URL analysis.",
            "Analysis results contain only risk indicators and scores — never your original message text.",
        ],
        "data_retention": (
            "Message text is discarded immediately after analysis completes. "
            "No raw message content is retained. "
            "If you have enabled history saving, only the risk score and risk level are stored — "
            "never the message itself."
        ),
    }
