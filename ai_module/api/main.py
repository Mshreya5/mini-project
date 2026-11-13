import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from ai_module.api.schemas import HealthResponse, MessageRequest, PredictionResponse
from ai_module.src.predict import load_artifacts, predict_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_artifacts()
        logger.info("SilverShield AI ML models and TF-IDF vectorizer preloaded successfully.")
    except FileNotFoundError as err:
        logger.warning(
            f"Artifacts not found during startup: {err}\n"
            "Endpoints will attempt on-demand loading or prompt to run 'python -m ai_module.src.train'."
        )
    yield


app = FastAPI(
    title="SilverShield AI — Scam Message Detection API",
    description=(
        "Machine learning prediction service designed to protect elderly individuals "
        "from SMS scams, social engineering, and fraudulent credential harvesting. "
        "Returns model predictions, confidence scores, heuristic indicators, and explainable guidance."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health and model readiness check",
)
@app.get(
    "/api/v1/health",
    response_model=HealthResponse,
    tags=["Health"],
    include_in_schema=False,
)
def health_check() -> HealthResponse:
    try:
        load_artifacts()
        loaded = True
    except Exception:
        loaded = False

    return HealthResponse(
        status="healthy",
        service="SilverShield AI Scam Detection Module",
        model_loaded=loaded,
        version="1.0.0",
    )


@app.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Scam Detection"],
    summary="Analyze SMS text for scam likelihood",
)
@app.post(
    "/api/v1/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Scam Detection"],
    include_in_schema=False,
)
def predict_endpoint(payload: MessageRequest) -> PredictionResponse:
    result = predict_message(payload.message)

    if result.get("status") == "error":
        error_msg = result.get("error_message", "Invalid input message.")
        if "not found" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=error_msg,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg,
        )

    return PredictionResponse(
        prediction=result["prediction"],
        confidence=result["confidence"],
        suspicious_indicators=result["suspicious_indicators"],
        explanation=result["explanation"],
        scam_probability=result.get("scam_probability"),
        status="success",
        disclaimer=result.get("disclaimer"),
    )


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "false").lower() == "true"

    uvicorn.run("ai_module.api.main:app", host=host, port=port, reload=reload)
