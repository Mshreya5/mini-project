import pytest
from fastapi import HTTPException

from ai_module.api.main import health_check, predict_endpoint
from ai_module.api.schemas import HealthResponse, MessageRequest, PredictionResponse


def test_health_check_endpoint():
    res = health_check()
    assert isinstance(res, HealthResponse)
    assert res.status == "healthy"
    assert res.model_loaded is True
    assert "SilverShield" in res.service


def test_predict_endpoint_contract():
    payload = MessageRequest(
        message="URGENT: Your bank account is locked. Verify details here: http://secure-bank.xyz"
    )
    res = predict_endpoint(payload)

    assert isinstance(res, PredictionResponse)
    assert res.prediction in {"scam", "legitimate"}
    assert isinstance(res.confidence, float)
    assert 0.0 <= res.confidence <= 1.0
    assert isinstance(res.suspicious_indicators, list)
    assert isinstance(res.explanation, str)
    assert len(res.explanation) > 0


def test_predict_endpoint_scam_message():
    payload = MessageRequest(
        message="URGENT: Action required immediately! Send your OTP to unblock your suspended bank account."
    )
    res = predict_endpoint(payload)

    assert res.prediction == "scam"
    assert res.confidence >= 0.50
    assert len(res.suspicious_indicators) > 0
    assert any("OTP" in ind or "Urgent" in ind or "suspension" in ind for ind in res.suspicious_indicators)
    assert "suspicious" in res.explanation.lower()


def test_predict_endpoint_legitimate_message():
    payload = MessageRequest(
        message="Hey, let me know what time we should meet for dinner tonight."
    )
    res = predict_endpoint(payload)

    assert res.prediction == "legitimate"
    assert res.confidence >= 0.50
    assert "normal" in res.explanation.lower() or "everyday" in res.explanation.lower()


def test_predict_endpoint_validation_errors():
    with pytest.raises(Exception):
        MessageRequest(message="a")

    with pytest.raises(Exception):
        MessageRequest(message="")

    with pytest.raises(Exception):
        MessageRequest(message="x" * 1005)
