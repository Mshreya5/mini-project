import json
from pathlib import Path
import pytest

from ai_module.src.config import (
    LOGISTIC_REGRESSION_MODEL_PATH,
    NAIVE_BAYES_MODEL_PATH,
    TFIDF_VECTORIZER_PATH,
)
from ai_module.src.predict import (
    load_artifacts,
    predict_message,
    validate_message_input,
)


def test_input_validation_rules():
    assert validate_message_input("") is not None
    assert validate_message_input("   ") is not None
    assert validate_message_input("a") is not None
    assert validate_message_input(None) is not None
    assert validate_message_input(12345) is not None
    assert validate_message_input("A" * 1001) is not None

    valid_msg = "Hello, are you coming over?"
    assert validate_message_input(valid_msg) is None


def test_load_artifacts():
    model, vectorizer = load_artifacts()
    assert model is not None
    assert vectorizer is not None
    assert hasattr(model, "predict")
    assert hasattr(vectorizer, "transform")


def test_predict_legitimate_message():
    msg = "Hi Dad, just checking if you need any groceries today. See you later!"
    result = predict_message(msg)

    assert result["status"] == "success"
    assert result["prediction"] == "legitimate"
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["scam_probability"] < 0.50
    assert isinstance(result["explanation"], str)
    assert len(result["explanation"]) > 0


def test_predict_scam_message():
    scam = (
        "URGENT: Your account has been suspended due to unauthorized access. "
        "Verify your identity immediately or your card will be blocked: http://secure-verify.xyz"
    )
    result = predict_message(scam)

    assert result["status"] == "success"
    assert result["prediction"] == "scam"
    assert result["confidence"] >= 0.50
    assert result["scam_probability"] >= 0.50
    assert len(result["suspicious_indicators"]) > 0
    assert isinstance(result["explanation"], str)


def test_predict_response_json_serializable():
    msg = "Congratulations! You won a cash prize of 500 pounds."
    res = predict_message(msg)
    serialized = json.dumps(res)
    assert len(serialized) > 0


def test_missing_artifact_graceful_error(tmp_path: Path):
    fake_model = tmp_path / "missing.joblib"
    fake_vec = tmp_path / "missing_vec.joblib"
    res = predict_message("Test message", model_path=fake_model, vectorizer_path=fake_vec)
    assert res["status"] == "error"
    assert "error_message" in res
