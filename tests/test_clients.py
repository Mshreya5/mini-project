"""Unit tests for the adapters: tolerant parsing and failure mapping."""

from __future__ import annotations

import pytest
import requests

from app.clients.base import JsonApiClient
from app.clients.parsing import as_confidence, as_text_list, first_present
from app.clients.scam_detector import ScamDetectorClient, parse_message_payload
from app.clients.url_analyzer import UrlAnalyzerClient, parse_url_payload
from app.core.models import ModuleState
from app.settings import Settings


class FakeResponse:
    def __init__(self, status_code: int = 200, payload=None) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self):
        if self._payload is None:
            raise ValueError("not json")
        return self._payload


class FakeSession:
    """Replays prepared responses or raises prepared exceptions."""

    def __init__(self, *responses) -> None:
        self.responses = list(responses)
        self.calls = 0

    def post(self, url, json=None, timeout=None):
        index = min(self.calls, len(self.responses) - 1)
        self.calls += 1
        item = self.responses[index]
        if isinstance(item, Exception):
            raise item
        return item


@pytest.fixture
def client_settings() -> Settings:
    return Settings(
        scam_api_url="http://scam.test/predict",
        url_api_url="http://url.test/analyze",
        request_timeout_seconds=0.5,
        max_retries=1,
    )




def test_first_present_searches_wrapped_payloads() -> None:
    payload = {"status": "ok", "data": {"verdict": "SCAM"}}
    assert first_present(payload, ("prediction", "verdict")) == "SCAM"


def test_first_present_ignores_blank_values() -> None:
    assert first_present({"prediction": "  "}, ("prediction",)) is None


def test_as_confidence_accepts_percentages_and_strings() -> None:
    assert as_confidence(0.82) == 0.82
    assert as_confidence(82) == 0.82
    assert as_confidence("0.5") == 0.5
    assert as_confidence(None) is None
    assert as_confidence("high") is None


def test_as_text_list_handles_strings_objects_and_case() -> None:
    assert as_text_list("Urgent Payment") == ("urgent_payment",)
    assert as_text_list([{"name": "OTP Request"}, "urgency"]) == ("otp_request", "urgency")
    assert as_text_list(None) == ()




def test_scam_payload_with_alias_fields_and_percentage_confidence() -> None:
    payload = {
        "data": {
            "label": "Spam",
            "probability": 87,
            "matched_keywords": [{"name": "OTP request"}, "Urgency"],
        }
    }

    analysis = parse_message_payload(payload)

    assert analysis is not None
    assert analysis.prediction == "SCAM"
    assert analysis.confidence == 0.87
    assert analysis.signals == ("otp_request", "urgency")


def test_scam_payload_without_prediction_is_unusable() -> None:
    assert parse_message_payload({"message": "hello"}) is None


def test_scam_client_maps_timeout(client_settings) -> None:
    session = FakeSession(requests.Timeout())
    client = ScamDetectorClient(client_settings, session=session)

    result = client.analyze("hi")

    assert result.state is ModuleState.TIMEOUT
    assert result.data is None
    assert session.calls == 2


def test_scam_client_maps_server_error_after_retries(client_settings) -> None:
    session = FakeSession(FakeResponse(503), FakeResponse(503))
    client = ScamDetectorClient(client_settings, session=session)

    result = client.analyze("hi")

    assert result.state is ModuleState.HTTP_ERROR
    assert "503" in (result.detail or "")


def test_scam_client_does_not_retry_client_errors(client_settings) -> None:
    session = FakeSession(FakeResponse(400), FakeResponse(200, {"prediction": "SCAM"}))
    client = ScamDetectorClient(client_settings, session=session)

    result = client.analyze("hi")

    assert result.state is ModuleState.HTTP_ERROR
    assert session.calls == 1


def test_scam_client_maps_non_json_body(client_settings) -> None:
    session = FakeSession(FakeResponse(200, None))
    client = ScamDetectorClient(client_settings, session=session)

    assert client.analyze("hi").state is ModuleState.INVALID_RESPONSE


def test_scam_client_maps_non_object_json(client_settings) -> None:
    session = FakeSession(FakeResponse(200, ["SCAM"]))
    client = ScamDetectorClient(client_settings, session=session)

    assert client.analyze("hi").state is ModuleState.INVALID_RESPONSE


def test_scam_client_unreachable_host(client_settings) -> None:
    session = FakeSession(requests.ConnectionError())
    client = ScamDetectorClient(client_settings, session=session)

    assert client.analyze("hi").state is ModuleState.UNAVAILABLE




def test_url_payload_flags_and_verdict() -> None:
    payload = {"verdict": "Suspicious", "reasons": ["Shortened URL", "No HTTPS"]}

    analysis = parse_url_payload(payload, "http://bit.ly/x")

    assert analysis is not None
    assert analysis.level == "SUSPICIOUS"
    assert analysis.flags == ("shortened_url", "no_https")


def test_url_payload_reads_boolean_transport_flags() -> None:
    payload = {"risk_level": "safe", "is_https": False, "is_shortened": True}

    analysis = parse_url_payload(payload, "http://example.com")

    assert analysis is not None
    assert analysis.level == "SAFE"
    assert "no_https" in analysis.flags
    assert "shortened" in analysis.flags


def test_url_payload_missing_level_is_unusable() -> None:
    assert parse_url_payload({"score": 0.4}, "http://example.com") is None


def test_url_client_invalid_response_when_level_unrecognised(client_settings) -> None:
    session = FakeSession(FakeResponse(200, {"verdict": "purple"}))
    client = UrlAnalyzerClient(client_settings, session=session)

    result = client.analyze("http://example.com")

    assert result.state is ModuleState.INVALID_RESPONSE
    assert result.data is None


def test_url_client_maps_http_error(client_settings) -> None:
    session = FakeSession(FakeResponse(500), FakeResponse(500))
    client = UrlAnalyzerClient(client_settings, session=session)

    assert client.analyze("http://example.com").state is ModuleState.HTTP_ERROR




def test_json_client_returns_elapsed_time(client_settings) -> None:
    session = FakeSession(FakeResponse(200, {"ok": True}))
    client = JsonApiClient("test", "http://test/predict", 0.5, 0, session=session)

    result = client.post({"message": "hi"})

    assert result.state is ModuleState.OK
    assert result.data == {"ok": True}
    assert isinstance(result.latency_ms, int)
