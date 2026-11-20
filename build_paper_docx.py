"""
Comprehensive Python script to generate an editable, professional IEEE-style
Microsoft Word (.docx) document for SilverShield AI research paper.
"""

import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

DOCX_OUTPUT = Path("Research_Paper/SilverShield_AI_Research_Paper.docx")
IMAGES_DIR = Path("Research_Paper/images")

def create_element(name):
    return OxmlElement(name)

def set_cell_border(cell, **kwargs):
    """
    Set cell borders: top, bottom, left, right.
    kwargs: top={"sz": 4, "val": "single", "color": "000000"}
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn('w:{}'.format(key)), str(val))

def set_table_borders(table):
    """Clean IEEE style table borders: top/bottom solid, thin header bottom line."""
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            # Simple border
            if i == 0:
                set_cell_border(cell,
                                top={"sz": 12, "val": "single", "color": "000000"},
                                bottom={"sz": 8, "val": "single", "color": "000000"},
                                left={"val": "none"}, right={"val": "none"})
            elif i == len(table.rows) - 1:
                set_cell_border(cell,
                                top={"val": "none"},
                                bottom={"sz": 12, "val": "single", "color": "000000"},
                                left={"val": "none"}, right={"val": "none"})
            else:
                set_cell_border(cell,
                                top={"val": "none"},
                                bottom={"sz": 4, "val": "single", "color": "D1D5DB"},
                                left={"val": "none"}, right={"val": "none"})

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.all_caps = True
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.bold = True
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9.5)
    run.font.italic = True
    return p

def add_body_p(doc, text, bold_prefix="", indent=0.2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.05
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent > 0:
        p.paragraph_format.first_line_indent = Inches(indent)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(9.5)
    return p

def add_equation(doc, eq_text, eq_num):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_eq = p.add_run(f"    {eq_text}")
    run_eq.font.name = 'Times New Roman'
    run_eq.font.size = Pt(9.5)
    run_eq.font.italic = True
    run_num = p.add_run(f"    ({eq_num})")
    run_num.font.name = 'Times New Roman'
    run_num.font.size = Pt(9.5)
    return p

def add_figure(doc, img_path, caption_text, width=Inches(3.3)):
    p_img = doc.add_paragraph()
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(img_path):
        run = p_img.add_run()
        run.add_picture(str(img_path), width=width)
    else:
        run = p_img.add_run(f"[Figure missing: {img_path}]")
        run.font.italic = True
    
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(8)
    p_cap.paragraph_format.keep_with_next = True
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True

def add_table_caption(doc, tab_num, tab_title):
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(2)
    p_cap.paragraph_format.keep_with_next = True
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_cap.add_run(f"{tab_num}\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.all_caps = True
    r2 = p_cap.add_run(tab_title)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(8.5)
    r2.font.all_caps = True

def build_paper():
    doc = docx.Document()

    # Base page settings: 8.5 x 11 inches, 0.75 in margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)

    # ==================== TITLE (Single Column) ====================
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Secure AI-Powered Elderly Digital Safety Companion with Privacy-Preserving Scam Detection and Early Warning")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.font.bold = True

    # ==================== AUTHORS ====================
    p_auth = doc.add_paragraph()
    p_auth.paragraph_format.space_before = Pt(0)
    p_auth.paragraph_format.space_after = Pt(4)
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_auth = p_auth.add_run("Achinta R S, M Shreya, Dhanya, Kiranshree N")
    r_auth.font.name = 'Times New Roman'
    r_auth.font.size = Pt(11)
    r_auth.font.bold = True

    p_affil = doc.add_paragraph()
    p_affil.paragraph_format.space_before = Pt(0)
    p_affil.paragraph_format.space_after = Pt(2)
    p_affil.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_affil = p_affil.add_run("Department of Computer Science and Engineering\nSahyadri College of Engineering & Management, Mangaluru, Karnataka, India\nEmails: {achinta.cs22, mshreya.cs22, dhanya.cs22, kiranshree.cs22}@sahyadri.edu.in")
    r_affil.font.name = 'Times New Roman'
    r_affil.font.size = Pt(9.5)

    p_guide = doc.add_paragraph()
    p_guide.paragraph_format.space_before = Pt(2)
    p_guide.paragraph_format.space_after = Pt(14)
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_guide = p_guide.add_run("Project Guide: Fathima Mehnaz, Assistant Professor\nDepartment of Computer Science and Engineering, Sahyadri College of Engineering & Management\nEmail: fathima.mehnaz@sahyadri.edu.in")
    r_guide.font.name = 'Times New Roman'
    r_guide.font.size = Pt(9.5)
    r_guide.font.italic = True

    # ==================== ABSTRACT & KEYWORDS ====================
    p_abs = doc.add_paragraph()
    p_abs.paragraph_format.left_indent = Inches(0.4)
    p_abs.paragraph_format.right_indent = Inches(0.4)
    p_abs.paragraph_format.space_after = Pt(6)
    p_abs.paragraph_format.line_spacing = 1.05
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_absh = p_abs.add_run("Abstract—")
    r_absh.font.name = 'Times New Roman'
    r_absh.font.size = Pt(9)
    r_absh.font.bold = True
    r_abst = p_abs.add_run("Elderly citizens face escalating exposure to sophisticated social engineering, smishing (SMS phishing), authority impersonation, and fraudulent payment demands. Existing commercial security software predominantly targets enterprise environments, relies on intrusive contact harvesting, emits complex technical telemetry, and lacks regional language accessibility. In this paper, we present SilverShield AI, a distributed, privacy-preserving digital safety companion engineered specifically for senior citizens and family caregivers. The platform employs a decoupled microservice architecture featuring an in-memory Natural Language Processing (NLP) scam detection engine, a zero-request 9-layer static URL heuristic inspector, and a central risk aggregator. Machine learning models were trained on a curated corpus of 5,160 deduplicated mobile messages using sublinear TF-IDF feature extraction. Logistic Regression achieved a champion performance of 98.06% classification accuracy, 93.75% scam recall, and an ROC-AUC of 0.9963, outperforming Multinomial Naive Bayes by halving false negatives (6.25% vs 12.50%). The URL security module performs structural inspection without transmitting requests to target domains, eliminating attacker telemetry. To guarantee senior privacy, the architecture enforces strict zero-raw-message database retention, compliant with India's Digital Personal Data Protection (DPDP) Act and GDPR. User authentication leverages memory-hard Argon2id cryptographic hashing, anti-enumeration timing equalizers, and sliding-window rate limiting. The assistive user interface incorporates tri-lingual localization across English, Hindi, and Kannada, multi-tier speech narration, WCAG AAA high-contrast styling, one-click caregiver WhatsApp escalation, and emergency integration with India's National Cyber Crime Helpline (1930). Comprehensive functional validation across 162 automated test cases confirms robust performance and graceful in-process degradation.")
    r_abst.font.name = 'Times New Roman'
    r_abst.font.size = Pt(9)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.left_indent = Inches(0.4)
    p_kw.paragraph_format.right_indent = Inches(0.4)
    p_kw.paragraph_format.space_after = Pt(14)
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_kwh = p_kw.add_run("Keywords—")
    r_kwh.font.name = 'Times New Roman'
    r_kwh.font.size = Pt(9)
    r_kwh.font.bold = True
    r_kwt = p_kw.add_run("Elderly digital safety, smishing detection, machine learning, natural language processing, heuristic URL inspection, explainable AI, privacy-by-design, Argon2id, assistive technology.")
    r_kwt.font.name = 'Times New Roman'
    r_kwt.font.size = Pt(9)

    # ==================== MAIN CONTENT: TWO COLUMNS ====================
    sec_cols = doc.add_section()
    sectPr = sec_cols._sectPr
    cols = sectPr.xpath('./w:cols')
    if cols:
        cols[0].set(qn('w:num'), '2')
        cols[0].set(qn('w:space'), '720')  # 0.5 in gap

    # ----------------- SECTION I: INTRODUCTION -----------------
    add_heading_1(doc, "I. Introduction")
    
    add_heading_2(doc, "A. Background")
    add_body_p(doc, "The accelerated digitization of financial systems, telecommunications, and governmental public services has integrated senior citizens into digital payment gateways, mobile banking applications, and messaging channels. However, this demographic transition has coincided with an unprecedented surge in targeted cyber fraud. Threat actors systematically exploit the digital literacy gap, visual limitations, and cognitive vulnerabilities of older adults through deceptive Short Message Service (SMS) smishing, WhatsApp messages, and artificial urgency tactics. Fraudulent communications routinely impersonate respected banking institutions (e.g., State Bank of India, HDFC Bank), regulatory authorities (e.g., Reserve Bank of India), power distribution utilities, and courier services, falsely claiming impending account suspensions, expired Know Your Customer (KYC) compliance, or pending electricity disconnections.")

    add_heading_2(doc, "B. Motivation")
    add_body_p(doc, "Traditional cybersecurity tools and commercial anti-spam smartphone applications exhibit critical shortcomings when deployed by senior citizens. First, commercial spam blockers typically operate by crowdsourcing phone numbers, requiring users to surrender their complete contact address books and transmitting private communication telemetry to external cloud servers. This creates severe privacy infringements that conflict with data protection frameworks such as India's Digital Personal Data Protection (DPDP) Act and the General Data Protection Regulation (GDPR). Second, mainstream threat indicators present intimidating technical jargon (e.g., DNS anomalies, SSL certificate cipher mismatches, autonomous system numbers) that causes cognitive fatigue and panic among non-technical seniors. Third, prevailing solutions operate almost exclusively in English, failing older adults in regional contexts who communicate primarily in native languages such as Kannada and Hindi. Fourth, existing spam filters rely on known-number blacklists, leaving seniors completely defenseless against zero-day smishing lures distributed from freshly acquired SIM cards or spoofed alphanumeric sender headers.")

    add_heading_2(doc, "C. Objectives")
    add_body_p(doc, "The primary objectives of the SilverShield AI project are fivefold:")
    add_body_p(doc, "1) To engineer a content-driven, privacy-preserving AI scam detection engine that classifies fraudulent SMS and messaging lures with low latency (<5 ms) and high recall.")
    add_body_p(doc, "2) To construct a zero-request 9-layer static URL heuristic analyzer capable of identifying malicious hyperlinks, brand impersonation, and obfuscated destinations without initiating outbound HTTP connections.")
    add_body_p(doc, "3) To formulate a deterministic risk aggregation engine that synthesizes textual and hyperlinked threat vectors into an objective score (0–100) and four plain-language risk tiers (SAFE, LOW, MEDIUM, HIGH) governed by mandatory safety overrides.")
    add_body_p(doc, "4) To implement memory-hard Argon2id authentication, anti-enumeration timing defenses, granular consent controls, and a strict zero-raw-message database storage architecture.")
    add_body_p(doc, "5) To develop an elderly-tailored, WCAG AAA compliant user interface offering tri-lingual support (English, Hindi, Kannada), resilient multi-tier speech narration, one-click family caregiver alerting, and National Cyber Crime Helpline (1930) access.")

    add_heading_2(doc, "D. Contributions of the Proposed System")
    add_body_p(doc, "The core contributions delivered in this research project include:")
    add_body_p(doc, "• Decoupled 4-Tier Topology with Graceful Degradation: Independent microservices for ML scam detection (Port 8001), URL security (Port 8002), risk orchestration (Port 8000), and assistive presentation (Port 8501), backed by seamless local in-process fallback execution.")
    add_body_p(doc, "• High-Recall Optimized Machine Learning: A calibrated sublinear TF-IDF Logistic Regression pipeline evaluated on 5,160 deduplicated messages, achieving an ROC-AUC of 0.9963 and reducing the false negative rate to 6.25% to prevent senior deception.")
    add_body_p(doc, "• Zero-Request Heuristic URL Inspection: A privacy-centric 9-layer URL parser that evaluates domain lookalikes, raw IP hosts, shorteners, and credential paths with automated query-string redaction.")
    add_body_p(doc, "• Explainable Intent Indicator Decomposition: Identification of 7 high-risk semantic patterns (OTP requests, financial transfers, authority threats) mapped directly to concrete, actionable behavioral instructions.")
    add_body_p(doc, "• Socio-Technical Accessibility Integration: Full localization into Kannada and Hindi alongside multi-tier Web Speech API synthesis, eliminating linguistic and sensory exclusion.")

    # ----------------- SECTION II: LITERATURE SURVEY -----------------
    add_heading_1(doc, "II. Literature Survey")

    add_heading_2(doc, "A. Review of Four Main Research Papers")
    add_body_p(doc, "To establish the theoretical and empirical foundation of this work, exactly four seminal, peer-reviewed academic research papers were investigated across the domains of elderly cyber vulnerability, machine learning phishing detection, explainable artificial intelligence, and mobile SMS spam classification.")

    add_heading_3(doc, "1) Elderly Phishing Susceptibility")
    add_body_p(doc, "Oliveira et al. [1] conducted an extensive in-home empirical study utilizing the Phishing Internet Task (PHIT) framework to examine how age cohorts interact with real-world phishing attacks. Investigating the psychological 'weapons of influence' (such as scarcity, reciprocation, and authority), the authors demonstrated that older adults exhibit significantly reduced discrimination sensitivity when distinguishing between legitimate communications and fraudulent lures. While younger participants were frequently triggered by scarcity and tech-related urgency, older adults showed acute vulnerability to authority impersonation, financial compliance notices, and reciprocal promises of prizes. Although Oliveira et al. provided vital behavioral insights into age-related cyber risk, their work was purely empirical and did not engineer an automated, assistive intervention software tool to protect vulnerable seniors in real time.")

    add_heading_3(doc, "2) Machine Learning URL Phishing Detection")
    add_body_p(doc, "Şahingöz et al. [2] introduced an advanced machine learning framework for detecting phishing attacks strictly through Natural Language Processing and character-level lexical features extracted directly from URL strings. Benchmarking seven classification algorithms on a massive corpus, their Random Forest model attained 97.98% classification accuracy. Crucially, the authors emphasized that analyzing URL structure alone without fetching the actual target webpage dramatically reduces latency and avoids active attacker surveillance. However, the study remained confined to web browser URL strings and did not address mobile SMS scam context, multi-factor OTP requests, or localized interfaces for senior users.")

    add_heading_3(doc, "3) Explainable Artificial Intelligence in Cybersecurity")
    add_body_p(doc, "Capuano et al. [3] presented an extensive survey detailing the integration of Explainable Artificial Intelligence (XAI) within cybersecurity, spanning spam filtering, intrusion detection, and phishing mitigation. The authors analyzed the 'black-box' dilemma inherent in complex deep neural networks and ensemble classifiers, proving that opaque confidence scores erode user trust and cause warning fatigue. The paper established that pairing machine learning predictions with local feature attribution and deterministic rule indicators is mandatory for high-stakes defensive tools. Nevertheless, Capuano et al. focused on enterprise security operations and theoretical taxonomies, leaving an unaddressed gap in translating XAI concepts into plain-language, jargon-free advice for non-technical senior citizens.")

    add_heading_3(doc, "4) SMS Spam Corpus and Baseline Modeling")
    add_body_p(doc, "Almeida et al. [4] created the seminal, globally recognized SMS Spam Collection benchmark dataset by curating and validating 5,574 authentic mobile text messages. The authors established baseline classification benchmarks using Support Vector Machines and Multinomial Naive Bayes, demonstrating that statistical term frequency and n-gram modeling provide effective discriminative power for short, informal mobile texts. While foundational, the original study focused exclusively on English text, evaluated static classification metrics without considering combined hyperlinked threats, and did not incorporate modern privacy protections, rate limiting, or assistive speech synthesis.")

    add_heading_2(doc, "B. Comparative Analysis")
    add_body_p(doc, "Table I provides a structured comparative synthesis of the four examined research papers against the architecture of SilverShield AI.")

    # TABLE I
    add_table_caption(doc, "TABLE I", "Comparison of the Four Existing Research Papers with SilverShield AI")
    tab_1 = doc.add_table(rows=6, cols=5)
    tab_1.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_1_data = [
        ["Author & Year", "Core Methodology", "Key Contributions", "Identified Limitations", "Relation to SilverShield AI"],
        ["Oliveira et al., 2017 [1]", "In-home behavioral testing via PHIT framework", "Proved reduced discrimination sensitivity in older adults", "Empirical study only; no defensive software system", "Inspired elderly-tailored UX, calm UI, and caregiver alerts"],
        ["Şahingöz et al., 2019 [2]", "Lexical NLP feature extraction on URLs", "97.98% accuracy via Random Forest without web fetching", "Evaluated URLs in isolation; ignored SMS/OTP context", "Guided Member 3 zero-request 9-layer static heuristic engine"],
        ["Capuano et al., 2022 [3]", "Survey of XAI paradigms (SHAP, LIME, rules)", "Demonstrated necessity of interpretability in cyber alerts", "Targeted SOC analysts; ignored non-technical seniors", "Directed Member 4 plain-language explainability and actions"],
        ["Almeida et al., 2011 [4]", "Mobile corpus curation and NB/SVM modeling", "Established the 5,574 SMS benchmark dataset", "English-only; no hybrid URL checking or speech synthesis", "Provided baseline dataset curated for SilverShield AI models"],
        ["SilverShield AI (Proposed)", "Hybrid ML (LR) + 9-Layer URL Heuristics", "Unified 0–100 risk score, DPDP privacy, tri-lingual TTS", "Offline-trained static weights; manual input", "Addresses the full socio-technical safety lifecycle"]
    ]
    for r_idx, r_data in enumerate(tab_1_data):
        row = tab_1.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_1)

    add_heading_2(doc, "C. Research Gap")
    add_body_p(doc, "While prior literature provides robust individual components—psychological insights into aging [1], lexical URL classifiers [2], explainability theory [3], and SMS text corpora [4]—there is a complete absence of an integrated, privacy-preserving socio-technical framework designed specifically for elderly individuals. Existing commercial tools either sacrifice privacy by logging user texts and contact books, or alienate seniors through complex telemetry and English-only interfaces. SilverShield AI bridges this critical research gap by combining high-recall NLP text classification, zero-request URL inspection, memory-hard authentication, granular consent management, and tri-lingual speech accessibility into a cohesive, senior-friendly companion.")

    # ----------------- SECTION III: PROBLEM FORMULATION -----------------
    add_heading_1(doc, "III. Problem Formulation")

    add_heading_2(doc, "A. Problem Definition")
    add_body_p(doc, "Let an incoming mobile message be denoted as M = {w_1, w_2, ..., w_n} containing n textual tokens and an optional set of embedded hyperlinks U = {u_1, u_2, ..., u_m}. The objective is to determine a mapping function:")
    add_equation(doc, "f(M, U) -> <R, S, I, A, W>", "1")
    add_body_p(doc, "where R in {SAFE, LOW, MEDIUM, HIGH} represents the unified categorical risk rating, S in [0.0, 1.0] denotes the normalized threat score, I is the set of human-interpretable threat indicators, A is a prioritized list of actionable behavioral instructions, and W is a localized plain-language warning message. This mapping must execute under strict constraints: zero persistent disk storage of M or raw U, zero outgoing HTTP network transmission to U, and an end-to-end execution latency below 100 ms on commodity hardware.")

    add_heading_2(doc, "B. Existing System")
    add_body_p(doc, "Current defensive mechanisms against mobile financial fraud rely on three fragmented technologies:")
    add_body_p(doc, "1) Crowdsourced Caller-ID and Number Blacklists: Applications that identify callers based on community tagging of phone numbers.")
    add_body_p(doc, "2) Keyword Blocklists on Mobile Operating Systems: Static on-device pattern filters matching rudimentary strings like 'win' or 'free'.")
    add_body_p(doc, "3) Cloud-Based Browser Protection: Endpoint security suites that query remote URL reputation databases or execute active sandboxed browser rendering.")

    add_heading_2(doc, "C. Limitations of Existing Systems")
    add_body_p(doc, "• Vulnerability to Zero-Day Attacks: Number blacklists are inherently reactive. Scammers routinely bypass them by rotating disposable virtual numbers, VoIP numbers, and unlisted SIM cards.")
    add_body_p(doc, "• Severe Privacy Violations: Crowdsourced filters routinely upload full contact address books and SMS metadata to external servers, violating data minimization principles.")
    add_body_p(doc, "• Attacker Telemetry in Active Scanning: Cloud URL scanners that visit destination links expose the victim's IP address and validate the message delivery to the scammer.")
    add_body_p(doc, "• Cognitive and Usability Barriers: Complex telemetry (SSL handshakes, ASN numbers) confuses seniors, while lack of regional language voice output excludes non-English speakers.")

    add_heading_2(doc, "D. Proposed System: SilverShield AI")
    add_body_p(doc, "SilverShield AI redefines elderly cyber defense through a privacy-first, content-driven assistive model. Rather than identifying who sent the message, it analyzes what the message demands and how embedded hyperlinks are structured. By executing in-memory TF-IDF NLP inference and 9-layer static heuristic URL inspection, the system computes transparent threat indicators without retaining user messages or pinging destination servers. The platform features an elderly-optimized presentation layer with Kannada, Hindi, and English voice synthesis and one-click emergency caregiver escalation.")

    add_heading_2(doc, "E. Advantages of the Proposed System")
    add_body_p(doc, "• Zero Attacker Telemetry: Zero-request URL inspection guarantees that malicious servers cannot confirm link interaction or log senior network metadata.")
    add_body_p(doc, "• DPDP and GDPR Privacy-by-Design: Raw message contents reside strictly in temporary volatile RAM, ensuring total confidentiality.")
    add_body_p(doc, "• High-Recall Defense Against Missed Scams: Optimized decision boundaries prevent false negatives on urgent fraud lures.")
    add_body_p(doc, "• Demographic-Centric Usability: WCAG AAA high-contrast layout, large touch targets, regional language voice synthesis, and direct connection to India's 1930 National Helpline.")

    # ----------------- SECTION IV: PROJECT DESIGN AND IMPLEMENTATION -----------------
    add_heading_1(doc, "IV. Project Design and Implementation")

    add_heading_2(doc, "A. Overall System Architecture")
    add_body_p(doc, "SilverShield AI is architected as a distributed 4-tier microservice system designed for resilience, modularity, and low operational overhead. Fig. 1 illustrates the system components and their inter-service communication channels.")

    add_figure(doc, IMAGES_DIR / "fig1_system_architecture.png", "Fig. 1. Overall System Architecture of SilverShield AI illustrating the 4-tier microservice topology, port assignments, and graceful in-process degradation fallback boundary.")

    add_body_p(doc, "The platform comprises four discrete functional tiers:")
    add_body_p(doc, "1) Presentation Tier (Port 8501): Built with Streamlit, providing reactive UI rendering, font scaling, contrast switching, and browser-native Web Speech narration.")
    add_body_p(doc, "2) Integration and Security Tier (Port 8000): Developed with FastAPI, hosting the central risk engine, Argon2id authentication, rate limiting, and SQLite storage.")
    add_body_p(doc, "3) AI/ML Scam Detection Tier (Port 8001): A dedicated FastAPI service running TF-IDF feature extraction, Logistic Regression inference, and intent indicator parsing.")
    add_body_p(doc, "4) URL Security Tier (Port 8002): A dedicated FastAPI service executing 9-layer static heuristic inspections, query parameter redaction, and PII scrubbing.")

    add_heading_2(doc, "B. System Workflow")
    add_body_p(doc, "The end-to-end execution pipeline of SilverShield AI follows a structured multi-stage trajectory, depicted in Fig. 2.")

    add_figure(doc, IMAGES_DIR / "fig2_system_workflow.png", "Fig. 2. End-to-End System Workflow Diagram depicting user submission, privacy validation, parallel microservice analysis, risk score aggregation, and multilingual assistive output.")

    add_body_p(doc, "When a senior user submits an SMS or WhatsApp message: (1) The frontend verifies consent and normalizes whitespace; (2) The payload is transmitted to the central orchestrator (Port 8000), which verifies payload boundaries (<= 64 KB) and strips PII; (3) The orchestrator concurrently dispatches text to the ML Scam Engine (Port 8001) and extracted hyperlinks to the URL Security API (Port 8002); (4) Signals are aggregated into a composite risk score governed by source caps and safety overrides; (5) The final response delivers the categorical risk level, threat indicators, plain-language warnings, actionable steps, and regional voice narration.")

    add_heading_2(doc, "C. Frontend Implementation")
    add_body_p(doc, "The user interface (silvershield_frontend.py) is crafted using Streamlit with custom CSS and HTML5 embeds (frontend/styles.py). Designed in adherence to human-computer interaction (HCI) standards for seniors: (1) Color Palette: Deep Purple (#49316F) provides calming, high-contrast headings; Soft Lavender (#EDE5FA) defines card backgrounds; and Crimson (#DC2626) highlights critical dangers. (2) Typography and Touch Targets: Standard base font of 15 px with toggleable Large scaling (17 px). All primary action buttons feature minimum touch heights of 44 px. (3) WCAG AAA High Contrast: A dedicated toggle transforms the entire interface into an ultra-high-contrast deep dark palette (#0B0814 background, #FFFFFF text, #B39DDB borders) achieving a contrast ratio >7:1. (4) Minimal Cognitive Friction: Navigation is housed within an unobtrusive top-right menu, removing clutter and confusing technical dials.")

    add_heading_2(doc, "D. Backend Implementation")
    add_body_p(doc, "The central integration backend (app/main.py) is implemented using FastAPI and served via Uvicorn. Inter-service HTTP requests are managed through resilient HTTPX/Requests adapters configured with 1.0-second timeout guards and zero retries to prevent blocking worker threads. If a microservice fails to respond within the allocated threshold, the orchestrator triggers Graceful In-Process Degradation: (1) If the ML Scam Engine (Port 8001) is unreachable, the orchestrator logs state as UNAVAILABLE, flags system status as DEGRADED, and sets a mandatory risk floor of MEDIUM. (2) If the URL Security API (Port 8002) is offline, URL status reports UNKNOWN while textual scam classification proceeds unhindered. (3) If the entire central API (Port 8000) is offline, the Streamlit frontend automatically activates its embedded Local AI Security Engine, executing identical Scikit-Learn models and URL heuristics in-process.")

    add_heading_2(doc, "E. AI/ML Implementation")
    add_body_p(doc, "The AI/ML scam detection architecture (ai_module/src/) processes informal mobile texts to distinguish between benign communications and fraudulent lures. The end-to-end training and inference pipeline is illustrated in Fig. 3.")

    add_figure(doc, IMAGES_DIR / "fig3_ml_workflow.png", "Fig. 3. AI/ML Scam Message Detection Pipeline illustrating dataset curation, TF-IDF vectorization, Logistic Regression classification, and 7-pattern semantic intent extraction.")

    add_heading_2(doc, "F. Dataset Description")
    add_body_p(doc, "The machine learning subsystem is trained on a curated corpus derived from the benchmark SMS Spam Collection [4]. The raw dataset comprises 5,572 mobile messages. Rigorous data hygiene and deduplication yielded 5,160 unique records, summarized in Table II.")

    # TABLE III (renamed in order)
    add_table_caption(doc, "TABLE II", "Dataset Description and Class Distribution")
    tab_3 = doc.add_table(rows=9, cols=3)
    tab_3.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_3_data = [
        ["Dataset Attribute", "Value / Count", "Percentage"],
        ["Raw Corpus Records", "5,572", "100.00%"],
        ["Deduplicated Unique Messages", "5,160", "100.00%"],
        ["Legitimate Class (Ham)", "4,518", "87.56%"],
        ["Scam / Fraud Class (Spam)", "642", "12.44%"],
        ["Training Partition (80%, Stratified)", "4,128", "80.00%"],
        ["Testing Partition (20%, Stratified)", "1,032", "20.00%"],
        ["Test Partition: Legitimate", "904", "87.60%"],
        ["Test Partition: Scam", "128", "12.40%"]
    ]
    for r_idx, r_data in enumerate(tab_3_data):
        row = tab_3.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_3)

    add_heading_2(doc, "G. Data Preprocessing")
    add_body_p(doc, "Text normalization (ai_module/src/preprocessing.py) executes sequentially: (1) Case Folding: All string characters are converted to lowercase; (2) PII Stripping: Phone numbers, email addresses, and credit card patterns are sanitized to prevent memorization of specific phone numbers; (3) Whitespace Normalization: Redundant tabs, trailing line breaks, and multi-spaces are collapsed; (4) Boundary Guarding: Messages shorter than 2 characters or exceeding 1,000 characters are rejected.")

    add_heading_2(doc, "H. TF-IDF Feature Extraction")
    add_body_p(doc, "Text representations are constructed using Scikit-Learn's TfidfVectorizer: (1) N-gram Range: Unigrams and bigrams (ngram_range=(1, 2)) to capture contextual compound phrases such as 'account blocked', 'verify kyc', and 'free cash'; (2) Term Frequency Scaling: Sublinear TF scaling (1 + log(tf)) to dampen the distorting impact of repeated tokens; (3) Frequency Thresholds: Minimum document frequency of min_df = 2 and maximum features capped at 5,000 top informative dimensions.")

    add_heading_2(doc, "I. Machine Learning Algorithms")
    add_body_p(doc, "Two supervised learning classifiers were configured, trained, and benchmarked:")
    add_body_p(doc, "1) Logistic Regression (Champion Model): Configured with balanced class weights (class_weight='balanced') to address the 87.56% vs 12.44% class imbalance, max_iter=1000, and random seed 42. Logistic Regression outputs calibrated posterior probabilities via the standard sigmoid activation:")
    add_equation(doc, "P(y = 1 | x) = 1 / (1 + e^-(w^T x + b))", "2")
    add_body_p(doc, "where x in R^5000 represents the sparse TF-IDF vector, w denotes the learned weight vector, and b is the scalar bias. A message is classified as SCAM when P(y = 1 | x) >= 0.50. The prediction confidence is defined as:")
    add_equation(doc, "Confidence = max(P(y = 1 | x), 1 - P(y = 1 | x))", "3")
    add_body_p(doc, "2) Multinomial Naive Bayes (Benchmark): Configured with Laplace smoothing parameter alpha = 0.1 and learned class priors.")

    add_heading_2(doc, "J. Scam Message Detection")
    add_body_p(doc, "Beyond probabilistic classification, the module incorporates a deterministic intent detector (ai_module/src/warning_indicators.py) scanning for 7 semantic deception categories: (1) urgent_payment: Pressures users to transfer funds, settle courier fees, or purchase gift cards; (2) otp_request: Demands one-time passwords, PINs, or security passcodes; (3) fake_prize: Unsolicited lottery wins, cashback vouchers, or gift rewards; (4) bank_impersonation: Claims of representing SBI, HDFC, ICICI, Axis, or central banks; (5) account_verification: Urges verification of identity, credentials, or KYC records; (6) account_suspension: Threats of account closure, SIM deactivation, or police warrants; (7) suspicious_link: Presence of shortened links or deceptive domains within text.")

    add_heading_2(doc, "K. Suspicious URL Analysis")
    add_body_p(doc, "The URL Security Engine (url_analysis/analyzer.py) inspects web hyperlinks using 9 zero-request static heuristic layers, illustrated in Fig. 4.")

    add_figure(doc, IMAGES_DIR / "fig4_url_workflow.png", "Fig. 4. Suspicious URL Analysis Workflow detailing PII redaction, query string stripping, and the 9 zero-request static heuristic inspection layers.")

    add_body_p(doc, "The 9 inspection layers operate strictly in memory: (1) IP Address Host: Regex matches direct IPv4/IPv6 hosts used to bypass DNS domain reputation filters; (2) URL Shorteners: Checks against 16 known shortening hosts (bit.ly, tinyurl.com, t.co, is.gd, etc.); (3) High-Risk TLDs: Evaluates extensions commonly abused in smishing (.xyz, .top, .club, .work, .click, .zip); (4) Brand Impersonation / Homoglyphs: Strips digits and identifies deceptive brand variations targeting 21 major entities (paypal, amazon, sbi, chase); (5) Subdomain Depth: Flags nesting depth exceeding 3 labels (login.verify.bank.secure.com); (6) Suspicious Path Keywords: Scans URL path strings for credential-harvesting tokens (login, signin, verify, banking, kyc); (7) Excessive Length: Flags URLs exceeding 200 characters designed to push domain names off mobile screens; (8) Embedded Redirects: Identifies nested http protocol markers in query tails; (9) Host Spoofing (@ Symbol): Flags '@' characters in authority components used to disguise destination hosts.")
    add_body_p(doc, "To preserve user privacy, query strings and session fragments are stripped prior to reporting:")
    add_equation(doc, "http://scam.xyz/pay?user=senior&token=9928 -> http://scam.xyz/pay", "4")

    # TABLE VI
    add_table_caption(doc, "TABLE III", "The 9 URL Heuristic Inspection Layers")
    tab_6 = doc.add_table(rows=10, cols=3)
    tab_6.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_6_data = [
        ["Layer #", "Inspection Target", "Detection Rule & Heuristic Logic"],
        ["Layer 1", "IP Address Host", "Regex matches raw IPv4 / IPv6 addresses bypassing DNS"],
        ["Layer 2", "URL Shortener", "Comparison against 16 known shortening services (bit.ly, tinyurl)"],
        ["Layer 3", "High-Risk TLD", "Evaluates abuse-prone domain extensions (.xyz, .top, .tk, .zip)"],
        ["Layer 4", "Brand Impersonation", "Normalized Levenshtein / homoglyph matches across 21 top brands"],
        ["Layer 5", "Subdomain Depth", "Counts domain labels, flagging depth >= 4 (labels > 3)"],
        ["Layer 6", "Sensitive Path", "Detects keywords (/login, /verify, /banking, /kyc) in URL path"],
        ["Layer 7", "Excessive Length", "Detects URLs > 200 characters designed to obscure domains"],
        ["Layer 8", "Embedded Redirect", "Identifies nested 'http' markers in URL query parameters"],
        ["Layer 9", "Host Spoofing", "Detects '@' character in authority components used to mislead"]
    ]
    for r_idx, r_data in enumerate(tab_6_data):
        row = tab_6.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_6)

    add_heading_2(doc, "L. Risk Assessment Engine")
    add_body_p(doc, "Implemented in app/core/risk_engine.py, the central risk engine translates signals into a unified threat score (0–100) and four categorical risk levels, depicted in Fig. 5.")

    add_figure(doc, IMAGES_DIR / "fig5_risk_assessment_workflow.png", "Fig. 5. Central Risk Assessment Workflow showing point allocation, module source caps, deterministic safety overrides, and final action mapping.")

    add_body_p(doc, "Points are assigned according to threat severity: CRITICAL (45 pts), HIGH (30 pts), MEDIUM (18 pts), and LOW (6 pts). To prevent a single anomalous indicator from distorting results, contributions are capped per module source:")
    add_equation(doc, "Total Score = min(55, S_msg) + min(45, S_url) + min(18, S_sys)", "5")
    add_body_p(doc, "Baseline thresholds: Score < 24 -> LOW; 24 <= Score < 55 -> MEDIUM; Score >= 55 -> HIGH.")
    add_body_p(doc, "Deterministic Safety Overrides: (1) OVR-01: ML scam prediction with confidence >= 0.80 forces risk to HIGH; (2) OVR-02: URL identified as MALICIOUS forces risk to HIGH; (3) OVR-03: OTP demand combined with an external link forces risk to HIGH; (4) OVR-04: Subsystem outage locks risk floor to MEDIUM.")

    # TABLE VII
    add_table_caption(doc, "TABLE IV", "Risk Categories and Prioritized Safety Actions")
    tab_7 = doc.add_table(rows=5, cols=4)
    tab_7.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_7_data = [
        ["Risk Tier", "Score Range", "Core Severity Meaning", "Prioritized Behavioral Safety Actions"],
        ["SAFE", "0 – 10", "Routine communication", "KEEP_CAUTIOUS: Stay cautious with unsolicited texts"],
        ["LOW", "11 – 23", "Low-probability anomalies", "KEEP_CAUTIOUS, VERIFY_SENDER: Verify identity before responding"],
        ["MEDIUM", "24 – 54", "Suspicious link or urgency", "DO_NOT_CLICK_LINK, VERIFY_OFFICIAL_CHANNEL, TAKE_TIME"],
        ["HIGH", "55 – 100", "Critical fraud / scam lure", "NEVER_SHARE_OTP, DO_NOT_TRANSFER_MONEY, REPORT_MESSAGE (1930)"]
    ]
    for r_idx, r_data in enumerate(tab_7_data):
        row = tab_7.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_7)

    add_heading_2(doc, "M. Explainable Warning System")
    add_body_p(doc, "Rather than displaying technical probabilities, SilverShield AI maps risk categories directly to concrete behavioral instructions (config/risk_config.json). A maximum of four prioritized actions are presented: (1) NEVER_SHARE_OTP: 'Never share an OTP, PIN or password. No bank, police officer or company will ever ask for it.' (2) DO_NOT_TRANSFER_MONEY: 'Do not transfer money to anyone you have not confirmed in person.' (3) DO_NOT_CLICK_LINK: 'Do not click the link. Open the organisation's own official app or type its address yourself.' (4) REPORT_MESSAGE: 'Report the message and block the sender, then delete it.'")

    add_heading_2(doc, "N. Privacy and Security Mechanisms")
    add_body_p(doc, "Security is implemented across all tiers (security/): (1) Argon2id Password Hashing: Complies with OWASP Gold Standards: time_cost = 2, memory_cost = 65,536 KiB (64 MiB RAM), parallelism = 1, and 16-byte random salts. (2) Anti-Enumeration Timing Equalizer: resist_timing_enumeration() executes a dummy Argon2id hash cycle whenever an email is not found, eliminating timing side-channels. (3) Sliding-Window Rate Limiting: Limits registration to 10 requests/min and login to 15 requests/min per IP. (4) JWT Session Protection: Stateless tokens signed with HMAC-SHA256 (HS256) expiring in 120 minutes, backed by a server-side revocation blacklist. (5) Zero-Raw-Message Rule: User messages are processed strictly in volatile RAM. No unencrypted text or private SMS is ever committed to disk or database tables.")

    # TABLE IX
    add_table_caption(doc, "TABLE V", "Security and Privacy Mechanisms Implemented in SilverShield AI")
    tab_9 = doc.add_table(rows=8, cols=3)
    tab_9.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_9_data = [
        ["Security Domain", "Underlying Technology", "Defensive Purpose & Safeguard"],
        ["Password Hashing", "Argon2id (OWASP Winner)", "64 MiB memory-hard parameter resists GPU/ASIC brute forcing"],
        ["Timing Attack Defense", "Dummy Argon2id Execution", "Equalizes response latency on failed user lookups to stop enumeration"],
        ["Brute Force Mitigation", "SlidingWindowRateLimiter", "Restricts login attempts to 15/min and registration to 10/min per IP"],
        ["Session Tokens", "PyJWT (HS256 HMAC)", "Stateless 120-minute tokens with server-side blacklist revocation"],
        ["Access Control", "Resource Ownership Checks", "Strict token identity derivation prevents cross-account data leakage"],
        ["Data Minimization", "In-Memory Volatile RAM", "Zero persistent storage of raw SMS texts or unredacted URLs"],
        ["Consent Governance", "Granular Unbundled Audit", "Separate opt-in toggles for analysis, history, and caregiver sharing"]
    ]
    for r_idx, r_data in enumerate(tab_9_data):
        row = tab_9.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_9)

    add_heading_2(doc, "O. Database Implementation")
    add_body_p(doc, "Managed through SQLite3 (data/silvershield.db), the schema enforces foreign keys and cascade deletions across three tables: (1) users: Stores unique user ID, normalized email, Argon2id password hash, role (senior or caregiver), helper contact details, and timestamps. (2) consent_records: Stores unbundled consent preferences, policy version, and timestamped audit logs. (3) scan_history: Stores non-PII risk ratings, numerical risk scores, and threat indicator lists.")

    add_heading_2(doc, "P. Accessibility and Multilingual Support")
    add_body_p(doc, "SilverShield AI provides comprehensive localization across English, Hindi (हिन्दी), and Kannada (ಕನ್ನಡ) (frontend/locales.py). The audio narration engine (frontend/components.py) implements a resilient multi-tier strategy: (1) Dynamically queries browser speech synthesis voices for regional tags (kn-IN, hi-IN, en-IN); (2) If no regional voice object is installed in the local OS, sets utter.lang = 'kn-IN', directing Chromium/Edge engines to synthesize native neural cloud speech; (3) If local speech fails, automatically falls back to an online text-to-speech audio stream with anonymous headers; (4) Crucially, Kannada text is never fed to an English voice engine, preventing unintelligible audio output.")

    add_heading_2(doc, "Q. Technologies Used")
    add_body_p(doc, "The complete software technology stack is detailed in Table VI.")

    # TABLE II (placed here)
    add_table_caption(doc, "TABLE VI", "Complete Technology Stack of SilverShield AI")
    tab_2 = doc.add_table(rows=14, cols=3)
    tab_2.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_2_data = [
        ["Component Tier", "Technology / Framework", "Configured Version & Purpose"],
        ["Execution Runtime", "Python", "3.12+ (Core execution environment across all tiers)"],
        ["Frontend Dashboard", "Streamlit", "1.30.0+ (Reactive UI with custom CSS & HTML5 embeds)"],
        ["REST Web APIs", "FastAPI", "0.110.0+ (High-performance ASGI microservices)"],
        ["ASGI Application Server", "Uvicorn", "0.27.0+ (Hosting services on Ports 8000, 8001, 8002)"],
        ["Data Contract Validation", "Pydantic v2", "2.6.0+ (Strict schema validation and type boundaries)"],
        ["Machine Learning", "Scikit-Learn", "1.4.0+ (TF-IDF vectorizer, Logistic Regression, Naive Bayes)"],
        ["Model Persistence", "Joblib", "1.3.0+ (Binary serialization of fitted estimators)"],
        ["Data Processing", "Pandas & NumPy", "2.0+ / 1.24+ (Dataset curation, matrix computations)"],
        ["Password Hashing", "Argon2-cffi (Argon2id)", "23.1.0+ (OWASP memory-hard password hashing)"],
        ["Session Tokens", "PyJWT (HS256)", "2.9.0+ (Stateless tokens with blacklist revocation)"],
        ["Database Storage", "SQLite3", "Native (Local persistent relational database engine)"],
        ["Automated Testing", "Pytest", "8.0.0+ (Automated unit and integration test suite)"],
        ["Speech Narration", "Web Speech API", "HTML5 Native (Multi-tier English, Hindi, Kannada TTS)"]
    ]
    for r_idx, r_data in enumerate(tab_2_data):
        row = tab_2.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_2)

    # ----------------- SECTION V: RESULTS AND DISCUSSION -----------------
    add_heading_1(doc, "V. Results and Discussion")

    add_heading_2(doc, "A. Application Results")
    add_body_p(doc, "SilverShield AI was evaluated end-to-end across multiple execution environments. The application starts seamlessly via start_all.py or standalone service commands, delivering full protection within 2.5 seconds of launch. The assistive dashboard displays immediate live status indicators ('Central AI Security Engine: Online' or 'Local AI Security Engine: Active') and renders real-time responses with sub-100 ms latency.")

    add_heading_2(doc, "B. Machine Learning Model Evaluation")
    add_body_p(doc, "The machine learning classifiers were evaluated on the held-out test partition of 1,032 samples (904 legitimate, 128 scam) using stratified 5-fold cross-validation. Table VII specifies the hyperparameter configurations, and Table VIII summarizes the comparative performance metrics.")

    # TABLE IV
    add_table_caption(doc, "TABLE VII", "Machine Learning Model Hyperparameter Configurations")
    tab_4 = doc.add_table(rows=9, cols=2)
    tab_4.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_4_data = [
        ["Hyperparameter Attribute", "Configured Setting / Value"],
        ["TF-IDF N-gram Range", "(1, 2) (Unigrams + Bigrams)"],
        ["TF-IDF Sublinear TF", "True (1 + log(tf) scaling)"],
        ["TF-IDF Vocabulary Size", "5,000 maximum informative features"],
        ["TF-IDF Document Frequency", "min_df = 2, max_df = 0.95"],
        ["Train / Test Split Ratio", "80% Train (4,128 msgs), 20% Test (1,032 msgs)"],
        ["Logistic Regression Solver", "L-BFGS, max_iter = 1000, random_state = 42"],
        ["Logistic Regression Weights", "Balanced (class_weight='balanced')"],
        ["Multinomial Naive Bayes", "Laplace smoothing alpha = 0.1, fit_prior = True"]
    ]
    for r_idx, r_data in enumerate(tab_4_data):
        row = tab_4.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_4)

    # TABLE V
    add_table_caption(doc, "TABLE VIII", "Comparative Model Performance Metrics on Held-Out Test Set")
    tab_5 = doc.add_table(rows=15, cols=3)
    tab_5.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_5_data = [
        ["Evaluation Metric", "Logistic Regression (Champion)", "Multinomial Naive Bayes (Benchmark)"],
        ["Overall Test Accuracy", "98.06%", "98.26%"],
        ["Scam Precision", "90.91%", "98.25%"],
        ["Scam Recall", "93.75%", "87.50%"],
        ["Scam F1-Score", "92.31%", "92.56%"],
        ["Macro-Averaged F1", "95.60%", "95.79%"],
        ["ROC-AUC Discriminative Score", "0.9963", "0.9892"],
        ["True Positives (Scams Detected)", "120", "112"],
        ["False Negatives (Scams Missed)", "8", "16"],
        ["False Negative Rate (FNR)", "6.25%", "12.50%"],
        ["True Negatives (Legitimate Correct)", "892", "902"],
        ["False Positives (False Alarms)", "12", "2"],
        ["False Positive Rate (FPR)", "1.33%", "0.22%"],
        ["5-Fold CV Mean Accuracy", "98.33%", "98.74%"],
        ["5-Fold CV Mean Macro-F1", "96.14%", "97.02%"]
    ]
    for r_idx, r_data in enumerate(tab_5_data):
        row = tab_5.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_5)

    add_heading_2(doc, "C. Performance Metrics Analysis")
    add_body_p(doc, "While Multinomial Naive Bayes achieved a fractionally higher raw accuracy (98.26% vs 98.06%) and scam precision (98.25% vs 90.91%), Logistic Regression was explicitly selected as the Champion Model for SilverShield AI due to the following critical cybersecurity reasons:")
    add_body_p(doc, "1) Halving the False Negative Rate: In defensive cybersecurity for vulnerable seniors, a False Negative (failing to detect an actual scam) can lead to catastrophic financial ruin. Multinomial Naive Bayes missed 16 scams (FNR = 12.50%), whereas Logistic Regression missed only 8 scams (FNR = 6.25%). Logistic Regression caught 8 additional fraud attempts.")
    add_body_p(doc, "2) Superior ROC-AUC Discriminative Power: Logistic Regression achieved an exceptional ROC-AUC score of 0.9963 compared to 0.9892 for Naive Bayes, demonstrating near-perfect class separation across diverse decision thresholds.")
    add_body_p(doc, "3) Probabilistic Calibration and Explainability: Logistic Regression produces well-calibrated posterior probabilities and interpretable linear feature coefficients, allowing individual n-grams to be explained transparently to senior citizens.")

    add_heading_2(doc, "D. Comparative Model Evaluation Plots")
    add_body_p(doc, "Fig. 6 illustrates the comparative performance metrics across Accuracy, Recall, Precision, and F1-Score.")
    add_figure(doc, IMAGES_DIR / "model_comparison_chart.png", "Fig. 6. Comparative performance metrics between Logistic Regression (Champion) and Multinomial Naive Bayes across key evaluation dimensions.")

    add_body_p(doc, "Fig. 7 displays the confusion matrix and Receiver Operating Characteristic (ROC) curve for the Champion Logistic Regression model.")
    add_figure(doc, IMAGES_DIR / "confusion_matrix.png", "Fig. 7. Confusion Matrix for Logistic Regression on held-out test partition (1,032 samples) showing 892 TN, 12 FP, 8 FN, and 120 TP.")
    add_figure(doc, IMAGES_DIR / "roc_curve.png", "Fig. 8. Receiver Operating Characteristic (ROC) curve for Logistic Regression achieving near-ideal discriminative separation with AUC = 0.9963.")

    add_heading_2(doc, "E. Functional Testing")
    add_body_p(doc, "The system implementation was verified through an automated test suite comprising 162 passing tests executed via Pytest. Table IX highlights representative functional test scenarios.")

    # TABLE VIII
    add_table_caption(doc, "TABLE IX", "Representative Functional Test Scenarios and Verified Outcomes")
    tab_8 = doc.add_table(rows=9, cols=3)
    tab_8.alignment = WD_TABLE_ALIGNMENT.CENTER
    tab_8_data = [
        ["Test ID", "Input Test Condition", "Observed System Verification Output"],
        ["TC-01", "Benign family message ('Groceries at 6pm')", "Overall Risk: LOW (0 pts), routine advice rendered"],
        ["TC-02", "Urgent bank block alert with OTP request", "Overall Risk: HIGH (OVR-01, OVR-03), OTP action prioritized"],
        ["TC-03", "Delivery notice with shortened link (bit.ly)", "Overall Risk: MEDIUM (URL Shortener detected), link warning"],
        ["TC-04", "OTP request accompanied by external URL", "Forced HIGH via OVR-03 override, immediate alert"],
        ["TC-05", "ML microservice connection timeout simulation", "Graceful degradation: Status DEGRADED, risk floor MEDIUM"],
        ["TC-06", "Access to /api/v1/auth/me without JWT token", "HTTP 401 Unauthorized returned, access denied"],
        ["TC-07", "20 rapid login attempts from same IP address", "HTTP 429 Rate Limit Exceeded returned by sliding window"],
        ["TC-08", "Non-existent user email login attempt", "Generic error returned with dummy Argon2id timing defense"]
    ]
    for r_idx, r_data in enumerate(tab_8_data):
        row = tab_8.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(8.5)
                if r_idx == 0:
                    r.font.bold = True
    set_table_borders(tab_8)

    add_heading_2(doc, "F. URL Analysis Testing")
    add_body_p(doc, "The 9 heuristic inspection layers were validated against a benchmark battery of deceptive URLs. Target test cases included: (1) http://192.168.1.5/login triggered IP Address Host and Credential Path keywords, classified as MALICIOUS; (2) https://bit.ly/sbi-kyc triggered URL Shortener and Suspicious Keywords, classified as SUSPICIOUS; (3) http://sbi.verify.xyz triggered High-Risk TLD (.xyz) and Subdomain Depth, classified as MALICIOUS; (4) https://g00gle.com/secure triggered Brand Homoglyph and Path Keyword, classified as SUSPICIOUS; and (5) https://google.com/search triggered zero flags, correctly classified as SAFE.")

    add_heading_2(doc, "G. Application Screenshots and Interface Walkthrough")
    add_body_p(doc, "The application interface provides an intuitive experience designed specifically for senior citizens. Fig. 9 showcases representative views of the implemented system across its core functional modules: (a) Home Dashboard with 24/7 National Cyber Helpline (1930) banner; (b) Scam Message Detection Input with font scaling; (c) Prediction Result Card with multi-tier audio narrator; (d) 9-Layer URL Security Inspection results; (e) Unified Risk Score Gauge with plain-language action cards; and (f) Settings & Accessibility with WCAG AAA high-contrast toggle.")

    add_figure(doc, IMAGES_DIR / "ui_dashboard.png", "Fig. 9. SilverShield AI Assistive Application Interface Views illustrating the elderly-friendly UI, risk gauge, plain-language guidance, and regional language settings.")

    add_heading_2(doc, "H. Discussion and Limitations")
    add_body_p(doc, "While SilverShield AI successfully delivers high-recall scam detection, zero-request URL analysis, and tri-lingual speech narration, certain technical limitations exist: (1) Offline Model Weights: The Scikit-Learn models utilize static offline weights. The platform does not currently perform online continual learning from newly reported scam variants. (2) Text-Only Input Pipeline: Voice calls (vishing) and screenshot images of fraudulent messages require manual transcription or external Optical Character Recognition (OCR) prior to analysis. (3) Windows Sandbox Socket Isolation: In restricted Windows environments with loopback socket isolation, microservice REST communication requires elevated port permissions or automatic fallback to the local direct execution engine.")

    # ----------------- SECTION VI: CONCLUSION -----------------
    add_heading_1(doc, "VI. Conclusion")
    add_body_p(doc, "This paper presented the design, implementation, and empirical evaluation of SilverShield AI, a secure, privacy-preserving digital safety companion engineered for senior citizens. By combining a 4-tier microservice architecture with graceful in-process degradation, the system eliminates reliance on invasive contact-harvesting commercial filters. Machine learning evaluations demonstrated that Logistic Regression with sublinear TF-IDF achieves 98.06% accuracy and an ROC-AUC of 0.9963, halving missed scams compared to Naive Bayes. The 9-layer URL heuristic engine successfully identifies deceptive links without transmitting outbound requests to malicious domains. Integrated with Argon2id memory-hard authentication, anti-enumeration defenses, zero-raw-message database retention, tri-lingual localization (English, Hindi, Kannada), multi-tier speech narration, and direct 1930 National Cyber Helpline access, SilverShield AI delivers an accessible, robust defense empowering older adults to navigate digital spaces securely.")

    # ----------------- SECTION VII: FUTURE SCOPE -----------------
    add_heading_1(doc, "VII. Future Scope")
    add_body_p(doc, "Future research and engineering enhancements will focus on four strategic directions:")
    add_body_p(doc, "1) On-Device Android Background Listener: Packaging the lightweight TF-IDF classifier into an Android background daemon to intercept incoming smishing messages automatically without cloud transmission.")
    add_body_p(doc, "2) Embedded Optical Character Recognition (OCR): Integrating an on-device Tesseract OCR engine to scan and evaluate screenshots of WhatsApp and SMS messages directly.")
    add_body_p(doc, "3) Automated Push Escalation Gateway: Establishing an automated SMS/Push gateway to dispatch instant alert notifications to designated family caregivers upon detection of HIGH risk threats.")
    add_body_p(doc, "4) Expanded Linguistic Coverage: Extending speech and text localization to additional regional languages including Telugu, Tamil, Marathi, and Bengali.")

    # ----------------- SECTION VIII: REFERENCES -----------------
    add_heading_1(doc, "References")

    refs = [
        ("[1]", "D. Oliveira, H. Rocha, H. Yang, D. Ellis, S. Dommaraju, M. Muradoglu, D. Weir, A. Soliman, T. Lin, and N. Ebner, \"Dissecting spear phishing emails for older vs young adults: On the interplay of weapons of influence and life domains in predicting susceptibility to phishing,\" in Proc. 2017 CHI Conf. Hum. Factors Comput. Syst. (CHI '17), Denver, CO, USA, 2017, pp. 3412–3424, doi: 10.1145/3025453.3025831."),
        ("[2]", "Ö. K. Şahingöz, E. Buber, Ö. Demir, and B. Diri, \"Machine learning based phishing detection from URLs,\" Expert Systems with Applications, vol. 117, pp. 345–357, 2019, doi: 10.1016/j.eswa.2018.09.029."),
        ("[3]", "N. Capuano, G. Fenza, V. Loia, and C. Stanzione, \"Explainable Artificial Intelligence in CyberSecurity: A Survey,\" IEEE Access, vol. 10, pp. 93575–93600, 2022, doi: 10.1109/ACCESS.2022.3204171."),
        ("[4]", "T. A. Almeida, J. M. Gómez Hidalgo, and A. Yamakami, \"Contributions to the Study of SMS Spam Filtering: New Collection and Results,\" in Proc. 2011 ACM Symp. Document Engineering (DocEng '11), Mountain View, CA, USA, 2011, pp. 259–262, doi: 10.1145/2034691.2034742.")
    ]

    for num, cit in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        p_ref.paragraph_format.space_before = Pt(1)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.05
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_num = p_ref.add_run(f"{num} ")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(8.5)
        r_num.font.bold = True
        r_cit = p_ref.add_run(cit)
        r_cit.font.name = 'Times New Roman'
        r_cit.font.size = Pt(8.5)

    doc.save(str(DOCX_OUTPUT))
    print(f"Successfully generated editable Word document: {DOCX_OUTPUT}")

if __name__ == "__main__":
    build_paper()
