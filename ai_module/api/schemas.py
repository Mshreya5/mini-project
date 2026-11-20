from typing import List, Optional

from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=2,
        max_length=1000,
        description="The raw SMS text to analyze for scam indicators.",
        json_schema_extra={
            "example": "URGENT: Your bank account is locked. Verify details here: http://secure-bank.xyz"
        },
    )


class PredictionResponse(BaseModel):
    prediction: str = Field(..., description="'scam' or 'legitimate'.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0.")
    suspicious_indicators: List[str] = Field(
        default_factory=list,
        description="Identified suspicious patterns (e.g. Urgent payment request, OTP request).",
    )
    explanation: str = Field(..., description="Understandable, elderly-friendly plain-English explanation.")
    scam_probability: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Raw calibrated scam probability score.",
    )
    status: str = Field(default="success", description="'success' or 'error'.")
    disclaimer: Optional[str] = Field(default=None, description="Standard automated assessment disclaimer.")


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Service health status.")
    service: str = Field(
        default="SilverShield AI Scam Detection Module",
        description="Name of the service.",
    )
    model_loaded: bool = Field(default=True, description="Whether ML models are in memory.")
    version: str = Field(default="1.0.0", description="API version.")
