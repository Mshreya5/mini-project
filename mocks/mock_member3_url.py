"""
Mock Microservice: Member 3 - Privacy, Security and URL Analysis API
Port: 8002
Endpoint: POST /api/v1/analyze-url

Simulates Member 3's URL inspection and privacy preservation module.
"""
import re
from typing import List, Optional
from urllib.parse import urlparse
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Member 3 URL Security & Privacy Service (Simulator)",
    version="1.0.0"
)


class URLRequest(BaseModel):
    text: str = Field(..., description="Raw text to sanitize and inspect for URLs.")
    urls: Optional[List[str]] = None
    anonymize_pii: bool = True


class URLResponse(BaseModel):
    urls_found: List[str]
    url_risk: str  # SAFE, SUSPICIOUS, MALICIOUS, NO_URL
    indicators: List[str]
    privacy_redacted: bool


# Suspicious TLDs commonly used in phishing campaigns
SUSPICIOUS_TLDS = {".xyz", ".top", ".tk", ".ml", ".cf", ".work", ".click", ".ru", ".buzz"}

# Shortener domains that mask the true destination
SHORTENERS = {"bit.ly", "tinyurl.com", "is.gd", "t.co", "cutt.ly", "rb.gy", "shorturl.at"}

# Brand impersonation patterns in subdomains/paths
PHISHING_KEYWORDS = ["kyc", "sbi", "hdfc", "login", "secure", "verify", "pan", "aadhar", "bonus", "free"]


def redact_pii(text: str) -> str:
    """Masks 10-digit phone numbers and email addresses for privacy preservation."""
    # Redact phone numbers
    redacted = re.sub(r"\b[6-9]\d{9}\b", "[PHONE_REDACTED]", text)
    # Redact emails
    redacted = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[EMAIL_REDACTED]", redacted)
    return redacted


@app.get("/health")
def health():
    return {"status": "ONLINE", "module": "Member 3 - URL Analysis & Privacy"}


@app.post("/api/v1/analyze-url", response_model=URLResponse)
def analyze_url(payload: URLRequest):
    text = payload.text
    if payload.anonymize_pii:
        text = redact_pii(text)

    # Extract URLs if not already supplied
    raw_urls = payload.urls or re.findall(
        r"(?:https?:\/\/|www\.)[^\s/$.?#].[^\s]*",
        text,
        re.IGNORECASE
    )

    if not raw_urls:
        return URLResponse(
            urls_found=[],
            url_risk="NO_URL",
            indicators=[],
            privacy_redacted=payload.anonymize_pii
        )

    indicators = []
    is_malicious = False
    is_suspicious = False

    for u in raw_urls:
        # Standardize for parsing
        test_url = u if u.startswith("http") else "http://" + u
        parsed = urlparse(test_url)
        hostname = (parsed.hostname or "").lower()

        # 1. IP address in hostname
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname):
            indicators.append(f"Direct IP address used instead of reputable domain ({hostname})")
            is_malicious = True

        # 2. Free URL shortener
        if any(shortener in hostname for shortener in SHORTENERS):
            indicators.append(f"Masked/Shortened URL hiding true destination ({hostname})")
            is_suspicious = True

        # 3. Suspicious high-risk TLD
        if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS):
            indicators.append(f"High-risk low-reputation top-level domain ({hostname})")
            is_suspicious = True

        # 4. Brand spoofing / phishing keywords in unfamiliar domain
        has_phish_term = any(k in hostname or k in parsed.path.lower() for k in PHISHING_KEYWORDS)
        is_official = hostname.endswith("sbi.co.in") or hostname.endswith("hdfcbank.com") or hostname.endswith("gov.in")
        if has_phish_term and not is_official:
            indicators.append(f"Potential brand impersonation / phishing keywords in link ({hostname})")
            is_suspicious = True

        # 5. Non-secure HTTP for sensitive claims
        if parsed.scheme == "http" and has_phish_term:
            indicators.append("Insecure unencrypted HTTP connection requesting sensitive actions")
            is_suspicious = True

    # Compute overall URL risk
    if is_malicious or len(indicators) >= 2:
        url_risk = "MALICIOUS" if is_malicious else "SUSPICIOUS"
    elif is_suspicious or len(indicators) == 1:
        url_risk = "SUSPICIOUS"
    else:
        url_risk = "SAFE"

    return URLResponse(
        urls_found=raw_urls,
        url_risk=url_risk,
        indicators=indicators,
        privacy_redacted=payload.anonymize_pii
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
