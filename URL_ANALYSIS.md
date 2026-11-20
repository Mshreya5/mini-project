# URL Analysis and Privacy Module Documentation

**Project Title:** Secure AI-Powered Elderly Digital Safety Companion with Privacy-Preserving Scam Detection and Early Warning  
**Module Owner:** Member 3 — Privacy, Cybersecurity and URL Analysis  
**Integrates With:** Member 1 (Frontend), Member 2 (AI Scam Detection), Member 4 (Risk Aggregation)  
**Status:** Implemented & Tested

---

## 1. Module Responsibilities & Strict Boundaries

| Responsibility | Owner |
|---|---|
| Frontend UI | Member 1 |
| ML scam classification | Member 2 |
| **URL extraction, structural analysis, privacy gate, API** | **Member 3 (this module)** |
| Final risk aggregation and warning logic | Member 4 |

This module does **not** perform ML classification (Member 2) and does **not** produce a final risk verdict (Member 4). It provides structured per-URL indicator data for Member 4 to aggregate.

---

## 2. Architecture Overview

```
User Message
     │
     ▼
[Privacy Gate]          url_analysis/privacy.py
  • Consent check
  • Input validation
  • PII sanitization (phone/email/card stripped)
     │
     ▼
[URL Extractor]         url_analysis/extractor.py
  • Regex-based URL detection
  • Handles http/https and bare www. URLs
  • Deduplication
     │
     ▼
[URL Analyzer]          url_analysis/analyzer.py  (per URL)
  • 9 structural/lexical checks (no HTTP requests)
  • suspicious = True only when risk_score ≥ 2
  • Query strings stripped from output
     │
     ▼
[API Response]          app.py  →  AnalyzeResponse JSON
  • Consumed by Member 4 for risk aggregation
```

---

## 3. File Structure

```
mini_project/
├── url_analysis/
│   ├── __init__.py       # Package exports
│   ├── models.py         # Pydantic request/response schemas
│   ├── extractor.py      # URL extraction from raw text
│   ├── analyzer.py       # Risk indicator checks
│   └── privacy.py        # Consent gate, validation, PII sanitization
├── app.py                # FastAPI application (endpoints)
├── tests/
│   ├── test_url_extractor.py
│   ├── test_url_analyzer.py
│   └── test_url_api.py
├── requirements-url.txt
└── URL_ANALYSIS.md       # This file
```

---

## 4. API Endpoints

### `POST /analyze-url`

Extracts and analyses URLs from a submitted message.

**Request:**
```json
{
  "message": "Your account is suspended. Verify now: http://paypal-secure.xyz/login",
  "consent_given": true
}
```

**Response:**
```json
{
  "urls_found": true,
  "url_count": 1,
  "results": [
    {
      "url": "http://paypal-secure.xyz/login",
      "url_found": true,
      "suspicious": true,
      "risk_score": 3,
      "risk_indicators": [
        "Suspicious top-level domain (.xyz)",
        "Possible brand impersonation: 'paypal' in domain",
        "Suspicious path keywords (login/verify/account/secure)"
      ],
      "explanation": "The URL contains 3 characteristics commonly associated with phishing or scam links. Exercise caution before clicking."
    }
  ],
  "privacy_note": "Your message was analyzed in memory only. No message text or URL content was stored or logged."
}
```

**Error responses:**

| Status | Condition |
|---|---|
| 403 | `consent_given: false` |
| 422 | Blank message or missing field |
| 500 | Unexpected internal error (detail never exposes internals) |

---

### `GET /privacy-info`

Returns plain-language privacy disclosure.

**Response:**
```json
{
  "what_is_processed": "...",
  "why_it_is_processed": "...",
  "how_data_is_protected": ["...", "..."],
  "data_retention": "..."
}
```

---

## 5. Risk Indicator Checks

All checks are **purely structural and lexical** — no HTTP requests are ever made.

| Check | Indicator Example |
|---|---|
| IP-based host | `"IP address used instead of domain name"` |
| URL shortener | `"URL shortener detected"` |
| Suspicious TLD | `"Suspicious top-level domain (.xyz)"` |
| Brand impersonation | `"Possible brand impersonation: 'paypal' in domain"` |
| Homoglyph substitution | `"Possible homoglyph substitution targeting 'paypal'"` |
| Excessive subdomains | `"Unusual subdomain depth (5 labels)"` |
| Suspicious path keywords | `"Suspicious path keywords (login/verify/account/secure)"` |
| Excessively long URL | `"Unusually long URL (may obscure destination)"` |
| Embedded redirect | `"Embedded redirect URL detected"` |
| @ symbol in URL | `"@ symbol in URL (host spoofing technique)"` |

**Threshold rule:** `suspicious = True` only when `risk_score >= 2`. A single indicator is reported but does not classify the URL as suspicious.

---

## 6. Privacy Design

| Principle | Implementation |
|---|---|
| Data minimization | Only URLs and risk scores are returned — never raw message text |
| Consent enforcement | `consent_given: false` → HTTP 403 before any processing |
| PII sanitization | Phone numbers, emails, card numbers stripped before URL extraction |
| No query string leakage | Query parameters stripped from all URLs in API responses |
| No logging of message content | Logger records only URL count and suspicious count |
| No external requests | All analysis is local — no third-party URL scanning services |
| Payload size limit | 64 KiB maximum (consistent with Member 2's privacy module) |

---

## 7. Integration Contract for Member 4 (Risk Aggregation)

Member 4 should call `POST /analyze-url` and consume the response as follows:

```python
import httpx

response = httpx.post(
    "http://localhost:8000/analyze-url",
    json={"message": user_message, "consent_given": True},
)
data = response.json()

# Aggregate across all found URLs
url_risk_scores = [r["risk_score"] for r in data["results"]]
any_suspicious = any(r["suspicious"] for r in data["results"])
all_indicators = [ind for r in data["results"] for ind in r["risk_indicators"]]

# Pass to Member 4's final risk aggregation logic
```

**Key fields for aggregation:**

| Field | Type | Description |
|---|---|---|
| `results[*].suspicious` | bool | True if ≥2 indicators fired |
| `results[*].risk_score` | int | Raw count of triggered indicators |
| `results[*].risk_indicators` | list[str] | Human-readable indicator labels |
| `results[*].explanation` | str | Plain-language summary for UI display |

---

## 8. Running the Application

### Install dependencies
```bash
pip install -r requirements-url.txt
```

### Start the API server
```bash
uvicorn app:app --reload --port 8000
```

### Run tests
```bash
python -m pytest tests/test_url_extractor.py tests/test_url_analyzer.py tests/test_url_api.py -v
```

---

## 9. Viva & Evaluation Guide

**State your role (30 seconds):**
> *"I am Member 3, responsible for Privacy, Cybersecurity, and URL Analysis. My module extracts URLs from user messages, checks them for structural phishing indicators using nine lexical checks, enforces user consent before any processing, and strips all PII from messages before analysis. No network requests are made — all analysis is local and privacy-preserving."*

**Key points to highlight:**
- **Privacy by Design:** PII is stripped before URL extraction; query strings are removed from all outputs; message text is never logged or stored.
- **Safe analysis:** Zero HTTP requests — no risk of accidentally triggering malicious URLs.
- **Conservative flagging:** A URL is only marked suspicious with 2+ indicators, avoiding false positives that could alarm elderly users unnecessarily.
- **Clean integration contract:** Structured JSON output with `risk_score` and `risk_indicators` ready for Member 4's aggregation.
