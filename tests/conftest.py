"""Shared fixtures and fake module clients.

The fakes stand in for Member 2 and Member 3 so the integration layer can be
tested end to end without their services running. They return the same
``RemoteCallResult`` objects the real adapters return, which means the tests
exercise the actual orchestration, engine and warning code.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.core.models import (
    ModuleState,
    MessageAnalysis,
    RemoteCallResult,
    UrlAnalysis,
)
from app.main import create_app
from app.settings import RiskConfig, Settings, get_risk_config


@pytest.fixture(scope="session")
def risk_config() -> RiskConfig:
    return get_risk_config()


@pytest.fixture
def settings() -> Settings:
    return Settings(
        scam_api_url="http://scam.test/predict",
        url_api_url="http://url.test/analyze",
        request_timeout_seconds=1.0,
        max_retries=0,
    )


class FakeScamClient:
    """Records calls and replays a prepared result."""

    def __init__(self, result: RemoteCallResult) -> None:
        self.result = result
        self.calls: list[str] = []

    def analyze(self, message: str) -> RemoteCallResult:
        self.calls.append(message)
        return self.result


class FakeUrlClient:
    """Records calls and replays a prepared result."""

    def __init__(self, result: RemoteCallResult) -> None:
        self.result = result
        self.calls: list[str] = []

    def analyze(self, url: str) -> RemoteCallResult:
        self.calls.append(url)
        return self.result


def message_ok(
    prediction: str = "LEGITIMATE",
    confidence: float | None = 0.1,
    signals: tuple[str, ...] = (),
) -> RemoteCallResult:
    return RemoteCallResult(
        state=ModuleState.OK,
        data=MessageAnalysis(
            prediction=prediction, confidence=confidence, signals=signals
        ),
        latency_ms=12,
    )


def url_ok(
    level: str = "SAFE", flags: tuple[str, ...] = (), url: str | None = None
) -> RemoteCallResult:
    return RemoteCallResult(
        state=ModuleState.OK,
        data=UrlAnalysis(level=level, flags=flags, url=url),
        latency_ms=9,
    )


def module_failure(
    state: ModuleState = ModuleState.TIMEOUT, detail: str = "module did not answer"
) -> RemoteCallResult:
    return RemoteCallResult(state=state, detail=detail, latency_ms=1000)


@pytest.fixture
def build_client(settings: Settings, risk_config: RiskConfig):
    """Build a TestClient with injected fake module clients."""

    def _build(
        scam_result: RemoteCallResult, url_result: RemoteCallResult
    ) -> tuple[TestClient, FakeScamClient, FakeUrlClient]:
        scam_client = FakeScamClient(scam_result)
        url_client = FakeUrlClient(url_result)
        app = create_app(
            settings=settings,
            config=risk_config,
            scam_client=scam_client,
            url_client=url_client,
        )
        return TestClient(app), scam_client, url_client

    return _build


def post_analyze(client: TestClient, payload: dict[str, Any]) -> Any:
    return client.post("/api/v1/analyze", json=payload)
