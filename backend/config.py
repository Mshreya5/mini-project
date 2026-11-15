"""
Configuration Settings for Risk Assessment and Integration Engine
Member 4: Risk Aggregation, Warning Logic and System Integration
"""
import os
from pydantic import BaseModel


class Settings(BaseModel):
    # Service Information
    APP_NAME: str = "SilverShield AI - Risk Aggregation & Integration Module"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Member 2: ML Scam Message Detection API
    MEMBER2_ML_API_URL: str = os.getenv("MEMBER2_ML_API_URL", "http://127.0.0.1:8001/api/v1/predict")
    
    # Member 3: Privacy & URL Security Analysis API
    MEMBER3_URL_API_URL: str = os.getenv("MEMBER3_URL_API_URL", "http://127.0.0.1:8002/api/v1/analyze-url")

    # API Request Timeout (in seconds)
    REQUEST_TIMEOUT_SECONDS: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "3.0"))

    # Configurable Risk Assessment Thresholds
    # (High risk if ML confidence >= 0.75, or malicious URL, or combined indicators)
    SCAM_CONFIDENCE_HIGH_THRESHOLD: float = 0.75
    SCAM_CONFIDENCE_MEDIUM_THRESHOLD: float = 0.40

    # Risk Weights for Multi-factor Calculation (Transparent & Configurable)
    WEIGHT_ML_SCAM: float = 0.45
    WEIGHT_URL_RISK: float = 0.35
    WEIGHT_HEURISTIC_TRIGGERS: float = 0.20

    # Score Classification Cutoffs
    HIGH_RISK_CUTOFF: float = 0.70
    MEDIUM_RISK_CUTOFF: float = 0.35


# Global instance
settings = Settings()
