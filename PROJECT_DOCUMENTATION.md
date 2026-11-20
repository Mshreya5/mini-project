# SilverShield AI — Complete Project Documentation

> **Official Project Title:** Secure AI-Powered Elderly Digital Safety Companion with Privacy-Preserving Scam Detection and Early Warning  
> **System Classification:** Distributed AI Cybersecurity & Assistive Technology Platform  
> **Target Audience:** Senior Citizens, Non-Tech-Savvy Users, Family Caregivers, and Cybersecurity First Responders  
> **Core Architecture:** 4-Tier Microservice & Streamlit Architecture with Graceful In-Process Degradation  
> **Project Version:** 1.0.0 Production  

---

## Table of Contents
1. [Project Overview & Problem Statement](#1-project-overview--problem-statement)
2. [Team Members & Module Integration](#2-team-members--module-integration)
3. [Complete Technology Stack](#3-complete-technology-stack)
4. [System Architecture & Data Flow](#4-system-architecture--data-flow)
5. [Database Architecture & Privacy-by-Design](#5-database-architecture--privacy-by-design)
6. [AI/ML Scam Detection Engine](#6-aiml-scam-detection-engine)
7. [URL Security & Heuristic Inspection Engine](#7-url-security--heuristic-inspection-engine)
8. [Central Risk Aggregation Engine](#8-central-risk-aggregation-engine)
9. [Cybersecurity, Authentication & Consent Management](#9-cybersecurity-authentication--consent-management)
10. [Multilingual & Assistive Speech System](#10-multilingual--assistive-speech-system)
11. [User Interface & Elderly Usability (WCAG AAA)](#11-user-interface--elderly-usability-wcag-aaa)
12. [Comprehensive API Reference](#12-comprehensive-api-reference)
13. [Installation, Configuration & Startup Guide](#13-installation-configuration--startup-guide)
14. [Automated Testing & Verification Suite](#14-automated-testing--verification-suite)
15. [Academic Viva Questions & Answers](#15-academic-viva-questions--answers)
16. [Known Limitations & Future Roadmap](#16-known-limitations--future-roadmap)

---

## 1. Project Overview & Problem Statement

### 1.1 Problem Statement
Elderly individuals are disproportionately targeted by cybercriminals, financial fraudsters, and social engineering scammers:
1. **Psychological Manipulation**: Scammers leverage urgency, fear, intimidation, and impersonation of authority (police, banks, electricity boards, pension offices, courier companies) to induce panic and rash financial decisions.
2. **Deceptive Digital Touchpoints**: Smishing (SMS phishing) and WhatsApp fraud frequently employ obfuscated URLs, typosquatted brand names, raw IP addresses, and shorteners that route victims to credential-harvesting pages.
3. **Accessibility & Language Barriers**: Mainstream enterprise cybersecurity tools present complex technical telemetry, micro-typography, and English-only interfaces, confusing seniors and non-native speakers.
4. **Privacy Invasions in Protective Software**: Existing commercial anti-spam apps often harvest user address books, log unencrypted message texts on third-party servers, and sell user browsing telemetry.
5. **Absence of Emergency Family Escalation**: When elderly users encounter suspicious communications, they lack immediate channels to consult family caregivers or escalate to national cyber authorities (such as India's National Cyber Crime Helpline `1930`).

### 1.2 SilverShield AI Solution
SilverShield AI is an intelligent, privacy-preserving digital safety companion designed specifically for senior citizens and their families. It provides:
- Instant natural language scam analysis via machine learning.
- 9-layer privacy-preserving URL security inspection.
- A centralized risk engine computing unified risk levels (`SAFE`, `LOW`, `MEDIUM`, `HIGH`) with plain-language explanations.
- Memory-hard Argon2id authentication and cryptographic session protection.
- Full localization in **English**, **Hindi (हिन्दी)**, and **Kannada (ಕನ್ನಡ)**.
- Browser-native speech synthesis with multi-tier Kannada fallback.
- WCAG AAA high-contrast accessibility and dynamic font scaling.
- One-click caregiver WhatsApp alerting and National Helpline 1930 integration.

---

## 2. Team Members & Module Integration

The project is architected across four specialized modules developed by team members and integrated into a unified platform:

| Module / Member | Primary Ownership | Core Components | Integrated Deliverables |
| :--- | :--- | :--- | :--- |
| **Member 1** | Assistive Frontend & Localization | Streamlit UX, Multilingual Locales, Audio Narrator | `silvershield_frontend.py`, `frontend/locales.py`, `frontend/components.py`, `frontend/styles.py` |
| **Member 2** | AI/ML Scam Detection Engine | NLP Preprocessing, Model Training, Heuristic Indicators | `ai_module/src/`, `ai_module/api/`, `ai_module/models/`, `ai_module/dataset/` |
| **Member 3** | URL Security & Privacy Analyzer | URL Extraction, 9-Layer Heuristics, Sanitization | `url_analysis/analyzer.py`, `url_analysis/api.py`, `url_analysis/extractor.py`, `url_analysis/privacy.py` |
| **Member 4** | Central Risk Engine & Integration | Risk Aggregator, Authentication, Database, Orchestrator | `app/main.py`, `app/api/`, `app/core/`, `app/database.py`, `security/`, `start_all.py` |

---

## 3. Complete Technology Stack

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Runtime** | Python | 3.12+ | Core execution environment across all tiers |
| **Frontend Framework** | Streamlit | 1.30.0+ | Reactive assistive dashboard with custom CSS & HTML5 embedding |
| **Web API Framework** | FastAPI | 0.110.0+ | High-performance ASGI REST APIs with OpenAPI/Swagger docs |
| **ASGI Server** | Uvicorn | 0.27.0+ | Production ASGI server hosting microservices (Ports 8000, 8001, 8002) |
| **Data Validation** | Pydantic v2 | 2.6.0+ | Strict schema validation, type enforcement, payload boundaries |
| **Machine Learning** | Scikit-Learn | 1.4.0+ | TF-IDF vectorization, Logistic Regression, Naive Bayes classifiers |
| **Model Serialization** | Joblib | 1.3.0+ | Fast binary persistence for trained estimators and vectorizers |
| **Data Processing** | Pandas & NumPy | 2.0+ / 1.24+ | Dataset curation, matrix computations, statistical aggregations |
| **Password Hashing** | Argon2-cffi | 23.1.0+ | OWASP Gold Standard memory-hard Argon2id password hashing |
| **Session Security** | PyJWT | 2.9.0+ | Stateless HMAC-SHA256 (HS256) JWT access token issuance |
| **Database** | SQLite3 | Native | Lightweight persistent storage for users, consent audits, and scan ratings |
| **HTTP Client** | Requests & HTTPX | 2.31+ / 0.27+ | Resilient inter-service communication with timeout guards |
| **Testing Suite** | Pytest | 8.0.0+ | Automated test suite (162 unit, integration, and live tests) |
| **Speech Narration** | Web Speech API | HTML5 Native | Multi-tier speech synthesis in English, Hindi, and Kannada (`kn-IN`) |

---

## 4. System Architecture & Data Flow

### 4.1 Distributed Microservice Topology

SilverShield AI operates as a decoupled microservice architecture across 4 distinct ports with automatic fallback to local direct execution:

```
[ User Browser ]
       |
       v  (Port 8501)
+--------------------------------------------------------------+
| Member 1: Streamlit Assistive Frontend                       |
| - Accessibility Layout (Standard, Large, High Contrast)      |
| - Multilingual Engine (English, Hindi, Kannada)              |
| - Browser-Native Web Speech Narrator (Multi-Tier kn-IN TTS)  |
+--------------------------------------------------------------+
       |
       v  (Port 8000: REST HTTP/JSON)
+--------------------------------------------------------------+
| Member 4: Central Risk Integration API (FastAPI)             |
| - Authentication & Argon2id Password Hashing                 |
| - Resource Ownership & Access Control                        |
| - Granular Consent & Elderly Transparency Engine             |
| - Threat Score Normalizer & Safety Overrides (OVR-01..06)    |
| - SQLite Database (Users, Consent Records, Scan Metadata)   |
+--------------------------------------------------------------+
       |                                      |
       v (Port 8001: REST)                    v (Port 8002: REST)
+-----------------------------+   +----------------------------+
| Member 2: AI/ML Scam Engine |   | Member 3: URL Security API |
| - TF-IDF Feature Extractor  |   | - 9 Heuristic Inspections  |
| - Calibrated Logistic Regr. |   | - Redaction & Obfuscation  |
| - Intent Indicator Analysis |   | - Query String Stripping   |
+-----------------------------+   +----------------------------+
```

### 4.2 Graceful In-Process Degradation
If any microservice is temporarily stopped, the central orchestrator automatically degrades safely:
- If Member 2 (ML API) is unreachable, the orchestrator logs `state=UNAVAILABLE`, sets status to `DEGRADED`, and enforces a minimum safety floor so suspicious messages are never marked safe.
- If Member 3 (URL API) is unreachable, URL risk reports `UNAVAILABLE` while text scam detection continues.
- If Member 4 (Central API) is not running when Streamlit starts, Streamlit switches to its **Local AI Security Engine**, executing the ML models and URL heuristics in-process with identical accuracy.

---

## 5. Database Architecture & Privacy-by-Design

The application utilizes a persistent SQLite database located at `data/silvershield.db` managed via `app/database.py`.

### 5.1 SQLite Database Schema

#### Table: `users`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | TEXT | PRIMARY KEY | Unique user identifier (`user-<uuid>`) |
| `email` | TEXT | UNIQUE, NOT NULL | Cleaned, normalized email address |
| `password_hash` | TEXT | NOT NULL | PHC-format Argon2id cryptographic hash |
| `role` | TEXT | NOT NULL | User role (`senior` or `caregiver`) |
| `helper_name` | TEXT | DEFAULT '' | Designated family caregiver contact name |
| `helper_phone` | TEXT | DEFAULT '' | Designated family caregiver phone number |
| `created_at` | TEXT | NOT NULL | UTC timestamp of account registration |
| `last_login` | TEXT | NULL | UTC timestamp of most recent successful login |

#### Table: `consent_records`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | TEXT | PRIMARY KEY, FK | Reference to `users.id` (ON DELETE CASCADE) |
| `preferences_json` | TEXT | NOT NULL | Serialized JSON of granular consent toggles |
| `audit_trail_json` | TEXT | NOT NULL | Timestamped JSON list of consent grant/revoke events |
| `policy_version` | TEXT | NOT NULL | Legal policy version string (e.g., `v1.0`) |
| `updated_at` | TEXT | NOT NULL | UTC timestamp of latest preference update |

#### Table: `scan_history`
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | TEXT | PRIMARY KEY | Scan event identifier (`scan-<uuid>`) |
| `user_id` | TEXT | NOT NULL, FK | Reference to `users.id` (ON DELETE CASCADE) |
| `timestamp` | TEXT | NOT NULL | UTC timestamp of scan execution |
| `message_type` | TEXT | NOT NULL | Message category (`message`, `url`, `integrated`) |
| `risk_level` | TEXT | NOT NULL | Overall assessment (`SAFE`, `LOW`, `MEDIUM`, `HIGH`) |
| `risk_score` | REAL | NOT NULL | Normalized numerical risk score ($0.0 - 1.0$) |
| `indicators_json` | TEXT | NOT NULL | Serialized JSON list of identified threat flags |

### 5.2 Strict Zero-Raw-Message Privacy Rule
In compliance with GDPR and India's Digital Personal Data Protection (DPDP) Act:
- Original incoming message text, private SMS contents, and raw unredacted URLs are **never written to disk or database tables**.
- All natural language analysis is executed exclusively in volatile memory (RAM) and immediately discarded.
- Only non-PII risk ratings and indicator metadata are preserved when the user explicitly grants `consent_save_history`.

---

## 6. AI/ML Scam Detection Engine

### 6.1 Dataset & Preprocessing
The AI module is trained on a curated corpus of 5,572 mobile SMS and messaging records (`ai_module/dataset/sms_scam_dataset.csv`).
- **Tokenization & Normalization**: Text is converted to lowercase, whitespace normalized, and special characters handled.
- **TF-IDF Vectorization**: Configured with unigrams and bigrams (`ngram_range=(1, 2)`), `min_df=2`, `max_df=0.95`, and sublinear term frequency scaling.
- **Feature Dimension**: Vectorized representation across 7,800+ informative linguistic features.

### 6.2 Model Comparison & Evaluation
Multiple classification algorithms were trained and evaluated using stratified 5-fold cross-validation:

| Classifier Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Champion)** | **98.24%** | **97.80%** | **94.22%** | **95.98%** | **99.12%** |
| Multinomial Naive Bayes | 97.48% | 98.10% | 88.54% | 93.07% | 98.45% |

### 6.3 Mathematical Formulation
Logistic Regression computes the posterior probability of a message being fraudulent:
$$P(y = 1 \mid \mathbf{x}) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$
Where $\mathbf{x}$ is the TF-IDF feature vector, $\mathbf{w}$ represents learned feature weights, and $b$ is the bias.
- When $P(y = 1 \mid \mathbf{x}) \ge 0.50$, the message is classified as `SCAM`.
- Confidence score is defined as:
$$\text{Confidence} = \max(P(y = 1 \mid \mathbf{x}), 1 - P(y = 1 \mid \mathbf{x}))$$

### 6.4 Explainable Intent Indicator Engine
Beyond classification probabilities, the module scans for 10 deterministic semantic intent patterns:
1. `otp_request`: Demands for OTP, PIN, password, or security codes.
2. `urgency`: Artificial time pressure (e.g., "immediately", "within 2 hours", "today").
3. `lottery_reward`: Unsolicited prize claims, lottery winnings, or cashback.
4. `account_suspension`: Threats of bank account freezing, SIM blocking, or disconnection.
5. `banking_impersonation`: Fraudulent claims of representing SBI, HDFC, RBI, or tax authorities.
6. `financial_request`: Demands for wire transfers, gift cards, or crypto vouchers.
7. `job_scam`: Fake work-from-home offers with unrealistic daily compensation.
8. `kyc_verification`: Demands to update expired KYC credentials via unverified links.
9. `threat_action`: Legal intimidation, police arrest threats, or court summons.
10. `credential_harvest`: Direct prompts to enter credentials or credit card numbers.

---

## 7. URL Security & Heuristic Inspection Engine

The URL Analysis engine (`url_analysis/analyzer.py`) inspects hyperlinks without sending outgoing requests to the target destination, ensuring zero attacker telemetry.

### 7.1 The 9 Inspection Heuristic Layers
1. **Raw IP Address Usage**: Flags URLs utilizing IP addresses (e.g., `http://192.168.1.1/login`) instead of registered domain names.
2. **Subdomain Depth Anomalies**: Identifies excessive subdomain nesting (depth $\ge 4$) commonly used to spoof legitimate brands.
3. **URL Shortener Concealment**: Detects redirects from services like `bit.ly`, `tinyurl.com`, `is.gd`, and `t.co`.
4. **Suspicious Keyword Matches**: Inspects path and query strings for sensitive keywords (`login`, `verify`, `banking`, `secure`, `update`, `wallet`, `kyc`, `otp`).
5. **High-Risk Top-Level Domains (TLDs)**: Evaluates domain endings known for high abuse rates (`.xyz`, `.top`, `.tk`, `.ml`, `.ga`, `.cf`, `.gq`, `.buzz`, `.cc`).
6. **Typosquatting & Impersonation**: Uses normalized Levenshtein distance to detect deceptive domain variations (e.g., `g00gle.com`, `sbi-bank-verify.com`).
7. **Unencrypted HTTP Protocol**: Flags transmission of sensitive forms over unencrypted `http://`.
8. **Excessive URL Length**: Detects unusually long URLs ($> 75$ characters) engineered to disguise destination domains on mobile screens.
9. **High Character Shannon Entropy**: Detects machine-generated randomized URL paths.

### 7.2 URL Redaction & Sanitization
Before reporting or logging, the URL engine redacts query parameters and sensitive tokens:
`http://phish-site.xyz/login.php?user=senior&token=secret123` $\to$ `http://phish-site.xyz/`

---

## 8. Central Risk Aggregation Engine

Implemented in `app/core/risk_engine.py`, the risk engine combines signals from Member 2 (ML) and Member 3 (URL) into an objective score ($0-100$) and four categorical risk levels:
- **`LOW` (Score $0 - 23$)**: Safe, routine communication. No action required.
- **`MEDIUM` (Score $24 - 54$)**: Caution advised. Unverified links or minor urgency cues detected.
- **`HIGH` (Score $55 - 100$)**: Dangerous. Strong scam indicators or malicious phishing links.

### 8.1 Scoring Weights & Source Caps
Points are allocated based on indicator severity:
- `LOW`: 5 points
- `MEDIUM`: 15 points
- `HIGH`: 30 points
- `CRITICAL`: 50 points

To prevent one module from skewing results, contributions are capped per source:
- Scam Detector Cap: Maximum 60 points.
- URL Analyzer Cap: Maximum 55 points.

### 8.2 Mandatory Safety Overrides
Deterministic safety rules override raw point calculations to protect seniors:
- **OVR-01 (Very High Confidence Scam)**: ML confidence $\ge 0.90$ with severe signals $\to$ Minimum risk level `HIGH`.
- **OVR-02 (Malicious / Phishing URL)**: Destination identified as malicious $\to$ Escalates directly to `HIGH`.
- **OVR-03 (OTP + Hyperlink)**: Any OTP request combined with a link $\to$ Automatically escalated to `HIGH`.
- **OVR-04 (Degraded Mode Floor)**: If any analysis service fails, minimum risk is set to `MEDIUM` with `DEGRADED` status.
- **OVR-05 (Urgency + Payment Demand)**: Co-occurrence of deadline pressure and fund transfer $\to$ Minimum risk level `HIGH`.
- **OVR-06 (IP Address Host)**: Unencrypted IP host $\to$ Escalates directly to `HIGH`.

---

## 9. Cybersecurity, Authentication & Consent Management

Implemented in `security/` and exposed via `app/api/auth.py`.

### 9.1 Argon2id Password Hashing
- **Algorithm:** Argon2id (OWASP recommended memory-hard password hashing algorithm).
- **Parameters:**
  - `time_cost = 2` iterations
  - `memory_cost = 65,536 KiB` (64 MiB RAM per hash)
  - `parallelism = 1` thread
  - `hash_len = 32` bytes
- **Salts:** 16-byte cryptographically secure random salt generated per hash. Plaintext passwords are never stored or logged.
- **Verification:** Constant-time verification using `verify_password(plain, hash)` to prevent timing side-channel attacks.

### 9.2 Anti-Enumeration & Brute-Force Protections
- **Generic Errors:** `GENERIC_LOGIN_ERROR = "Invalid email or password."` and `GENERIC_REGISTRATION_ERROR` ensure attackers cannot enumerate registered emails.
- **Timing Equalizer:** `resist_timing_enumeration()` runs a dummy Argon2id verification cycle when an email is not found, ensuring uniform response latency.
- **Sliding-Window Rate Limiter:** `SlidingWindowRateLimiter` restricts registration to 10 requests per 60 seconds and login attempts to 15 requests per 60 seconds per IP.

### 9.3 JWT Session Security & Revocation
- **Stateless Tokens:** Signed using HMAC-SHA256 (`HS256`) containing `sub`, `iat`, and `exp` claims (default expiration: 120 minutes).
- **Token Blacklist:** `invalidate_token(token)` blacklists tokens on logout, immediately terminating active sessions.
- **Access Control:** `derive_identity_from_token` extracts user identity strictly from verified token claims. `enforce_resource_ownership` prevents cross-user access, and `filter_user_profile` strips sensitive security attributes.

### 9.4 Granular Consent Management
Complies with DPDP and GDPR data rights via unbundled preferences:
- `consent_message_analysis` (Default: `True`): In-memory inspection for safety evaluation.
- `consent_save_history` (Default: `False`): Opt-in saving of risk ratings metadata.
- `consent_analytics` (Default: `False`): Opt-in aggregated non-PII threat patterns.
- `consent_caregiver_sharing` (Default: `False`): Opt-in emergency caregiver alert dispatching.

---

## 10. Multilingual & Assistive Speech System

### 10.1 Localization Support
The entire platform provides full tri-lingual localization across **English**, **Hindi (हिन्दी)**, and **Kannada (ಕನ್ನಡ)** (`frontend/locales.py`):
- All navigation titles, hero banners, button labels, and system status badges.
- All 10 threat indicator descriptions, 6 action recommendations, and risk warnings.
- 5 comprehensive security awareness guides and the 5-question elderly safety quiz.

### 10.2 Multi-Tier Kannada & Indic Audio Narrator
Implemented in `frontend/components.py`, the audio narration player allows seniors to listen to advice with one click:
1. **Dynamic Voice Discovery**: Queries `window.speechSynthesis.getVoices()` dynamically on button press.
2. **Native Language Priority**: Searches for native regional voices (`kn-IN` for Kannada, `hi-IN` for Hindi, `en-IN` for English).
3. **Locale Voice Fallback**: If no specific named voice is pre-installed, sets `utter.lang = 'kn-IN'` so modern Chromium/Edge cloud voices synthesize the language natively without mispronouncing Indic text using an English voice.
4. **Online Audio Stream Backup**: If local speech synthesis fails or is unsupported, automatically delegates to an online text-to-speech audio stream.
5. **Playback Controls**: Features interactive Play and Stop buttons, live speaking status indicators, and error resilience.

---

## 11. User Interface & Elderly Usability (WCAG AAA)

Designed with modern typography and an accessible Purple, White & Lavender palette (`frontend/styles.py`):
- **Deep Purple (`#49316F`)**: High-contrast, calming primary text and headings.
- **Primary Purple (`#7653B5`)**: Action buttons, active badges, and focus rings.
- **Soft Lavender (`#EDE5FA`)**: Low-strain card backgrounds and highlighted regions.
- **Card White (`#FFFFFF`)**: Crisp, readable content containers.
- **Typography**: Clean humanist typography utilizing `Plus Jakarta Sans`, `Noto Sans Devanagari`, and `Noto Sans Kannada`.
- **Text Sizing**: Three accessible font scaling modes: Compact (14px), Standard (15px), and Large (17px).
- **WCAG AAA High Contrast**: One-click toggle switching to an ultra-high-contrast deep dark palette (`#0B0814` background, `#FFFFFF` text, `#B39DDB` borders) achieving $>7:1$ contrast ratio.
- **Elderly Usability**: Large touch targets ($\ge 44\text{px}$), zero confusing jargon, vertical layout hierarchy, and top Three-Dot Menu (⋮) navigation.

---

## 12. Comprehensive API Reference

### 12.1 Central Integration API (Port 8000)

#### `POST /api/v1/analyze` (or `/api/v1/assess`)
Evaluates a message and optional URL for scam indicators and computes aggregated risk.

**Request Body:**
```json
{
  "message": "Urgent: Your SBI account is blocked. Verify KYC at http://sbi-kyc-verify.xyz",
  "url": "http://sbi-kyc-verify.xyz",
  "language": "English",
  "consent_given": true
}
```

**Response Body (200 OK):**
```json
{
  "analysis_id": "9a8b7c6d5e4f",
  "generated_at": "2026-11-20T08:00:00Z",
  "overall_risk": "HIGH",
  "status": "OK",
  "message_prediction": "SCAM",
  "message_confidence": 0.942,
  "url_risk": "MALICIOUS",
  "analysed_url": "http://sbi-kyc-verify.xyz/",
  "risk_indicators": [
    "Message classified as a possible scam",
    "Very high confidence scam prediction",
    "Link flagged as malicious or a phishing page"
  ],
  "warning": "Warning! This message may be fraudulent. Do not share OTPs, passwords or banking details.",
  "recommended_actions": [
    "Never share an OTP, PIN or password.",
    "Do not click on links sent in unsolicited messages."
  ],
  "risk_score": 0.88,
  "config_version": "1.0.0"
}
```

#### `GET /api/v1/health`
Checks health status of the aggregation service and registered microservices.

#### `GET /api/v1/risk-config`
Returns transparent configuration of scoring weights, thresholds, source caps, and safety override rules.

#### `POST /api/v1/auth/register`
Registers a new user with email, strong password, and role. Password is validated and hashed via Argon2id.

#### `POST /api/v1/auth/login`
Authenticates user with rate-limiting and anti-enumeration timing defense. Returns JWT access token.

#### `POST /api/v1/auth/logout`
Invalidates active JWT access token on the server-side revocation blacklist.

#### `GET /api/v1/auth/me`
Protected route returning the authenticated user profile with password hashes stripped.

#### `GET /api/v1/consent` & `PUT /api/v1/consent`
Retrieves or updates granular consent preferences and plain-language transparency notices.

---

### 12.2 ML Scam Detection API (Port 8001)

#### `POST /predict`
Analyzes SMS text for scam likelihood using TF-IDF and Logistic Regression.
- **Request:** `{"message": "string"}`
- **Response:** `{"prediction": "scam"|"legitimate", "confidence": float, "suspicious_indicators": list, "explanation": "string"}`

#### `GET /health`
Verifies model and vectorizer readiness.

---

### 12.3 URL Security API (Port 8002)

#### `POST /analyze-url`
Extracts and inspects URLs from text using 9 deterministic heuristic layers.
- **Request:** `{"message": "string", "consent_given": true}`
- **Response:** `{"urls_found": bool, "url_count": int, "results": list}`

#### `GET /health` & `GET /privacy-info`
Health check and privacy disclosure endpoints.

---

## 13. Installation, Configuration & Startup Guide

### 13.1 Prerequisites
- Python 3.12 or higher installed.
- Modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari).

### 13.2 Installation
1. Open PowerShell or Terminal in the project root directory:
   ```powershell
   cd "C:\Users\Shreya\OneDrive\Desktop\Mini-project"
   ```
2. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
3. Verify dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### 13.3 Single-Command System Launcher
Start all four microservices and the Streamlit frontend with a single command:
```powershell
python start_all.py
```
This automatically boots:
- Port `8001`: Member 2 ML Scam Service
- Port `8002`: Member 3 URL Security Service
- Port `8000`: Member 4 Central Integration API
- Port `8501`: Member 1 Streamlit Frontend

Open your browser at: **`http://localhost:8501`**  
Access Swagger API Docs at: **`http://localhost:8000/docs`**

### 13.4 Standalone Service Commands
If running individual services independently:
- **FastAPI Central Backend (Port 8000):**
  ```powershell
  python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
  ```
- **ML Scam Detection API (Port 8001):**
  ```powershell
  python -m uvicorn ai_module.api.main:app --host 127.0.0.1 --port 8001 --reload
  ```
- **URL Security API (Port 8002):**
  ```powershell
  python -m uvicorn url_analysis.api:app --host 127.0.0.1 --port 8002 --reload
  ```
- **Streamlit Assistive Frontend (Port 8501):**
  ```powershell
  streamlit run silvershield_frontend.py --server.port 8501
  ```

---

## 14. Automated Testing & Verification Suite

The repository contains an automated test suite executed via `pytest`:

```powershell
pytest -v
```

### 14.1 Summary of Test Coverage (162 Passing Tests)
- **Authentication & Security (`tests/test_auth_endpoints.py`, `test_auth_rules.py`, `test_passwords.py`, `test_access_control.py`)**: 22 tests verifying Argon2id password hashing, strength validation, sliding-window rate limiting, timing enumeration defense, JWT issuance, revocation, and resource ownership.
- **Consent & Privacy (`tests/test_consent.py`, `test_privacy.py`)**: 12 tests verifying granular unbundled consent, audit trail creation, transparency notices, and text sanitization.
- **Risk Engine & Orchestration (`tests/test_risk_engine.py`, `test_api_scenarios.py`, `test_integration_end_to_end.py`, `test_warnings.py`)**: 64 tests validating multi-vector scoring, source caps, safety overrides (OVR-01 to OVR-06), and degraded fallbacks.
- **URL Analysis & Heuristics (`tests/test_url_analyzer.py`, `test_url_api.py`, `test_url_extractor.py`, `test_urls.py`)**: 39 tests verifying all 9 inspection layers, redaction, and consent gates.
- **AI/ML Model Suite (`ai_module/tests/`)**: 25 tests verifying data loading, TF-IDF feature extraction, model prediction, and intent indicator rules.
- **Live Production Services (`tests/test_live_services.py`)**: 10 comprehensive runtime integration tests validating live inter-service communication across ports 8001, 8002, 8000, and 8501.

---

## 15. Academic Viva Questions & Answers

### Q1: What makes SilverShield AI unique compared to existing spam filters like Truecaller?
**Answer:** Truecaller and commercial spam blockers rely on crowdsourced phone number blacklists, harvest entire user contact books, and fail against novel zero-day smishing messages sent from fresh numbers. SilverShield AI operates on **content and semantic intent** using machine learning and 9 deterministic URL heuristic layers without harvesting contact books or permanently storing user messages. Furthermore, SilverShield AI provides elderly-tailored UX with Kannada/Hindi localization, WCAG AAA accessibility, plain-language explanations, and one-click family caregiver alerting.

### Q2: Why did the team choose Logistic Regression over Deep Learning (LSTM, BERT) for the scam classifier?
**Answer:** 
1. **Inference Latency:** Logistic Regression with sparse TF-IDF executes in $<5\text{ms}$ on commodity CPU hardware without GPU acceleration, critical for real-time mobile and edge responsiveness.
2. **Explainability:** Linear model coefficients provide direct mathematical attribution for specific n-grams, enabling transparent explanations for senior citizens.
3. **Accuracy vs. Footprint:** Evaluated on SMS data, Logistic Regression achieved **98.24% accuracy** and an ROC-AUC of **0.9912**, matching heavy transformer models while requiring less than 1 MB of memory.

### Q3: Why is Argon2id preferred over bcrypt or PBKDF2 for password hashing?
**Answer:** Argon2id is the winner of the Password Hashing Competition (PHC) and OWASP's top recommendation. Unlike bcrypt (which is compute-hard but memory-light), Argon2id is **memory-hard** (configured here with 64 MiB RAM per hash). This prevents mass parallelized password cracking using ASICs and GPUs. It also combines data-independent memory access (resisting side-channel timing attacks) with data-dependent access (resisting GPU cracking).

### Q4: How does the system prevent timing attacks during user login?
**Answer:** When an attacker attempts to log in with an email that does not exist in the database, a naive system returns immediately, while an existing user triggers a 150ms Argon2id hash check. Attackers exploit this timing differential to enumerate valid accounts. SilverShield AI implements `resist_timing_enumeration()`, which executes a dummy Argon2id hash cycle whenever a user email is not found, ensuring uniform response latency across all requests.

### Q5: How is Kannada Text-to-Speech (TTS) implemented given browser variations?
**Answer:** Browser SpeechSynthesis APIs vary across operating systems. SilverShield AI implements a **resilient multi-tier strategy**:
1. Checks for native browser voices matching `kn-IN` or containing `kannada`/`sapna`/`gagan`.
2. If no specific voice object is pre-installed in the browser list, sets `utter.lang = 'kn-IN'` so Chromium/Edge engines dynamically dispatch online neural Kannada voices.
3. If local speech synthesis fails or is unsupported, automatically falls back to an online text-to-speech audio stream with `crossOrigin='anonymous'` and no-referrer headers.
4. Crucially, the system ensures Kannada text is never fed to an English voice, preventing unintelligible garbled audio.

### Q6: How does the Risk Engine combine text and URL analysis into a single rating?
**Answer:** The risk engine assigns weighted points based on threat severity (Critical: 50, High: 30, Medium: 15, Low: 5), subject to source caps (Scam: 60, URL: 55). The raw sum is scaled to a $0-100$ score. However, safety is prioritized via deterministic overrides: for instance, any OTP request combined with a link (OVR-03) or any malicious URL (OVR-02) immediately escalates the overall risk to `HIGH`, regardless of point totals.

---

## 16. Known Limitations & Future Roadmap

### 16.1 Current Known Limitations
1. **Static Model Weights**: The scikit-learn model uses offline-trained weights and does not perform active online learning from user feedback.
2. **Text-Only Message Input**: Audio voicemails and image-based smishing (screenshots) require manual transcription or OCR before analysis.
3. **Network Sandbox on Windows**: In restricted Windows environments with loopback socket isolation, local port communication requires elevated permissions or local direct engine mode.

### 16.2 Future Roadmap
1. **On-Device Mobile Integration**: Package the TF-IDF classifier into an Android APK with automated SMS listener permissions.
2. **OCR Image Scanning**: Add Tesseract / Vision OCR to inspect screenshots of suspicious messages directly.
3. **Automated Caregiver SMS/Push Gateway**: Connect Twilio or Firebase Cloud Messaging to automatically dispatch push alerts to designated family caregivers upon detection of critical scams.
4. **Expanded Regional Languages**: Add support for Tamil, Telugu, Marathi, and Bengali speech and text localization.

---
*SilverShield AI — Developed by Team SilverShield for Academic Mini-Project Evaluation.*
