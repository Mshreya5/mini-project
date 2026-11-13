"""Adapter for Member 2's scam classification API.

Contract (see docs/contracts.md):

    POST <SCAM_API_URL>   {"message": "..."}
    -> 200 {"prediction": "SCAM" | "LEGITIMATE", "confidence": 0.0-1.0,
            "signals": ["otp_request", "urgency", ...]}

Only the raw signal tokens are read from Member 2. No text features are computed
here: classification stays entirely inside their module.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.clients.base import JsonApiClient
from app.clients.parsing import (
    as_confidence,
    as_text_list,
    first_present,
    normalise_token,
)
from app.core.models import (
    ModuleState,
    PREDICTION_LEGITIMATE,
    PREDICTION_SCAM,
    PREDICTION_UNKNOWN,
    MessageAnalysis,
    RemoteCallResult,
)
from app.settings import Settings

_PREDICTION_KEYS = (
    "prediction",
    "message_prediction",
    "label",
    "classification",
    "scam_prediction",
    "result_label",
)
_CONFIDENCE_KEYS = (
    "confidence",
    "confidence_score",
    "probability",
    "scam_probability",
    "score",
)
_SIGNAL_KEYS = (
    "signals",
    "signal",
    "keywords",
    "matched_keywords",
    "indicators",
    "red_flags",
    "flags",
    "evidence",
)

_SCAM_LABELS = {
    "scam",
    "fraud",
    "fraudulent",
    "spam",
    "phishing",
    "malicious",
    "1",
    "true",
    "yes",
    "scam_message",
}
_LEGITIMATE_LABELS = {
    "legitimate",
    "legit",
    "ham",
    "safe",
    "benign",
    "not_scam",
    "not_spam",
    "non_scam",
    "0",
    "false",
    "no",
    "normal",
}


def normalise_prediction(value: Any) -> str:
    """Map a member's label onto SCAM / LEGITIMATE / UNKNOWN."""
    token = normalise_token(value if isinstance(value, str) else str(value))
    if token in _SCAM_LABELS:
        return PREDICTION_SCAM
    if token in _LEGITIMATE_LABELS:
        return PREDICTION_LEGITIMATE
    return PREDICTION_UNKNOWN


def parse_message_payload(payload: Mapping[str, Any]) -> MessageAnalysis | None:
    """Read a scam detector payload, returning None when it is unusable."""
    raw_prediction = first_present(payload, _PREDICTION_KEYS)
    if raw_prediction is None:
        return None

    prediction = normalise_prediction(raw_prediction)
    confidence = as_confidence(first_present(payload, _CONFIDENCE_KEYS))
    signals = as_text_list(first_present(payload, _SIGNAL_KEYS))

    return MessageAnalysis(
        prediction=prediction,
        confidence=confidence,
        signals=signals,
    )


class ScamDetectorClient:
    """Calls Member 2's prediction endpoint and normalises the response."""

    module_name = "scam_detector"

    def __init__(self, settings: Settings, session: Any | None = None) -> None:
        self._http = JsonApiClient(
            name=self.module_name,
            endpoint=settings.scam_api_url,
            timeout_seconds=settings.request_timeout_seconds,
            max_retries=settings.max_retries,
            session=session,
        )

    def analyze(self, message: str) -> RemoteCallResult[MessageAnalysis]:
        result = self._http.post({"message": message})
        if result.state is not ModuleState.OK or result.data is None:
            return RemoteCallResult(
                state=result.state,
                detail=result.detail,
                latency_ms=result.latency_ms,
            )

        analysis = parse_message_payload(result.data)
        if analysis is None:
            return RemoteCallResult(
                state=ModuleState.INVALID_RESPONSE,
                detail="scam detector response did not contain a prediction field",
                latency_ms=result.latency_ms,
            )

        return RemoteCallResult(
            state=ModuleState.OK,
            data=analysis,
            latency_ms=result.latency_ms,
        )
