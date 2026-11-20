from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field

from app.database import (
    authenticate_user,
    fetch_user_history,
    get_consent_record,
    get_user_by_id,
    record_scan_history,
    register_user,
    save_consent_update,
    update_caregiver,
    wipe_user_history,
)
from security.access_control import (
    AccessDeniedError,
    derive_identity_from_token,
    enforce_resource_ownership,
    filter_user_profile,
)
from security.auth_rules import (
    GENERIC_LOGIN_ERROR,
    create_token,
    invalidate_token,
    is_token_blacklisted,
    rate_limiter,
)
from security.consent import get_elderly_transparency_notices

logger = logging.getLogger("app.api.auth")

auth_router = APIRouter(prefix="/auth", tags=["Authentication & Security"])
consent_router = APIRouter(prefix="/consent", tags=["Privacy & Consent"])
history_router = APIRouter(prefix="/history", tags=["Scan History"])

JWT_SECRET_KEY = "silvershield_ai_jwt_production_secret_key_minimum_32_bytes"


class RegisterRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password (min 8 chars, letters and digits)")
    role: str = Field(default="senior", description="User role: senior or caregiver")


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]


class CaregiverUpdateRequest(BaseModel):
    helper_name: str
    helper_phone: str


class ConsentUpdateRequest(BaseModel):
    consent_message_analysis: Optional[bool] = None
    consent_save_history: Optional[bool] = None
    consent_analytics: Optional[bool] = None
    consent_caregiver_sharing: Optional[bool] = None


def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials not provided.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split("Bearer ", 1)[1].strip()
    try:
        user_id = derive_identity_from_token(token, secret_key=JWT_SECRET_KEY)
        return user_id
    except AccessDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@auth_router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request) -> AuthResponse:
    client_ip = request.client.host if request.client else "127.0.0.1"
    allowed, retry_after = rate_limiter.is_allowed(f"register:{client_ip}", max_requests=10, window_seconds=60)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many registration attempts. Please retry after {retry_after} seconds.",
        )

    user, err = register_user(email=payload.email, password=payload.password, role=payload.role)
    if err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    token = create_token(subject=user["id"], secret_key=JWT_SECRET_KEY, expires_minutes=120)
    return AuthResponse(access_token=token, token_type="bearer", user=filter_user_profile(user))


@auth_router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, request: Request) -> AuthResponse:
    client_ip = request.client.host if request.client else "127.0.0.1"
    allowed, retry_after = rate_limiter.is_allowed(f"login:{client_ip}", max_requests=15, window_seconds=60)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Please retry after {retry_after} seconds.",
        )

    user, err = authenticate_user(email=payload.email, password=payload.password)
    if err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err)

    token = create_token(subject=user["id"], secret_key=JWT_SECRET_KEY, expires_minutes=120)
    return AuthResponse(access_token=token, token_type="bearer", user=filter_user_profile(user))


@auth_router.post("/logout")
def logout(authorization: Optional[str] = Header(None)) -> Dict[str, str]:
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ", 1)[1].strip()
        invalidate_token(token)
    return {"message": "Successfully logged out. Session terminated."}


@auth_router.get("/me")
def get_profile(user_id: str = Depends(get_current_user_id)) -> Dict[str, Any]:
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return filter_user_profile(user)


@auth_router.put("/caregiver")
def set_caregiver(
    payload: CaregiverUpdateRequest, user_id: str = Depends(get_current_user_id)
) -> Dict[str, Any]:
    success = update_caregiver(user_id, payload.helper_name, payload.helper_phone)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update caregiver.")
    user = get_user_by_id(user_id)
    return {"status": "success", "user": filter_user_profile(user)}


@consent_router.get("")
def get_consent(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    user_id = "guest_user"
    if authorization and authorization.startswith("Bearer "):
        try:
            token = authorization.split("Bearer ", 1)[1].strip()
            user_id = derive_identity_from_token(token, secret_key=JWT_SECRET_KEY)
        except Exception:
            pass

    record = get_consent_record(user_id)
    notices = get_elderly_transparency_notices(record.preferences)
    return {
        "user_id": user_id,
        "policy_version": record.policy_version,
        "preferences": record.preferences.model_dump(),
        "transparency_notices": notices,
        "updated_at": record.updated_at.isoformat(),
    }


@consent_router.put("")
def update_consent(
    payload: ConsentUpdateRequest, user_id: str = Depends(get_current_user_id)
) -> Dict[str, Any]:
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    updated_record = save_consent_update(user_id, updates)
    return {
        "status": "success",
        "preferences": updated_record.preferences.model_dump(),
        "updated_at": updated_record.updated_at.isoformat(),
    }


@history_router.get("")
def list_history(user_id: str = Depends(get_current_user_id)) -> List[Dict[str, Any]]:
    return fetch_user_history(user_id)


@history_router.delete("")
def clear_history(user_id: str = Depends(get_current_user_id)) -> Dict[str, str]:
    wipe_user_history(user_id)
    return {"message": "Scan history successfully erased."}
