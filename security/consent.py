"""Consent Management and Privacy Rights Rules.

Member 2 (Cybersecurity & Privacy) module.
Implements granular, unbundled consent business logic, elderly-accessible disclosures,
and timestamped audit entry generation complying with GDPR / DPDP guidelines.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

DEFAULT_POLICY_VERSION = "v1.0"


class ConsentPreferences(BaseModel):
    """Granular consent choices. Optional consent items must default to False."""

    # 1. Processing message during on-demand analysis (strictly necessary for service delivery)
    consent_message_analysis: bool = Field(
        default=True,
        description="Allow in-memory inspection of message text to calculate scam risk score.",
    )

    # 2. Saving analysis history (Optional - Default False)
    consent_save_history: bool = Field(
        default=False,
        description="Optional: Save risk rating metadata in your account for future review.",
    )

    # 3. Anonymous threat analytics (Optional - Default False)
    consent_analytics: bool = Field(
        default=False,
        description="Optional: Share aggregated, non-PII scam patterns to improve safety models.",
    )

    # 4. Caregiver notification (Optional - Default False, disabled pending team approval)
    consent_caregiver_sharing: bool = Field(
        default=False,
        description="Optional (Future Feature): Notify a designated family contact on high-risk scams.",
    )


class ConsentAuditEntry(BaseModel):
    """Audit trail entry recording every consent modification."""

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    purpose: str
    consented: bool
    action: str  # "granted" | "withdrawn"
    policy_version: str = DEFAULT_POLICY_VERSION


class ConsentRecord(BaseModel):
    """Complete consent state and audit trail for a user."""

    user_id: str
    policy_version: str = DEFAULT_POLICY_VERSION
    preferences: ConsentPreferences = Field(default_factory=ConsentPreferences)
    audit_trail: List[ConsentAuditEntry] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def create_default_consent(
    user_id: str,
    policy_version: str = DEFAULT_POLICY_VERSION,
    opt_in_history: bool = False,
) -> ConsentRecord:
    """Create initial baseline consent for a new user.

    Ensures optional consent items are never pre-selected unless explicitly opted-in by user.
    """
    now = datetime.now(timezone.utc)
    prefs = ConsentPreferences(
        consent_message_analysis=True,
        consent_save_history=bool(opt_in_history),
        consent_analytics=False,
        consent_caregiver_sharing=False,
    )

    initial_audit = [
        ConsentAuditEntry(
            timestamp=now,
            purpose="consent_message_analysis",
            consented=True,
            action="granted",
            policy_version=policy_version,
        )
    ]
    if opt_in_history:
        initial_audit.append(
            ConsentAuditEntry(
                timestamp=now,
                purpose="consent_save_history",
                consented=True,
                action="granted",
                policy_version=policy_version,
            )
        )

    return ConsentRecord(
        user_id=str(user_id),
        policy_version=policy_version,
        preferences=prefs,
        audit_trail=initial_audit,
        updated_at=now,
    )


def record_consent_update(
    current_record: ConsentRecord,
    updated_fields: Dict[str, bool],
    policy_version: str = DEFAULT_POLICY_VERSION,
) -> ConsentRecord:
    """Update granular consent preferences and append timestamped audit entries.

    Ensures strict purpose separation: updating one purpose never alters any other purpose.
    """
    now = datetime.now(timezone.utc)
    current_dict = current_record.preferences.model_dump()
    new_audit_entries: List[ConsentAuditEntry] = []

    for key, new_val in updated_fields.items():
        if key not in current_dict:
            continue
        old_val = current_dict[key]
        if old_val != new_val:
            current_dict[key] = new_val
            action = "granted" if new_val else "withdrawn"
            new_audit_entries.append(
                ConsentAuditEntry(
                    timestamp=now,
                    purpose=key,
                    consented=bool(new_val),
                    action=action,
                    policy_version=policy_version,
                )
            )

    updated_prefs = ConsentPreferences(**current_dict)
    updated_audit = list(current_record.audit_trail) + new_audit_entries

    return ConsentRecord(
        user_id=current_record.user_id,
        policy_version=policy_version,
        preferences=updated_prefs,
        audit_trail=updated_audit,
        updated_at=now,
    )


def get_elderly_transparency_notices(preferences: ConsentPreferences) -> List[Dict[str, Any]]:
    """Produce plain-language, transparent privacy disclosures for non-technical seniors."""
    return [
        {
            "purpose_key": "consent_message_analysis",
            "title": "Immediate Safety Check (Required)",
            "description": (
                "When you check a message, our safety engine analyzes the text in computer memory to find scam patterns. "
                "The message text is deleted from memory right after the check. "
                "No outside companies or advertisers will ever see your messages."
            ),
            "is_strictly_necessary": True,
            "current_value": preferences.consent_message_analysis,
            "can_withdraw": False,
        },
        {
            "purpose_key": "consent_save_history",
            "title": "Save Past Check Results (Optional)",
            "description": (
                "Saves past safety scores to your personal account so you can review what you checked. "
                "You can turn this off or delete your saved history at any time with one click."
            ),
            "is_strictly_necessary": False,
            "current_value": preferences.consent_save_history,
            "can_withdraw": True,
        },
        {
            "purpose_key": "consent_analytics",
            "title": "Help Protect Other Seniors (Optional)",
            "description": (
                "Shares anonymous scam keywords (with all personal names, phone numbers, and codes removed) "
                "to help train better protections for other seniors."
            ),
            "is_strictly_necessary": False,
            "current_value": preferences.consent_analytics,
            "can_withdraw": True,
        },
        {
            "purpose_key": "consent_caregiver_sharing",
            "title": "Family / Caregiver Alerts (Optional - Future Preview)",
            "description": (
                "Sends a gentle warning to a designated family member if a critical scam is detected. "
                "Note: This feature is currently in preview and will not send alerts until approved by your team."
            ),
            "is_strictly_necessary": False,
            "current_value": preferences.consent_caregiver_sharing,
            "can_withdraw": True,
        },
    ]


def can_process_message(preferences: ConsentPreferences) -> bool:
    """Enforce consent check: message analysis must be permitted."""
    return bool(preferences.consent_message_analysis)


def can_save_history(preferences: ConsentPreferences) -> bool:
    """Enforce consent check: analysis history can only be saved if explicitly opted-in."""
    return bool(preferences.consent_save_history)


def can_share_caregiver(preferences: ConsentPreferences) -> bool:
    """Enforce consent check: caregiver sharing is blocked if consent is absent or withdrawn."""
    return bool(preferences.consent_caregiver_sharing)
