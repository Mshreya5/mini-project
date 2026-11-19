from __future__ import annotations

import logging
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from url_analysis.analyzer import analyze_url
from url_analysis.extractor import extract_urls
from url_analysis.models import (
    AnalyzeRequest,
    AnalyzeResponse,
    PrivacyInfoResponse,
    URLAnalysisResult,
)
from url_analysis.privacy import (
    check_consent,
    get_privacy_info,
    sanitize_message_for_extraction,
    validate_message,
)

logger = logging.getLogger("url_analysis.api")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

app = FastAPI(
    title="URL Analysis API",
    description="Member 3 — Privacy-preserving URL extraction and risk indicator analysis.",
    version="1.0.0",
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred. Please try again."},
    )


@app.post(
    "/analyze-url",
    response_model=AnalyzeResponse,
    summary="Extract and analyse URLs from a message",
    status_code=status.HTTP_200_OK,
)
async def analyze_url_endpoint(payload: AnalyzeRequest) -> AnalyzeResponse:
    permitted, reason = check_consent(payload.consent_given)
    if not permitted:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=reason)

    valid, error = validate_message(payload.message)
    if not valid:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error)

    sanitized = sanitize_message_for_extraction(payload.message)
    urls = extract_urls(sanitized)

    if not urls:
        return AnalyzeResponse(
            urls_found=False,
            url_count=0,
            results=[],
        )

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
    info = get_privacy_info()
    return PrivacyInfoResponse(**info)


@app.get("/health", include_in_schema=False)
async def health() -> dict:
    return {"status": "ok"}
