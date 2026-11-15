"""Application factory for the risk aggregation service."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app import __version__
from app.api.routes import router
from app.core.orchestrator import RiskAggregator
from app.settings import RiskConfig, Settings, get_risk_config

logger = logging.getLogger(__name__)


def create_app(
    *,
    settings: Settings | None = None,
    config: RiskConfig | None = None,
    scam_client: Any | None = None,
    url_client: Any | None = None,
) -> FastAPI:
    """Build the FastAPI app, optionally with injected settings or clients."""
    resolved_settings = settings or Settings.from_env()
    resolved_config = config or get_risk_config()

    app = FastAPI(
        title="Elderly Digital Safety - Risk Aggregation Service",
        version=__version__,
        description=(
            "Aggregates the scam classification (Member 2) and URL analysis "
            "(Member 3) modules into one risk level with an elderly friendly "
            "warning and concrete safety actions."
        ),
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    app.state.settings = resolved_settings
    app.state.risk_config = resolved_config
    app.state.aggregator = RiskAggregator(
        config=resolved_config,
        settings=resolved_settings,
        scam_client=scam_client,
        url_client=url_client,
    )

    app.include_router(router, prefix="/api/v1")

    @app.exception_handler(RequestValidationError)
    async def _validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = []
        for error in exc.errors():
            location = ".".join(str(part) for part in error.get("loc", ()) if part != "body")
            details.append({"field": location or "body", "issue": error.get("msg", "invalid value")})
        return JSONResponse(
            status_code=422,
            content={
                "error": "invalid_request",
                "message": (
                    "The request could not be accepted. Send a non-empty message "
                    "and, if you include a link, a full http or https address."
                ),
                "details": details,
            },
        )

    @app.exception_handler(Exception)
    async def _unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error while analysing a message")
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": (
                    "Something went wrong while checking this message. Please try "
                    "again; do not treat the message as safe."
                ),
            },
        )

    @app.get("/", include_in_schema=False)
    def _root() -> dict[str, str]:
        return {
            "service": "risk-aggregation-service",
            "version": __version__,
            "analyze": "POST /api/v1/analyze",
            "docs": "/docs",
        }

    return app


app = create_app()
