from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from security.auth_rules import (
    GENERIC_LOGIN_ERROR,
    GENERIC_REGISTRATION_ERROR,
    resist_timing_enumeration,
    validate_password_strength,
)
from security.consent import (
    ConsentAuditEntry,
    ConsentPreferences,
    ConsentRecord,
    DEFAULT_POLICY_VERSION,
    create_default_consent,
    record_consent_update,
)
from security.passwords import hash_password, verify_password

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "silvershield.db"


def get_db_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    target_path = db_path or DEFAULT_DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Optional[Path] = None) -> None:
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'senior',
                    helper_name TEXT DEFAULT '',
                    helper_phone TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    last_login TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS consent_records (
                    user_id TEXT PRIMARY KEY,
                    preferences_json TEXT NOT NULL,
                    audit_trail_json TEXT NOT NULL,
                    policy_version TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS scan_history (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    message_type TEXT NOT NULL,
                    risk_level TEXT NOT NULL,
                    risk_score REAL NOT NULL,
                    indicators_json TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
                """
            )
    finally:
        conn.close()


def register_user(
    email: str, password: str, role: str = "senior", db_path: Optional[Path] = None
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    email_clean = (email or "").strip().lower()
    if not email_clean or "@" not in email_clean:
        return None, "A valid email address is required."

    is_valid_pw, pw_msg = validate_password_strength(password)
    if not is_valid_pw:
        return None, pw_msg

    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email_clean,))
        if cur.fetchone() is not None:
            return None, GENERIC_REGISTRATION_ERROR

        user_id = f"user-{uuid.uuid4().hex[:12]}"
        hashed_pw = hash_password(password)
        now_iso = datetime.now(timezone.utc).isoformat()

        with conn:
            conn.execute(
                "INSERT INTO users (id, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, email_clean, hashed_pw, role, now_iso),
            )
            consent = create_default_consent(user_id=user_id)
            conn.execute(
                """
                INSERT INTO consent_records (user_id, preferences_json, audit_trail_json, policy_version, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    json.dumps(consent.preferences.model_dump()),
                    json.dumps([a.model_dump(mode="json") for a in consent.audit_trail]),
                    consent.policy_version,
                    consent.updated_at.isoformat(),
                ),
            )

        return {
            "id": user_id,
            "email": email_clean,
            "role": role,
            "helper_name": "",
            "helper_phone": "",
            "created_at": now_iso,
        }, None
    finally:
        conn.close()


def authenticate_user(
    email: str, password: str, db_path: Optional[Path] = None
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    email_clean = (email or "").strip().lower()
    if not email_clean or not password:
        return None, GENERIC_LOGIN_ERROR

    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, password_hash, role, helper_name, helper_phone, created_at FROM users WHERE email = ?",
            (email_clean,),
        )
        row = cur.fetchone()

        if row is None:
            resist_timing_enumeration()
            return None, GENERIC_LOGIN_ERROR

        if not verify_password(password, row["password_hash"]):
            return None, GENERIC_LOGIN_ERROR

        now_iso = datetime.now(timezone.utc).isoformat()
        with conn:
            conn.execute("UPDATE users SET last_login = ? WHERE id = ?", (now_iso, row["id"]))

        return {
            "id": row["id"],
            "email": row["email"],
            "role": row["role"],
            "helper_name": row["helper_name"] or "",
            "helper_phone": row["helper_phone"] or "",
            "created_at": row["created_at"],
            "last_login": now_iso,
        }, None
    finally:
        conn.close()


def get_user_by_id(user_id: str, db_path: Optional[Path] = None) -> Optional[Dict[str, Any]]:
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, role, helper_name, helper_phone, created_at, last_login FROM users WHERE id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()


def update_caregiver(
    user_id: str, helper_name: str, helper_phone: str, db_path: Optional[Path] = None
) -> bool:
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        with conn:
            cur = conn.execute(
                "UPDATE users SET helper_name = ?, helper_phone = ? WHERE id = ?",
                (helper_name.strip(), helper_phone.strip(), user_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()


def get_consent_record(user_id: str, db_path: Optional[Path] = None) -> ConsentRecord:
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT preferences_json, audit_trail_json, policy_version, updated_at FROM consent_records WHERE user_id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        if row is None:
            record = create_default_consent(user_id=user_id)
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO consent_records (user_id, preferences_json, audit_trail_json, policy_version, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        json.dumps(record.preferences.model_dump()),
                        json.dumps([a.model_dump(mode="json") for a in record.audit_trail]),
                        record.policy_version,
                        record.updated_at.isoformat(),
                    ),
                )
            return record

        prefs_dict = json.loads(row["preferences_json"])
        audit_raw = json.loads(row["audit_trail_json"])
        audit_entries = [
            ConsentAuditEntry(
                timestamp=datetime.fromisoformat(a["timestamp"]),
                purpose=a["purpose"],
                consented=bool(a["consented"]),
                action=a["action"],
                policy_version=a.get("policy_version", DEFAULT_POLICY_VERSION),
            )
            for a in audit_raw
        ]
        return ConsentRecord(
            user_id=user_id,
            policy_version=row["policy_version"],
            preferences=ConsentPreferences(**prefs_dict),
            audit_trail=audit_entries,
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
    finally:
        conn.close()


def save_consent_update(
    user_id: str, updated_fields: Dict[str, bool], db_path: Optional[Path] = None
) -> ConsentRecord:
    record = get_consent_record(user_id, db_path)
    updated = record_consent_update(record, updated_fields)
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                UPDATE consent_records
                SET preferences_json = ?, audit_trail_json = ?, policy_version = ?, updated_at = ?
                WHERE user_id = ?
                """,
                (
                    json.dumps(updated.preferences.model_dump()),
                    json.dumps([a.model_dump(mode="json") for a in updated.audit_trail]),
                    updated.policy_version,
                    updated.updated_at.isoformat(),
                    user_id,
                ),
            )
        return updated
    finally:
        conn.close()


def record_scan_history(
    user_id: str,
    message_type: str,
    risk_level: str,
    risk_score: float,
    indicators: List[str],
    db_path: Optional[Path] = None,
) -> Dict[str, Any]:
    init_db(db_path)
    scan_id = f"scan-{uuid.uuid4().hex[:10]}"
    now_iso = datetime.now(timezone.utc).isoformat()
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO scan_history (id, user_id, timestamp, message_type, risk_level, risk_score, indicators_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    scan_id,
                    user_id,
                    now_iso,
                    message_type,
                    risk_level,
                    float(risk_score),
                    json.dumps(indicators),
                ),
            )
        return {
            "id": scan_id,
            "user_id": user_id,
            "timestamp": now_iso,
            "message_type": message_type,
            "risk_level": risk_level,
            "risk_score": float(risk_score),
            "indicators": indicators,
        }
    finally:
        conn.close()


def fetch_user_history(user_id: str, limit: int = 20, db_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, timestamp, message_type, risk_level, risk_score, indicators_json
            FROM scan_history WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT ?
            """,
            (user_id, limit),
        )
        rows = cur.fetchall()
        result = []
        for r in rows:
            result.append(
                {
                    "id": r["id"],
                    "timestamp": r["timestamp"],
                    "message_type": r["message_type"],
                    "risk_level": r["risk_level"],
                    "risk_score": r["risk_score"],
                    "indicators": json.loads(r["indicators_json"]),
                }
            )
        return result
    finally:
        conn.close()


def wipe_user_history(user_id: str, db_path: Optional[Path] = None) -> bool:
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute("DELETE FROM scan_history WHERE user_id = ?", (user_id,))
            return True
    finally:
        conn.close()
