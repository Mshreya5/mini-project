"""
FastAPI Central Assessment & System Integration API
Member 4: Risk Aggregation, Warning Logic and System Integration

Main application entry point orchestrating communication between:
- Member 1: Frontend (Streamlit)
- Member 2: ML Scam Message Classification API
- Member 3: Privacy & URL Security Analysis API
"""
from datetime import datetime, timezone
import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.schemas import (
    AssessmentRequest,
    AssessmentResponse,
    OverallRiskLevel
)
from backend.risk_engine import RiskAggregationEngine
from backend.warning_generator import WarningGenerator
from backend.integrations import IntegrationClient

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("silvershield.api")

app = FastAPI(
    title="SilverShield AI - Risk Assessment & System Integration Engine",
    description=(
        "Central Risk Aggregation and Early Warning Engine for Secure AI-Powered "
        "Elderly Digital Safety Companion."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend and external integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate core engines
risk_engine = RiskAggregationEngine()
integration_client = IntegrationClient()


@app.get("/", tags=["General"])
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "RUNNING",
        "documentation": "/docs",
        "health_check": "/health"
    }


@app.get("/health", tags=["General"])
def health_check():
    """
    Health check probe reporting engine status and external API endpoints.
    """
    return {
        "status": "HEALTHY",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "configured_services": {
            "member2_ml_api": settings.MEMBER2_ML_API_URL,
            "member3_url_api": settings.MEMBER3_URL_API_URL,
            "timeout_seconds": settings.REQUEST_TIMEOUT_SECONDS
        }
    }


@app.get("/api/v1/config", tags=["Configuration"])
def get_risk_configuration():
    """
    Returns the transparent, configurable weights and thresholds used by the engine.
    """
    return {
        "weights": {
            "ml_scam_weight": settings.WEIGHT_ML_SCAM,
            "url_risk_weight": settings.WEIGHT_URL_RISK,
            "heuristic_weight": settings.WEIGHT_HEURISTIC_TRIGGERS
        },
        "thresholds": {
            "high_risk_cutoff": settings.HIGH_RISK_CUTOFF,
            "medium_risk_cutoff": settings.MEDIUM_RISK_CUTOFF,
            "scam_confidence_high": settings.SCAM_CONFIDENCE_HIGH_THRESHOLD,
            "scam_confidence_medium": settings.SCAM_CONFIDENCE_MEDIUM_THRESHOLD
        }
    }


@app.post(
    "/api/v1/assess",
    response_model=AssessmentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Assessment"]
)
def assess_message(request: AssessmentRequest):
    """
    Primary Integration Endpoint:
    1. Validates incoming message.
    2. Calls Member 2 ML scam classification API (with timeout & fallback).
    3. Calls Member 3 URL security & privacy API (with timeout & fallback).
    4. Aggregates findings through the multi-factor Risk Aggregation Engine.
    5. Generates clear, elderly-friendly warnings and practical recommendations.
    6. Returns structured JSON output matching project specifications.
    """
    cleaned_message = request.message.strip()
    if not cleaned_message:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message content cannot be empty or only whitespace."
        )

    logger.info(f"Initiating risk assessment for message (length: {len(cleaned_message)})")

    # Step 1: Query Member 2 (ML Scam Detection API)
    ml_result, ml_available = integration_client.call_member2_ml(cleaned_message)

    # Step 2: Query Member 3 (URL Security API)
    url_result, url_available = integration_client.call_member3_url(cleaned_message)

    # Step 3: Multi-factor Risk Aggregation
    assessment = risk_engine.aggregate_risk(
        message=cleaned_message,
        ml_prediction=ml_result.prediction.value,
        ml_confidence=ml_result.confidence,
        ml_triggers=ml_result.detected_triggers,
        ml_available=ml_available,
        url_risk=url_result.url_risk.value,
        url_indicators=url_result.indicators,
        urls_found=url_result.urls_found,
        url_available=url_available
    )

    overall_risk: OverallRiskLevel = assessment["overall_risk"]
    risk_indicators = assessment["risk_indicators"]
    composite_score = assessment["composite_score"]

    # Step 4: Warning and Recommended Action Generation
    lang = request.language or "English"
    warning_text = WarningGenerator.generate_warning(
        overall_risk=overall_risk,
        risk_indicators=risk_indicators,
        language=lang
    )

    recommended_actions = WarningGenerator.generate_recommended_actions(
        overall_risk=overall_risk,
        risk_indicators=risk_indicators,
        has_url=len(url_result.urls_found) > 0,
        message_text=cleaned_message,
        language=lang
    )

    # Step 5: Assemble Structured Response
    response = AssessmentResponse(
        overall_risk=overall_risk,
        message_prediction=ml_result.prediction.value,
        url_risk=url_result.url_risk.value,
        risk_indicators=risk_indicators,
        warning=warning_text,
        recommended_actions=recommended_actions,
        risk_score=composite_score,
        module_status={
            "ml_service": "ONLINE" if ml_available else "OFFLINE_FALLBACK",
            "url_service": "ONLINE" if url_available else "OFFLINE_FALLBACK"
        },
        timestamp=datetime.now(timezone.utc).isoformat()
    )

    logger.info(
        f"Completed assessment -> Risk: {overall_risk.value}, Score: {composite_score}, "
        f"ML: {ml_result.prediction.value}, URL: {url_result.url_risk.value}"
    )

    return response
