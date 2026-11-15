# SilverShield AI — Secure AI-Powered Elderly Digital Safety Companion

**Project Title:** Secure AI-Powered Elderly Digital Safety Companion with Privacy-Preserving Scam Detection and Early Warning  
**Group Mini Project**

---

## 👥 Project Team Roles & Architecture

| Role | Module | Responsibility | Technology |
|---|---|---|---|
| **Member 1** | Frontend & Accessibility | Trilingual UI (English, Hindi, Kannada), WCAG AAA High Contrast, Web Speech Audio, Font Scaling, Helper Alerts | Streamlit, HTML5, Web Speech API |
| **Member 2** | ML Scam Classification | Text classification, confidence estimation, trigger detection | Python, Scikit-Learn / Transformers, FastAPI |
| **Member 3** | Privacy & URL Security | PII sanitization/anonymization, domain & TLD inspection, typosquatting detection | Python, Urllib, FastAPI |
| **Member 4** | Central Risk Engine & Integration | Risk aggregation, transparent multi-factor scoring, elderly warning logic, API orchestrator, error handling | Python, FastAPI, Pydantic, Requests |

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Entire System with One Command
```bash
python start_all.py
```
This automatically starts:
- 📱 **Member 1 Accessible Frontend:** [http://localhost:8501](http://localhost:8501)
- 🧠 **Member 2 ML Scam Service:** [http://localhost:8001/health](http://localhost:8001/health)
- 🔗 **Member 3 URL Security Service:** [http://localhost:8002/health](http://localhost:8002/health)
- 🛡️ **Member 4 Central Integration API:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Automated Tests

A comprehensive test suite of 20 unit and integration tests is included, verifying all 7 evaluation scenarios:

```bash
python -m pytest -v
```

### Evaluation Test Scenarios Covered
1. **Legitimate Messages:** Normal family conversations correctly identified as `LOW RISK`.
2. **Scam Messages:** Urgent banking & suspension threats classified as `HIGH RISK`.
3. **Suspicious URLs:** Masked / shortened / deceptive links flagged as `SUSPICIOUS` or `MALICIOUS`.
4. **OTP Requests:** Solicitation of OTPs, passwords, or PINs immediately escalated to `HIGH RISK`.
5. **Messages with No URLs:** Evaluated with dynamic weight reallocation and `NO_URL` status.
6. **API Failures & Timeouts:** Demonstrates fail-safe resilience (never defaults to safe when down).
7. **Invalid Inputs:** Empty messages or whitespace rejected with standard `422 Unprocessable Content`.

---

## ♿ Member 1: Elderly Accessibility Highlights

- **WCAG 2.1 AAA Compliant High Contrast Mode:** Deep dark canvas with high-visibility gold and pure white borders for visually impaired seniors.
- **Dynamic Text Scaling:** Standard (18px), Large (22px), and Extra Large (26px) fonts.
- **Trilingual Audio Narration:** Browser-native Web Speech API reading aloud in English, Hindi, and Kannada.
- **Large Touch Targets:** All buttons have a minimum height of 52px with distinct hover and focus states.
- **Emergency Helpline & Trusted Helper:** One-click WhatsApp alert generator and instant link to India's **1930 National Cyber Crime Helpline**.

---

## 📑 Project Deliverables

- `silvershield_frontend.py` & `frontend/app.py`: Member 1 Accessibility Frontend.
- `backend/`: Member 4 Central Risk Aggregation, Warning Engine, and Integration API.
- `mocks/`: Standalone microservice simulators for Member 2 & Member 3.
- `tests/`: Complete Pytest evaluation suite (20/20 passing tests).
- `API_DOCUMENTATION.md`: Complete API contracts and architecture documentation.
- `start_all.py`: Single-command launcher for all services.
