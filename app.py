"""FastAPI application — Member 3: URL Analysis API.

Endpoints:
  POST /analyze-url   — Extract and analyse URLs from a submitted message.
  GET  /privacy-info  — Return plain-language privacy disclosure.

Integration notes for Member 1 (Frontend) and Member 4 (Risk Aggregation):
  - /analyze-url accepts JSON: {"message": "...", "consent_given": true}
  - Response schema: AnalyzeResponse (see url_analysis/models.py)
  - Each URLAnalysisResult carries: url, suspicious, risk_score, risk_indicators, explanation
  - Member 4 should consume `results[*].risk_score` and `results[*].risk_indicators`
    for final risk aggregation — do NOT re-implement aggregation here.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from url_analysis.analyzer import analyze_url
from url_analysis.extractor import extract_urls
from url_analysis.models import AnalyzeRequest, AnalyzeResponse, PrivacyInfoResponse, URLAnalysisResult
from url_analysis.privacy import check_consent, get_privacy_info, sanitize_message_for_extraction, validate_message

# ---------------------------------------------------------------------------
# Logging — message text is NEVER logged (privacy by design)
# ---------------------------------------------------------------------------
logger = logging.getLogger("url_analysis.api")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

app = FastAPI(
    title="URL Analysis API",
    description="Member 3 — Privacy-preserving URL extraction and risk indicator analysis.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Global error handler — never expose internal details to clients
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred. Please try again."},
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post(
    "/analyze-url",
    response_model=AnalyzeResponse,
    summary="Extract and analyse URLs from a message",
    status_code=status.HTTP_200_OK,
)
async def analyze_url_endpoint(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Analyse a user-submitted message for suspicious URLs.

    Processing steps:
    1. Consent check — reject if consent_given is False.
    2. Input validation — size and type guards.
    3. PII sanitization — strip phone/email/card numbers before extraction.
    4. URL extraction — find all URLs in the sanitized text.
    5. Per-URL structural analysis — check risk indicators.
    6. Return structured JSON — raw message text is never included in response.
    """
    # 1. Consent gate
    permitted, reason = check_consent(payload.consent_given)
    if not permitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=reason)

    # 2. Input validation
    valid, error = validate_message(payload.message)
    if not valid:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error)

    # 3. Sanitize — remove PII, keep URLs intact
    sanitized = sanitize_message_for_extraction(payload.message)

    # 4. Extract URLs
    urls = extract_urls(sanitized)

    if not urls:
        return AnalyzeResponse(
            urls_found=False,
            url_count=0,
            results=[],
        )

    # 5. Analyse each URL
    results: list[URLAnalysisResult] = []
    for url in urls:
        ar = analyze_url(url)
        results.append(
            URLAnalysisResult(
                url=ar.url,
                url_found=ar.url_found,
                suspicious=ar.suspicious,
                risk_score=ar.risk_score,
                risk_indicators=ar.risk_indicators,
                explanation=ar.explanation,
            )
        )

    # Log only metadata — never the message text or full URLs
    logger.info("Analyzed %d URL(s); suspicious count: %d", len(results), sum(r.suspicious for r in results))

    return AnalyzeResponse(
        urls_found=True,
        url_count=len(results),
        results=results,
    )


@app.get(
    "/privacy-info",
    response_model=PrivacyInfoResponse,
    summary="Privacy disclosure for this module",
    status_code=status.HTTP_200_OK,
)
async def privacy_info_endpoint() -> PrivacyInfoResponse:
    """Return plain-language privacy information about what data is processed and how it is protected."""
    info = get_privacy_info()
    return PrivacyInfoResponse(**info)


@app.get("/health", include_in_schema=False)
async def health() -> dict:
    return {"status": "ok"}
