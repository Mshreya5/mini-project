"""Tests for Granular Consent Business Rules and Transparency.

Member 2 (Cybersecurity & Privacy) test suite.
"""

from __future__ import annotations

from security.consent import (
    can_process_message,
    can_save_history,
    can_share_caregiver,
    create_default_consent,
    get_elderly_transparency_notices,
    record_consent_update,
)


def test_default_consent_optional_items_unselected():
    """Verify that optional consent choices are never pre-selected by default."""
    record = create_default_consent(user_id="senior-001")
    prefs = record.preferences

    # Service delivery is required
    assert prefs.consent_message_analysis is True
    # All optional purposes MUST be False
    assert prefs.consent_save_history is False
    assert prefs.consent_analytics is False
    assert prefs.consent_caregiver_sharing is False

    assert len(record.audit_trail) == 1
    assert record.audit_trail[0].purpose == "consent_message_analysis"
    assert record.audit_trail[0].action == "granted"


def test_consent_update_and_audit_trail_recording():
    """Verify that consent updates record timestamped audit entries."""
    record = create_default_consent(user_id="senior-002")

    # 1. User grants optional history saving
    updated = record_consent_update(record, {"consent_save_history": True})
    assert updated.preferences.consent_save_history is True
    assert len(updated.audit_trail) == 2
    last_audit = updated.audit_trail[-1]
    assert last_audit.purpose == "consent_save_history"
    assert last_audit.consented is True
    assert last_audit.action == "granted"

    # 2. User later withdraws consent
    withdrawn = record_consent_update(updated, {"consent_save_history": False})
    assert withdrawn.preferences.consent_save_history is False
    assert len(withdrawn.audit_trail) == 3
    final_audit = withdrawn.audit_trail[-1]
    assert final_audit.purpose == "consent_save_history"
    assert final_audit.consented is False
    assert final_audit.action == "withdrawn"


def test_consent_strict_purpose_separation():
    """Verify that consenting to one purpose never implicitly grants unrelated purposes."""
    record = create_default_consent(user_id="senior-003")

    # User opts into analytics only
    updated = record_consent_update(record, {"consent_analytics": True})
    assert updated.preferences.consent_analytics is True
    # History and Caregiver must remain False
    assert updated.preferences.consent_save_history is False
    assert updated.preferences.consent_caregiver_sharing is False


def test_elderly_transparency_notices_plain_language():
    """Verify that plain-language disclosures are generated for all consent categories."""
    record = create_default_consent(user_id="senior-004")
    notices = get_elderly_transparency_notices(record.preferences)

    assert len(notices) == 4
    purpose_keys = [n["purpose_key"] for n in notices]
    assert "consent_message_analysis" in purpose_keys
    assert "consent_save_history" in purpose_keys
    assert "consent_analytics" in purpose_keys
    assert "consent_caregiver_sharing" in purpose_keys

    for notice in notices:
        assert len(notice["title"]) > 5
        assert len(notice["description"]) > 25
        # Ensure description states third parties/advertisers never see messages
        if notice["purpose_key"] == "consent_message_analysis":
            assert "advertisers" in notice["description"].lower()


def test_permission_check_helpers():
    """Verify permission check helper functions."""
    record = create_default_consent(user_id="senior-005")

    # Default state: message analysis permitted, history & caregiver blocked
    assert can_process_message(record.preferences) is True
    assert can_save_history(record.preferences) is False
    assert can_share_caregiver(record.preferences) is False

    # After opting into history
    updated = record_consent_update(record, {"consent_save_history": True})
    assert can_save_history(updated.preferences) is True
    # Caregiver remains blocked
    assert can_share_caregiver(updated.preferences) is False
