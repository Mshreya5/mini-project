import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import joblib

from ai_module.src.config import (
    LABEL_LEGITIMATE,
    LABEL_SCAM,
    LOGISTIC_REGRESSION_MODEL_PATH,
    MAX_MESSAGE_LENGTH,
    MIN_MESSAGE_LENGTH,
    STANDARD_DISCLAIMER,
    TFIDF_VECTORIZER_PATH,
)
from ai_module.src.explainability import generate_explanation
from ai_module.src.preprocessing import normalize_text
from ai_module.src.warning_indicators import detect_suspicious_indicators

logger = logging.getLogger(__name__)

_CACHED_MODEL = None
_CACHED_VECTORIZER = None


def load_artifacts(
    model_path: Path = LOGISTIC_REGRESSION_MODEL_PATH,
    vectorizer_path: Path = TFIDF_VECTORIZER_PATH,
    force_reload: bool = False,
) -> Tuple[Any, Any]:
    global _CACHED_MODEL, _CACHED_VECTORIZER

    model_path = Path(model_path)
    vectorizer_path = Path(vectorizer_path)

    default_model = Path(LOGISTIC_REGRESSION_MODEL_PATH)
    default_vec = Path(TFIDF_VECTORIZER_PATH)
    using_defaults = (model_path == default_model and vectorizer_path == default_vec)

    if not force_reload and using_defaults and _CACHED_MODEL is not None and _CACHED_VECTORIZER is not None:
        return _CACHED_MODEL, _CACHED_VECTORIZER

    if not model_path.exists():
        raise FileNotFoundError(
            f"Trained model not found at '{model_path}'. "
            f"Please run 'python -m ai_module.src.train' first."
        )

    if not vectorizer_path.exists():
        raise FileNotFoundError(
            f"Fitted TF-IDF vectorizer not found at '{vectorizer_path}'. "
            f"Please run 'python -m ai_module.src.train' first."
        )

    logger.info(f"Loading model from {model_path} and vectorizer from {vectorizer_path}...")
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    _CACHED_MODEL = model
    _CACHED_VECTORIZER = vectorizer
    return model, vectorizer


def validate_message_input(message: Any) -> Optional[str]:
    if message is None:
        return "Message cannot be None. Please provide a text message."

    if not isinstance(message, str):
        return f"Invalid input type: expected string, got {type(message).__name__}."

    stripped = message.strip()
    if len(stripped) < MIN_MESSAGE_LENGTH:
        return (
            f"Message is too short ({len(stripped)} character{'s' if len(stripped) != 1 else ''}). "
            f"Please provide a meaningful text message of at least {MIN_MESSAGE_LENGTH} characters."
        )

    if len(message) > MAX_MESSAGE_LENGTH:
        return (
            f"Message exceeds maximum allowed length ({len(message)} > {MAX_MESSAGE_LENGTH} characters). "
            f"Please provide a standard-length SMS message."
        )

    return None


def predict_message(
    message: str,
    model_path: Path = LOGISTIC_REGRESSION_MODEL_PATH,
    vectorizer_path: Path = TFIDF_VECTORIZER_PATH,
) -> Dict[str, Any]:
    validation_err = validate_message_input(message)
    if validation_err:
        return {
            "status": "error",
            "error_message": validation_err,
            "prediction": "unknown",
            "confidence": 0.0,
            "scam_probability": 0.0,
            "suspicious_indicators": [],
            "explanation": "Unable to evaluate message due to invalid input.",
            "disclaimer": STANDARD_DISCLAIMER,
        }

    try:
        model, vectorizer = load_artifacts(model_path, vectorizer_path)
    except FileNotFoundError as fnf_err:
        logger.error(str(fnf_err))
        return {
            "status": "error",
            "error_message": str(fnf_err),
            "prediction": "unknown",
            "confidence": 0.0,
            "scam_probability": 0.0,
            "suspicious_indicators": detect_suspicious_indicators(message),
            "explanation": "Scam detection service is unavailable due to missing model artifacts.",
            "disclaimer": STANDARD_DISCLAIMER,
        }

    clean_text = normalize_text(message)
    X_vec = vectorizer.transform([clean_text])

    try:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X_vec)[0]
            classes = list(model.classes_)
            scam_idx = classes.index(LABEL_SCAM) if LABEL_SCAM in classes else 1
            legit_idx = classes.index(LABEL_LEGITIMATE) if LABEL_LEGITIMATE in classes else 0

            scam_prob = float(proba[scam_idx])
            legit_prob = float(proba[legit_idx])

            if scam_prob >= 0.50:
                prediction_label = "scam"
                confidence = round(scam_prob, 4)
            else:
                prediction_label = "legitimate"
                confidence = round(legit_prob, 4)

            scam_probability = round(scam_prob, 4)
        else:
            raw_pred = model.predict(X_vec)[0]
            prediction_label = "scam" if raw_pred == LABEL_SCAM else "legitimate"
            confidence = 0.90 if prediction_label == "scam" else 0.85
            scam_probability = 0.90 if prediction_label == "scam" else 0.10

    except Exception as exc:
        logger.error(f"Inference error during message evaluation: {exc}")
        return {
            "status": "error",
            "error_message": f"Inference execution failed: {exc}",
            "prediction": "unknown",
            "confidence": 0.0,
            "scam_probability": 0.0,
            "suspicious_indicators": detect_suspicious_indicators(message),
            "explanation": "An error occurred while evaluating the message patterns.",
            "disclaimer": STANDARD_DISCLAIMER,
        }

    suspicious_indicators = detect_suspicious_indicators(clean_text)

    explanation = generate_explanation(
        prediction=prediction_label,
        confidence=confidence,
        suspicious_indicators=suspicious_indicators,
    )

    return {
        "status": "success",
        "prediction": prediction_label,
        "confidence": confidence,
        "scam_probability": scam_probability,
        "suspicious_indicators": suspicious_indicators,
        "explanation": explanation,
        "disclaimer": STANDARD_DISCLAIMER,
    }
