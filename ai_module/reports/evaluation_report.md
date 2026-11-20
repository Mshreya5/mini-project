# SilverShield AI — Scam Detection Model Evaluation & Research Report

## 1. Executive Summary
This report documents the machine learning model training, evaluation, and comparative analysis 
for the **SilverShield AI** elderly digital safety companion scam detection module.

Two classifiers were trained and evaluated on an identical held-out test split (20% stratified):
1. **Logistic Regression (Baseline Classifier)**: Linear model with `class_weight='balanced'` and L2 regularization.
2. **Multinomial Naive Bayes (Comparison Classifier)**: Probabilistic text classifier with Laplace smoothing (`alpha=0.1`).

---

## 2. Quantitative Performance Comparison

| Metric | Logistic Regression (Baseline) | Multinomial Naive Bayes |
|---|---|---|
| **Test Accuracy** | 98.43% | 98.16% |
| **Scam Precision** | 93.89% | 96.97% |
| **Scam Recall** | 96.02% | 90.91% |
| **Scam F1-Score** | 94.94% | 93.84% |
| **Macro F1-Score** | 97.01% | 96.38% |
| **ROC-AUC** | 0.9939 | 0.9915 |
| **Missed Scams (False Negatives)** | **7** | **16** |
| **False Alarms (False Positives)** | 11 | 5 |
| **Correctly Detected Scams (True Positives)** | 169 | 160 |
| **Correct Legitimate (True Negatives)** | 957 | 963 |

---

## 3. In-Depth False Negative (FN) Analysis: Why Missing a Scam is Critical for Elderly Safety

In safety applications for vulnerable demographics such as elderly citizens, classification errors carry **highly asymmetric real-world consequences**:

### A. The Danger of False Negatives (FN)
- **What Happens**: A fraudulent SMS message (e.g. fake bank account freeze, fake lottery reward, or urgent wire transfer) is classified as `0 = Legitimate`.
- **Real-World Impact**: Elderly users are often trusting, less familiar with modern deceptive digital interfaces, or easily unsettled by urgent authority claims. A missed scam could cause them to:
  1. Readily share a one-time password (OTP) or credit card PIN.
  2. Transfer life savings or retirement funds under the guise of an overdue utility bill or tax levy.
  3. Tap malicious phishing links that harvest browser sessions and personal identity information.
- **Design Requirement**: Minimizing False Negatives (maximizing Recall for Class 1) is a primary design objective. In our benchmark, **Logistic Regression achieved higher recall (93.75%)** with only 8 missed scams, whereas unweighted Naive Bayes missed 16 scams (recall 87.50%).

### B. The Context of False Positives (FP)
- **What Happens**: An authentic message (e.g., from a grandchild or doctor's office) is flagged as suspicious.
- **Real-World Impact**: Unnecessary anxiety, panic, or user annoyance.
- **Mitigation**: Rather than issuing aggressive, terrifying alarm sirens, SilverShield AI pairs every prediction with **calm, respectful explanations** and safe next steps (e.g., calling the official number on the back of an existing bank card).

### C. Multi-Layered Defense & Aggregation
- The ML model confidence score is kept strictly decoupled from the final warning state.
- As agreed with Member 4 (Risk Aggregation), the ML model outputs an objective, calibrated probability, which Member 4 aggregates alongside device telemetry and contact reputation.

---

## 4. Conclusion and Production Recommendation

- **Primary Baseline Model**: **Logistic Regression** is recommended as the core classifier. It provides superior recall on fraudulent messages (minimizing dangerous false negatives), produces well-calibrated probabilistic scores, and yields linear feature weights that enhance model interpretability.
- **Heuristic Explainability Integration**: Because no machine learning model achieves 100% recall on zero-day attacks, the system combines Logistic Regression with boundary-aware regex warning indicators to explain specific behavioral patterns (OTP requests, urgent payments, fake prizes).