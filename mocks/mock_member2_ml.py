"""
Mock Microservice: Member 2 - ML Scam Message Classification API
Port: 8001
Endpoint: POST /api/v1/predict

Simulates Member 2's trained ML model prediction API.
"""
import re
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="Member 2 ML Scam Detection Service (Simulator)",
    version="1.0.0"
)


class MLRequest(BaseModel):
    text: str = Field(..., description="Message text to classify.")


class MLResponse(BaseModel):
    prediction: str = Field(..., description="SCAM, SUSPICIOUS, or LEGITIMATE")
    confidence: float = Field(..., ge=0.0, le=1.0)
    detected_triggers: List[str]


# Known scam patterns for the simulator
SCAM_PATTERNS = [
    (r"\b(urgent|immediately|within 24 hours|account suspended|deactivated|blocked)\b", "Urgent deadline pressure"),
    (r"\b(sbi|hdfc|icici|pnb|axis bank|rbi|bank account)\b", "Bank impersonation"),
    (r"\b(otp|one time password|verification code|pin|password|cvv)\b", "Credential / OTP harvesting"),
    (r"\b(won|lottery|prize|reward|gift voucher|crore|lakh)\b", "Unsolicited prize or lottery claim"),
    (r"\b(digital arrest|police warrant|court notice|cbi arrest)\b", "Digital arrest law enforcement scam"),
    (r"\b(electricity power cut|disconnection tonight|bill unpaid)\b", "Utility bill disconnection threat"),
    (r"\b(kyc update|pan link|aadhaar verify|update kyc)\b", "KYC update urgency")
]


@app.get("/health")
def health():
    return {"status": "ONLINE", "module": "Member 2 - ML Scam Classifier"}


@app.post("/api/v1/predict", response_model=MLResponse)
def predict_scam(payload: MLRequest):
    text = payload.text
    triggers = []

    for pattern, label in SCAM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            triggers.append(label)

    # Classification logic
    if len(triggers) >= 2:
        prediction = "SCAM"
        confidence = min(0.98, 0.75 + (0.07 * len(triggers)))
    elif len(triggers) == 1:
        # Check if single trigger is critical (like OTP or digital arrest)
        if any("OTP" in t or "arrest" in t for t in triggers):
            prediction = "SCAM"
            confidence = 0.82
        else:
            prediction = "SUSPICIOUS"
            confidence = 0.65
    else:
        prediction = "LEGITIMATE"
        confidence = 0.94

    return MLResponse(
        prediction=prediction,
        confidence=round(confidence, 2),
        detected_triggers=triggers
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
