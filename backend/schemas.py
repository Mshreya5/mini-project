"""
Pydantic Schemas for Request/Response Validation and API Contracts
Member 4: Risk Aggregation, Warning Logic and System Integration
"""
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict


class OverallRiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class MessagePrediction(str, Enum):
    LEGITIMATE = "LEGITIMATE"
    SUSPICIOUS = "SUSPICIOUS"
    SCAM = "SCAM"
    UNVERIFIED = "UNVERIFIED"


class URLRiskLevel(str, Enum):
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    MALICIOUS = "MALICIOUS"
    NO_URL = "NO_URL"
    UNVERIFIED = "UNVERIFIED"


# ---------------- Client Requests ----------------

class AssessmentRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The raw text message to be analyzed for scam risk."
    )
    sender: Optional[str] = Field(
        default=None,
        description="Optional sender name or phone number."
    )
    language: Optional[str] = Field(
        default="English",
        description="Preferred language for warnings (English, Hindi, Kannada)."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Urgent! Your SBI bank account is suspended. Update KYC now at http://bit.ly/sbi-verify-kyc",
                "sender": "+919876543210",
                "language": "English"
            }
        }
    )


# ---------------- Member 2 API Contracts ----------------

class Member2MLRequest(BaseModel):
    text: str = Field(..., description="Message text for ML scam classification.")


class Member2MLResponse(BaseModel):
    prediction: MessagePrediction = Field(..., description="Classification outcome.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0.0 to 1.0.")
    detected_triggers: List[str] = Field(
        default_factory=list,
        description="Detected scam triggers e.g., urgency, bank_impersonation, otp_solicitation."
    )


# ---------------- Member 3 API Contracts ----------------

class Member3URLRequest(BaseModel):
    text: str = Field(..., description="Text containing potential URLs to parse and inspect.")
    anonymize_pii: bool = Field(default=True, description="Privacy preservation flag.")


class Member3URLResponse(BaseModel):
    urls_found: List[str] = Field(default_factory=list, description="Extracted URLs.")
    url_risk: URLRiskLevel = Field(..., description="Calculated URL threat level.")
    indicators: List[str] = Field(
        default_factory=list,
        description="Suspicious features e.g., ip_address, shortened_url, brand_typo."
    )
    privacy_redacted: bool = Field(default=True, description="Whether PII was sanitized.")


# ---------------- Final Integrated Assessment Response ----------------

class AssessmentResponse(BaseModel):
    overall_risk: OverallRiskLevel = Field(
        ...,
        description="Overall synthesized risk level: LOW, MEDIUM, HIGH."
    )
    message_prediction: str = Field(
        ...,
        description="Prediction from Member 2 ML module or fallback: SCAM, SUSPICIOUS, LEGITIMATE, UNVERIFIED."
    )
    url_risk: str = Field(
        ...,
        description="URL risk from Member 3 module or fallback: SAFE, SUSPICIOUS, MALICIOUS, NO_URL, UNVERIFIED."
    )
    risk_indicators: List[str] = Field(
        default_factory=list,
        description="Aggregated list of concrete warning signs identified across all modules."
    )
    warning: str = Field(
        ...,
        description="Elderly-friendly, empathetic, clear warning statement."
    )
    recommended_actions: List[str] = Field(
        default_factory=list,
        description="Actionable, safe next steps for the senior citizen."
    )
    risk_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalized aggregated risk score (0.0=safe, 1.0=critical danger)."
    )
    module_status: Dict[str, str] = Field(
        default_factory=dict,
        description="Operational health status of external Member 2 and Member 3 modules."
    )
    timestamp: str = Field(
        ...,
        description="ISO 8601 evaluation timestamp."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "overall_risk": "HIGH",
                "message_prediction": "SCAM",
                "url_risk": "SUSPICIOUS",
                "risk_indicators": [
                    "Urgent payment request",
                    "Suspicious URL"
                ],
                "warning": "Warning! This message may be fraudulent. Do not share OTPs, passwords or banking details.",
                "recommended_actions": [
                    "Do not click the link",
                    "Do not share OTPs",
                    "Verify the sender"
                ],
                "risk_score": 0.85,
                "module_status": {
                    "ml_service": "ONLINE",
                    "url_service": "ONLINE"
                },
                "timestamp": "2026-11-15T18:30:00Z"
            }
        }
    )
