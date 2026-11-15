"""End to end orchestration of one analysis.

Flow:
    message + optional URL
        -> scam detector (Member 2)   \
        -> URL analyser (Member 3)    / called concurrently when a link exists
        -> indicator building
        -> risk engine (overrides, caps, thresholds, degraded floor)
        -> warning and actions
        -> AnalyseResponse
"""

from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from app.clients.scam_detector import ScamDetectorClient
from app.clients.url_analyzer import UrlAnalyzerClient
from app.core.indicators import build_indicators
from app.core.models import (
    PREDICTION_UNKNOWN,
    URL_NOT_APPLICABLE,
    URL_UNKNOWN,
    ModuleState,
    ModuleStatus,
    RemoteCallResult,
    UrlAnalysis,
)
from app.core.risk_engine import RiskEngine
from app.core.urls import extract_first_url, normalise_url, redact_url
from app.core.warnings import build_actions, build_warning, describe_indicators
from app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    ContributionModel,
    ModuleStatusModel,
    ScoreModel,
)
from app.settings import RiskConfig, Settings


class RiskAggregator:
    """Coordinates the collaborating modules and the risk engine."""

    def __init__(
        self,
        config: RiskConfig,
        settings: Settings,
        scam_client: ScamDetectorClient | None = None,
        url_client: UrlAnalyzerClient | None = None,
    ) -> None:
        self._config = config
        self._settings = settings
        self._scam_client = scam_client or ScamDetectorClient(settings)
        self._url_client = url_client or UrlAnalyzerClient(settings)
        self._engine = RiskEngine(config)

    # ------------------------------------------------------------------ public

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        target_url = self._resolve_url(request)
        has_link = target_url is not None

        message_result, url_result = self._call_modules(request.message, target_url)

        message_analysis = message_result.data if message_result.ok else None
        url_analysis = url_result.data if url_result.ok else None

        message_failed = message_result.state.is_failure
        url_failed = has_link and url_result.state.is_failure
        degraded = message_failed or url_failed

        indicators = build_indicators(
            self._config,
            message=message_analysis,
            url=url_analysis,
            message_unavailable=message_failed,
            url_unavailable=url_failed,
        )

        prediction = (
            message_analysis.prediction if message_analysis else PREDICTION_UNKNOWN
        )
        confidence = message_analysis.confidence if message_analysis else None
        if not has_link:
            url_level = URL_NOT_APPLICABLE
        elif url_analysis is not None:
            url_level = url_analysis.level
        else:
            url_level = URL_UNKNOWN

        assessment = self._engine.assess(
            indicators,
            prediction=prediction,
            confidence=confidence,
            url_level=url_level,
            has_link=has_link,
            floor=self._config.degraded_floor if degraded else None,
            degraded=degraded,
        )

        module_status = [
            self._to_status("scam_detector", message_result),
            self._to_status("url_analyzer", url_result),
        ]

        return AnalyzeResponse(
            analysis_id=uuid.uuid4().hex,
            generated_at=datetime.now(timezone.utc),
            overall_risk=assessment.level,  # type: ignore[arg-type]
            status="DEGRADED" if degraded else "OK",
            message_prediction=prediction,
            message_confidence=confidence,
            url_risk=url_level,
            analysed_url=redact_url(target_url) if target_url else None,
            risk_indicators=describe_indicators(assessment.indicators),
            warning=build_warning(self._config, assessment.level, degraded=degraded),
            recommended_actions=build_actions(
                self._config, assessment.level, assessment.indicators
            ),
            module_status=module_status,
            score=ScoreModel(
                total=assessment.score,
                raw_total=assessment.raw_score,
                thresholds=self._config.thresholds,
                capped_sources=assessment.capped_sources,
                contributions=[
                    ContributionModel(
                        indicator_id=item.indicator_id,
                        label=item.label,
                        source=item.source,
                        severity=item.severity,
                        points=item.points,
                        applied_points=item.applied_points,
                    )
                    for item in assessment.contributions
                ],
                applied_overrides=assessment.overrides,
                reasons=assessment.reasons,
            ),
            config_version=self._config.version,
        )

    # ---------------------------------------------------------------- internal

    def _resolve_url(self, request: AnalyzeRequest) -> str | None:
        if request.url:
            return request.url
        detected = extract_first_url(request.message)
        if detected is None:
            return None
        return normalise_url(detected) or detected

    def _call_modules(
        self, message: str, target_url: str | None
    ) -> tuple[RemoteCallResult, RemoteCallResult]:
        if target_url is None:
            return (
                self._scam_client.analyze(message),
                RemoteCallResult(state=ModuleState.SKIPPED, detail="no link in message"),
            )

        with ThreadPoolExecutor(max_workers=2) as pool:
            message_future = pool.submit(self._scam_client.analyze, message)
            url_future = pool.submit(self._url_client.analyze, target_url)
            return message_future.result(), url_future.result()

    @staticmethod
    def _to_status(name: str, result: RemoteCallResult) -> ModuleStatusModel:
        status = ModuleStatus(
            name=name,
            state=result.state,
            detail=result.detail,
            latency_ms=result.latency_ms,
        )
        return ModuleStatusModel(
            name=status.name,
            state=status.state.value,
            failed=status.failed,
            detail=status.detail,
            latency_ms=status.latency_ms,
        )


__all__ = ["RiskAggregator", "UrlAnalysis"]
