"""Route definitions.

Endpoints are deliberately synchronous ``def`` functions: FastAPI runs them in a
worker thread, which lets the adapters use the ``requests`` library as required by
the project's stack without blocking the event loop.
"""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ErrorResponse,
    HealthResponse,
    ModuleHealthModel,
    RiskConfigResponse,
)
from app import __version__

router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Assess one message for scam risk",
    responses={
        422: {"model": ErrorResponse, "description": "The request body was invalid."},
        200: {"description": "Aggregated risk assessment."},
    },
)
@router.post(
    "/assess",
    response_model=AnalyzeResponse,
    summary="Assess one message for scam risk (Frontend Alias)",
    include_in_schema=False,
)
def analyze(payload: AnalyzeRequest, request: Request) -> AnalyzeResponse:
    """Run the message through every module and return the aggregated result."""
    return request.app.state.aggregator.analyze(payload)


@router.get("/health", response_model=HealthResponse, summary="Service health")
def health(request: Request) -> HealthResponse:
    config = request.app.state.risk_config
    settings = request.app.state.settings
    return HealthResponse(
        service="risk-aggregation-service",
        version=__version__,
        status="ok",
        config_version=config.version,
        thresholds=config.thresholds,
        modules=[
            ModuleHealthModel(
                name="scam_detector",
                endpoint=settings.scam_api_url,
                configured=bool(settings.scam_api_url),
            ),
            ModuleHealthModel(
                name="url_analyzer",
                endpoint=settings.url_api_url,
                configured=bool(settings.url_api_url),
            ),
        ],
    )


@router.get(
    "/risk-config",
    response_model=RiskConfigResponse,
    summary="The rule set used to decide risk levels",
)
def risk_config(request: Request) -> RiskConfigResponse:
    """Transparency endpoint: the exact weights, caps, thresholds and overrides."""
    config = request.app.state.risk_config
    return RiskConfigResponse(
        version=config.version,
        thresholds=config.thresholds,
        severity_points=dict(config.severity_points),
        module_caps=config.module_caps,
        scam_confidence=config.scam_confidence,
        degraded_floor=config.degraded_floor,
        indicators={key: entry.label for key, entry in config.indicators.items()},
        overrides=[
            {
                "id": rule.id,
                "level": rule.level,
                "indicator": rule.indicator,
                "when": rule.when,
                "reason": rule.reason,
            }
            for rule in config.overrides
        ],
    )
