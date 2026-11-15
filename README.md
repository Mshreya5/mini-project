# Risk Aggregation & Integration Service

Member 4 deliverable for the *Secure AI-Powered Elderly Digital Safety Companion*.

This service is the integration point of the project. It calls the scam
classification module (Member 2) and the URL analysis module (Member 3), turns
their outputs into named risk indicators, and produces one explainable risk level
with an elderly friendly warning and concrete safety actions.

It does **not** reimplement any ML model or URL reputation logic. It classifies
nothing itself; it aggregates.

---

## 1. Run it

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.txt   # Windows
# source .venv/bin/activate && pip install -r requirements-dev.txt  # macOS / Linux

cp .env.example .env          # then edit the two module URLs
.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000
```

| URL | What it is |
| --- | --- |
| `http://127.0.0.1:8000/docs` | Interactive OpenAPI docs |
| `POST /api/v1/analyze` | The endpoint the frontend calls |
| `GET /api/v1/health` | Liveness plus configured module endpoints |
| `GET /api/v1/risk-config` | The exact rule set used for decisions |

Run the tests with `python -m pytest` (61 tests, no network required).

---

## 2. Request

```http
POST /api/v1/analyze
Content-Type: application/json
```

```json
{
  "message": "URGENT: your account is blocked. Share the OTP to keep it active.",
  "url": "http://secure-bank-verify.xyz/login"
}
```

`url` is optional. When it is omitted, the first link found inside `message` is
analysed. When the message contains no link at all, the URL module is not called
and the response reports `"url_risk": "NOT_APPLICABLE"` — that is a normal
outcome, not a failure.

## 3. Response

```json
{
  "analysis_id": "9f2c...",
  "generated_at": "2026-11-13T14:44:56Z",
  "overall_risk": "HIGH",
  "status": "OK",
  "message_prediction": "SCAM",
  "message_confidence": 0.94,
  "url_risk": "SUSPICIOUS",
  "analysed_url": "http://secure-bank-verify.xyz/",
  "risk_indicators": [
    "Very high confidence scam prediction",
    "Asks for an OTP, PIN or password",
    "Uses urgency or a short deadline",
    "Link shows suspicious characteristics"
  ],
  "warning": "Warning! This message may be fraudulent. Do not share OTPs, passwords or banking details.",
  "recommended_actions": [
    "Never share an OTP, PIN or password. No bank, police officer or company will ever ask for it.",
    "Do not transfer money to anyone you have not confirmed in person or by a number you looked up yourself.",
    "Do not reply to this message and do not call any number it gives you.",
    "Confirm who really sent this before you respond or share anything."
  ],
  "module_status": [
    { "name": "scam_detector", "state": "OK", "failed": false, "latency_ms": 84 },
    { "name": "url_analyzer", "state": "OK", "failed": false, "latency_ms": 121 }
  ],
  "score": {
    "total": 55,
    "raw_total": 78,
    "thresholds": { "medium": 24, "high": 55 },
    "capped_sources": ["message"],
    "contributions": [
      {
        "indicator_id": "SCAM_PREDICTION",
        "label": "Message classified as a possible scam",
        "source": "message",
        "severity": "HIGH",
        "points": 30,
        "applied_points": 30
      }
    ],
    "applied_overrides": ["OVR-01"],
    "reasons": ["OVR-01: The scam model is highly confident that this message is fraudulent."]
  },
  "config_version": "1.0.0"
}
```

The six fields you asked for (`overall_risk`, `message_prediction`, `url_risk`,
`risk_indicators`, `warning`, `recommended_actions`) are present unchanged. The
additional blocks exist for transparency and for the frontend's "why?" panel.

---

## 4. How the risk level is decided

Never by adding the two modules' scores together. Three explicit steps:

**Step 1 — Indicators.** Module outputs become named indicators. A confidence of
`0.94` plus `signals: ["otp_request"]` becomes `SCAM_PREDICTION`,
`HIGH_CONFIDENCE_SCAM` and `OTP_REQUEST`. Each carries a fixed severity from the
rule set.

**Step 2 — Deterministic overrides.** Some combinations are decided outright:

| Rule | Condition | Result |
| --- | --- | --- |
| `OVR-01` | scam prediction with confidence >= 0.8 | HIGH |
| `OVR-02` | URL module says `MALICIOUS` | HIGH |
| `OVR-03` | an OTP is requested **and** a link is present | HIGH |

These rules are why a clean URL result can never dilute a strong scam verdict.
They are marked `decisive`, so they contribute no points and cannot be counted
twice.

**Step 3 — Scored aggregation.** Remaining indicators add severity points
(`CRITICAL 45`, `HIGH 30`, `MEDIUM 18`, `LOW 6`). Each module's contribution is
capped — `message` 55, `url` 45, `system` 18 — so one module cannot dominate. The
score maps to a level at `>= 24` MEDIUM and `>= 55` HIGH. The final level is the
more severe of the override result and the threshold result.

Every weight, cap and threshold lives in [`config/risk_config.json`](config/risk_config.json).
Change the numbers, not the code. `GET /api/v1/risk-config` publishes them.

### When a module fails

| Situation | Outcome |
| --- | --- |
| A required module times out / errors / returns something unusable | `status: "DEGRADED"`, level floored at **MEDIUM**, indicator recorded, warning states that the check was incomplete |
| Message has no link | `url_risk: "NOT_APPLICABLE"`, level unaffected |
| Invalid input | `422` with `error: "invalid_request"` and per-field details |

A degraded result is never `LOW`, which satisfies the rule that an unavailable
module must not make a message look safe.

---

## 5. Project layout

```
app/
  main.py                 application factory, CORS, error handlers
  settings.py             env settings + risk rule set loading and validation
  schemas.py              public request/response models
  api/routes.py           analyze, health, risk-config
  clients/
    base.py               JSON POST with timeout, retry, failure classification
    parsing.py            tolerant field aliases for upstream payloads
    scam_detector.py      Member 2 adapter
    url_analyzer.py       Member 3 adapter
  core/
    models.py             normalised domain models
    urls.py               link discovery and normalisation
    indicators.py         module output -> indicator catalogue
    risk_engine.py        overrides, caps, thresholds, degraded floor
    warnings.py           warning and action wording
    orchestrator.py       concurrent calls + response assembly
config/risk_config.json   the entire assessment policy
docs/contracts.md         what each member must expose
tests/                    61 tests across all seven required scenarios
```

## 6. Documentation for the other members

* [`docs/contracts.md`](docs/contracts.md) — the exact request and response
  contract for Member 2 and Member 3, the tolerance rules, and the integration
  checklist for Member 1.
