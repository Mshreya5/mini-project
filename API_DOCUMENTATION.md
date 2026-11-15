# SilverShield AI — API & System Architecture Documentation

**Project Title:** Secure AI-Powered Elderly Digital Safety Companion with Privacy-Preserving Scam Detection and Early Warning  
**Module:** Member 4 — Risk Aggregation, Warning Logic, and System Integration (Integrating Member 1, 2, and 3)

---

## 1. System Architecture & Component Mapping

```
                                      +------------------------------------+
                                      |   Member 1: Accessible Frontend    |
                                      |    (Streamlit on Port 8501)        |
                                      |   - WCAG 2.1 AAA High Contrast     |
                                      |   - Multilingual Audio (EN/HI/KN)  |
                                      |   - Font Scaling (18px, 22px, 26px)|
                                      +-----------------+------------------+
                                                        |
                                                        | POST /api/v1/assess
                                                        v
                                      +------------------------------------+
                                      |  Member 4: Central Risk Engine     |
                                      |     (FastAPI on Port 8000)         |
                                      |   - Multi-factor Risk Aggregation  |
                                      |   - Senior-Friendly Warning Logic  |
                                      |   - Fail-Safe Error Handling       |
                                      +--------+------------------+--------+
                                               |                  |
                       POST /api/v1/predict    |                  |  POST /api/v1/analyze-url
                                               v                  v
+------------------------------------------------+      +-----------------------------------------------+
|      Member 2: ML Scam Prediction API          |      |  Member 3: Privacy & URL Security API         |
|             (Port 8001)                        |      |             (Port 8002)                       |
|   - ML text scam classification                |      |   - PII Sanitization & Masking                |
|   - Confidence score estimation                |      |   - Domain reputation & TLD inspection        |
|   - Scam trigger extraction                    |      |   - Typosquatting & IP address detection      |
+------------------------------------------------+      +-----------------------------------------------+
```

---

## 2. Documented API Contracts

### A. Central Assessment Endpoint (Member 4 Integration API)
- **Method:** `POST`
- **Route:** `/api/v1/assess`
- **Port:** `8000`

#### Request Payload
```json
{
  "message": "Urgent! Your SBI netbanking account is suspended. Update KYC immediately at http://bit.ly/sbi-verify-kyc",
  "sender": "+919876543210",
  "language": "English"
}
```

#### Field Specifications
| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | Message text (1 to 5000 chars, whitespace trimmed). |
| `sender` | string | No | Optional sender name or phone number. |
| `language` | string | No | Desired response language (`English`, `Hindi`, `Kannada`). Defaults to `English`. |

#### Response Payload (HTTP 200 OK)
```json
{
  "overall_risk": "HIGH",
  "message_prediction": "SCAM",
  "url_risk": "SUSPICIOUS",
  "risk_indicators": [
    "Urgent deadline pressure",
    "Bank impersonation",
    "Masked/Shortened URL hiding true destination",
    "Frightening threat of account blockage or utility disconnection"
  ],
  "warning": "Warning! This message may be fraudulent. Do not share OTPs, passwords or banking details.",
  "recommended_actions": [
    "Do not click any links or website addresses in this message.",
    "Do not transfer money or enter your UPI PIN for unexpected requests.",
    "Verify the sender by contacting the organization using official numbers from your passbook or bills.",
    "Take your time and discuss this message with your trusted family helper or caregiver."
  ],
  "risk_score": 0.85,
  "module_status": {
    "ml_service": "ONLINE",
    "url_service": "ONLINE"
  },
  "timestamp": "2026-11-15T18:30:00Z"
}
```

---

### B. Member 2 API: ML Scam Prediction API
- **Method:** `POST`
- **Route:** `/api/v1/predict`
- **Port:** `8001`

#### Request Payload
```json
{
  "text": "Your account is frozen due to pending KYC."
}
```

#### Response Payload
```json
{
  "prediction": "SCAM",
  "confidence": 0.89,
  "detected_triggers": [
    "Urgent deadline pressure",
    "Bank impersonation"
  ]
}
```

---

### C. Member 3 API: Privacy & URL Security Analysis API
- **Method:** `POST`
- **Route:** `/api/v1/analyze-url`
- **Port:** `8002`

#### Request Payload
```json
{
  "text": "Update KYC at http://bit.ly/sbi-kyc-verify",
  "urls": ["http://bit.ly/sbi-kyc-verify"],
  "anonymize_pii": true
}
```

#### Response Payload
```json
{
  "urls_found": ["http://bit.ly/sbi-kyc-verify"],
  "url_risk": "SUSPICIOUS",
  "indicators": [
    "Masked/Shortened URL hiding true destination (bit.ly)",
    "Potential brand impersonation / phishing keywords in link (sbi-kyc-verify)"
  ],
  "privacy_redacted": true
}
```

---

## 3. Risk Aggregation & Scoring Formulation

Rather than naively adding confidence percentages from different domains, Member 4 employs a transparent, multi-factor evaluation engine:

$$Composite\_Score = (w_{ML} \cdot Score_{ML}) + (w_{URL} \cdot Score_{URL}) + (w_{Heur} \cdot Score_{Heur})$$

- **Weights:** $w_{ML} = 0.45$, $w_{URL} = 0.35$, $w_{Heur} = 0.20$ (When no URLs are present, $w_{URL}$ is dynamically reallocated to ML and heuristic analysis).
- **Domain Escalation Overrides:**
  1. If `url_risk == MALICIOUS` $\rightarrow$ Escalates to **HIGH RISK**.
  2. If `ml_prediction == SCAM` and $confidence \ge 0.75$ $\rightarrow$ Escalates to **HIGH RISK**.
  3. If OTP or password harvesting patterns are identified with any supporting suspicion $\rightarrow$ Escalates to **HIGH RISK**.
  4. If multiple indicators are present ($\ge 2$) $\rightarrow$ Escalates to **HIGH RISK**.
  5. If single moderate indicator exists $\rightarrow$ Classified as **MEDIUM RISK**.
  6. Clean message with clean/no URL $\rightarrow$ Classified as **LOW RISK**.

---

## 4. Fail-Safe Resilience & Graceful Degradation

If external microservices experience network errors, 500 status codes, or timeouts (configured threshold: 3.0s):
- **Fail-Safe Principle:** The system **NEVER** defaults to `LOW RISK` if an error occurs.
- If Member 2 or 3 is unreachable, baseline risk is elevated to at least **MEDIUM RISK** or **HIGH RISK** if heuristic danger signs (such as OTP solicitation or account suspension threats) are detected.
- The `module_status` response explicitly marks the service as `OFFLINE_FALLBACK`.
