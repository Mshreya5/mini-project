"""Public API schemas.

These models are the contract with Member 1's frontend. Field names in the
response mirror the agreed example so the UI can render a result without any
transformation, and extra fields are purely additive.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.core.urls import normalise_url

RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]
AnalysisStatus = Literal["OK", "DEGRADED"]


class AnalyzeRequest(BaseModel):
    """One message to assess, with an optional URL supplied separately."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The SMS, email or chat message to assess.",
        examples=["Dear customer, your account is blocked. Share the OTP to reactivate."],
    )
    url: str | None = Field(
        default=None,
        description=(
            "Optional URL to analyse. When omitted, the first link found inside "
            "the message is analysed."
        ),
        examples=["http://secure-bank-verify.xyz/login"],
    )
    language: str | None = Field(
        default="English",
        description="Optional preferred language for output instructions and warnings.",
    )
    consent_given: bool = Field(
        default=True,
        description="User consent for message safety and URL analysis.",
    )

    @field_validator("message")
    @classmethod
    def _message_not_blank(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("message must not be empty or whitespace only")
        return stripped

    @field_validator("url")
    @classmethod
    def _url_is_http(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not value.strip():
            return None
        normalised = normalise_url(value)
        if normalised is None:
            raise ValueError("url must be an http or https address")
        return normalised


class ModuleStatusModel(BaseModel):
    """What happened inside one collaborating module for this analysis."""

    name: str
    state: str = Field(description="OK, SKIPPED, TIMEOUT, UNAVAILABLE, HTTP_ERROR or INVALID_RESPONSE")
    failed: bool
    detail: str | None = None
    latency_ms: int | None = None


class ContributionModel(BaseModel):
    """How one indicator contributed points before and after the module cap."""

    indicator_id: str
    label: str
    source: str
    severity: str
    points: int
    applied_points: int


class ScoreModel(BaseModel):
    """Full transparency block: nothing about the decision is hidden."""

    total: int
    raw_total: int = Field(description="Sum before per-module caps were applied.")
    thresholds: dict[str, int]
    capped_sources: list[str] = Field(default_factory=list)
    contributions: list[ContributionModel] = Field(default_factory=list)
    applied_overrides: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    """The integrated result returned to the frontend."""

    analysis_id: str
    generated_at: datetime
    overall_risk: RiskLevel
    status: AnalysisStatus = Field(
        description=(
            "OK when every required module answered. DEGRADED when one of them "
            "did not, in which case the level is never LOW."
        )
    )
    message_prediction: str = Field(description="SCAM, LEGITIMATE or UNKNOWN")
    message_confidence: float | None = None
    url_risk: str = Field(
        description="MALICIOUS, SUSPICIOUS, SAFE, NOT_APPLICABLE or UNKNOWN"
    )
    analysed_url: str | None = Field(
        default=None, description="Host level form of the URL that was checked."
    )
    risk_indicators: list[str] = Field(
        default_factory=list, description="Plain language reasons, ordered by weight."
    )
    warning: str
    recommended_actions: list[str] = Field(default_factory=list)
    explanation: str | None = Field(
        default=None, description="Explainable AI reasoning from Member 2."
    )
    module_status: list[ModuleStatusModel] = Field(default_factory=list)
    score: ScoreModel
    risk_score: float = Field(default=0.0, description="Normalized risk score between 0.0 and 1.0.")
    config_version: str


class ModuleHealthModel(BaseModel):
    name: str
    endpoint: str
    configured: bool


class HealthResponse(BaseModel):
    service: str
    version: str
    status: Literal["ok"]
    config_version: str
    thresholds: dict[str, int]
    modules: list[ModuleHealthModel]


class RiskConfigResponse(BaseModel):
    """Exposed so the UI and reviewers can see exactly how levels are decided."""

    version: str
    thresholds: dict[str, int]
    severity_points: dict[str, int]
    module_caps: dict[str, int]
    scam_confidence: dict[str, float]
    degraded_floor: str
    indicators: dict[str, str]
    overrides: list[dict[str, object]]


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: list[dict[str, str]] | None = None
