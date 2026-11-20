from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.database import init_db
from app.main import create_app
from security.auth_rules import GENERIC_LOGIN_ERROR


@pytest.fixture
def auth_client(tmp_path):
    test_db = tmp_path / "test_auth.db"
    init_db(test_db)
    app = create_app()
    return TestClient(app), test_db


def test_auth_registration_and_login_flow(auth_client, monkeypatch):
    client, test_db = auth_client
    monkeypatch.setattr("app.database.DEFAULT_DB_PATH", test_db)
    from security.auth_rules import rate_limiter
    rate_limiter.reset()

    res_weak = client.post(
        "/api/v1/auth/register",
        json={"email": "senior@example.com", "password": "weak"},
    )
    assert res_weak.status_code == 400
    assert "at least 8 characters" in res_weak.json()["detail"]

    res_reg = client.post(
        "/api/v1/auth/register",
        json={"email": "senior@example.com", "password": "SafeSeniorPass2026!"},
    )
    assert res_reg.status_code == 201
    data_reg = res_reg.json()
    assert "access_token" in data_reg
    assert data_reg["user"]["email"] == "senior@example.com"
    token = data_reg["access_token"]

    res_dup = client.post(
        "/api/v1/auth/register",
        json={"email": "senior@example.com", "password": "SafeSeniorPass2026!"},
    )
    assert res_dup.status_code == 400

    res_bad_pw = client.post(
        "/api/v1/auth/login",
        json={"email": "senior@example.com", "password": "WrongPassword123!"},
    )
    assert res_bad_pw.status_code == 401
    assert res_bad_pw.json()["detail"] == GENERIC_LOGIN_ERROR

    res_login = client.post(
        "/api/v1/auth/login",
        json={"email": "senior@example.com", "password": "SafeSeniorPass2026!"},
    )
    assert res_login.status_code == 200
    assert "access_token" in res_login.json()
    new_token = res_login.json()["access_token"]

    res_me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {new_token}"})
    assert res_me.status_code == 200
    assert res_me.json()["email"] == "senior@example.com"
    assert "password_hash" not in res_me.json()

    res_care = client.put(
        "/api/v1/auth/caregiver",
        headers={"Authorization": f"Bearer {new_token}"},
        json={"helper_name": "Ramesh", "helper_phone": "9876543210"},
    )
    assert res_care.status_code == 200
    assert res_care.json()["user"]["helper_name"] == "Ramesh"

    res_consent = client.get("/api/v1/consent", headers={"Authorization": f"Bearer {new_token}"})
    assert res_consent.status_code == 200
    assert res_consent.json()["preferences"]["consent_message_analysis"] is True
    assert len(res_consent.json()["transparency_notices"]) > 0

    res_up_consent = client.put(
        "/api/v1/consent",
        headers={"Authorization": f"Bearer {new_token}"},
        json={"consent_save_history": True},
    )
    assert res_up_consent.status_code == 200
    assert res_up_consent.json()["preferences"]["consent_save_history"] is True

    res_logout = client.post(
        "/api/v1/auth/logout", headers={"Authorization": f"Bearer {new_token}"}
    )
    assert res_logout.status_code == 200

    res_me_revoked = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {new_token}"})
    assert res_me_revoked.status_code == 401
