"""
Script to generate high-resolution, professional academic diagrams and placeholders
for SilverShield AI research paper.
"""

import shutil
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = Path("Research_Paper/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Copy real project evaluation charts
REPORTS_DIR = Path("reports")
for fname in ["confusion_matrix.png", "roc_curve.png", "model_comparison_chart.png"]:
    src = REPORTS_DIR / fname
    if src.exists():
        shutil.copy(src, OUTPUT_DIR / fname)
        print(f"Copied {src} -> {OUTPUT_DIR / fname}")

# Style setup for IEEE academic diagrams
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["DejaVu Serif", "Times New Roman", "Times"]
plt.rcParams["mathtext.fontset"] = "dejavuserif"

def create_system_architecture():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Top: User Layer
    rect_user = patches.FancyBboxPatch((30, 88), 40, 8, boxstyle="round,pad=1", facecolor='#F3F4F6', edgecolor='#1F2937', linewidth=1.5)
    ax.add_patch(rect_user)
    ax.text(50, 92, "Elderly User / Family Caregiver (Browser Interface)", ha='center', va='center', fontsize=11, fontweight='bold', color='#111827')

    # Arrow User -> Frontend
    ax.annotate("", xy=(50, 78), xytext=(50, 88), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))
    ax.text(52, 83, "HTTP / HTTPS (Port 8501)", fontsize=8, color='#4B5563')

    # Tier 1: Frontend
    rect_fe = patches.FancyBboxPatch((10, 62), 80, 16, boxstyle="round,pad=1.5", facecolor='#EDE9FE', edgecolor='#6D28D9', linewidth=2)
    ax.add_patch(rect_fe)
    ax.text(50, 74, "MEMBER 1: Assistive Streamlit Frontend (silvershield_frontend.py)", ha='center', va='center', fontsize=11, fontweight='bold', color='#5B21B6')
    ax.text(50, 68, "• Multilingual UI (English, Hindi, Kannada)   • WCAG AAA High-Contrast & Font Scaling\n• Multi-Tier Speech Synthesizer (kn-IN TTS)   • 1-Click Caregiver Alert & 1930 Helpline", ha='center', va='center', fontsize=8.5, color='#374151')

    # Arrow Frontend -> Backend
    ax.annotate("", xy=(50, 50), xytext=(50, 62), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#1F2937'))
    ax.text(52, 56, "REST API (JSON over HTTP/Port 8000)", fontsize=8, color='#4B5563')

    # Tier 2: Central Integration Backend
    rect_be = patches.FancyBboxPatch((10, 31), 80, 19, boxstyle="round,pad=1.5", facecolor='#F0FDF4', edgecolor='#16A34A', linewidth=2)
    ax.add_patch(rect_be)
    ax.text(50, 46.5, "MEMBER 4: Central Risk Integration API & Security Orchestrator (FastAPI)", ha='center', va='center', fontsize=11, fontweight='bold', color='#15803D')
    ax.text(50, 39.5, "• Central Risk Aggregator (Score: 0–100, Levels: SAFE, LOW, MEDIUM, HIGH)\n• Deterministic Safety Overrides (OVR-01 to OVR-06)   • Granular DPDP/GDPR Consent Audit\n• Argon2id Memory-Hard Password Hashing   • Anti-Enumeration & Sliding-Window Rate Limiting\n• SQLite Storage (users, consent_records, scan_history)", ha='center', va='center', fontsize=8, color='#1F2937')

    # Arrows to microservices
    ax.annotate("", xy=(28, 20), xytext=(35, 31), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#2563EB'))
    ax.text(23, 26, "REST (Port 8001)", fontsize=8, color='#1D4ED8')

    ax.annotate("", xy=(72, 20), xytext=(65, 31), arrowprops=dict(arrowstyle="<->", lw=1.5, color='#DC2626'))
    ax.text(70, 26, "REST (Port 8002)", fontsize=8, color='#B91C1C')

    # Tier 3 Left: ML Scam Detection Engine
    rect_ml = patches.FancyBboxPatch((5, 4), 42, 16, boxstyle="round,pad=1.2", facecolor='#EFF6FF', edgecolor='#2563EB', linewidth=1.8)
    ax.add_patch(rect_ml)
    ax.text(26, 16.5, "MEMBER 2: AI/ML Scam Detection", ha='center', va='center', fontsize=10, fontweight='bold', color='#1E40AF')
    ax.text(26, 10, "• TF-IDF N-gram (1,2) Vectorizer (5,000 feats)\n• Logistic Regression Classifier (98.06% Acc)\n• Multinomial Naive Bayes (98.26% Acc)\n• 7 Semantic Intent Rules (OTP, Urgency, etc.)", ha='center', va='center', fontsize=7.5, color='#1E3A8A')

    # Tier 3 Right: URL Security API
    rect_url = patches.FancyBboxPatch((53, 4), 42, 16, boxstyle="round,pad=1.2", facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.8)
    ax.add_patch(rect_url)
    ax.text(74, 16.5, "MEMBER 3: URL Security & Privacy", ha='center', va='center', fontsize=10, fontweight='bold', color='#991B1B')
    ax.text(74, 10, "• 9-Layer Static Heuristics (Zero-Request)\n• IP, Shortener, TLD, Typosquatting, Depth\n• Strict PII Redaction & Query Stripping\n• In-Memory Processing (Zero-Log Guarantee)", ha='center', va='center', fontsize=7.5, color='#7F1D1D')

    # Fallback dashed box
    rect_fallback = patches.FancyBboxPatch((2, 1), 96, 78, boxstyle="round,pad=0.5", facecolor='none', edgecolor='#9CA3AF', linewidth=1, linestyle='--')
    ax.add_patch(rect_fallback)
    ax.text(97, 76, "Graceful In-Process Degradation Fallback Boundary", ha='right', va='top', fontsize=7.5, fontstyle='italic', color='#6B7280')

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig1_system_architecture.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Generated fig1_system_architecture.png")

def create_system_workflow():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    steps = [
        ("1. User Submission", "Senior enters suspicious SMS / WhatsApp message or web URL\n(via Streamlit dashboard with font & contrast selection)", 92, '#E0E7FF', '#3730A3'),
        ("2. Privacy Sanitization & Consent Check", "Consent flag verified (DPDP compliant); PII (phone, email, cards) redacted;\nRaw text processed strictly in volatile RAM (Zero Disk Storage)", 76, '#FEF3C7', '#92400E'),
        ("3. Concurrent Microservice Inspection", "Dual-Pipeline Parallel Execution:\n• Branch A: NLP Preprocessing, TF-IDF Vectorization & Logistic Regression\n• Branch B: URL Extraction & 9-Layer Zero-Request Heuristic Verification", 60, '#E0F2FE', '#075985'),
        ("4. Feature & Intent Signal Extraction", "Aggregates ML scam probability, confidence score, and 7 semantic intent flags\n(OTP demand, urgency, impersonation, high-risk TLDs, IP hosting)", 44, '#F3E8FF', '#6B21A8'),
        ("5. Central Risk Aggregation & Overrides", "Calculates composite score (0–100); applies module caps (Msg: 55, URL: 45);\nApplies safety overrides (OVR-01: high conf, OVR-02: malicious URL, OVR-03: OTP+link)", 28, '#DCFCE7', '#166534'),
        ("6. Explainable Multilingual Alert & Actions", "Renders risk gauge (SAFE, LOW, MEDIUM, HIGH) with plain-language guidance;\nEnables Kannada/Hindi TTS voice narration, 1930 Helpline & Caregiver WhatsApp Alert", 12, '#FFE4E6', '#9F1239')
    ]

    for title, desc, y, bg, border in steps:
        box = patches.FancyBboxPatch((12, y-5), 76, 9.5, boxstyle="round,pad=1", facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(box)
        ax.text(15, y+2.5, title, fontsize=9.5, fontweight='bold', color=border)
        ax.text(15, y-1.5, desc, fontsize=7.8, color='#1F2937')

        if y > 15:
            ax.annotate("", xy=(50, y-5.5), xytext=(50, y-7.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4B5563'))

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig2_system_workflow.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Generated fig2_system_workflow.png")

def create_ml_workflow():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Boxes across columns
    # Left: Data pipeline
    box1 = patches.FancyBboxPatch((5, 70), 26, 22, boxstyle="round,pad=1", facecolor='#F3F4F6', edgecolor='#4B5563', linewidth=1.5)
    ax.add_patch(box1)
    ax.text(18, 88, "Dataset Curation", ha='center', fontsize=9.5, fontweight='bold', color='#111827')
    ax.text(18, 80, "• 5,572 raw SMS records\n• Deduplication to 5,160 msgs\n• 4,518 Legitimate (87.56%)\n• 642 Scam (12.44%)\n• Stratified 80/20 train/test", ha='center', fontsize=7.8, color='#374151')

    # Arrow 1 -> 2
    ax.annotate("", xy=(36, 81), xytext=(31, 81), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))

    # Middle Top: Preprocessing
    box2 = patches.FancyBboxPatch((37, 70), 26, 22, boxstyle="round,pad=1", facecolor='#EFF6FF', edgecolor='#2563EB', linewidth=1.5)
    ax.add_patch(box2)
    ax.text(50, 88, "NLP Preprocessing", ha='center', fontsize=9.5, fontweight='bold', color='#1E40AF')
    ax.text(50, 80, "• Lowercase conversion\n• PII token stripping\n• Whitespace normalization\n• TF-IDF N-gram (1,2)\n• Sublinear TF, min_df=2", ha='center', fontsize=7.8, color='#1E3A8A')

    # Arrow 2 -> 3
    ax.annotate("", xy=(68, 81), xytext=(63, 81), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))

    # Right: Feature Matrix
    box3 = patches.FancyBboxPatch((69, 70), 26, 22, boxstyle="round,pad=1", facecolor='#FDF2F8', edgecolor='#DB2777', linewidth=1.5)
    ax.add_patch(box3)
    ax.text(82, 88, "Feature Representation", ha='center', fontsize=9.5, fontweight='bold', color='#9D174D')
    ax.text(82, 80, "• 5,000 max features\n• Unigrams & Bigrams\n• Sparse CSR Matrix\n• Preserves vocabulary\n• Serialized via Joblib", ha='center', fontsize=7.8, color='#831843')

    # Branching arrows down to Classifiers and Intent rules
    ax.annotate("", xy=(30, 58), xytext=(50, 69), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4B5563'))
    ax.annotate("", xy=(70, 58), xytext=(50, 69), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4B5563'))

    # Bottom Left: Statistical ML Classifiers
    box4 = patches.FancyBboxPatch((5, 26), 42, 31, boxstyle="round,pad=1.2", facecolor='#ECFDF5', edgecolor='#059669', linewidth=1.5)
    ax.add_patch(box4)
    ax.text(26, 53, "ML Classification Models", ha='center', fontsize=9.5, fontweight='bold', color='#065F46')
    ax.text(26, 40, "Logistic Regression (Champion Model):\n• Balanced class weights, max_iter=1000\n• Accuracy: 98.06%, Scam Recall: 93.75%\n• ROC-AUC: 0.9963, Macro-F1: 0.9560\n• Calibrated posterior probability P(Scam|x)\n\nMultinomial Naive Bayes (Benchmark):\n• Laplace alpha=0.1, Acc: 98.26%, Recall: 87.50%", ha='center', fontsize=7.5, color='#064E3B')

    # Bottom Right: Semantic Intent Indicators
    box5 = patches.FancyBboxPatch((53, 26), 42, 31, boxstyle="round,pad=1.2", facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
    ax.add_patch(box5)
    ax.text(74, 53, "Semantic Intent Detector (7 Patterns)", ha='center', fontsize=9.5, fontweight='bold', color='#92400E')
    ax.text(74, 40, "1. Urgent Payment Request (fees, giftcards)\n2. OTP / PIN Request (confidential credential)\n3. Fake Lottery / Prize Bait (unsolicited reward)\n4. Bank Impersonation (SBI, HDFC, ICICI, etc.)\n5. Account Verification Link (kyc, profile update)\n6. Account Suspension Threat (police, legal fine)\n7. Suspicious Link In Message (shorteners, xyz)", ha='center', fontsize=7.5, color='#78350F')

    # Convergence arrow to final output
    ax.annotate("", xy=(50, 16), xytext=(26, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))
    ax.annotate("", xy=(50, 16), xytext=(74, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))

    box6 = patches.FancyBboxPatch((20, 3), 60, 12, boxstyle="round,pad=1", facecolor='#EDE9FE', edgecolor='#7C3AED', linewidth=1.8)
    ax.add_patch(box6)
    ax.text(50, 11, "Combined ML Prediction & Transparent Explanation", ha='center', fontsize=9.5, fontweight='bold', color='#5B21B6')
    ax.text(50, 6, "Output: Prediction (SCAM / LEGITIMATE), Confidence Score, Identified Threat Flags & Plain-Language Explanation", ha='center', fontsize=7.5, color='#374151')

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig3_ml_workflow.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Generated fig3_ml_workflow.png")

def create_url_workflow():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Top: Input URL
    box_in = patches.FancyBboxPatch((25, 87), 50, 9, boxstyle="round,pad=1", facecolor='#F3F4F6', edgecolor='#1F2937', linewidth=1.5)
    ax.add_patch(box_in)
    ax.text(50, 92.5, "Input: Extracted or Direct Web Link", ha='center', fontsize=10, fontweight='bold', color='#111827')
    ax.text(50, 88.5, "e.g., http://sbi-kyc-verify.xyz/login.php?token=xyz123", ha='center', fontsize=8, fontfamily='monospace', color='#4B5563')

    ax.annotate("", xy=(50, 78), xytext=(50, 87), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))

    # Middle Top: Privacy Guard
    box_priv = patches.FancyBboxPatch((20, 68), 60, 9.5, boxstyle="round,pad=1", facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.5)
    ax.add_patch(box_priv)
    ax.text(50, 74, "Privacy Enforcement & Query Redaction Layer", ha='center', fontsize=9.5, fontweight='bold', color='#991B1B')
    ax.text(50, 70, "• Consent Verification   • Strip Sensitive Query Params (?token=...)   • Zero External Network Requests", ha='center', fontsize=8, color='#7F1D1D')

    ax.annotate("", xy=(50, 58), xytext=(50, 68), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))

    # Middle: The 9 Static Heuristic Checks Grid
    box_9 = patches.FancyBboxPatch((5, 23), 90, 34, boxstyle="round,pad=1.5", facecolor='#F8FAFC', edgecolor='#0284C7', linewidth=2)
    ax.add_patch(box_9)
    ax.text(50, 53.5, "9-Layer Zero-Request Static Heuristic Inspection Engine", ha='center', fontsize=10.5, fontweight='bold', color='#0369A1')

    checks = [
        ("Layer 1: IP Address Check", "Detects raw IPv4/IPv6 hosts bypassing DNS registration"),
        ("Layer 2: Shortener Detection", "Flags bit.ly, tinyurl, t.co, is.gd, etc."),
        ("Layer 3: High-Risk TLDs", "Flags abuse-prone endings (.xyz, .top, .tk, .click, etc.)"),
        ("Layer 4: Brand Impersonation", "Detects spoofed brands & homoglyphs (e.g., g00gle, paypa1)"),
        ("Layer 5: Subdomain Depth", "Flags deep multi-level subdomains (labels > 3)"),
        ("Layer 6: Credential Path Keywords", "Detects /login, /verify, /banking, /kyc in URL path"),
        ("Layer 7: Excessive Length", "Detects URLs > 200 chars obscuring true destination"),
        ("Layer 8: Embedded Redirects", "Detects nested http:// in URL tail"),
        ("Layer 9: Host Spoofing (@ Symbol)", "Detects @ symbol used to mislead mobile URL display")
    ]

    for i, (ch_title, ch_desc) in enumerate(checks):
        col = i % 3
        row = i // 3
        cx = 8 + col * 29
        cy = 42 - row * 9.5
        cbox = patches.FancyBboxPatch((cx, cy), 26, 7.5, boxstyle="round,pad=0.6", facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1)
        ax.add_patch(cbox)
        ax.text(cx+1, cy+5, ch_title, fontsize=7.8, fontweight='bold', color='#1E293B')
        ax.text(cx+1, cy+2, ch_desc, fontsize=6.8, color='#475569')

    ax.annotate("", xy=(50, 14), xytext=(50, 23), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))

    # Bottom: Output Decision
    box_out = patches.FancyBboxPatch((15, 2), 70, 11.5, boxstyle="round,pad=1", facecolor='#ECFDF5', edgecolor='#10B981', linewidth=1.5)
    ax.add_patch(box_out)
    ax.text(50, 9.5, "URL Safety Classification & Risk Indicators", ha='center', fontsize=9.5, fontweight='bold', color='#065F46')
    ax.text(50, 5, "Risk Score (Indicator count) | Classification (SAFE, SUSPICIOUS >= 2, MALICIOUS)\nRedacted URL Output + Plain-Language Elderly Explanations", ha='center', fontsize=7.5, color='#064E3B')

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig4_url_workflow.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Generated fig4_url_workflow.png")

def create_risk_assessment_workflow():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Left: Inputs from Member 2 and 3
    box_m2 = patches.FancyBboxPatch((5, 58), 26, 32, boxstyle="round,pad=1", facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.5)
    ax.add_patch(box_m2)
    ax.text(18, 86, "Member 2: Scam Detector", ha='center', fontsize=9.5, fontweight='bold', color='#1D4ED8')
    ax.text(18, 72, "• ML Scam Prediction\n• Prediction Confidence (0–1)\n• Semantic Intent Signals:\n  - OTP / Credential Request\n  - Urgent Payment\n  - Account Suspension Threat\n  - Fake Lottery / Prize", ha='center', fontsize=7.5, color='#1E40AF')

    box_m3 = patches.FancyBboxPatch((5, 12), 26, 38, boxstyle="round,pad=1", facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.5)
    ax.add_patch(box_m3)
    ax.text(18, 46, "Member 3: URL Analyzer", ha='center', fontsize=9.5, fontweight='bold', color='#B91C1C')
    ax.text(18, 30, "• URL Risk Level:\n  (SAFE, SUSPICIOUS, MALICIOUS)\n• Structural Indicators:\n  - Raw IP Host\n  - Known Shortener\n  - High-Risk TLD (.xyz, etc.)\n  - Lookalike / Brand Spoof\n  - Subdomain Depth >= 4\n  - Sensitive Path Keywords", ha='center', fontsize=7.5, color='#991B1B')

    # Arrows to Aggregator
    ax.annotate("", xy=(37, 65), xytext=(31, 74), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))
    ax.annotate("", xy=(37, 45), xytext=(31, 35), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1F2937'))

    # Middle: Point Scoring & Source Caps
    box_agg = patches.FancyBboxPatch((38, 25), 28, 55, boxstyle="round,pad=1.2", facecolor='#F8FAFC', edgecolor='#64748B', linewidth=1.8)
    ax.add_patch(box_agg)
    ax.text(52, 75, "Risk Calculation Engine", ha='center', fontsize=10, fontweight='bold', color='#0F172A')
    ax.text(52, 60, "Severity Point Weights:\n• CRITICAL: 45 points\n• HIGH: 30 points\n• MEDIUM: 18 points\n• LOW: 6 points\n\nModule Source Caps:\n• Message Cap: 55 pts max\n• URL Cap: 45 pts max\n• System Cap: 18 pts max\n\nRaw Score Sum: 0 – 100", ha='center', fontsize=7.5, color='#334155')

    # Arrow to Safety Overrides
    ax.annotate("", xy=(72, 65), xytext=(66, 65), arrowprops=dict(arrowstyle="->", lw=1.5, color='#DC2626'))

    # Right Top: Safety Overrides
    box_ovr = patches.FancyBboxPatch((72, 48), 25, 42, boxstyle="round,pad=1", facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
    ax.add_patch(box_ovr)
    ax.text(84.5, 86, "Safety Overrides", ha='center', fontsize=9.5, fontweight='bold', color='#92400E')
    ax.text(84.5, 68, "OVR-01: High Confidence Scam\n(Conf >= 0.80) -> Force HIGH\n\nOVR-02: Malicious URL\n(URL=MALICIOUS) -> Force HIGH\n\nOVR-03: OTP + External Link\n(OTP request with link) -> Force HIGH\n\nDegraded Mode Floor:\nService failure -> Minimum MEDIUM", ha='center', fontsize=7.2, color='#78350F')

    # Arrow down to Final Output
    ax.annotate("", xy=(84.5, 34), xytext=(84.5, 48), arrowprops=dict(arrowstyle="->", lw=1.5, color='#16A34A'))
    ax.annotate("", xy=(66, 20), xytext=(52, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#16A34A'))

    # Bottom Right: Final Categorization
    box_final = patches.FancyBboxPatch((55, 3), 42, 28, boxstyle="round,pad=1.2", facecolor='#ECFDF5', edgecolor='#10B981', linewidth=1.8)
    ax.add_patch(box_final)
    ax.text(76, 26.5, "Calibrated Assessment & Guidance", ha='center', fontsize=9.5, fontweight='bold', color='#065F46')
    ax.text(76, 14, "Final Risk Level: SAFE | LOW | MEDIUM | HIGH\nNormalized Threat Score: 0.00 – 1.00\n\nActions & Warnings:\n• Plain-Language Warning Message\n• Prioritized Safety Actions (max 4)\n• Voice Narration & Emergency Escalations", ha='center', fontsize=7.3, color='#064E3B')

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "fig5_risk_assessment_workflow.png", dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Generated fig5_risk_assessment_workflow.png")

def create_ui_placeholders():
    screens = [
        ("ui_dashboard.png", "SilverShield AI Home Dashboard", "High-contrast assistive interface with purple/lavender theme,\nmultilingual selection (EN/HI/KN), emergency helpline banner, and core feature tiles."),
        ("ui_auth.png", "Login and Registration Interface", "Argon2id-secured authentication screen with memory-hard hashing,\nsliding-window rate limiting, and generic error messages preventing user enumeration."),
        ("ui_scam_detector.png", "Scam Message Detection Interface", "Elderly-friendly message input area with font scaling options,\nsample test cases, and in-memory privacy preservation disclosure."),
        ("ui_scam_result.png", "Scam Message Prediction Result", "Clear binary prediction (SCAM / LEGITIMATE) with calibrated confidence gauge,\nsemantic intent flags, plain-language explanation, and one-click audio playback."),
        ("ui_url_analysis.png", "Suspicious URL Analysis Interface", "Zero-request heuristic analyzer showing 9 structural inspection layers,\nquery string stripping, brand typosquatting alerts, and safe domain validation."),
        ("ui_risk_assessment.png", "Unified Risk Assessment Result", "Consolidated 0–100 threat score gauge with risk categorization (LOW/MEDIUM/HIGH),\nsafety overrides display, and prioritized step-by-step protective instructions."),
        ("ui_settings_accessibility.png", "Settings and Accessibility Features", "WCAG AAA high-contrast toggle, tri-level font scaling (Compact/Standard/Large),\nregional voice synthesizer controls, and granular DPDP consent toggles.")
    ]

    for fname, title, desc in screens:
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        fig.patch.set_facecolor('#F8FAFC')
        ax.set_facecolor('#F8FAFC')

        border = patches.FancyBboxPatch((4, 4), 92, 92, boxstyle="round,pad=1", facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.5)
        ax.add_patch(border)

        header = patches.Rectangle((4, 80), 92, 16, facecolor='#49316F')
        ax.add_patch(header)
        ax.text(50, 88, f"SilverShield AI — {title}", ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF')

        badge = patches.FancyBboxPatch((25, 62), 50, 10, boxstyle="round,pad=0.5", facecolor='#EDE5FA', edgecolor='#7653B5', linewidth=1)
        ax.add_patch(badge)
        ax.text(50, 67, "[ Application Interface View ]", ha='center', va='center', fontsize=10, fontweight='bold', color='#5B21B6')

        ax.text(50, 44, desc, ha='center', va='center', fontsize=9, color='#334155', linespacing=1.6)

        footer = patches.Rectangle((4, 4), 92, 14, facecolor='#F1F5F9')
        ax.add_patch(footer)
        ax.text(50, 11, "Sahyadri College of Engineering & Management • Department of CSE", ha='center', va='center', fontsize=8, color='#64748B')

        plt.tight_layout()
        fig.savefig(OUTPUT_DIR / fname, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"Generated {fname}")

if __name__ == "__main__":
    create_system_architecture()
    create_system_workflow()
    create_ml_workflow()
    create_url_workflow()
    create_risk_assessment_workflow()
    create_ui_placeholders()
    print("All diagrams and placeholder figures generated successfully!")
