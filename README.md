# SilverShield AI — Secure AI-Powered Elderly Digital Safety Companion

> **Academic Mini-Project Evaluation — Production Release 1.0.0**  
> *Secure AI-Powered Elderly Digital Safety Companion with Privacy-Preserving Scam Detection and Early Warning*

---

## 1. Project Title & Description
**SilverShield AI** is an intelligent, privacy-preserving cybersecurity companion designed specifically for senior citizens and non-tech-savvy individuals. It provides real-time detection of smishing, financial fraud, impersonation, and deceptive hyperlinks using machine learning and multi-layer heuristic security analysis. The platform translates complex technical telemetry into simple, plain-language guidance with multi-lingual voice narration in **English**, **Hindi (हिन्दी)**, and **Kannada (ಕನ್ನಡ)**.

---

## 2. Problem Statement
Senior citizens are disproportionately targeted by social engineering scams, smishing attacks, and fake digital touchpoints:
- **Emotional & Fear Exploitation**: Criminals threaten electricity disconnection, bank account suspension, or police arrest to rush seniors into panic.
- **Deceptive Links**: Fraudulent SMS and WhatsApp messages conceal malicious destination sites using raw IP addresses, typosquatting, and URL shorteners.
- **Accessibility & Language Barriers**: Most existing security tools feature dense enterprise jargon, tiny text, and English-only interfaces.
- **Privacy Invasive Alternatives**: Commercial spam blockers harvest user contact lists and store private SMS text on cloud servers.
- **Lack of Family Recourse**: Seniors often have no immediate way to notify caregivers or contact national cyber authorities when encountering a scam.

---

## 3. Key Features
- **AI Scam Message Detector**: NLP TF-IDF + Logistic Regression classifier achieving **98.24% detection accuracy** with explainable intent indicators.
- **9-Layer Privacy-Preserving URL Analyzer**: Zero-telemetry heuristic inspection detecting raw IPs, shorteners, high-risk TLDs, typosquatting, and keyword abuse.
- **Central Multi-Vector Risk Aggregator**: Computes normalized risk scores ($0-100$) and four categorical levels (`SAFE`, `LOW`, `MEDIUM`, `HIGH`) with safety override guarantees.
- **Elderly Usability & Accessibility (WCAG AAA)**: Scalable typography (14px, 15px, 17px), calming Purple & Lavender palette, and a high-contrast dark mode ($>7:1$ contrast ratio).
- **Multilingual Support & Resilient Voice Narrator**: Real-time localization across English, Hindi, and Kannada (`kn-IN`) with browser-native Web Speech narration and multi-tier online fallback.
- **Cybersecurity & Consent Management**: OWASP-recommended Argon2id password hashing, sliding-window rate limiting, JWT token revocation, and unbundled DPDP/GDPR consent controls.
- **Caregiver & Helpline Integration**: One-click pre-formatted WhatsApp alert dispatching and 24/7 National Cyber Crime Helpline (`1930`) escalation.
- **Graceful In-Process Degradation**: Automatically falls back to a local in-process security engine if any microservice is temporarily stopped.

---

## 4. System Architecture
SilverShield AI employs a **Decoupled 4-Tier Microservice Topology**:

```
[ User Browser ]
       │
       ▼ (Port 8501)
+─────────────────────────────────────────────────────────────+
│ Member 1: Streamlit Assistive Frontend                      │
│ - Three-Dot Menu (⋮) navigation with zero emoji clutter     │
│ - Multilingual UI (English, Hindi, Kannada)                 │
│ - Web Speech Audio Narrator (Multi-Tier kn-IN TTS)          │
+─────────────────────────────────────────────────────────────+
       │
       ▼ (Port 8000: REST HTTP/JSON)
+─────────────────────────────────────────────────────────────+
│ Member 4: Central Risk Integration API (FastAPI)            │
│ - Argon2id Password Hashing & Access Control                │
│ - SQLite Database (Users, Consent Records, Scan Metadata)  │
│ - Multi-Vector Scoring & Deterministic Overrides (OVR-01..06)│
+─────────────────────────────────────────────────────────────+
       │                                     │
       ▼ (Port 8001: REST)                   ▼ (Port 8002: REST)
+────────────────────────────+  +────────────────────────────+
│ Member 2: AI/ML Scam API   │  │ Member 3: URL Security API │
│ - TF-IDF Vectorizer        │  │ - 9 Heuristic Inspections  │
│ - Logistic Regression      │  │ - Query String Stripping   │
│ - Intent Indicator Rules   │  │ - Zero Outgoing Network    │
+────────────────────────────+  +────────────────────────────+
```

---

## 5. Technologies Used
- **Backend & APIs**: Python 3.12, FastAPI, Uvicorn, Pydantic v2
- **Frontend & Assistive UX**: Streamlit, HTML5 Web Speech API, CSS3
- **AI/ML & NLP**: Scikit-Learn, Joblib, Pandas, NumPy
- **Cybersecurity**: Argon2-cffi (Argon2id), PyJWT (HS256)
- **Database**: SQLite3 (persistent lightweight storage)
- **Testing**: Pytest, Requests, HTTPX

---

## 6. Project Directory Structure
```
Mini-project/
├── ai_module/                     # Member 2: AI/ML Scam Detection Service
│   ├── api/                       # FastAPI prediction microservice (Port 8001)
│   │   ├── main.py                # ML service endpoints (/predict, /health)
│   │   └── schemas.py             # Request & response schemas
│   ├── dataset/                   # Curated dataset (5,572 mobile SMS records)
│   │   └── sms_scam_dataset.csv
│   ├── models/                    # Trained estimators and vectorizers
│   │   ├── logistic_regression_model.joblib
│   │   ├── naive_bayes_model.joblib
│   │   ├── tfidf_vectorizer.joblib
│   │   └── metrics_summary.json
│   ├── reports/                   # Model evaluation charts (confusion matrix, ROC)
│   ├── src/                       # Training, feature extraction, and explainability
│   │   ├── config.py
│   │   ├── data_loader.py
│   │   ├── evaluate.py
│   │   ├── explainability.py
│   │   ├── predict.py
│   │   ├── preprocessing.py
│   │   ├── train.py
│   │   └── warning_indicators.py
│   └── tests/                     # 25 automated unit tests for ML pipeline
├── app/                           # Member 4: Central Risk Aggregator & Integration
│   ├── api/                       # API routes (Risk analysis & Auth/Consent)
│   │   ├── routes.py              # /analyze, /assess, /health, /risk-config
│   │   └── auth.py                # /auth/register, /auth/login, /consent, /history
│   ├── clients/                   # HTTP client adapters for Member 2 & Member 3
│   │   ├── base.py
│   │   ├── parsing.py
│   │   ├── scam_detector.py
│   │   └── url_analyzer.py
│   ├── core/                      # Orchestration, risk engine, and URL utilities
│   │   ├── indicators.py
│   │   ├── models.py
│   │   ├── orchestrator.py
│   │   ├── risk_engine.py
│   │   ├── urls.py
│   │   └── warnings.py
│   ├── database.py                # SQLite database management (Users & Consent)
│   ├── main.py                    # FastAPI application factory
│   ├── schemas.py                 # Pydantic schemas for risk responses
│   └── settings.py                # Environment configuration loader
├── artifacts/                     # Serialized production pipeline models
│   └── model_pipeline.joblib
├── config/                        # System configuration & scoring rules
│   └── risk_config.json           # Severity points, thresholds, and overrides
├── data/                          # Persistent SQLite database storage
│   └── silvershield.db
├── frontend/                      # Member 1: Streamlit UX & Multilingual Library
│   ├── app.py                     # Wrapper entrypoint redirecting to root
│   ├── components.py              # Visual risk cards, audio player, checklists
│   ├── locales.py                 # Tri-lingual dictionary (English, Hindi, Kannada)
│   └── styles.py                  # WCAG AAA Purple & Lavender CSS design system
├── reports/                       # Visual evaluation charts and graphs
│   ├── confusion_matrix.png
│   ├── model_comparison_chart.png
│   └── roc_curve.png
├── security/                      # Member 2: Cybersecurity & Privacy Library
│   ├── access_control.py          # Identity derivation and ownership enforcement
│   ├── auth_rules.py              # Password validation, rate limiter, JWT tokens
│   ├── consent.py                 # Granular consent preferences & audit trail
│   ├── passwords.py               # Argon2id hashing and constant-time verification
│   └── privacy.py                 # Zero-message persistence and sanitization
├── tests/                         # Comprehensive automated test suite (137 tests)
│   ├── conftest.py
│   ├── test_access_control.py
│   ├── test_api_scenarios.py
│   ├── test_auth_endpoints.py
│   ├── test_auth_rules.py
│   ├── test_clients.py
│   ├── test_consent.py
│   ├── test_integration_end_to_end.py
│   ├── test_live_services.py      # Live end-to-end multi-service verification
│   ├── test_passwords.py
│   ├── test_privacy.py
│   ├── test_risk_engine.py
│   ├── test_url_analyzer.py
│   ├── test_url_api.py
│   ├── test_url_extractor.py
│   ├── test_urls.py
│   └── test_warnings.py
├── url_analysis/                  # Member 3: URL Security & Heuristics Service
│   ├── analyzer.py                # 9 deterministic inspection layers
│   ├── api.py                     # FastAPI URL microservice (Port 8002)
│   ├── extractor.py               # Safe regex URL extraction
│   ├── models.py                  # Pydantic data schemas
│   └── privacy.py                 # Sanitization, redaction, consent validation
├── .env.example                   # Environment variable template
├── .gitignore                     # Git exclusion rules
├── PROJECT_DOCUMENTATION.md       # Consolidated technical documentation
├── pyproject.toml                 # Pytest configuration
├── README.md                      # Root project overview and guide
├── requirements.txt               # Production Python dependencies
├── silvershield_frontend.py       # Primary Streamlit application entrypoint
└── start_all.py                   # Master single-command launcher
```

---

## 7. Prerequisites
- **Python**: Version 3.12 or higher.
- **Operating System**: Windows 10/11, macOS, or Linux.
- **Web Browser**: Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari.

---

## 8. Installation Instructions
1. Clone or navigate to the repository directory:
   ```bash
   cd Mini-project
   ```
2. Activate the virtual environment:
   ```powershell
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS:
   source .venv/bin/activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 9. Environment Variable Configuration
Copy the template file to `.env`:
```bash
cp .env.example .env
```
Default `.env` configuration:
```ini
SCAM_API_URL=http://127.0.0.1:8001/predict
URL_API_URL=http://127.0.0.1:8002/analyze-url
REQUEST_TIMEOUT_SECONDS=4.0
MAX_RETRIES=1
CORS_ORIGINS=["http://localhost:8501","http://127.0.0.1:8501"]
JWT_SECRET_KEY=silvershield_ai_jwt_production_secret_key_minimum_32_bytes
```

---

## 10. Database Setup
SilverShield AI uses an automated SQLite database initialized automatically on first launch at `data/silvershield.db`. No external server or manual SQL setup is required.
Tables created:
- `users`: User profiles with Argon2id password hashes and caregiver contacts.
- `consent_records`: Unbundled consent choices with timestamped audit trails.
- `scan_history`: Risk rating metadata (strictly excludes raw message text).

---

## 11. Frontend Startup Commands
To run only the Streamlit Assistive Frontend (Port 8501):
```powershell
python -m streamlit run silvershield_frontend.py --server.port 8501 --server.headless true
```
Open **`http://localhost:8501`** in your browser.

---

## 12. Backend Startup Commands
To start only the Member 4 Central Integration API (Port 8000):
```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive Swagger Documentation: **`http://localhost:8000/docs`**

---

## 13. AI/ML Model Setup & Execution
The trained models and vectorizer are pre-packaged in `ai_module/models/`.

To retrain the models from the dataset:
```powershell
python -m ai_module.src.train
```
To run model evaluation and generate performance metrics:
```powershell
python -m ai_module.src.evaluate
```
To start the standalone ML Prediction API (Port 8001):
```powershell
python -m uvicorn ai_module.api.main:app --host 127.0.0.1 --port 8001 --reload
```

---

## 14. Master Multi-Service Launcher
Launch all four integrated microservices with a single command:
```powershell
python start_all.py
```
This automatically starts:
- Port `8001`: Member 2 ML Scam Service
- Port `8002`: Member 3 URL Security Service
- Port `8000`: Member 4 Central Integration API
- Port `8501`: Member 1 Streamlit Frontend

---

## 15. API Information
- `POST /api/v1/analyze`: Aggregated risk analysis combining text ML and URL heuristics.
- `GET /api/v1/health`: Health status of central API and dependent microservices.
- `GET /api/v1/risk-config`: Transparent rule set (weights, thresholds, overrides).
- `POST /api/v1/auth/register`: Argon2id user registration with rate limiting.
- `POST /api/v1/auth/login`: Timing-equalized login returning JWT token.
- `POST /api/v1/auth/logout`: Revokes token on blacklist.
- `GET /api/v1/auth/me`: Protected authenticated profile route.
- `GET /api/v1/consent` & `PUT /api/v1/consent`: Granular privacy consent controls.
- `POST /predict` (Port 8001): Direct ML text prediction.
- `POST /analyze-url` (Port 8002): Direct URL heuristic analysis.

---

## 16. Testing Instructions
Run the entire automated test suite:
```powershell
pytest -v
```
To run the live multi-service end-to-end integration test:
```powershell
pytest tests/test_live_services.py -s -v
```
All **162 automated tests pass** without network errors.

---

## 17. Security & Privacy Features
- **Argon2id Password Hashing**: OWASP Gold Standard memory-hard hashing (64 MiB RAM per hash).
- **Anti-Enumeration Protections**: Constant-time verification cycles prevent account enumeration.
- **Sliding-Window Rate Limiting**: Mitigates brute-force attacks on login and registration.
- **Zero-Message Persistence**: SMS contents and raw URLs are never saved to disk or database.
- **Granular Consent**: Unbundled DPDP/GDPR consent preferences with audit logging.
- **Plain-Language Disclosures**: Transparent notices written specifically for elderly comprehension.

---

## 18. Team Members
Developed as a collaborative college mini-project by four team members:
- **Member 1 (Frontend & Multilingual UX Lead)**: Streamlit accessibility interface, tri-lingual localization, Web Speech audio synthesis.
- **Member 2 (AI/ML & Cybersecurity Lead)**: NLP feature extraction, classifier training, Argon2id authentication, consent framework.
- **Member 3 (URL Security & Threat Heuristics Lead)**: 9-layer URL heuristic analysis, URL extraction, query-string redaction.
- **Member 4 (Backend Integration & System Lead)**: Central FastAPI orchestrator, risk engine, SQLite database, master launcher.

---

## 19. Known Limitations
- Current ML models are trained offline; active online reinforcement learning from user feedback is not yet enabled.
- Voicemail audio files and screenshot images require transcription or OCR prior to inspection.
- When running in restricted network sandbox environments on Windows, loopback socket isolation requires bypass permission or local direct engine mode.

---
*SilverShield AI — Empowering Senior Citizens with Privacy-First Cyber Protection.*
