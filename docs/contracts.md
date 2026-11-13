# Module Contracts

Everything here is what this service *actually* sends and reads. Adapter code is
in `app/clients/`. If a field below does not match your module, change the module
or tell me - do not add a second endpoint.

---

## Member 2 - Scam classification API

### Request

```http
POST {SCAM_API_URL}
Content-Type: application/json

{ "message": "Dear customer, share the OTP to unblock your account." }
```

`SCAM_API_URL` defaults to `http://127.0.0.1:8001/predict`.

### Response

```json
{
  "prediction": "SCAM",
  "confidence": 0.94,
  "signals": ["otp_request", "urgency"]
}
```

| Field | Required | Accepted aliases | Notes |
| --- | --- | --- | --- |
| `prediction` | yes | `message_prediction`, `label`, `classification`, `scam_prediction`, `result_label` | `SCAM` / `LEGITIMATE`. Also accepts `spam`, `phishing`, `fraud`, `ham`, `safe`, `1`, `0`, booleans |
| `confidence` | recommended | `confidence_score`, `probability`, `scam_probability`, `score` | `0.0`-`1.0`. `87` and `"0.87"` are both accepted |
| `signals` | optional | `signal`, `keywords`, `matched_keywords`, `indicators`, `red_flags`, `flags`, `evidence` | Strings or objects with `name`/`token`/`id`/`label`. Case and spaces are normalised |

The payload may be wrapped in `data`, `result`, `analysis`, `response` or
`payload`; the adapter unwraps it.

### The one thing I need from you

`signals` is what turns your output into concrete advice. Any of these token
values is recognised today (add more in `config/risk_config.json` →
`signal_map`):

`otp`, `otp_request`, `one_time_password`, `verification_code`, `password`, `pin`,
`credentials`, `bank_details`, `bank_account`, `card_details`, `cvv`,
`account_number`, `payment`, `payment_request`, `money_transfer`, `gift_card`,
`crypto`, `wire_transfer`, `urgency`, `time_pressure`, `immediate_action`,
`act_now`, `deadline`, `account_suspension`, `legal_action`, `account_blocked`,
`deactivation`, `impersonation`, `authority_claim`, `bank_claim`,
`government_claim`, `delivery_claim`, `prize`, `lottery`, `refund`, `reward`,
`cashback`, `login_link`, `password_reset`, `verify_account`,
`personal_information`, `identity_document`, `kyc_update`.

Sending raw feature names or SHAP contributions instead is fine too - they are
accepted and simply ignored when unmapped. Nothing here re-runs your model.

### Behaviour I rely on

* `confidence` is your model's confidence that the message is a **scam**, even
  when `prediction` is `LEGITIMATE`. If it means something else, tell me and I
  will invert the reading.
* A missing `prediction` is treated as an unusable response, not as "safe".

---

## Member 3 - URL analysis API

### Request

```http
POST {URL_API_URL}
Content-Type: application/json

{ "url": "http://secure-bank-verify.xyz/login" }
```

`URL_API_URL` defaults to `http://127.0.0.1:8002/analyze-url`. Exactly one URL is
sent per call: the explicit `url` field if the frontend supplied one, otherwise
the first link found in the message.

### Response

```json
{
  "url_risk": "SUSPICIOUS",
  "flags": ["shortened", "no_https"],
  "score": 0.61
}
```

| Field | Required | Accepted aliases | Notes |
| --- | --- | --- | --- |
| `url_risk` | yes | `risk_level`, `risk`, `verdict`, `classification`, `level`, `label` | `SAFE` / `SUSPICIOUS` / `MALICIOUS`. Also accepts `clean`, `benign`, `phishing`, `dangerous`, `unsafe`, `high`, `medium`, `low` |
| `flags` | optional | `reasons`, `indicators`, `signals`, `red_flags`, `findings`, `issues` | Recognised: `shortened`, `shortened_url`, `url_shortener`, `ip_address`, `raw_ip`, `lookalike`, `typosquatting`, `homoglyph`, `punycode`, `suspicious_tld`, `phishing_keywords`, `no_https`, `not_https` |
| `score` | optional | `risk_score`, `confidence` | Recorded but never summed against the ML confidence |

Boolean shortcuts are read too: `is_shortened`, `is_ip_address`, `lookalike`,
`is_https` (false adds `no_https`), `is_malicious`, `is_suspicious`, `is_safe`.

### Behaviour I rely on

* An unrecognised verdict string is treated as an unusable response, which makes
  the overall result `DEGRADED` and never `LOW`. Silently returning `SAFE` for a
  URL you could not analyse would defeat the safety guarantee.
* The full URL is not echoed back to the frontend. The response exposes only the
  scheme and host (`analysed_url`), so query strings and tokens do not leak.

---

## Member 1 - Frontend integration

* One call does everything: `POST /api/v1/analyze` with `{ "message": "..." }`.
* Render `warning` as the headline and `recommended_actions` as a list. Both are
  already written in plain language; no UI copy is needed.
* Colour by `overall_risk` only. Use `status` for a secondary badge:
  `DEGRADED` means "we could not finish every check".
* `risk_indicators` are short labels suitable for an expandable "Why?" section.
  `score.reasons` gives the audit explanation if you want a detail view.
* `module_status` is safe to surface as a small diagnostics line
  (e.g. "Link check unavailable").
* CORS origins come from `CORS_ORIGINS` (comma separated).

---

## Integration checklist

1. Member 1: confirm the frontend origin for `CORS_ORIGINS`.
2. Member 2: confirm `SCAM_API_URL`, the `confidence` semantics, and whether
   `signals` will be populated.
3. Member 3: confirm `URL_API_URL`, the exact `url_risk` vocabulary, and flag
   names.
4. Run `python -m pytest` - the fake clients prove the pipeline; then point
   `.env` at the live services and check `GET /api/v1/health`.
