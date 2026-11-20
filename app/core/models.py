"""Normalised domain models shared by the adapters, the engine and the API layer.

The collaborating modules (Member 2 and Member 3) each have their own response
shape and their own notion of "how suspicious is this". Nothing crosses a module
boundary as a raw score: every module result is normalised into these models and
then translated into indicators by the risk engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Generic, TypeVar


class ModuleState(str, Enum):
    """Outcome of a single call to a collaborating module."""

    OK = "OK"
    SKIPPED = "SKIPPED"
    TIMEOUT = "TIMEOUT"
    UNAVAILABLE = "UNAVAILABLE"
    HTTP_ERROR = "HTTP_ERROR"
    INVALID_RESPONSE = "INVALID_RESPONSE"

    @property
    def is_failure(self) -> bool:
        return self not in (ModuleState.OK, ModuleState.SKIPPED)


PREDICTION_SCAM = "SCAM"
PREDICTION_LEGITIMATE = "LEGITIMATE"
PREDICTION_UNKNOWN = "UNKNOWN"

URL_SAFE = "SAFE"
URL_SUSPICIOUS = "SUSPICIOUS"
URL_MALICIOUS = "MALICIOUS"
URL_UNKNOWN = "UNKNOWN"
URL_NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class ModuleStatus:
    """Public, reportable status of one module in one analysis."""

    name: str
    state: ModuleState
    detail: str | None = None
    latency_ms: int | None = None

    @property
    def failed(self) -> bool:
        return self.state.is_failure


@dataclass(frozen=True)
class MessageAnalysis:
    """Normalised output of Member 2's scam classification API."""

    prediction: str
    confidence: float | None = None
    signals: tuple[str, ...] = ()
    explanation: str | None = None

    @property
    def is_scam(self) -> bool:
        return self.prediction == PREDICTION_SCAM


@dataclass(frozen=True)
class UrlAnalysis:
    """Normalised output of Member 3's URL analysis API."""

    level: str
    flags: tuple[str, ...] = ()
    url: str | None = None
    score: float | None = None


@dataclass(frozen=True)
class Indicator:
    """One concrete reason contributing to the risk assessment."""

    id: str
    label: str
    severity: str
    source: str
    actions: tuple[str, ...] = ()
    decisive: bool = False


@dataclass(frozen=True)
class Contribution:
    """How a single indicator was converted into points."""

    indicator_id: str
    label: str
    source: str
    severity: str
    points: int
    applied_points: int


@dataclass
class Assessment:
    """Result of aggregating indicators into one risk level."""

    level: str
    score: int
    raw_score: int
    indicators: list[Indicator] = field(default_factory=list)
    contributions: list[Contribution] = field(default_factory=list)
    overrides: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    capped_sources: list[str] = field(default_factory=list)
    degraded: bool = False


T = TypeVar("T")


@dataclass(frozen=True)
class RemoteCallResult(Generic[T]):
    """Transport-level outcome of an upstream call, with parsed payload if any."""

    state: ModuleState
    data: T | None = None
    detail: str | None = None
    latency_ms: int | None = None

    @property
    def ok(self) -> bool:
        return self.state is ModuleState.OK and self.data is not None
