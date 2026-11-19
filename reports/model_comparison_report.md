# SilverShield AI — Model Evaluation & Comparison Report

## 1. Executive Summary
This report summarizes the comparative evaluation of three traditional machine learning candidate models for the **SilverShield AI** scam detection module, designed specifically to protect elderly users.

All models were evaluated on an identical held-out test set (20% stratified split) after 5-fold cross-validation on the training set. Learned text vectorization (TF-IDF) was strictly encapsulated in scikit-learn Pipelines to eliminate any data leakage.

**Selected Production Model**: **Linear SVM (Calibrated)**

---

## 2. Model Performance Comparison Table

| Candidate Model | Test Accuracy | Spam Precision | Spam Recall | Spam F1-Score | Macro F1 | ROC-AUC | False Alarms (FP) | Missed Scams (FN) |
|---|---|---|---|---|---|---|---|---|
| **Multinomial Naive Bayes** | 98.26% | 98.25% | 87.50% | 92.56% | 95.79% | 0.9892 | 2 | 16 |
| **Logistic Regression** | 98.06% | 90.91% | 93.75% | 92.31% | 95.60% | 0.9963 | 12 | 8 |
| **Linear SVM (Calibrated)** | 98.84% | 96.77% | 93.75% | 95.24% | 97.29% | 0.9954 | 4 | 8 |

---

## 3. False Negative vs. False Positive Trade-Off Analysis

In digital safety for elderly individuals, the consequences of classification errors have asymmetric impacts:

1. **False Negatives (Missed Scams)**:
   - A fraudulent text is classified as legitimate.
   - **Risk**: The elderly user may be deceived into clicking a malicious link, calling an extortionate helpline, or sharing an OTP/PIN.
   - **Mitigation**: We prioritize high spam recall and pair the ML prediction with rule-based heuristic warning indicators.

2. **False Positives (False Alarms)**:
   - A legitimate message (e.g., from family, a doctor, or an authentic bank update) is flagged as scam.
   - **Risk**: Anxiety, confusion, or ignoring important legitimate notifications.
   - **Mitigation**: Calm, reassuring explanations that explain *why* something raised a flag, without inducing panic or blocking legitimate communications.

---

## 4. Why Traditional ML & TF-IDF?
- **Low Latency & Zero Cost**: Runs locally in milliseconds without API keys, GPU infrastructure, or third-party cloud costs.
- **Explainability**: Coefficients and n-gram weights can be inspected directly.
- **Robust Baseline**: For SMS-length messages, TF-IDF paired with linear models provides competitive accuracy with zero hallucination risk.

---

## 5. Scope & Limitations
- **English-Centric**: Trained on English SMS communications; regional slang or vernacular Indian/multilingual phrases require domain-specific fine-tuning.
- **Channel Specificity**: Focuses on text SMS, not WhatsApp voice notes or multimodal PDF phishing.
- **Non-Proof Disclaimer**: A legitimate classification is an automated statistical estimate, not a guarantee of safety.
