"""Transport layer shared by both adapters.

Every failure mode is converted into a :class:`ModuleState` instead of an
exception, so the aggregation step always has something to report to the user.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from app.core.models import ModuleState, RemoteCallResult


def _elapsed_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)


class JsonApiClient:
    """POSTs a JSON body and returns a parsed payload or a typed failure."""

    def __init__(
        self,
        name: str,
        endpoint: str,
        timeout_seconds: float = 4.0,
        max_retries: int = 1,
        session: requests.Session | None = None,
    ) -> None:
        self.name = name
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self._session = session or requests.Session()

    def post(self, payload: dict[str, Any]) -> RemoteCallResult[dict[str, Any]]:
        started = time.perf_counter()
        detail: str | None = None
        state = ModuleState.UNAVAILABLE

        for attempt in range(self.max_retries + 1):
            try:
                response = self._session.post(
                    self.endpoint, json=payload, timeout=self.timeout_seconds
                )
            except requests.Timeout:
                state = ModuleState.TIMEOUT
                detail = (
                    f"{self.name} did not answer within "
                    f"{self.timeout_seconds:g}s"
                )
                continue
            except requests.ConnectionError:
                state = ModuleState.UNAVAILABLE
                detail = f"{self.name} is unreachable"
                continue
            except requests.RequestException as exc:
                return RemoteCallResult(
                    state=ModuleState.UNAVAILABLE,
                    detail=f"{self.name} request failed ({type(exc).__name__})",
                    latency_ms=_elapsed_ms(started),
                )

            if response.status_code >= 500:
                state = ModuleState.HTTP_ERROR
                detail = f"{self.name} returned HTTP {response.status_code}"
                if attempt < self.max_retries:
                    continue
                return RemoteCallResult(
                    state=state, detail=detail, latency_ms=_elapsed_ms(started)
                )

            if response.status_code >= 400:
                return RemoteCallResult(
                    state=ModuleState.HTTP_ERROR,
                    detail=f"{self.name} rejected the request with HTTP {response.status_code}",
                    latency_ms=_elapsed_ms(started),
                )

            try:
                body = response.json()
            except ValueError:
                return RemoteCallResult(
                    state=ModuleState.INVALID_RESPONSE,
                    detail=f"{self.name} returned a body that is not JSON",
                    latency_ms=_elapsed_ms(started),
                )

            if not isinstance(body, dict):
                return RemoteCallResult(
                    state=ModuleState.INVALID_RESPONSE,
                    detail=f"{self.name} returned JSON that is not an object",
                    latency_ms=_elapsed_ms(started),
                )

            return RemoteCallResult(
                state=ModuleState.OK, data=body, latency_ms=_elapsed_ms(started)
            )

        return RemoteCallResult(state=state, detail=detail, latency_ms=_elapsed_ms(started))
