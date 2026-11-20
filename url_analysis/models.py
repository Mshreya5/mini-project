"""Pydantic schemas for URL Analysis API request and response contracts.

Member 3: Privacy, Cybersecurity and URL Analysis.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class AnalyzeRequest(BaseModel):
    """Incoming request: raw message text or direct URL submitted by the user."""

    message: Optional[str] = Field(
        default=None,
        description="Raw message text to analyze for URLs.",
    )
    url: Optional[str] = Field(
        default=None,
        description="Optional direct URL to analyze.",
    )
    consent_given: bool = Field(
        default=True,
        description="User has consented to message analysis for safety checking.",
    )

    @model_validator(mode="after")
    def check_at_least_one_text(self) -> "AnalyzeRequest":
        msg = (self.message or "").strip()
        u = (self.url or "").strip()
        if not msg and not u:
            raise ValueError("Message or URL must not be blank.")
        return self


class URLAnalysisResult(BaseModel):
    """Analysis result for a single extracted URL."""

    url: str = Field(..., description="The extracted URL (scheme + host + path, query stripped for privacy).")
    url_found: bool = Field(..., description="Whether a URL was present.")
    suspicious: bool = Field(..., description="True only when 2 or more risk indicators are detected.")
    risk_score: int = Field(..., ge=0, description="Count of triggered risk indicators.")
    risk_indicators: List[str] = Field(default_factory=list, description="List of detected suspicious characteristics.")
    explanation: str = Field(..., description="Plain-language summary of findings.")
    risk_level: str = Field(default="LOW", description="Risk tier: LOW, MEDIUM, or HIGH.")


class AnalyzeResponse(BaseModel):
    """Top-level API response for /analyze-url."""

    urls_found: bool = Field(..., description="Whether any URLs were detected in the message.")
    url_count: int = Field(..., ge=0, description="Number of URLs extracted.")
    results: List[URLAnalysisResult] = Field(default_factory=list, description="Per-URL analysis results.")
    privacy_note: str = Field(
        default=(
            "Your message was analyzed in memory only. "
            "No message text or URL content was stored or logged."
        )
    )


class PrivacyInfoResponse(BaseModel):
    """Response for /privacy-info endpoint."""

    what_is_processed: str
    why_it_is_processed: str
    how_data_is_protected: List[str]
    data_retention: str
