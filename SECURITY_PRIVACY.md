# Cybersecurity and Privacy Architecture Documentation

**Project Title:** Secure AI-Powered Elderly Digital Safety Companion with Privacy-Preserving Scam Detection and Early Warning  
**Module Owner:** Member 2 — Cybersecurity and Privacy  
**Target Collaborator:** Member 4 (Main Backend & Database Integration Lead)  
**Academic Review:** College Mini-Project Evaluation  
**Status:** Implemented & 100% Tested (29/29 Pytest Tests Passing)

---

## 1. Module Responsibilities & Strict Boundaries

In our four-member team:
- **Member 1 (ML Engineer):** Owns scam dataset, scikit-learn model training, feature vectorization, and model inference file.
- **Member 2 (Me - Cybersecurity & Privacy):** Owns password hashing, authentication security rules, consent management logic, privacy-by-design data handling, access control, and security unit tests.
- **Member 3 (Frontend Engineer):** Owns the React user interface, accessible elderly-friendly layouts, and browser client logic.
- **Member 4 (Backend Integration Lead):** Owns the main FastAPI application entry point, database connection and collections, API routing, integration of Member 1's ML model into `/analyze`, and application deployment.

### Strict Scope Compliance:
Member 2 **does not** create the main backend application from scratch, **does not** configure the production database, and **does not** implement the machine-learning prediction model. Instead, Member 2 provides an isolated, reusable Python package (`security/`) and a comprehensive test suite (`tests/`) designed for Member 4 to easily import and enforce across backend routes.

---

## 2. Password Hashing and Authentication Security Rules

All cryptographic and authentication rules are implemented in `security/passwords.py` and `security/auth_rules.py`.

### Argon2id Password Hashing (`security/passwords.py`)
- **Algorithm:** Argon2id (OWASP recommended memory-hard password hashing algorithm).
- **Parameters:**
  - `time_cost = 2` iterations
  - `memory_cost = 65536 KiB` (64 MiB RAM usage per hash)
  - `parallelism = 1` thread
  - `hash_len = 32` bytes
- **Salts:** 16-byte cryptographically secure random salt automatically generated per password by `argon2-cffi`. Plaintext passwords are never stored or logged.
- **Verification:** Constant-time verification using `verify_password(plain, hash)` to resist timing side-channel attacks.
- **Rehashing Detection:** `needs_rehash(hash)` detects if stored hashes require parameter upgrades.

### Server-Side Password Strength Rules (`security/auth_rules.py`)
Function: `validate_password_strength(password: str) -> (bool, str)`
- **Length:** Minimum 8 characters, maximum 128 characters (prevents CPU exhaustion attacks via overly large hashing payloads).
- **Complexity:** Must contain both letters and numbers. Designed to maintain strong hygiene without overburdening elderly users.

### Anti-Enumeration Protections
- **Generic Errors:** `GENERIC_LOGIN_ERROR = "Invalid email or password."` and `GENERIC_REGISTRATION_ERROR` prevent attackers from determining whether a specific elderly person's email is registered.
- **Timing Equalizer:** `resist_timing_enumeration()` runs a dummy Argon2id verification cycle when an account is not found, ensuring uniform response times.

### Sliding-Window Rate Limiting (`security/auth_rules.py`)
Class: `SlidingWindowRateLimiter`
- Tracks request timestamps per client IP / key within a sliding time window.
- Returns `(is_allowed, retry_after_seconds)`.
- **Recommended Thresholds for Member 4:**
  - Login attempts: Max 5 attempts per 60 seconds per IP.
  - Registration: Max 3 attempts per 300 seconds per IP.
- Triggers HTTP 429 with `Retry-After` header when exceeded.

### Session & Token Security
- **JWT Issuance:** `create_token(subject, secret_key, expires_minutes=60)` signs tokens using HMAC-SHA256 (`HS256`) with required `sub`, `iat`, and `exp` claims.
- **Token Invalidation / Blacklist:** `invalidate_token(token)` and `is_token_blacklisted(token)` enable immediate session revocation on logout.
- **Dual Session Recommendation for Member 4 & Member 3:**
  - **HttpOnly Cookies:** Recommend setting `access_token` in an `HttpOnly`, `SameSite=Lax` cookie (`Secure=True` in production HTTPS). This prevents XSS attacks from reading tokens in JavaScript.
  - **CSRF Defense:** For cookie-authenticated state-changing requests (`POST`, `PUT`, `DELETE`), Member 4 should verify an `X-CSRF-Token` header using `verify_csrf_token(token, session_id, csrf_secret)` (HMAC-SHA256).
  - **Bearer Header:** Support `Authorization: Bearer <token>` for API testing and Swagger UI.

---

## 3. Consent Management Business Logic

All consent rules and validation logic are implemented in `security/consent.py`.

### Granular, Unbundled Consent Model
In compliance with data protection principles (GDPR, India's DPDP Act), consent must never be bundled or pre-selected:

| Consent Key | Category | Default State | Legal Basis & Rule |
|---|---|---|---|
| `consent_message_analysis` | Immediate Safety Analysis | **True** (Required) | **Service Delivery:** Strictly necessary to analyze the message in memory. Text is discarded immediately after analysis. |
| `consent_save_history` | Save Past Check Results | **False** (Unselected) | **Optional Feature:** Allows seniors to view past safety ratings. Must never be pre-selected. |
| `consent_analytics` | Anonymous Threat Statistics | **False** (Unselected) | **Optional Feature:** Aggregated threat keywords with all PII removed. Must never be pre-selected. |
| `consent_caregiver_sharing` | Caregiver Notification | **False** (Disabled) | **Future Extension:** Marked as an optional preview feature. Disabled pending team approval. |

### Audit Trail Generation
- `record_consent_update(current_record, updated_fields, policy_version)` updates preferences and automatically appends a timestamped `ConsentAuditEntry`.
- Records: `timestamp`, `purpose`, `consented` (boolean), `action` (`"granted"` or `"withdrawn"`), and `policy_version`.

### Plain-Language Elderly Transparency Notices
`get_elderly_transparency_notices(preferences)` produces structured disclosures written in simple, non-jargon language for Member 3's React UI to display:
- Explains that messages are analyzed in computer memory and deleted immediately.
- Confirms that messages are **never shared with external advertisers or commercial entities**.
- Informs users that they can withdraw optional consent or erase history at any time.

---

## 4. Privacy-Preserving Data Handling Policy

Implemented in `security/privacy.py`.

### Zero Permanent Message Persistence
- **Rule:** Original SMS, email text, or URL contents must **never** be written to permanent database storage.
- Analysis is executed strictly in volatile RAM.
- When `consent_save_history` is enabled, Member 4 must call `prepare_history_record(user_id, message_type, risk_level, risk_score)` which extracts **only risk metadata** and strictly excludes raw message content.

### Sensitive Data Scrubbing & Log Filter
`SensitiveDataRedactingFilter` intercepts application logging records and masks:
- Passwords and secrets $\rightarrow$ `[REDACTED_SECRET]`
- Bearer tokens $\rightarrow$ `Bearer [REDACTED_TOKEN]`
- Credit card numbers $\rightarrow$ `[REDACTED_CARD_NUMBER]`
- OTP / 2FA codes $\rightarrow$ `[REDACTED_OTP]`
- Phone numbers $\rightarrow$ `[REDACTED_PHONE]`
- Email addresses $\rightarrow$ `a***@domain.com`
- Raw message contents $\rightarrow$ `[MESSAGE_CONTENT_NOT_LOGGED_FOR_PRIVACY]`

### Request Payload Limiting (DoS Defense)
- `validate_payload_size(content_length)` enforces `MAX_MESSAGE_PAYLOAD_BYTES = 65536` (64 KiB) to prevent memory exhaustion DoS attacks on the scam analysis endpoint.

---

## 5. Access-Control Rules

Implemented in `security/access_control.py`.

### Principles:
1. **Token-Derived Identity:** Identity is extracted exclusively from cryptographically verified tokens via `derive_identity_from_token(token, secret_key)`.
2. **Rejection of Client-Supplied IDs:** Client-provided query parameters or body fields (`?user_id=...`) are **never** trusted as proof of identity.
3. **Resource Ownership Enforcement:** `enforce_resource_ownership(authenticated_user_id, resource_owner_id)` guarantees that User A can never view or modify User B's records, raising `AccessDeniedError` on mismatch.
4. **Response Data Filtering:** `filter_user_profile(user_data)` ensures internal password hashes and salts are stripped before returning data to clients.
5. **Action Gatekeeping:** `verify_action_consent(preferences, purpose)` checks that active consent exists before performing protected actions (e.g. blocking analysis if consent is withdrawn).

---

## 6. Integration Contract and Handover Guide for Member 4

Member 4 can integrate Member 2's security module using simple Python imports:

### A. Registering a User & Hashing Passwords
```python
from security.passwords import hash_password
from security.auth_rules import validate_password_strength, GENERIC_REGISTRATION_ERROR
from security.consent import create_default_consent

# 1. Validate password strength
is_valid, error_msg = validate_password_strength(request.password)
if not is_valid:
    raise HTTPException(status_code=422, detail=error_msg)

# 2. Check duplicate email safely
if await db.users.find_one({"email": request.email.lower()}):
    raise HTTPException(status_code=400, detail=GENERIC_REGISTRATION_ERROR)

# 3. Hash with Argon2id and create default consent
hashed_pwd = hash_password(request.password)
consent_doc = create_default_consent(user_id=new_user_id, opt_in_history=request.consent_save_history)
```

### B. Authenticating Login & Rate Limiting
```python
from security.passwords import verify_password
from security.auth_rules import rate_limiter, resist_timing_enumeration, create_token, generate_csrf_token, GENERIC_LOGIN_ERROR

# 1. Check rate limit
allowed, retry_after = rate_limiter.is_allowed(f"login:{client_ip}", max_requests=5, window_seconds=60)
if not allowed:
    raise HTTPException(status_code=429, detail={"error": "Too many attempts", "retry_after": retry_after})

# 2. Authenticate user
user = await db.users.find_one({"email": request.email.lower()})
if not user or not verify_password(request.password, user["password_hash"]):
    resist_timing_enumeration()
    raise HTTPException(status_code=401, detail=GENERIC_LOGIN_ERROR)

# 3. Issue token
token = create_token(subject=user["id"], secret_key=SECRET_KEY)
csrf_token = generate_csrf_token(session_id=user["id"], csrf_secret=CSRF_SECRET)
```

### C. Protecting Routes & Enforcing Ownership
```python
from security.access_control import derive_identity_from_token, enforce_resource_ownership

# Extract authenticated user identity
auth_header = request.headers.get("Authorization", "")
token = auth_header.replace("Bearer ", "")
user_id = derive_identity_from_token(token, secret_key=SECRET_KEY)

# Verify ownership before returning private history
record = await db.analysis_history.find_one({"id": record_id})
enforce_resource_ownership(authenticated_user_id=user_id, resource_owner_id=record["user_id"])
```

### D. Enforcing Privacy on the `/analyze` Endpoint
```python
from security.privacy import validate_payload_size, prepare_history_record, SensitiveDataRedactingFilter
from security.consent import can_process_message, can_save_history

# 1. Validate payload size
valid, msg = validate_payload_size(request.headers.get("content-length"))
if not valid:
    raise HTTPException(status_code=413, detail=msg)

# 2. Verify active consent
if not can_process_message(user_consent.preferences):
    raise HTTPException(status_code=403, detail="Consent for message analysis has been revoked.")

# 3. Process ML inference in memory (Member 1's model)
risk_score, risk_level = ml_model.predict(request.content)

# 4. Optional history saving: SAVE METADATA ONLY, NEVER RAW CONTENT
if can_save_history(user_consent.preferences):
    history_entry = prepare_history_record(user_id=user_id, message_type=request.type, risk_level=risk_level, risk_score=risk_score)
    await db.analysis_history.insert_one(history_entry)
```

---

## 7. Security Test Suite & Actual Results

Run tests via:
```bash
python -m pytest tests/ -v
```

**Actual Verified Test Results (29 Passed):**
```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\Dhanya\Desktop\mini_project
collected 29 items

tests/test_access_control.py::test_derive_identity_from_valid_token PASSED [  3%]
tests/test_access_control.py::test_derive_identity_from_invalid_token_fails PASSED [  6%]
tests/test_access_control.py::test_derive_identity_from_revoked_token_fails PASSED [ 10%]
tests/test_access_control.py::test_resource_ownership_enforcement PASSED [ 13%]
tests/test_access_control.py::test_user_profile_filtering PASSED         [ 17%]
tests/test_access_control.py::test_action_consent_verification PASSED    [ 20%]
tests/test_auth_rules.py::test_password_strength_validation PASSED       [ 24%]
tests/test_auth_rules.py::test_anti_enumeration_constants_and_timing PASSED [ 27%]
tests/test_auth_rules.py::test_sliding_window_rate_limiter PASSED        [ 31%]
tests/test_auth_rules.py::test_jwt_issuance_and_decoding PASSED          [ 34%]
tests/test_auth_rules.py::test_token_invalidation_and_blacklist PASSED   [ 37%]
tests/test_auth_rules.py::test_csrf_token_generation_and_constant_time_verification PASSED [ 41%]
tests/test_consent.py::test_default_consent_optional_items_unselected PASSED [ 44%]
tests/test_consent.py::test_consent_update_and_audit_trail_recording PASSED [ 48%]
tests/test_consent.py::test_consent_strict_purpose_separation PASSED     [ 51%]
tests/test_consent.py::test_elderly_transparency_notices_plain_language PASSED [ 55%]
tests/test_consent.py::test_permission_check_helpers PASSED              [ 58%]
tests/test_passwords.py::test_hash_password_uses_argon2id PASSED         [ 62%]
tests/test_passwords.py::test_verify_password_correct PASSED             [ 65%]
tests/test_passwords.py::test_verify_password_incorrect PASSED           [ 68%]
tests/test_passwords.py::test_hash_password_empty_raises_error PASSED    [ 72%]
tests/test_passwords.py::test_unique_salts_produce_different_hashes PASSED [ 75%]
tests/test_passwords.py::test_needs_rehash_behavior PASSED               [ 79%]
tests/test_privacy.py::test_sanitize_text_redacts_credentials_and_tokens PASSED [ 82%]
tests/test_privacy.py::test_sanitize_text_redacts_banking_cards_and_otp PASSED [ 86%]
tests/test_privacy.py::test_sanitize_text_redacts_phone_numbers_and_message_content PASSED [ 89%]
tests/test_privacy.py::test_redacting_logger_filter PASSED               [ 93%]
tests/test_privacy.py::test_payload_size_validation PASSED               [ 96%]
tests/test_privacy.py::test_history_record_contains_zero_raw_message_text PASSED [100%]

============================= 29 passed in 2.40s ==============================
```

---

## 8. Incomplete Features & Limitations

1. **Caregiver Notification Feature:**
   - *Status:* Modeled in the consent schema as an optional flag (`consent_caregiver_sharing`), but notification dispatch (SMS/email) is intentionally not implemented.
   - *Reason:* Documented as a future preview extension pending explicit team and ethical review.
2. **Distributed Rate Limiting:**
   - *Status:* Implemented using an in-memory sliding-window counter.
   - *Limitation:* Operates per application process. For multi-server load-balanced deployments, Member 4 can back the sliding window with Redis.
3. **Distributed Token Revocation:**
   - *Status:* Implemented using an in-memory blacklist with automatic expiry cleanup.
   - *Limitation:* For distributed deployments, Member 4 can store revoked tokens in MongoDB with a TTL index.

---

## 9. Viva & College Evaluation Presentation Guide

When demonstrating Member 2's individual contribution to project examiners:

1. **State Your Exact Role Clearly (30 seconds):**
   > *"I am Member 2, responsible for Cybersecurity and Privacy. My focus is protecting our elderly users' accounts and sensitive personal communications through Privacy by Design, Argon2id cryptography, anti-brute-force defenses, and granular consent management."*

2. **Run the Automated Test Suite Live (30 seconds):**
   > *"Let me demonstrate my test suite. Running `pytest tests/ -v` executes 29 automated tests covering Argon2id password hashing, sliding-window rate limiting, token revocation, consent audit logging, PII log redaction, and cross-user access isolation in 2.4 seconds."*

3. **Highlight Key Security Innovations (1 minute):**
   - **Privacy by Design:** Explain that raw SMS/email messages are processed strictly in RAM and never stored in the database.
   - **Elderly-Friendly Security:** Explain the password rules (minimum 8 characters, letters and numbers) and plain-language transparency notices designed so seniors understand what data is processed.
   - **Defensive Engineering:** Point out the log redacting filter that prevents accidental leakage of OTPs, credit cards, and passwords in application logs.
