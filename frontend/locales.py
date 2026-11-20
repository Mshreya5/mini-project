"""
SilverShield AI - Comprehensive Multilingual Translation System
Languages supported: English, Hindi (हिन्दी), Kannada (ಕನ್ನಡ)
Covers all UI navigation, headings, buttons, alerts, quiz, safety guides,
and dynamic mapping of backend ML and URL security analysis results.
"""

from typing import Any, Dict, List

LANGUAGES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Kannada": "kn-IN"
}

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "English": {
        "app_title": "SilverShield AI",
        "app_tagline": "AI-Powered Cyber Protection for Seniors & Families",
        "system_status_live": "Central AI Security Engine: Online",
        "system_status_fallback": "Local AI Security Engine: Active",
        
        "nav_dashboard": "Home Dashboard",
        "nav_message_checker": "Scam Message Detector",
        "nav_url_checker": "URL Safety Checker",
        "nav_awareness": "Security Awareness Centre",
        "nav_safety_guide": "Elderly Safety Guide & Quiz",
        "nav_settings": "Settings & Accessibility",
        "nav_account": "Account & Security",
        
        "sidebar_language_label": "Select Language",
        "sidebar_quick_helpline": "Emergency Cyber Helpline: 1930 (Toll-Free, 24x7)",
        "sidebar_disclaimer": "SilverShield AI is an assistive digital safety companion designed to protect seniors from digital fraud.",
        
        "dash_hero_badge": "Next-Gen AI Cyber Protection",
        "dash_hero_title": "Stay Protected Against Digital Fraud & Scams",
        "dash_hero_sub": "SilverShield AI uses machine learning and multi-layer URL security analysis to detect fraud, verify suspicious links, and protect seniors from financial harm.",
        "dash_stat_protection": "Real-Time AI Scan",
        "dash_stat_protection_sub": "Dual-layer Scam & Link Check",
        "dash_stat_helpline": "National Cyber Helpline",
        "dash_stat_helpline_sub": "Dial 1930 for Immediate Help",
        "dash_stat_privacy": "Privacy-First Architecture",
        "dash_stat_privacy_sub": "No Private Message Storage",
        
        "dash_actions_heading": "Core Protection Features",
        "dash_action_msg_title": "Scam Message Detector",
        "dash_action_msg_desc": "Scan suspicious WhatsApp texts, bank alerts, electricity notices, or lottery claims using machine learning.",
        "dash_action_msg_btn": "Analyze Message",
        "dash_action_url_title": "URL Safety Checker",
        "dash_action_url_desc": "Inspect unfamiliar web links for phishing traps, malicious domains, and disguise tricks.",
        "dash_action_url_btn": "Check URL",
        "dash_action_risk_title": "Unified Risk Assessment",
        "dash_action_risk_desc": "Combines message semantics and hyperlink security into an instant, calibrated 0–100 threat score.",
        "dash_action_risk_btn": "Learn Scoring",
        "dash_action_aware_title": "Security Awareness & Safety",
        "dash_action_aware_desc": "Learn about OTP traps, fake calls, and quiz yourself on modern cyber threats.",
        "dash_action_aware_btn": "View Guides & Quiz",
        
        "dash_tip_badge": "Daily Safety Tip",
        "dash_tip_title": "Security Tip of the Day",
        "dash_tip_next_btn": "Show Another Tip",
        
        "dash_rules_heading": "The 3 Golden Rules of Digital Safety",
        "rule_1_title": "Never Share Your OTP or PIN",
        "rule_1_desc": "Your bank, government agencies, and police will NEVER ask for an OTP, UPI PIN, or card password.",
        "rule_2_title": "Never Rush Under Pressure",
        "rule_2_desc": "Fraudsters create artificial urgency with threats of power cuts, sim blocking, or police arrest. Always pause.",
        "rule_3_title": "Consult a Family Helper or Call 1930",
        "rule_3_desc": "When uncertain, show the message to your trusted caregiver or dial the 1930 national cyber fraud helpline.",

        "msg_title": "Scam Message Detector",
        "msg_subtitle": "Paste any suspicious SMS, WhatsApp message, email excerpt, or customer care chat to detect fraud patterns.",
        "msg_input_label": "Paste your message here:",
        "msg_input_placeholder": "Example: Urgent! Your SBI NetBanking is suspended due to expired KYC. Update immediately at http://bit.ly/sbi-kyc-verify...",
        "msg_btn_analyze": "Analyze Message Safety",
        "msg_btn_clear": "Clear Input",
        "msg_btn_narrate": "Listen to Result (Read Aloud)",
        "msg_sample_label": "Try real-world example messages:",
        "sample_sbi": "Bank KYC Suspension Scam",
        "sample_power": "Electricity Disconnection Scam",
        "sample_otp": "Fake Executive OTP Request",
        "sample_job": "Part-Time Job / WFH Offer Scam",
        "sample_legit": "Legitimate Family Message",
        
        "res_heading": "AI Threat Assessment Result",
        "res_risk_level": "Overall Risk Level",
        "res_risk_score": "Risk Score",
        "res_confidence": "Model Confidence",
        "res_scam_prob": "Scam Probability",
        "res_prediction": "ML Classification",
        "res_url_risk": "Embedded Link Risk",
        "res_explanation_title": "AI Explainability & Reasoning",
        "res_indicators_title": "Detected Threat Indicators",
        "res_actions_title": "Recommended Immediate Actions",
        "res_tech_details": "View Technical Breakdown (For Evaluators & Caregivers)",
        "res_caregiver_share": "Alert Trusted Helper on WhatsApp",
        "res_caregiver_notice": "Note: Clicking this button opens WhatsApp with a prefilled alert message. You can review it before sending.",
        "res_no_indicators": "No adverse threat patterns detected in this message.",
        "res_input_required": "Please type or paste a message to analyze.",
        
        "url_title": "URL Safety Checker",
        "url_subtitle": "Analyze web links, shortened URLs, and suspicious domains for phishing attacks, brand impersonation, and security flaws.",
        "url_input_label": "Enter Website Address or Link:",
        "url_input_placeholder": "https://example-bank-login.xyz/verify or http://bit.ly/update-now",
        "url_btn_analyze": "Check Link Safety",
        "url_btn_clear": "Clear URL",
        "url_sample_label": "Try sample test links:",
        "url_sample_phish": "Phishing Lookalike Link",
        "url_sample_short": "Shortened Bit.ly Link",
        "url_sample_ip": "Raw IP Address Link",
        "url_sample_safe": "Official Verified Bank URL",
        "url_res_heading": "URL Security Inspection Results",
        "url_res_status": "URL Classification",
        "url_res_domain": "Target Domain / Host",
        "url_res_https": "Secure Connection (HTTPS)",
        "url_res_explanation": "Security Explanation",
        "url_res_indicators": "URL Risk Indicators",
        "url_input_required": "Please enter a valid web link starting with http:// or https://",
        
        "aware_title": "Security Awareness Centre",
        "aware_subtitle": "Learn how modern cyber criminals target senior citizens and how you can spot their schemes effortlessly.",
        "aware_tab_scams": "Common Scams Breakdown",
        "aware_tab_library": "Scam Message Library",
        "aware_tab_prevention": "Practical Prevention Checklist",
        
        "scam_otp_title": "1. OTP & 2FA Harvesting Scams",
        "scam_otp_desc": "Fraudsters pose as bank officers, telecom staff, or courier agents asking for the 6-digit SMS code to cancel an unauthorized charge. Never share OTPs.",
        "scam_bank_title": "2. Bank KYC & Account Freeze Traps",
        "scam_bank_desc": "Messages threatening that your bank account, debit card, or PAN has been blocked and requesting you to update your details on a fake website.",
        "scam_lottery_title": "3. Lottery, Prize & Cashback Scams",
        "scam_lottery_desc": "Notices claiming you won ₹25 Lakhs in KBC, a lucky draw, or an income tax refund, requiring a small processing fee to release funds.",
        "scam_job_title": "4. Fake Job & YouTube Likes Scams",
        "scam_job_desc": "Unsolicited offers promising ₹2,000–₹5,000 daily for liking YouTube videos or completing Google reviews, eventually trapping victims into Ponzi schemes.",
        "scam_digital_arrest_title": "5. The 'Digital Arrest' Video Call Scam",
        "scam_digital_arrest_desc": "Scammers disguise as police or CBI over Skype/WhatsApp video calls, accusing you of receiving illegal parcels and demanding bail money.",
        "scam_remote_title": "6. Remote Desktop Screen Sharing Traps",
        "scam_remote_desc": "A caller instructs you to install AnyDesk, TeamViewer, or QuickSupport to 'assist' you. Once installed, they take complete control of your banking.",
        
        "guide_title": "Elderly Digital Safety Guide & Quiz",
        "guide_subtitle": "Practical emergency instructions, official cyber crime reporting procedures, and an interactive quiz to test your vigilance.",
        "guide_tab_rules": "Safety Rules & Guidelines",
        "guide_tab_emergency": "Emergency Steps: What to Do",
        "guide_tab_quiz": "Scam Awareness Quiz",
        
        "emer_step1_title": "Scenario A: If you clicked a suspicious link",
        "emer_step1_desc": "1. Immediately close the browser tab or app.\n2. Do NOT enter any passwords, PINs, or personal details.\n3. Disconnect your phone from Wi-Fi and mobile data temporarily.\n4. Run a device security scan and restart your phone.",
        "emer_step2_title": "Scenario B: If you accidentally shared an OTP or password",
        "emer_step2_desc": "1. Immediately call your bank's official toll-free card blocking number.\n2. Lock your net banking and mobile banking app via official portal.\n3. Change your net banking passwords from a separate trusted device.\n4. Inform your family helper immediately.",
        "emer_step3_title": "Scenario C: If money was unauthorizedly debited",
        "emer_step3_desc": "1. Immediately dial 1930 (National Cyber Crime Helpline) within the 'Golden Hour' to freeze fraudulent bank transfers.\n2. File a formal complaint at https://cybercrime.gov.in.\n3. Take screenshots of the fraudulent SMS, transaction ID, and phone numbers.\n4. Visit your nearest bank branch to submit a written fraud intimation.",
        
        "set_title": "Settings & Accessibility",
        "set_subtitle": "Tailor the interface for comfortable reading, high contrast viewing, and trusted caregiver alerts.",
        "set_font_size_label": "Reading Text Size",
        "set_font_standard": "Compact (14px)",
        "set_font_large": "Standard (15px)",
        "set_font_xlarge": "Large (17px)",
        "set_contrast_label": "High Contrast Mode (WCAG AAA)",
        "set_contrast_desc": "Switches to high-contrast deep palette with vivid borders for optimal readability.",
        "set_helper_heading": "Trusted Helper (Caregiver) Setup",
        "set_helper_desc": "Store your family member's contact so you can send them one-click alerts when you spot a suspicious message.",
        "set_helper_name": "Caregiver / Helper Name",
        "set_helper_relation": "Relationship (e.g., Son, Daughter, Grandchild)",
        "set_helper_phone": "WhatsApp / Phone Number (Include Country Code, e.g., 919876543210)",
        "set_helper_save_btn": "Save Caregiver Details",
        "set_helper_saved_msg": "Caregiver information successfully saved for this session.",
        "set_history_heading": "Session Analysis History",
        "set_history_desc": "View scans performed during this active session. No private message data is stored permanently on disk.",
        "set_history_clear_btn": "Clear History",
        "set_history_empty": "No analysis history in this session yet.",
        "set_history_cleared": "Session scan history cleared.",
        "set_reset_btn": "Restore Default Settings",
        "set_reset_success": "Accessibility settings restored to defaults.",
        
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "btn_submit": "Submit",
        "btn_close": "Close",
        "btn_view": "View Details",
        "btn_copy": "Copy",
        
        "quiz_title": "Test Your Scam Awareness",
        "quiz_subtitle": "Answer 4 quick scenarios to see how well you can detect fraudulent messages and traps.",
        "quiz_score_prefix": "Your Score:",
        "quiz_btn_check": "Check Answer",
        "quiz_btn_reset": "Retake Quiz",
        "quiz_correct": "Correct! Excellent vigilance.",
        "quiz_incorrect": "Incorrect. Be careful with this pattern.",
        "quiz_q1": "You receive an SMS: 'Dear SBI user, your account will be blocked in 2 hours. Click http://bit.ly/sbi-kyc to update PAN.' What should you do?",
        "quiz_q1_o1": "Click the link immediately so account is not blocked",
        "quiz_q1_o2": "Delete the message and verify only through official YONO app or bank branch",
        "quiz_q1_o3": "Forward the message to all your friends to warn them",
        "quiz_q1_exp": "Banks NEVER send shortened links (like bit.ly) or threaten 2-hour account blocks. Always check directly via your bank branch or official app.",
        "quiz_q2": "A polite caller claims to be a bank officer and says: 'To reverse a wrong charge of ₹12,000, please tell me the 6-digit OTP you just received.' What do you do?",
        "quiz_q2_o1": "Share the OTP since they want to help cancel the debit",
        "quiz_q2_o2": "Never share the OTP under any circumstance and hang up",
        "quiz_q2_o3": "Ask them to call back in 10 minutes",
        "quiz_q2_exp": "An OTP is like your signature. Sharing an OTP allows the scammer to finalize an unauthorized transaction.",
        "quiz_q3": "You receive a WhatsApp video call from a person dressed in a police uniform who says you are placed under 'Digital Arrest' for a package with contraband. What should you do?",
        "quiz_q3_o1": "Stay on the call and transfer money for bail as instructed",
        "quiz_q3_o2": "Disconnect immediately and report the number to 1930 / cybercrime.gov.in",
        "quiz_q3_o3": "Send your Aadhaar card and PAN card to prove your innocence",
        "quiz_q3_exp": "There is NO legal concept of 'Digital Arrest' in India. Police and courts NEVER arrest or hold trials over WhatsApp video calls.",
        "quiz_q4": "A message offers a part-time job earning ₹3,000/day just for giving 5-star reviews to hotels on Google Maps. Is this safe?",
        "quiz_q4_o1": "Yes, it is easy extra income with no risk",
        "quiz_q4_o2": "No, it is a task-based investment scam designed to steal your savings",
        "quiz_q4_o3": "Yes, as long as you use a spare bank account",
        "quiz_q4_exp": "These 'task scams' pay small amounts initially (₹100–₹500) to gain trust, then trick victims into depositing lakhs into fake investment portals."
    },
    
    "Hindi": {
        "app_title": "सिल्वरशील्ड AI",
        "app_tagline": "बुजुर्गों एवं परिवारों के लिए AI-संचालित साइबर सुरक्षा कवच",
        "system_status_live": "केंद्रीय AI सुरक्षा प्रणाली: ऑनलाइन",
        "system_status_fallback": "स्थानीय AI सुरक्षा प्रणाली: सक्रिय",
        
        "nav_dashboard": "मुख्य डैशबोर्ड",
        "nav_message_checker": "संदेश धोखाधड़ी जाँच",
        "nav_url_checker": "वेबसाइट लिंक जाँच",
        "nav_awareness": "सुरक्षा जागरूकता केंद्र",
        "nav_safety_guide": "सुरक्षा गाइड एवं प्रश्नोत्तरी",
        "nav_settings": "सेटिंग्स एवं सुगमता",
        "nav_account": "खाता एवं सुरक्षा",
        
        "sidebar_language_label": "भाषा चुनें",
        "sidebar_quick_helpline": "राष्ट्रीय साइबर हेल्पलाइन: 1930 (टोल-फ्री, 24x7)",
        "sidebar_disclaimer": "सिल्वरशील्ड AI बुजुर्गों को ऑनलाइन धोखाधड़ी और साइबर अपराध से बचाने हेतु एक डिजिटल सुरक्षा सहायक है।",
        
        "dash_hero_badge": "आधुनिक AI साइबर सुरक्षा",
        "dash_hero_title": "ऑनलाइन धोखाधड़ी और घोटालों से सुरक्षित रहें",
        "dash_hero_sub": "सिल्वरशील्ड AI मशीन लर्निंग और बहुस्तरीय लिंक विश्लेषण का उपयोग करके संदेहास्पद संदेशों और फर्जी वेबसाइटों से बुजुर्गों की सुरक्षा करता है।",
        "dash_stat_protection": "रीयल-टाइम AI जाँच",
        "dash_stat_protection_sub": "संदेश एवं लिंक सुरक्षा जाँच",
        "dash_stat_helpline": "राष्ट्रीय हेल्पलाइन",
        "dash_stat_helpline_sub": "तुरंत मदद के लिए 1930 डायल करें",
        "dash_stat_privacy": "पूर्णतः गोपनीय प्रणाली",
        "dash_stat_privacy_sub": "संदेशों का कोई स्थायी भंडारण नहीं",
        
        "dash_actions_heading": "प्रमुख सुरक्षा सुविधाएँ",
        "dash_action_msg_title": "संदेश धोखा पहचान",
        "dash_action_msg_desc": "संदिग्ध WhatsApp संदेश, बैंक चेतावनी, बिजली बिल कटने की धमकी या लॉटरी संदेशों की सुरक्षा परखें।",
        "dash_action_msg_btn": "संदेश जाँचें",
        "dash_action_url_title": "वेबसाइट लिंक सुरक्षा जाँच",
        "dash_action_url_desc": "अपरिचित लिंक, फर्जी बैंक वेबसाइट, शॉर्ट लिंक एवं खतरनाक वेब पतों की जाँच करें।",
        "dash_action_url_btn": "लिंक जाँचें",
        "dash_action_risk_title": "सटीक जोखिम मूल्यांकन",
        "dash_action_risk_desc": "संदेश भाषा और वेब लिंक दोनों का संयुक्त 0–100 साइबर खतरा स्कोर प्रदान करता है।",
        "dash_action_risk_btn": "जोखिम प्रणाली देखें",
        "dash_action_aware_title": "सुरक्षा जागरूकता एवं सुझाव",
        "dash_action_aware_desc": "ओटीपी धोखाधड़ी, फर्जी कॉल और डिजिटल अरेस्ट से बचने के उपाय और क्विज़ देखें।",
        "dash_action_aware_btn": "जागरूकता केंद्र खोलें",
        
        "dash_tip_badge": "आज का सुरक्षा सुझाव",
        "dash_tip_title": "दैनिक साइबर सुरक्षा सलाह",
        "dash_tip_next_btn": "दूसरा सुझाव देखें",
        
        "dash_rules_heading": "डिजिटल सुरक्षा के 3 सुनहरे नियम",
        "rule_1_title": "अपना OTP या PIN कभी किसी को न दें",
        "rule_1_desc": "आपका बैंक, पुलिस या कोई भी सरकारी संस्था कभी भी फोन या SMS पर OTP या पासवर्ड नहीं मांगती।",
        "rule_2_title": "जल्दबाजी या डर में कोई कदम न उठाएं",
        "rule_2_desc": "धोखेबाज बिजली कटने, सिम बंद होने या गिरफ्तारी का डर दिखाकर घबराहट पैदा करते हैं। हमेशा शांत रहें।",
        "rule_3_title": "परिवार के सदस्य से पूछें या 1930 पर कॉल करें",
        "rule_3_desc": "संदेह होने पर तुरंत अपने भरोसेमंद स्वजन को दिखाएं अथवा 1930 साइबर हेल्पलाइन पर सहायता लें।",

        "msg_title": "संदेश धोखाधड़ी जाँच (Scam Detector)",
        "msg_subtitle": "कोई भी संदिग्ध SMS, WhatsApp संदेश या ईमेल यहाँ पेस्ट करें। हमारी AI प्रणाली खतरे का विश्लेषण करेगी।",
        "msg_input_label": "अपना संदेश यहाँ दर्ज करें:",
        "msg_input_placeholder": "उदाहरण: तुरंत ध्यान दें! आपका बैंक खाता KYC न होने के कारण आज बंद कर दिया जाएगा। पुनः सक्रिय करने हेतु http://bit.ly/sbi-kyc पर क्लिक करें...",
        "msg_btn_analyze": "संदेश की सुरक्षा जाँचे",
        "msg_btn_clear": "हटाएं",
        "msg_btn_narrate": "परिणाम बोलकर सुनें (Read Aloud)",
        "msg_sample_label": "उदाहरण संदेश चुनकर परखें:",
        "sample_sbi": "बैंक KYC निलंबन घोटाला",
        "sample_power": "बिजली बिल डिस्कनेक्शन घोटाला",
        "sample_otp": "फर्जी बैंक अधिकारी द्वारा OTP मांग",
        "sample_job": "घर बैठे नौकरी / पार्ट-टाइम जॉब झांसा",
        "sample_legit": "सामान्य पारिवारिक संदेश",
        
        "res_heading": "AI सुरक्षा जाँच परिणाम",
        "res_risk_level": "कुल जोखिम स्तर",
        "res_risk_score": "जोखिम स्कोर",
        "res_confidence": "मॉडल विश्वसनीयता",
        "res_scam_prob": "धोखाधड़ी संभावना",
        "res_prediction": "ML वर्गीकरण",
        "res_url_risk": "संदेश में शामिल लिंक का जोखिम",
        "res_explanation_title": "AI व्याख्या एवं कारण",
        "res_indicators_title": "पहचाने गए संदिग्ध खतरे के संकेत",
        "res_actions_title": "तुरंत क्या सावधानी बरतें?",
        "res_tech_details": "तकनीकी विवरण देखें (मूल्यांकन एवं सहायकों हेतु)",
        "res_caregiver_share": "WhatsApp द्वारा भरोसेमंद स्वजन को सूचित करें",
        "res_caregiver_notice": "सूचना: यह बटन दबाने पर WhatsApp में पहले से लिखा संदेश खुलेगा जिसे आप देखकर भेज सकते हैं।",
        "res_no_indicators": "इस संदेश में कोई प्रतिकूल या संदेहास्पद संकेत नहीं मिला।",
        "res_input_required": "कृपया जाँच के लिए कोई संदेश टाइप या पेस्ट करें।",
        
        "url_title": "वेबसाइट लिंक सुरक्षा जाँच",
        "url_subtitle": "किसी भी संदिग्ध वेबसाइट पते, शॉर्ट लिंक या फ़िशिंग लिंक की सुरक्षा स्थिति तुरंत जांचें।",
        "url_input_label": "वेबसाइट लिंक (URL) दर्ज करें:",
        "url_input_placeholder": "https://example-bank-login.xyz/verify अथवा http://bit.ly/update-now",
        "url_btn_analyze": "लिंक की सुरक्षा जाँचे",
        "url_btn_clear": "हटाएं",
        "url_sample_label": "परीक्षण हेतु नमूना लिंक:",
        "url_sample_phish": "फ़िशिंग फर्जी बैंक लिंक",
        "url_sample_short": "छुपा हुआ शॉर्ट लिंक (bit.ly)",
        "url_sample_ip": "असुरक्षित IP एड्रेस लिंक",
        "url_sample_safe": "आधिकारिक सुरक्षित बैंक लिंक",
        "url_res_heading": "लिंक सुरक्षा विश्लेषण परिणाम",
        "url_res_status": "लिंक स्थिति",
        "url_res_domain": "वेबसाइट डोमेन",
        "url_res_https": "सुरक्षित कनेक्शन (HTTPS)",
        "url_res_explanation": "सुरक्षा व्याख्या",
        "url_res_indicators": "लिंक में मिले खतरे के संकेत",
        "url_input_required": "कृपया http:// या https:// से शुरू होने वाला एक मान्य वेब लिंक दर्ज करें।",
        
        "aware_title": "सुरक्षा जागरूकता केंद्र",
        "aware_subtitle": "साइबर अपराधी बुजुर्गों को कैसे निशाना बनाते हैं, उनके तौर-तरीकों को समझें और खुद को सुरक्षित रखें।",
        "aware_tab_scams": "प्रमुख घोटालों की जानकारी",
        "aware_tab_library": "धोखाधड़ी संदेशों का संग्रह",
        "aware_tab_prevention": "सुरक्षा उपाय चेकलिस्ट",
        
        "scam_otp_title": "1. OTP और पासवर्ड चोरी का घोटाला",
        "scam_otp_desc": "धोखेबाज बैंक अधिकारी या पार्सल डिलीवरी एजेंट बनकर फोन करते हैं और गलत ट्रांजेक्शन रद्द करने के बहाने 6-अंकों का OTP मांगते हैं। कभी OTP न बताएं।",
        "scam_bank_title": "2. बैंक KYC और खाता बंद होने की धमकी",
        "scam_bank_desc": "SMS भेजते हैं कि आपका खाता या पैन कार्ड ब्लॉक हो गया है और तुरंत दिए गए लिंक पर अपनी जानकारी दर्ज करें। बैंक कभी ऐसे लिंक नहीं भेजते।",
        "scam_lottery_title": "3. लॉटरी, इनाम और कैशबैक का झांसा",
        "scam_lottery_desc": "KBC या लकी ड्रा में 25 लाख जीतने का झूठा संदेश भेजकर प्रोसेसिंग फीस के नाम पर पहले पैसे ऐंठ लेते हैं।",
        "scam_job_title": "4. घर बैठे यूट्यूब लाइक जॉब का लालच",
        "scam_job_desc": "वीडियो लाइक करने या होटल रिव्यू लिखने के बदले रोज 2,000–5,000 रुपये देने का वादा करके बाद में बड़े फर्जी निवेश में फंसा लेते हैं।",
        "scam_digital_arrest_title": "5. 'डिजिटल अरेस्ट' फर्जी वीडियो कॉल",
        "scam_digital_arrest_desc": "धोखेबाज पुलिस या CBI की वर्दी पहनकर वीडियो कॉल करते हैं, गैर-कानूनी पार्सल का झूठा आरोप लगाते हैं और जमानत के नाम पर पैसे ट्रांसफर करवाते हैं।",
        "scam_remote_title": "6. रिमोट कंट्रोल ऐप (AnyDesk) का जाल",
        "scam_remote_desc": "तकनीकी मदद के बहाने AnyDesk या TeamViewer ऐप डाउनलोड करवाते हैं। ऐप इंस्टॉल होते ही वे आपका पूरा फोन और बैंक खाते देख लेते हैं।",
        
        "guide_title": "वरिष्ठ नागरिक सुरक्षा गाइड एवं प्रश्नोत्तरी",
        "guide_subtitle": "आपातकालीन कदम, साइबर अपराध की आधिकारिक रिपोर्टिंग प्रक्रिया और अपनी सतर्कता परखने हेतु प्रश्नोत्तरी।",
        "guide_tab_rules": "महत्वपूर्ण सुरक्षा नियम",
        "guide_tab_emergency": "आपातकालीन स्थिति में क्या करें",
        "guide_tab_quiz": "साइबर सुरक्षा प्रश्नोत्तरी",
        
        "emer_step1_title": "स्थिति A: यदि आपने किसी संदिग्ध लिंक पर क्लिक कर दिया",
        "emer_step1_desc": "1. तुरंत उस ब्राउज़र या पेज को बंद कर दें।\n2. उस पेज पर कोई भी पासवर्ड, PIN या व्यक्तिगत जानकारी न भरें।\n3. फोन का मोबाइल डेटा और वाई-फाई तुरंत बंद करें।\n4. फोन को एंटीवायरस से स्कैन करें और रीस्टार्ट करें।",
        "emer_step2_title": "स्थिति B: यदि आपने गलती से OTP या पासवर्ड बता दिया",
        "emer_step2_desc": "1. तुरंत अपने बैंक के आधिकारिक टोल-फ्री नंबर पर फोन करके कार्ड व नेट बैंकिंग ब्लॉक करवाएं।\n2. बैंक ऐप में लॉगिन करके कार्ड लॉक करें।\n3. किसी दूसरे सुरक्षित फोन से नेट बैंकिंग का पासवर्ड तुरंत बदलें।\n4. परिवार के सदस्य को तुरंत जानकारी दें।",
        "emer_step3_title": "स्थिति C: यदि आपके बैंक खाते से पैसे कट गए",
        "emer_step3_desc": "1. बिना देरी किए 'गोल्डन ऑवर' में तुरंत 1930 राष्ट्रीय साइबर हेल्पलाइन पर कॉल करें ताकि ट्रांसफर फ्रीज हो सके।\n2. आधिकारिक पोर्टल https://cybercrime.gov.in पर शिकायत दर्ज करें।\n3. फर्जी SMS, बैंक स्टेटमेंट और कॉल रिकॉर्ड के स्क्रीनशॉट सुरक्षित रखें।\n4. अपनी नजदीकी बैंक शाखा में जाकर लिखित शिकायत दें।",
        
        "set_title": "सेटिंग्स एवं सुगमता (Accessibility)",
        "set_subtitle": "अक्षरों का आकार, हाई कंट्रास्ट रंग एवं परिवार के सहायक के संपर्क का प्रबंधन करें।",
        "set_font_size_label": "पढ़ने के लिए अक्षरों का आकार",
        "set_font_standard": "संक्षिप्त (14px)",
        "set_font_large": "सामान्य (15px)",
        "set_font_xlarge": "बड़ा (17px)",
        "set_contrast_label": "हाई कंट्रास्ट मोड (WCAG AAA)",
        "set_contrast_desc": "कमजोर दृष्टि के लिए गहरे रंग और स्पष्ट बॉर्डर के साथ अत्यधिक पठनीय रूपरेखा।",
        "set_helper_heading": "भरोसेमंद सहायक (केयरगिवर) की जानकारी",
        "set_helper_desc": "अपने परिवार के किसी सदस्य का विवरण सुरक्षित रखें ताकि संदिग्ध संदेश दिखने पर एक क्लिक में उन्हें सतर्क कर सकें।",
        "set_helper_name": "सहायक / स्वजन का नाम",
        "set_helper_relation": "संबंध (जैसे बेटा, बेटी, पोता)",
        "set_helper_phone": "WhatsApp / फोन नंबर (देश कोड सहित, जैसे 919876543210)",
        "set_helper_save_btn": "विवरण सुरक्षित करें",
        "set_helper_saved_msg": "सहायक का विवरण सफलतापूर्वक सहेज लिया गया।",
        "set_history_heading": "सत्र जाँच इतिहास (Session History)",
        "set_history_desc": "इस सत्र में जाँचे गए संदेशों व लिंक की सूची। आपकी कोई भी गोपनीय जानकारी स्थायी रूप से जमा नहीं की जाती।",
        "set_history_clear_btn": "इतिहास साफ़ करें",
        "set_history_empty": "इस सत्र में अभी तक कोई जाँच नहीं की गई है।",
        "set_history_cleared": "जाँच इतिहास हटा दिया गया।",
        "set_reset_btn": "डिफ़ॉल्ट सेटिंग्स पुनर्स्थापित करें",
        "set_reset_success": "सभी सेटिंग्स सामान्य स्थिति में रीसेट कर दी गईं।",
        
        "btn_save": "सहेजें",
        "btn_cancel": "रद्द करें",
        "btn_submit": "जमा करें",
        "btn_close": "बंद करें",
        "btn_view": "विवरण देखें",
        "btn_copy": "कॉपी करें",
        
        "quiz_title": "अपनी साइबर सुरक्षा सतर्कता परखें",
        "quiz_subtitle": "4 आसान सवालों के जवाब देकर जानें कि क्या आप ऑनलाइन धोखाधड़ी की चालों को पहचान सकते हैं।",
        "quiz_score_prefix": "आपका स्कोर:",
        "quiz_btn_check": "उत्तर जाँचे",
        "quiz_btn_reset": "प्रश्नोत्तरी पुनः दें",
        "quiz_correct": "शाबाश! सही उत्तर। आपकी सतर्कता सराहनीय है।",
        "quiz_incorrect": "यह उत्तर गलत है। कृपया सतर्क रहें।",
        "quiz_q1": "आपको संदेश आता है: 'SBI ग्राहक ध्यान दें! आपका खाता 2 घंटे में बंद हो जाएगा। पैन अपडेट करने हेतु http://bit.ly/sbi-kyc खोलें।' आपको क्या करना चाहिए?",
        "quiz_q1_o1": "तुरंत लिंक खोलकर जानकारी भरें ताकि खाता चालू रहे",
        "quiz_q1_o2": "संदेश को तुरंत मिटा दें और केवल आधिकारिक ऐप या बैंक शाखा से ही जानकारी लें",
        "quiz_q1_o3": "यह संदेश अपने सभी मित्रों को फॉरवर्ड कर दें",
        "quiz_q1_exp": "बैंक कभी भी bit.ly जैसे छोटे लिंक नहीं भेजते और न ही 2 घंटे में खाता बंद करने की धमकी देते हैं।",
        "quiz_q2": "फोन पर एक व्यक्ति बैंक अधिकारी बनकर कहता है: 'आपके खाते से गलती से 12,000 कट गए हैं, इसे वापस पाने के लिए फोन पर आया 6 अंकों का OTP बताएं।' क्या करेंगे?",
        "quiz_q2_o1": "पैसे वापस पाने के लिए तुरंत OTP बता देंगे",
        "quiz_q2_o2": "किसी भी स्थिति में OTP नहीं बताएंगे और तुरंत फोन काट देंगे",
        "quiz_q2_o3": "उन्हें 10 मिनट बाद फोन करने को कहेंगे",
        "quiz_q2_exp": "OTP आपके डिजिटल हस्ताक्षर जैसा है। OTP बताते ही धोखेबाज आपके खाते से पैसे निकाल लेते हैं। बैंक कभी OTP नहीं मांगता।",
        "quiz_q3": "पुलिस की वर्दी पहने व्यक्ति का WhatsApp वीडियो कॉल आता है और वह कहता है कि आप पर 'डिजिटल अरेस्ट' लगाया गया है। आपको क्या करना चाहिए?",
        "quiz_q3_o1": "डरे हुए रहकर उनके बताए खाते में जमानत के पैसे भेज दें",
        "quiz_q3_o2": "तुरंत कॉल काटें और 1930 पर या cybercrime.gov.in पर रिपोर्ट करें",
        "quiz_q3_o3": "निर्दोष साबित करने के लिए अपना आधार और पैन कार्ड भेजें",
        "quiz_q3_exp": "भारत में 'डिजिटल अरेस्ट' नाम का कोई कानून नहीं है। पुलिस कभी WhatsApp वीडियो कॉल पर गिरफ्तारी नहीं करती।",
        "quiz_q4": "घर बैठे Google रिव्यू लिखने पर रोजाना 3,000 रुपये देने का WhatsApp ऑफर आता है। क्या यह सुरक्षित है?",
        "quiz_q4_o1": "हाँ, बिना मेहनत के अतिरिक्त पैसे कमाने का अच्छा जरिया है",
        "quiz_q4_o2": "नहीं, यह एक जाना-माना टास्क घोटाला है जो बाद में आपकी गाढ़ी कमाई लूट लेता है",
        "quiz_q4_o3": "हाँ, बशर्ते आप कोई पुराना बैंक खाता दें",
        "quiz_q4_exp": "शुरुआत में ये धोखेबाज 100-200 रुपये देकर भरोसा जीतते हैं, फिर बड़े निवेश के नाम पर लाखों रुपये हड़प लेते हैं।"
    },
    
    "Kannada": {
        "app_title": "ಸಿಲ್ವರ್‌ಶೀಲ್ಡ್ AI",
        "app_tagline": "ಹಿರಿಯ ನಾಗರಿಕರು ಮತ್ತು ಕುಟುಂಬಗಳಿಗೆ AI ಸೈಬರ್ ಭದ್ರತಾ ಒಡನಾಡಿ",
        "system_status_live": "ಕೇಂದ್ರ AI ಭದ್ರತಾ ವ್ಯವಸ್ಥೆ: ಸಕ್ರಿಯವಾಗಿದೆ (Online)",
        "system_status_fallback": "ಸ್ಥಳೀಯ AI ಭದ್ರತಾ ಎಂಜಿನ್: ಸಕ್ರಿಯವಾಗಿದೆ",
        
        "nav_dashboard": "ಮುಖಪುಟ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "nav_message_checker": "ವಂಚನೆ ಸಂದೇಶ ಪತ್ತೆ",
        "nav_url_checker": "ವೆಬ್‌ಸೈಟ್ ಲಿಂಕ್ ಪರಿಶೀಲನೆ",
        "nav_awareness": "ಭದ್ರತಾ ಜಾಗೃತಿ ಕೇಂದ್ರ",
        "nav_safety_guide": "ಸುರಕ್ಷತಾ ಮಾರ್ಗದರ್ಶಿ ಮತ್ತು ರಸಪ್ರಶ್ನೆ",
        "nav_settings": "ಸೆಟ್ಟಿಂಗ್ಸ್ ಮತ್ತು ಸುಲಭ ಓದುವಿಕೆ",
        "nav_account": "ಖಾತೆ ಮತ್ತು ಭದ್ರತೆ",
        
        "sidebar_language_label": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
        "sidebar_quick_helpline": "ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಸಹಾಯವಾಣಿ: 1930 (ಉಚಿತ ಕರೆ, 24x7)",
        "sidebar_disclaimer": "ಸಿಲ್ವರ್‌ಶೀಲ್ಡ್ AI ಹಿರಿಯರನ್ನು ಡಿಜಿಟಲ್ ವಂಚನೆ ಮತ್ತು ಸೈಬರ್ ಅಪರಾಧಗಳಿಂದ ರಕ್ಷಿಸಲು ವಿನ್ಯಾಸಗೊಳಿಸಲಾದ ಸುರಕ್ಷತಾ ಸಹಾಯಕವಾಗಿದೆ.",
        
        "dash_hero_badge": "ಸುಧಾರಿತ AI ಸೈಬರ್ ರಕ್ಷಣೆ",
        "dash_hero_title": "ಆನ್‌ಲೈನ್ ವಂಚನೆ ಮತ್ತು ಸೈಬರ್ ದಾಳಿಗಳಿಂದ ಸುರಕ್ಷಿತವಾಗಿರಿ",
        "dash_hero_sub": "ಸಿಲ್ವರ್‌ಶೀಲ್ಡ್ AI ಮೆಷಿನ್ ಲರ್ನಿಂಗ್ ಮತ್ತು ಬಹುಸ್ತರದ ಲಿಂಕ್ ಭದ್ರತಾ ತಂತ್ರಜ್ಞಾನವನ್ನು ಬಳಸಿ ಹಿರಿಯರನ್ನು ಆರ್ಥಿಕ ನಷ್ಟದಿಂದ ರಕ್ಷಿಸುತ್ತದೆ.",
        "dash_stat_protection": "ನೈಜ-ಸಮಯದ AI ಸ್ಕ್ಯಾನ್",
        "dash_stat_protection_sub": "ಸಂದೇಶ ಮತ್ತು ಲಿಂಕ್ ರಕ್ಷಣೆ",
        "dash_stat_helpline": "ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಸಹಾಯವಾಣಿ",
        "dash_stat_helpline_sub": "ತಕ್ಷಣದ ಸಹಾಯಕ್ಕಾಗಿ 1930 ಕರೆ ಮಾಡಿ",
        "dash_stat_privacy": "ಸಂಪೂರ್ಣ ಗೌಪ್ಯತೆ",
        "dash_stat_privacy_sub": "ಸಂದೇಶಗಳ ಯಾವುದೇ ಶಾಶ್ವತ ಸಂಗ್ರಹವಿಲ್ಲ",
        
        "dash_actions_heading": "ಮುಖ್ಯ ರಕ್ಷಣಾ ವೈಶಿಷ್ಟ್ಯಗಳು",
        "dash_action_msg_title": "ಸಂದೇಶ ವಂಚನೆ ಪತ್ತೆಕಾರಕ",
        "dash_action_msg_desc": "ಅನುಮಾನಾಸ್ಪದ ವಾಟ್ಸಾಪ್ ಸಂದೇಶಗಳು, ಬ್ಯಾಂಕ್ ಎಚ್ಚರಿಕೆಗಳು, ವಿದ್ಯುತ್ ಕಡಿತ ಅಥವಾ ಲಾಟರಿ ಸಂದೇಶಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ಪರೀಕ್ಷಿಸಿ.",
        "dash_action_msg_btn": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "dash_action_url_title": "ವೆಬ್ ಲಿಂಕ್ ಸುರಕ್ಷತಾ ತಪಾಸಣೆ",
        "dash_action_url_desc": "ಅಪರಿಚಿತ ವೆಬ್ ಲಿಂಕ್‌ಗಳು, ನಕಲಿ ಬ್ಯಾಂಕ್ ವೆಬ್‌ಸೈಟ್‌ಗಳು ಮತ್ತು ಅಪಾಯಕಾರಿ ಲಿಂಕ್‌ಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ.",
        "dash_action_url_btn": "ಲಿಂಕ್ ಪರಿಶೀಲಿಸಿ",
        "dash_action_risk_title": "ಸಮಗ್ರ ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ",
        "dash_action_risk_desc": "ಸಂದೇಶ ಭಾಷೆ ಮತ್ತು ವೆಬ್ ಲಿಂಕ್‌ಗಳೆರಡನ್ನೂ ಪರಿಶೀಲಿಸಿ ತಕ್ಷಣವೇ 0–100 ರ ಅಪಾಯ ಅಂಕ ನೀಡುತ್ತದೆ.",
        "dash_action_risk_btn": "ಅಪಾಯ ವ್ಯವಸ್ಥೆ ತಿಳಿಯಿರಿ",
        "dash_action_aware_title": "ಭದ್ರತಾ ಜಾಗೃತಿ ಮತ್ತು ಸಲಹೆಗಳು",
        "dash_action_aware_desc": "OTP ವಂಚನೆ, ನಕಲಿ ಕರೆಗಳು ಮತ್ತು ಆನ್‌ಲೈನ್ ಬೆದರಿಕೆಗಳನ್ನು ತಪ್ಪಿಸುವ ಮುನ್ನೆಚ್ಚರಿಕೆಗಳನ್ನು ತಿಳಿಯಿರಿ.",
        "dash_action_aware_btn": "ಜಾಗೃತಿ ಮತ್ತು ರಸಪ್ರಶ್ನೆ",
        
        "dash_tip_badge": "ದೈನಂದಿನ ಸುರಕ್ಷತಾ ಸಲಹೆ",
        "dash_tip_title": "ಇಂದಿನ ಡಿಜಿಟಲ್ ಸುರಕ್ಷತಾ ಸಲಹೆ",
        "dash_tip_next_btn": "ಮತ್ತೊಂದು ಸಲಹೆ ವೀಕ್ಷಿಸಿ",
        
        "dash_rules_heading": "ಡಿಜಿಟಲ್ ಸುರಕ್ಷತೆಯ 3 ಸುವರ್ಣ ನಿಯಮಗಳು",
        "rule_1_title": "ನಿಮ್ಮ OTP ಅಥವಾ PIN ಅನ್ನು ಯಾರಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ",
        "rule_1_desc": "ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿಗಳು, ಪೊಲೀಸರು ಅಥವಾ ಯಾವುದೇ ಸಂಸ್ಥೆ ಎಂದಿಗೂ ಫೋನ್‌ನಲ್ಲಿ ನಿಮ್ಮ ರಹಸ್ಯ OTP ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ಕೇಳುವುದಿಲ್ಲ.",
        "rule_2_title": "ಅವಸರದಲ್ಲಿ ಅಥವಾ ಭಯದಲ್ಲಿ ಯಾವುದೇ ತೀರ್ಮಾನ ತೆಗೆದುಕೊಳ್ಳಬೇಡಿ",
        "rule_2_desc": "ವಂಚಕರು ಕರೆಂಟ್ ಕಟ್, ಸಿಮ್ ಬ್ಲಾಕ್ ಅಥವಾ ಅರೆಸ್ಟ್ ಮಾಡುವ ಸುಳ್ಳು ಬೆದರಿಕೆ ಹಾಕಿ ಭಯ ಹುಟ್ಟಿಸುತ್ತಾರೆ. ಸಮಾಧಾನವಾಗಿರಿ.",
        "rule_3_title": "ಕುಟುಂಬದವರನ್ನು ಕೇಳಿ ಅಥವಾ 1930 ಗೆ ಕರೆ ಮಾಡಿ",
        "rule_3_desc": "ಅನುಮಾನ ಬಂದಾಗ ಸಂದೇಶವನ್ನು ಮನೆಯವರಿಗೆ ತೋರಿಸಿ ಅಥವಾ 1930 ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ.",

        "msg_title": "ವಂಚನೆ ಸಂದೇಶ ಪತ್ತೆಕಾರಕ (Scam Detector)",
        "msg_subtitle": "ಯಾವುದೇ ಅನುಮಾನಾಸ್ಪದ SMS, ವಾಟ್ಸಾಪ್ ಸಂದೇಶ ಅಥವಾ ಇಮೇಲ್ ಪಠ್ಯವನ್ನು ಇಲ್ಲಿ ಹಾಕಿ. ನಮ್ಮ AI ಅಪಾಯವನ್ನು ಪತ್ತೆ ಮಾಡುತ್ತದೆ.",
        "msg_input_label": "ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ:",
        "msg_input_placeholder": "ಉದಾಹರಣೆ: ತುರ್ತು ಸೂಚನೆ! KYC ಅವಧಿ ಮೀರಿದ್ದರಿಂದ ನಿಮ್ಮ SBI ಖಾತೆ ಸ್ಥಗಿತಗೊಂಡಿದೆ. ಖಾತೆ ರದ್ದಾಗುವುದನ್ನು ತಪ್ಪಿಸಲು http://bit.ly/sbi-kyc ಕ್ಲಿಕ್ ಮಾಡಿ...",
        "msg_btn_analyze": "ಸಂದೇಶದ ಸುರಕ್ಷತೆ ಪರಿಶೀಲಿಸಿ",
        "msg_btn_clear": "ಅಳಿಸಿ",
        "msg_btn_narrate": "ಫಲಿತಾಂಶವನ್ನು ಆಡಿಯೋ ಮೂಲಕ ಕೇಳಿ (Read Aloud)",
        "msg_sample_label": "ಮಾದರಿ ಸಂದೇಶವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ:",
        "sample_sbi": "ಬ್ಯಾಂಕ್ KYC ಸ್ಥಗಿತ ವಂಚನೆ",
        "sample_power": "ವಿದ್ಯುತ್ ಸಂಪರ್ಕ ಕಡಿತ ವಂಚನೆ",
        "sample_otp": "ನಕಲಿ ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿಯಿಂದ OTP ಬೇಡಿಕೆ",
        "sample_job": "ಮನೆಯಲ್ಲೇ ಕುಳಿತು ಕೆಲಸ (WFH) ವಂಚನೆ",
        "sample_legit": "ಕುಟುಂಬದ ಸಾಮಾನ್ಯ ಸಂದೇಶ",
        
        "res_heading": "AI ಭದ್ರತಾ ವಿಶ್ಲೇಷಣೆ ಫಲಿತಾಂಶ",
        "res_risk_level": "ಒಟ್ಟಾರೆ ಅಪಾಯದ ಮಟ್ಟ",
        "res_risk_score": "ಅಪಾಯದ ಅಂಕ (Score)",
        "res_confidence": "ಮಾದರಿ ವಿಶ್ವಾಸಾರ್ಹತೆ",
        "res_scam_prob": "ವಂಚನೆ ಸಂಭವನೀಯತೆ",
        "res_prediction": "ML ವರ್ಗೀಕರಣ",
        "res_url_risk": "ಸಂದೇಶದಲ್ಲಿರುವ ಲಿಂಕ್‌ನ ಅಪಾಯ",
        "res_explanation_title": "AI ವಿವರಣೆ ಮತ್ತು ಕಾರಣ",
        "res_indicators_title": "ಕಂಡುಬಂದ ಅನುಮಾನಾಸ್ಪದ ಲಕ್ಷಣಗಳು",
        "res_actions_title": "ನೀವು ಈಗ ಕೈಗೊಳ್ಳಬೇಕಾದ ಸುರಕ್ಷತಾ ಕ್ರಮಗಳು",
        "res_tech_details": "ತಾಂತ್ರಿಕ ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ (ಮೌಲ್ಯಮಾಪಕರಿಗೆ)",
        "res_caregiver_share": "ನಂಬಿಕಸ್ಥ ಸಹಾಯಕರಿಗೆ WhatsApp ಮೂಲಕ ತಿಳಿಸಿ",
        "res_caregiver_notice": "ಸೂಚನೆ: ಈ ಬಟನ್ ಕ್ಲಿಕ್ ಮಾಡಿದಾಗ WhatsApp ನಲ್ಲಿ ಮುಂಚಿತವಾಗಿ ಸಿದ್ಧಪಡಿಸಿದ ಸಂದೇಶ ತೆರೆಯುತ್ತದೆ. ನೀವು ಅದನ್ನು ಪರಿಶೀಲಿಸಿ ಕಳುಹಿಸಬಹುದು.",
        "res_no_indicators": "ಈ ಸಂದೇಶದಲ್ಲಿ ಯಾವುದೇ ಅಪಾಯಕಾರಿ ಅಂಶಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
        "res_input_required": "ದಯವಿಟ್ಟು ಪರಿಶೀಲಿಸಲು ಸಂದೇಶವನ್ನು ಟೈಪ್ ಮಾಡಿ ಅಥವಾ ಪೇಸ್ಟ್ ಮಾಡಿ.",
        
        "url_title": "ವೆಬ್‌ಸೈಟ್ ಲಿಂಕ್ ಸುರಕ್ಷತಾ ಪರೀಕ್ಷಕ",
        "url_subtitle": "ಅನುಮಾನಾಸ್ಪದ ವೆಬ್ ಲಿಂಕ್‌ಗಳು, ಸಂಕ್ಷಿಪ್ತ ಲಿಂಕ್‌ಗಳು ಮತ್ತು ಫಿಶಿಂಗ್ ಪುಟಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ಪರೀಕ್ಷಿಸಿ.",
        "url_input_label": "ವೆಬ್‌ಸೈಟ್ ಲಿಂಕ್ (URL) ನಮೂದಿಸಿ:",
        "url_input_placeholder": "https://example-bank-login.xyz/verify ಅಥವಾ http://bit.ly/update-now",
        "url_btn_analyze": "ಲಿಂಕ್ ಸುರಕ್ಷತೆ ಪರಿಶೀಲಿಸಿ",
        "url_btn_clear": "ಅಳಿಸಿ",
        "url_sample_label": "ಪರೀಕ್ಷೆಗಾಗಿ ಮಾದರಿ ಲಿಂಕ್‌ಗಳು:",
        "url_sample_phish": "ಫಿಶಿಂಗ್ ನಕಲಿ ಬ್ಯಾಂಕ್ ಲಿಂಕ್",
        "url_sample_short": "ಅಡಗಿಸಲಾದ ಶಾರ್ಟ್ ಲಿಂಕ್ (bit.ly)",
        "url_sample_ip": "ಅಸುರಕ್ಷಿತ IP ವಿಳಾಸ ಲಿಂಕ್",
        "url_sample_safe": "ಅಧಿಕೃತ ಸುರಕ್ಷಿತ ಬ್ಯಾಂಕ್ ಲಿಂಕ್",
        "url_res_heading": "ಲಿಂಕ್ ತಪಾಸಣಾ ಫಲಿತಾಂಶಗಳು",
        "url_res_status": "ಲಿಂಕ್ ಸ್ಥಿತಿ",
        "url_res_domain": "ವೆಬ್‌ಸೈಟ್ ಡೊಮೇನ್",
        "url_res_https": "ಸುರಕ್ಷಿತ ಸಂಪರ್ಕ (HTTPS)",
        "url_res_explanation": "ಸುರಕ್ಷತಾ ವಿವರಣೆ",
        "url_res_indicators": "ಲಿಂಕ್‌ನಲ್ಲಿರುವ ಅಪಾಯದ ಲಕ್ಷಣಗಳು",
        "url_input_required": "ದಯವಿಟ್ಟು http:// ಅಥವಾ https:// ನಿಂದ ಪ್ರಾರಂಭವಾಗುವ ಮಾನ್ಯ ವೆಬ್ ಲಿಂಕ್ ನಮೂದಿಸಿ.",
        
        "aware_title": "ಭದ್ರತಾ ಜಾಗೃತಿ ಕೇಂದ್ರ",
        "aware_subtitle": "ಸೈಬರ್ ಅಪರಾಧಿಗಳು ಹಿರಿಯ ನಾಗರಿಕರನ್ನು ಹೇಗೆ ಗುರಿಯಾಗಿಸುತ್ತಾರೆ ಮತ್ತು ಅವರ ತಂತ್ರಗಳನ್ನು ಹೇಗೆ ಗುರುತಿಸಬೇಕೆಂದು ತಿಳಿಯಿರಿ.",
        "aware_tab_scams": "ಪ್ರಮುಖ ವಂಚನೆಗಳ ಪರಿಚಯ",
        "aware_tab_library": "ವಂಚನೆ ಸಂದೇಶಗಳ ಗ್ರಂಥಾಲಯ",
        "aware_tab_prevention": "ಸುರಕ್ಷತಾ ಮುನ್ನೆಚ್ಚರಿಕೆಗಳ ಪಟ್ಟಿ",
        
        "scam_otp_title": "1. OTP ಮತ್ತು ಪಾಸ್‌ವರ್ಡ್ ಕಳ್ಳತನದ ವಂಚನೆ",
        "scam_otp_desc": "ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿ ಅಥವಾ ಕೊರಿಯರ್ ಏಜೆಂಟ್ ಎಂದು ಕರೆ ಮಾಡಿ, ತಪ್ಪಾಗಿ ಹಣ ಕಡಿತಗೊಂಡಿದೆ ಅದನ್ನು ರದ್ದು ಮಾಡಲು 6 ಅಂಕಿಯ OTP ತಿಳಿಸಿ ಎನ್ನುತ್ತಾರೆ. ಎಂದಿಗೂ OTP ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.",
        "scam_bank_title": "2. ಬ್ಯಾಂಕ್ KYC ಮತ್ತು ಖಾತೆ ರದ್ದತಿ ಬೆದರಿಕೆ",
        "scam_bank_desc": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆ ಅಥವಾ ಪ್ಯಾನ್ ಕಾರ್ಡ್ ಬ್ಲಾಕ್ ಆಗಿದೆ ಎಂದು ನಕಲಿ ಲಿಂಕ್ ಕಳುಹಿಸಿ ಖಾತೆಯ ವಿವರಗಳನ್ನು ಕದಿಯುವ ತಂತ್ರ.",
        "scam_lottery_title": "3. ಲಾಟರಿ, ಬಹುಮಾನ ಮತ್ತು ಕ್ಯಾಶ್‌ಬ್ಯಾಕ್ ಆಮಿಷ",
        "scam_lottery_desc": "KBC ಅಥವಾ ಲಕ್ಕಿ ಡ್ರಾನಲ್ಲಿ 25 ಲಕ್ಷ ರೂಪಾಯಿ ಬಹುಮಾನ ಬಂದಿದೆ ಎಂದು ನಂಬಿಸಿ, ತೆರಿಗೆ ಅಥವಾ ಪ್ರೊಸೆಸಿಂಗ್ ಶುಲ್ಕದ ಹೆಸರಿನಲ್ಲಿ ಹಣ ವಸೂಲಿ ಮಾಡುತ್ತಾರೆ.",
        "scam_job_title": "4. ಸುಲಭ ಯೂಟ್ಯೂಬ್ ಲೈಕ್ ಪಾರ್ಟ್‌ಟೈಮ್ ಉದ್ಯೋಗ",
        "scam_job_desc": "ವೀಡಿಯೊ ಲೈಕ್ ಮಾಡಲು ದಿನಕ್ಕೆ 2,000–5,000 ರೂ ನೀಡುವುದಾಗಿ ಆಮಿಷವೊಡ್ಡಿ, ನಂತರ ದೊಡ್ಡ ಹೂಡಿಕೆ ವಂಚನೆಯಲ್ಲಿ ಸಿಲುಕಿಸುತ್ತಾರೆ.",
        "scam_digital_arrest_title": "5. 'ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್' ನಕಲಿ ವಿಡಿಯೋ ಕಾಲ್",
        "scam_digital_arrest_desc": "ಪೊಲೀಸ್ ಅಥವಾ ಸಿಬಿಐ ಸಮವಸ್ತ್ರ ಧರಿಸಿ ವಿಡಿಯೋ ಕಾಲ್ ಮಾಡಿ, ನಿಮ್ಮ ಹೆಸರಿನಲ್ಲಿ ಮಾದಕ ದ್ರವ್ಯ ಪಾರ್ಸೆಲ್ ಬಂದಿದೆ ಎಂದು ಬೆದರಿಸಿ ಹಣ ಪೀಕುತ್ತಾರೆ.",
        "scam_remote_title": "6. ರಿಮೋಟ್ ಸ್ಕ್ರೀನ್ ಶೇರಿಂಗ್ (AnyDesk) ಬಲೆ",
        "scam_remote_desc": "ಸಹಾಯ ಮಾಡುವ ನೆಪದಲ್ಲಿ AnyDesk ಅಥವಾ TeamViewer ಆ್ಯಪ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿಸುತ್ತಾರೆ. ಆ್ಯಪ್ ಇನ್‌ಸ್ಟಾಲ್ ಆದ ತಕ್ಷಣ ನಿಮ್ಮ ಬ್ಯಾಂಕಿಂಗ್ ಪಾಸ್‌ವರ್ಡ್ ಕದ್ದು ಹಣ ದೋಚುತ್ತಾರೆ.",
        
        "guide_title": "ಹಿರಿಯರ ಸುರಕ್ಷತಾ ಮಾರ್ಗದರ್ಶಿ ಮತ್ತು ರಸಪ್ರಶ್ನೆ",
        "guide_subtitle": "ತುರ್ತು ಪರಿಸ್ಥಿತಿಯ ಕ್ರಮಗಳು, ಸೈಬರ್ ಅಪರಾಧ ವರದಿ ಮಾಡುವ ವಿಧಾನ ಮತ್ತು ನಿಮ್ಮ ಜಾಗರೂಕತೆಯನ್ನು ಪರೀಕ್ಷಿಸುವ ರಸಪ್ರಶ್ನೆ.",
        "guide_tab_rules": "ಪ್ರಮುಖ ಸುರಕ್ಷತಾ ನಿಯಮಗಳು",
        "guide_tab_emergency": "ತುರ್ತು ಸಂದರ್ಭದಲ್ಲಿ ಏನು ಮಾಡಬೇಕು?",
        "guide_tab_quiz": "ಸೈಬರ್ ಸುರಕ್ಷತಾ ರಸಪ್ರಶ್ನೆ",
        
        "emer_step1_title": "ಸಂದರ್ಭ A: ನೀವು ಅನುಮಾನಾಸ್ಪದ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಿದ್ದರೆ",
        "emer_step1_desc": "1. ತಕ್ಷಣವೇ ಆ ಬ್ರೌಸರ್ ಪುಟ ಅಥವಾ ಆ್ಯಪ್ ಅನ್ನು ಮುಚ್ಚಿ.\n2. ಆ ಪುಟದಲ್ಲಿ ಯಾವುದೇ ಪಾಸ್‌ವರ್ಡ್, PIN ಅಥವಾ ವೈಯಕ್ತಿಕ ವಿವರ ನಮೂದಿಸಬೇಡಿ.\n3. ನಿಮ್ಮ ಮೊಬೈಲ್ ಡೇಟಾ ಮತ್ತು ವೈ-ಫೈ ತಕ್ಷಣ ಆಫ್ ಮಾಡಿ.\n4. ಫೋನ್ ಅನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ ರೀಸ್ಟಾರ್ಟ್ ಮಾಡಿ.",
        "emer_step2_title": "ಸಂದರ್ಭ B: ನೀವು ಆಕಸ್ಮಿಕವಾಗಿ OTP ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ಹಂಚಿಕೊಂಡಿದ್ದರೆ",
        "emer_step2_desc": "1. ತಕ್ಷಣ ಬ್ಯಾಂಕ್‌ನ ಅಧಿಕೃತ ಟೋಲ್-ಫ್ರೀ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ ಕಾರ್ಡ್ ಹಾಗೂ ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್ ಬ್ಲಾಕ್ ಮಾಡಿ.\n2. ಅಧಿಕೃತ ಬ್ಯಾಂಕ್ ಆ್ಯಪ್ ಮೂಲಕ ಕಾರ್ಡ್ ಲಾಕ್ ಮಾಡಿ.\n3. ಮತ್ತೊಂದು ಸುರಕ್ಷಿತ ಫೋನ್‌ನಿಂದ ನೆಟ್ ಬ್ಯಾಂಕಿಂಗ್ ಪಾಸ್‌ವರ್ಡ್ ತಕ್ಷಣ ಬದಲಾಯಿಸಿ.\n4. ಕುಟುಂಬದ ಸಹಾಯಕರಿಗೆ ತಕ್ಷಣವೇ ತಿಳಿಸಿ.",
        "emer_step3_title": "ಸಂದರ್ಭ C: ನಿಮ್ಮ ಖಾತೆಯಿಂದ ಹಣ ಅಕ್ರಮವಾಗಿ ಕಡಿತಗೊಂಡಿದ್ದರೆ",
        "emer_step3_desc": "1. ಹಣ ಕಳೆದುಕೊಂಡ ತಕ್ಷಣವೇ 'ಗೋಲ್ಡನ್ ಅವರ್' ಒಳಗೆ 1930 ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ ಹಣ ವರ್ಗಾವಣೆಯನ್ನು ತಡೆಯಿರಿ.\n2. ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್ https://cybercrime.gov.in ನಲ್ಲಿ ದೂರು ದಾಖಲಿಸಿ.\n3. ವಂಚನೆಯ SMS, ವಹಿವಾಟು ಸಂಖ್ಯೆ ಹಾಗೂ ಫೋನ್ ಸಂಖ್ಯೆಗಳ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಇಟ್ಟುಕೊಳ್ಳಿ.\n4. ನಿಮ್ಮ ಹತ್ತಿರದ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ತೆರಳಿ ಲಿಖಿತ ದೂರು ಸಲ್ಲಿಸಿ.",
        
        "set_title": "ಸೆಟ್ಟಿಂಗ್ಸ್ ಮತ್ತು ಸುಲಭ ಓದುವಿಕೆ",
        "set_subtitle": "ಅಕ್ಷರಗಳ ಗಾತ್ರ, ಹೈ ಕಾಂಟ್ರಾಸ್ಟ್ ಮೋಡ್ ಮತ್ತು ಕುಟುಂಬದ ಸಹಾಯಕರ ಸಂಪರ್ಕವನ್ನು ಹೊಂದಿಸಿ.",
        "set_font_size_label": "ಓದುವ ಅಕ್ಷರಗಳ ಗಾತ್ರ",
        "set_font_standard": "ಸಾಂದ್ರ (14px)",
        "set_font_large": "ಸಾಮಾನ್ಯ (15px)",
        "set_font_xlarge": "ದೊಡ್ಡದು (17px)",
        "set_contrast_label": "ಹೈ ಕಾಂಟ್ರಾಸ್ಟ್ ಮೋಡ್ (WCAG AAA)",
        "set_contrast_desc": "ಸುಲಭವಾಗಿ ಓದಲು ಗಾಢ ಹಿನ್ನೆಲೆ ಮತ್ತು ಪ್ರಕಾಶಮಾನ ಬಾರ್ಡರ್‌ಗಳ ವ್ಯವಸ್ಥೆ.",
        "set_helper_heading": "ನಂಬಿಕಸ್ಥ ಸಹಾಯಕರು (Caregiver)",
        "set_helper_desc": "ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶ ಬಂದಾಗ ತಕ್ಷಣ ಒಂದೇ ಕ್ಲಿಕ್‌ನಲ್ಲಿ ಎಚ್ಚರಿಸಲು ನಿಮ್ಮ ಕುಟುಂಬದ ಸದಸ್ಯರ ವಿವರ ಉಳಿಸಿ.",
        "set_helper_name": "ಸಹಾಯಕರ / ಸ್ವಜನರ ಹೆಸರು",
        "set_helper_relation": "ಸಂಬಂಧ (ಉದಾ: ಮಗ, ಮಗಳು, ಮೊಮ್ಮಗ)",
        "set_helper_phone": "WhatsApp / ಫೋನ್ ಸಂಖ್ಯೆ (ದೇಶದ ಕೋಡ್ ಸೇರಿಸಿ, ಉದಾ: 919876543210)",
        "set_helper_save_btn": "ವಿವರಗಳನ್ನು ಉಳಿಸಿ",
        "set_helper_saved_msg": "ಸಹಾಯಕರ ವಿವರಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ.",
        "set_history_heading": "ತಪಾಸಣಾ ಇತಿಹಾಸ (Session History)",
        "set_history_desc": "ಈ ಅವಧಿಯಲ್ಲಿ ಪರೀಕ್ಷಿಸಲಾದ ಸಂದೇಶಗಳು ಮತ್ತು ಲಿಂಕ್‌ಗಳ ಪಟ್ಟಿ. ಯಾವುದೇ ಖಾಸಗಿ ಮಾಹಿತಿಯನ್ನು ಶಾಶ್ವತವಾಗಿ ಸಂಗ್ರಹಿಸಲಾಗುವುದಿಲ್ಲ.",
        "set_history_clear_btn": "ಇತಿಹಾಸ ಅಳಿಸಿ",
        "set_history_empty": "ಈ ಸೆಷನ್‌ನಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ತಪಾಸಣೆ ನಡೆದಿಲ್ಲ.",
        "set_history_cleared": "ತಪಾಸಣಾ ಇತಿಹಾಸವನ್ನು ಅಳಿಸಲಾಗಿದೆ.",
        "set_reset_btn": "ಡೀಫಾಲ್ಟ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಮರುಸ್ಥಾಪಿಸಿ",
        "set_reset_success": "ಎಲ್ಲಾ ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು ಮೊದಲಿನ ಸ್ಥಿತಿಗೆ ಮರುಹೊಂದಿಸಲಾಗಿದೆ.",
        
        "btn_save": "ಉಳಿಸಿ",
        "btn_cancel": "ರದ್ದುಮಾಡಿ",
        "btn_submit": "ಸಲ್ಲಿಸಿ",
        "btn_close": "ಮುಚ್ಚಿ",
        "btn_view": "ವಿವರ ನೋಡಿ",
        "btn_copy": "ಕಾಪಿ ಮಾಡಿ",
        
        "quiz_title": "ನಿಮ್ಮ ಸೈಬರ್ ಜಾಗೃತಿಯನ್ನು ಪರೀಕ್ಷಿಸಿ",
        "quiz_subtitle": "4 ಸರಳ ಸನ್ನಿವೇಶಗಳಿಗೆ ಉತ್ತರಿಸಿ ನೀವು ವಂಚನೆಗಳನ್ನು ಎಷ್ಟು ನಿಖರವಾಗಿ ಗುರುತಿಸಬಲ್ಲಿರಿ ಎಂದು ತಿಳಿಯಿರಿ.",
        "quiz_score_prefix": "ನಿಮ್ಮ ಅಂಕ:",
        "quiz_btn_check": "ಉತ್ತರ ಪರೀಕ್ಷಿಸಿ",
        "quiz_btn_reset": "ರಸಪ್ರಶ್ನೆ ಮರುಪ್ರಾರಂಭಿಸಿ",
        "quiz_correct": "ಸರಿಯಾದ ಉತ್ತರ! ನಿಮ್ಮ ಜಾಗರೂಕತೆ ಅತ್ಯುತ್ತಮವಾಗಿದೆ.",
        "quiz_incorrect": "ತಪ್ಪಾದ ಉತ್ತರ. ಇಂತಹ ಸಂದೇಶಗಳ ಬಗ್ಗೆ ಎಚ್ಚರದಿಂದಿರಿ.",
        "quiz_q1": "ನಿಮಗೆ ಸಂದೇಶ ಬರುತ್ತದೆ: 'SBI ಗ್ರಾಹಕರೇ, ನಿಮ್ಮ ಖಾತೆ 2 ಗಂಟೆಯಲ್ಲಿ ಸ್ಥಗಿತಗೊಳ್ಳುತ್ತದೆ. ಪ್ಯಾನ್ ಅಪ್‌ಡೇಟ್ ಮಾಡಲು http://bit.ly/sbi-kyc ಕ್ಲಿಕ್ ಮಾಡಿ.' ನೀವು ಏನು ಮಾಡುವಿರಿ?",
        "quiz_q1_o1": "ಖಾತೆ ರದ್ದಾಗದಂತೆ ತಕ್ಷಣ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಿ ವಿವರ ನಮೂದಿಸುವೆ",
        "quiz_q1_o2": "ಸಂದೇಶವನ್ನು ತಕ್ಷಣ ಅಳಿಸಿ, ಅಧಿಕೃತ ಬ್ಯಾಂಕ್ ಶಾಖೆ ಅಥವಾ YONO ಆ್ಯಪ್ ಮೂಲಕ ಮಾತ್ರ ಪರೀಕ್ಷಿಸುವೆ",
        "quiz_q1_o3": "ಎಚ್ಚರಿಸಲು ಈ ಸಂದೇಶವನ್ನು ಎಲ್ಲಾ ಸ್ನೇಹಿತರಿಗೆ ಫಾರ್ವರ್ಡ್ ಮಾಡುವೆ",
        "quiz_q1_exp": "ಬ್ಯಾಂಕುಗಳು ಎಂದಿಗೂ bit.ly ನಂತಹ ಅಡಗಿಸಿದ ಲಿಂಕ್ ಕಳುಹಿಸುವುದಿಲ್ಲ ಮತ್ತು 2 ಗಂಟೆಯಲ್ಲಿ ಖಾತೆ ಸ್ಥಗಿತಗೊಳಿಸುವುದಾಗಿ ಬೆದರಿಸುವುದಿಲ್ಲ.",
        "quiz_q2": "ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿಯಂತೆ ಮಾತನಾಡುವ ವ್ಯಕ್ತಿ: 'ತಪ್ಪಾಗಿ ಕಡಿತವಾದ 12,000 ರೂ ಮರುಪಡೆಯಲು ನಿಮ್ಮ ಫೋನ್‌ಗೆ ಬಂದ 6 ಅಂಕಿಯ OTP ತಿಳಿಸಿ' ಎನ್ನುತ್ತಾರೆ. ನೀವು ಏನು ಮಾಡುವಿರಿ?",
        "quiz_q2_o1": "ಹಣ ವಾಪಸ್ ಬರುತ್ತದೆ ಎಂದು ತಕ್ಷಣ OTP ತಿಳಿಸುವೆ",
        "quiz_q2_o2": "ಯಾವುದೇ ಕಾರಣಕ್ಕೂ OTP ಹಂಚಿಕೊಳ್ಳುವುದಿಲ್ಲ ಮತ್ತು ತಕ್ಷಣ ಕರೆ ಕಟ್ ಮಾಡುವೆ",
        "quiz_q2_o3": "10 ನಿಮಿಷದ ನಂತರ ಕರೆ ಮಾಡಲು ತಿಳಿಸುವೆ",
        "quiz_q2_exp": "OTP ನಿಮ್ಮ ರಹಸ್ಯ ಸಹಿಯಂತಿದೆ. OTP ನೀಡಿದ ತಕ್ಷಣ ವಂಚಕರು ನಿಮ್ಮ ಹಣವನ್ನು ಕದಿಯುತ್ತಾರೆ. ಬ್ಯಾಂಕ್ ಎಂದಿಗೂ OTP ಕೇಳುವುದಿಲ್ಲ.",
        "quiz_q3": "ಪೊಲೀಸ್ ಸಮವಸ್ತ್ರ ಧರಿಸಿದ ವ್ಯಕ್ತಿಯಿಂದ WhatsApp ವಿಡಿಯೋ ಕಾಲ್ ಬಂದು, ನಿಮ್ಮ ಹೆಸರಿನ ಪಾರ್ಸೆಲ್‌ನಲ್ಲಿ ನಿಷೇಧಿತ ವಸ್ತು ಪತ್ತೆಯಾಗಿದೆ, ನೀವು 'ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್' ನಲ್ಲಿದ್ದೀರಿ ಎನ್ನುತ್ತಾರೆ. ಏನು ಮಾಡುವಿರಿ?",
        "quiz_q3_o1": "ಹೆದರಿ ಅವರು ಹೇಳಿದ ಖಾತೆಗೆ ಜಾಮೀನು ಹಣ ವರ್ಗಾಯಿಸುವೆ",
        "quiz_q3_o2": "ತಕ್ಷಣ ಕಾಲ್ ಕಟ್ ಮಾಡಿ 1930 ಅಥವಾ cybercrime.gov.in ಗೆ ದೂರು ನೀಡುವೆ",
        "quiz_q3_o3": "ನನ್ನ ನಿರಪರಾಧಿತ್ವ ಸಾಬೀತುಪಡಿಸಲು ಆಧಾರ್ ಹಾಗೂ ಪ್ಯಾನ್ ಕಾರ್ಡ್ ಕಳುಹಿಸುವೆ",
        "quiz_q3_exp": "ಭಾರತದಲ್ಲಿ 'ಡಿಜಿಟಲ್ ಅರೆಸ್ಟ್' ಎಂಬ ಯಾವುದೇ ಕಾನೂನು ಇಲ್ಲ. ಪೊಲೀಸರು ಎಂದಿಗೂ WhatsApp ವಿಡಿಯೋ ಕಾಲ್ ಮೂಲಕ ಬಂಧಿಸುವುದಿಲ್ಲ.",
        "quiz_q4": "ಮನೆಯಲ್ಲೇ ಕುಳಿತು Google Maps ನಲ್ಲಿ ಹೋಟೆಲ್‌ಗಳಿಗೆ ರೇಟಿಂಗ್ ನೀಡಿದರೆ ದಿನಕ್ಕೆ 3,000 ರೂ ನೀಡುವುದಾಗಿ ಸಂದೇಶ ಬಂದಿದೆ. ಇದು ಸುರಕ್ಷಿತವೇ?",
        "quiz_q4_o1": "ಹೌದು, ಸುಲಭವಾಗಿ ಹಣ ಗಳಿಸುವ ಉತ್ತಮ ಅವಕಾಶ",
        "quiz_q4_o2": "ಇಲ್ಲ, ಇದು ಜನರ ಉಳಿತಾಯದ ಹಣವನ್ನು ದೋಚುವ ಮೋಸದ ಹೂಡಿಕೆ ವಂಚನೆ (Task Scam)",
        "quiz_q4_o3": "ಹೌದು, ಬೇರೆ ಬ್ಯಾಂಕ್ ಖಾತೆ ನೀಡಿದರೆ ತೊಂದರೆಯಿಲ್ಲ",
        "quiz_q4_exp": "ಆರಂಭದಲ್ಲಿ 100-200 ರೂ ನೀಡಿ ನಂಬಿಕೆ ಗಳಿಸುತ್ತಾರೆ, ನಂತರ ಲಕ್ಷಾಂತರ ರೂಪಾಯಿ ಹೂಡಿಕೆ ಮಾಡಿಸಿ ಮೋಸ ಮಾಡುತ್ತಾರೆ."
    }
}

RISK_LEVEL_TRANSLATIONS = {
    "HIGH": {
        "English": "HIGH RISK (DANGEROUS)",
        "Hindi": "उच्च जोखिम (अत्यधिक खतरनाक)",
        "Kannada": "ಹೆಚ್ಚಿನ ಅಪಾಯ (ಅಪಾಯಕಾರಿ)"
    },
    "MEDIUM": {
        "English": "MEDIUM RISK (CAUTION)",
        "Hindi": "मध्यम जोखिम (सावधानी)",
        "Kannada": "ಮಧ್ಯಮ ಅಪಾಯ (ಎಚ್ಚರಿಕೆಯಿರಲಿ)"
    },
    "LOW": {
        "English": "LOW RISK (SAFE)",
        "Hindi": "कम जोखिम (सुरक्षित)",
        "Kannada": "ಕಡಿಮೆ ಅಪಾಯ (ಸುರಕ್ಷಿತ)"
    }
}

PREDICTION_TRANSLATIONS = {
    "SCAM": {
        "English": "Fraudulent / Scam Pattern Detected",
        "Hindi": "धोखाधड़ी / फर्जी संदेश के लक्षण मिले",
        "Kannada": "ವಂಚನೆಯ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿವೆ"
    },
    "LEGITIMATE": {
        "English": "Legitimate / Normal Communication",
        "Hindi": "सामान्य एवं वैध संदेश",
        "Kannada": "ಸಾಮಾನ್ಯ ಮತ್ತು ಸುರಕ್ಷಿತ ಸಂವಹನ"
    },
    "UNKNOWN": {
        "English": "Uncertain / Requires Further Review",
        "Hindi": "अनिश्चित / अतिरिक्त जाँच आवश्यक",
        "Kannada": "ಅನಿಶ್ಚಿತ / ಹೆಚ್ಚಿನ ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ"
    }
}

URL_RISK_TRANSLATIONS = {
    "MALICIOUS": {
        "English": "MALICIOUS / PHISHING LINK",
        "Hindi": "दुर्भावनापूर्ण / फ़िशिंग लिंक",
        "Kannada": "ಅಪಾಯಕಾರಿ / ಫಿಶಿಂಗ್ ಲಿಂಕ್"
    },
    "SUSPICIOUS": {
        "English": "SUSPICIOUS / UNVERIFIED LINK",
        "Hindi": "संदेहास्पद / अपुಷ್ಟ लिंक",
        "Kannada": "ಅನುಮಾನಾಸ್ಪದ / ಅಪರಿಚಿತ ಲಿಂಕ್"
    },
    "SAFE": {
        "English": "SAFE / REPUTABLE LINK",
        "Hindi": "सुरक्षित एवं सत्यापित लिंक",
        "Kannada": "ಸುರಕ್ಷಿತ ಮತ್ತು ವಿಶ್ವಾಸಾರ್ಹ ಲಿಂಕ್"
    },
    "NOT_APPLICABLE": {
        "English": "No Web Link in Message",
        "Hindi": "संदेश में कोई लिंक नहीं मिला",
        "Kannada": "ಸಂದೇಶದಲ್ಲಿ ಯಾವುದೇ ಲಿಂಕ್ ಇಲ್ಲ"
    },
    "UNKNOWN": {
        "English": "Unclassified Link",
        "Hindi": "अवर्गीकृत लिंक",
        "Kannada": "ವರ್ಗೀಕರಿಸದ ಲಿಂಕ್"
    }
}

INDICATOR_TRANSLATIONS = {
    "Message classified as a possible scam": {
        "English": "Message classified as a possible scam",
        "Hindi": "संदेश को संभावित धोखाधड़ी के रूप में वर्गीकृत किया गया है",
        "Kannada": "ಸಂದೇಶವನ್ನು ಸಂಭಾವ್ಯ ವಂಚನೆ ಎಂದು ಗುರುತಿಸಲಾಗಿದೆ"
    },
    "Very high confidence scam prediction": {
        "English": "Very high confidence scam prediction",
        "Hindi": "अत्यधिक निश्चितता के साथ फर्जी संदेश की पुष्टि",
        "Kannada": "ಅತ್ಯಂತ ಹೆಚ್ಚಿನ ವಿಶ್ವಾಸಾರ್ಹತೆಯೊಂದಿಗೆ ವಂಚನೆ ಎಂದು ದೃಢಪಟ್ಟಿದೆ"
    },
    "Asks for an OTP, PIN or password": {
        "English": "Asks for an OTP, PIN or password",
        "Hindi": "गोपनीय OTP, PIN या पासवर्ड की मांग की गई है",
        "Kannada": "ರಹಸ್ಯ OTP, PIN ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ಕೇಳಲಾಗಿದೆ"
    },
    "Asks for bank or card details": {
        "English": "Asks for bank or card details",
        "Hindi": "बैंक खाता या डेबिट/क्रेडिट कार्ड की जानकारी मांगी गई है",
        "Kannada": "ಬ್ಯಾಂಕ್ ಖಾತೆ ಅಥವಾ ಕಾರ್ಡ್ ವಿವರಗಳನ್ನು ಕೇಳಲಾಗಿದೆ"
    },
    "Asks for a payment, transfer or gift card": {
        "English": "Asks for a payment, transfer or gift card",
        "Hindi": "पैसे ट्रांसफर या गिफ्ट कार्ड खरीदने का अनुरोध है",
        "Kannada": "ಹಣ ವರ್ಗಾವಣೆ ಅಥವಾ ಗಿಫ್ಟ್ ಕಾರ್ಡ್ ಕೇಳಲಾಗಿದೆ"
    },
    "Asks you to log in through a link": {
        "English": "Asks you to log in through an external link",
        "Hindi": "बाहरी लिंक के माध्यम से लॉगिन करने के लिए कहा गया है",
        "Kannada": "ಬಾಹ್ಯ ಲಿಂಕ್ ಮೂಲಕ ಲಾಗಿನ್ ಆಗಲು ಕೋರಲಾಗಿದೆ"
    },
    "Claims to be from a bank, government body or known company": {
        "English": "Claims to be from a bank, government body or known company",
        "Hindi": "बैंक, सरकारी विभाग या प्रतिष्ठित कंपनी का नाम लेकर दावा किया गया है",
        "Kannada": "ಬ್ಯಾಂಕ್, ಸರ್ಕಾರಿ ಇಲಾಖೆ ಅಥವಾ ಪ್ರಸಿದ್ಧ ಕಂಪನಿಯ ಹೆಸರು ಹೇಳಿ ದಾರಿತಪ್ಪಿಸಲಾಗಿದೆ"
    },
    "Threatens account closure, a fine or legal action": {
        "English": "Threatens account closure, electricity disconnection or legal action",
        "Hindi": "खाता बंद करने, बिजली काटने या कानूनी कार्रवाई की धमकी दी गई है",
        "Kannada": "ಖಾತೆ ರದ್ದತಿ, ಕರೆಂಟ್ ಕಟ್ ಅಥವಾ ಕಾನೂನು ಕ್ರಮದ ಬೆದರಿಕೆ ಹಾಕಲಾಗಿದೆ"
    },
    "Uses urgency or a short deadline": {
        "English": "Uses urgency or artificial short deadline",
        "Hindi": "तुरंत निर्णय लेने का अनुचित दबाव या समय सीमा दी गई है",
        "Kannada": "ತಕ್ಷಣವೇ ಕ್ರಮ ಕೈಗೊಳ್ಳಲು ಸುಳ್ಳು ಅವಸರ ಅಥವಾ ಗಡುವು ನೀಡಲಾಗಿದೆ"
    },
    "Promises a prize, refund or reward": {
        "English": "Promises a lottery, cashback, refund or reward",
        "Hindi": "लॉटरी, कैशबैक, रिफंड या इनाम का झूठा प्रलोभन दिया गया है",
        "Kannada": "ಲಾಟರಿ, ಕ್ಯಾಶ್‌ಬ್ಯಾಕ್ ಅಥವಾ ಬಹುಮಾನದ ಸುಳ್ಳು ಆಮಿಷ ನೀಡಲಾಗಿದೆ"
    },
    "Asks for identity or personal information": {
        "English": "Asks for Aadhaar, PAN or personal identity data",
        "Hindi": "आधार, पैन या व्यक्तिगत पहचान विवरण मांगे गए हैं",
        "Kannada": "ಆಧಾರ್, ಪ್ಯಾನ್ ಅಥವಾ ಖಾಸಗಿ ಗುರುತಿನ ವಿವರಗಳನ್ನು ಕೇಳಲಾಗಿದೆ"
    },
    "Link flagged as malicious or a phishing page": {
        "English": "Link flagged as malicious or a phishing page",
        "Hindi": "लिंक को खतरनाक फ़िशिंग वेबसाइट के रूप में चिह्नित किया गया है",
        "Kannada": "ಲಿಂಕ್ ಅನ್ನು ಅಪಾಯಕಾರಿ ಫಿಶಿಂಗ್ ಪುಟ ಎಂದು ಗುರುತಿಸಲಾಗಿದೆ"
    },
    "Link shows suspicious characteristics": {
        "English": "Link shows suspicious characteristics",
        "Hindi": "वेब लिंक में संदेहास्पद और असामान्य लक्षण पाए गए हैं",
        "Kannada": "ವೆಬ್ ಲಿಂಕ್‌ನಲ್ಲಿ ಅನುಮಾನಾಸ್ಪದ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿವೆ"
    },
    "Link imitates the address of a known website": {
        "English": "Link imitates the address of a known website (Lookalike)",
        "Hindi": "लिंक किसी जानी-मानी वेबसाइट के पते की नकल कर रहा है",
        "Kannada": "ಲಿಂಕ್ ಪ್ರಸಿದ್ಧ ವೆಬ್‌ಸೈಟ್‌ನ ವಿಳಾಸವನ್ನು ನಕಲು ಮಾಡಿದೆ"
    },
    "Link uses a raw IP address instead of a domain name": {
        "English": "Link uses a raw IP address instead of a domain name",
        "Hindi": "वेबसाइट के नाम के स्थान पर असुरक्षित IP एड्रेस का उपयोग हुआ है",
        "Kannada": "ವೆಬ್‌ಸೈಟ್ ಹೆಸರಿನ ಬದಲು ಅಸುರಕ್ಷಿತ IP ವಿಳಾಸವನ್ನು ಬಳಸಲಾಗಿದೆ"
    },
    "Link is shortened, so the destination is hidden": {
        "English": "Link is shortened, so the destination website is hidden",
        "Hindi": "शॉर्ट लिंक का उपयोग किया गया है ताकि असली वेबसाइट छुप सके",
        "Kannada": "ಅಸಲಿ ವೆಬ್‌ಸೈಟ್ ಮುಚ್ಚಿಡಲು ಶಾರ್ಟ್ ಲಿಂಕ್ ಬಳಸಲಾಗಿದೆ"
    },
    "Link does not use a secure connection": {
        "English": "Link does not use a secure connection (No HTTPS)",
        "Hindi": "वेबसाइट असुरक्षित है (HTTPS कनेक्शन उपलब्ध नहीं है)",
        "Kannada": "ವೆಬ್‌ಸೈಟ್ ಅಸುರಕ್ಷಿತವಾಗಿದೆ (HTTPS ಸಂಪರ್ಕವಿಲ್ಲ)"
    },
    "OTP is requested together with an external link": {
        "English": "Dangerous combination: OTP requested alongside external link",
        "Hindi": "गंभीर खतरा: बाहरी लिंक के साथ ही OTP भी मांगा गया है",
        "Kannada": "ಗಂಭೀರ ಅಪಾಯ: ಬಾಹ್ಯ ಲಿಂಕ್ ಜೊತೆಗೆ OTP ಸಹ ಕೇಳಲಾಗಿದೆ"
    },
    "URL shortener detected": {
        "English": "URL shortener detected (bit.ly, tinyurl, etc.)",
        "Hindi": "शॉर्ट लिंक पाया गया (bit.ly, tinyurl आदि)",
        "Kannada": "ಶಾರ್ಟ್ ಲಿಂಕ್ ಪತ್ತೆಯಾಗಿದೆ (bit.ly, tinyurl ಇತ್ಯಾದಿ)"
    },
    "Brand impersonation detected": {
        "English": "Brand impersonation detected in web address",
        "Hindi": "वेब पते में बैंक या ब्रांड की नकल पाई गई",
        "Kannada": "ವೆಬ್ ವಿಳಾಸದಲ್ಲಿ ಬ್ರ್ಯಾಂಡ್ ಅಥವಾ ಬ್ಯಾಂಕ್ ನಕಲು ಪತ್ತೆಯಾಗಿದೆ"
    },
    "Raw IP address used instead of domain": {
        "English": "Raw IP address used instead of domain name",
        "Hindi": "डोमेन नाम के बजाय असुरक्षित IP एड्रेस का प्रयोग",
        "Kannada": "ಡೊಮೇನ್ ಹೆಸರಿನ ಬದಲು ನೇರ IP ವಿಳಾಸ ಬಳಸಲಾಗಿದೆ"
    },
    "Suspicious top-level domain": {
        "English": "Suspicious top-level domain (.xyz, .top, .live, etc.)",
        "Hindi": "संदिग्ध टॉप-लेवल डोमेन (.xyz, .top आदि)",
        "Kannada": "ಅನುಮಾನಾಸ್ಪದ ಡೊಮೇನ್ ವಿಸ್ತರಣೆ (.xyz, .top ಇತ್ಯಾದಿ)"
    },
    "Bank impersonation": {
        "English": "Impersonates a bank or financial entity",
        "Hindi": "बैंक या वित्तीय संस्था का नाम लेकर धोखा देने का प्रयास",
        "Kannada": "ಬ್ಯಾಂಕ್ ಅಥವಾ ಹಣಕಾಸು ಸಂಸ್ಥೆಯ ನಕಲಿ ಹೆಸರು ಬಳಕೆ"
    },
    "Suspicious link": {
        "English": "Unverified or suspicious web link present",
        "Hindi": "संदेहास्पद या असुरक्षित वेब लिंक मौजूद है",
        "Kannada": "ಅನುಮಾನಾಸ್ಪದ ವೆಬ್ ಲಿಂಕ್ ಕಂಡುಬಂದಿದೆ"
    },
    "Urgent payment request": {
        "English": "Urgent payment or monetary transfer demand",
        "Hindi": "तुरंत भुगतान या पैसे भेजने की मांग",
        "Kannada": "ತುರ್ತು ಹಣ ವರ್ಗಾವಣೆ ಬೇಡಿಕೆ"
    },
    "OTP request": {
        "English": "Demand for secret verification code (OTP)",
        "Hindi": "गोपनीय सुरक्षा कोड (OTP) की मांग",
        "Kannada": "ರಹಸ್ಯ OTP ನೀಡುವಂತೆ ಒತ್ತಾಯ"
    }
}

ACTION_TRANSLATIONS = {
    "Never share an OTP, PIN or password. No bank, police officer or company will ever ask for it.": {
        "English": "Never share an OTP, PIN or password. No bank, police officer or company will ever ask for it.",
        "Hindi": "अपना OTP, PIN या पासवर्ड कभी किसी को न बताएं। बैंक या पुलिस कभी इसे नहीं मांगते।",
        "Kannada": "ನಿಮ್ಮ OTP, PIN ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ಯಾರೊಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. ಬ್ಯಾಂಕ್ ಅಥವಾ ಪೊಲೀಸರು ಎಂದಿಗೂ ಇದನ್ನು ಕೇಳುವುದಿಲ್ಲ."
    },
    "Do not give out your bank account, card or identity numbers.": {
        "English": "Do not give out your bank account, card or identity numbers.",
        "Hindi": "अपना बैंक खाता, डेबिट कार्ड नंबर या आधार/पैन विवरण न साझा करें।",
        "Kannada": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆ, ಕಾರ್ಡ್ ಅಥವಾ ಆಧಾರ್ ಸಂಖ್ಯೆಯನ್ನು ಯಾರಿಗೂ ನೀಡಬೇಡಿ."
    },
    "Do not transfer money to anyone you have not confirmed in person or by a number you looked up yourself.": {
        "English": "Do not transfer money to anyone you have not confirmed in person or by an official number.",
        "Hindi": "किसी भी अनजान व्यक्ति को पैसे न भेजें जब तक कि आधिकारिक नंबर से पुष्टि न हो।",
        "Kannada": "ಅಧಿಕೃತ ಸಂಖ್ಯೆಯಿಂದ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳದೆ ಯಾವುದೇ ಅಪರಿಚಿತರಿಗೆ ಹಣ ವರ್ಗಾಯಿಸಬೇಡಿ."
    },
    "Do not click the link. Open the organisation's own app or type its address yourself.": {
        "English": "Do not click the link. Open the organisation's own verified app or official website directly.",
        "Hindi": "इस लिंक पर क्लिक न करें। केवल संस्था के आधिकारिक ऐप या वेबसाइट से ही संपर्क करें।",
        "Kannada": "ಲಿಂಕ್ ಮೇಲೆ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ. ಸಂಬಂಧಿತ ಸಂಸ್ಥೆಯ ಅಧಿಕೃತ ಆ್ಯಪ್ ಅಥವಾ ವೆಬ್‌ಸೈಟ್‌ಗೆ ನೇರವಾಗಿ ಭೇಟಿ ನೀಡಿ."
    },
    "Do not reply to this message and do not call any number it gives you.": {
        "English": "Do not reply to this message and do not call any phone number mentioned in it.",
        "Hindi": "इस संदेश का उत्तर न दें और इसमें दिए गए किसी भी फोन नंबर पर कॉल न करें।",
        "Kannada": "ಈ ಸಂದೇಶಕ್ಕೆ ಉತ್ತರಿಸಬೇಡಿ ಮತ್ತು ಇದರಲ್ಲಿ ನೀಡಿರುವ ಯಾವುದೇ ದೂರವಾಣಿ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಬೇಡಿ."
    },
    "Check with the organisation using the phone number printed on your card, bill or passbook.": {
        "English": "Verify with the organisation using the official helpline printed on your bank passbook or bill.",
        "Hindi": "अपनी पासबुक, कार्ड या आधिकारिक बिल पर छपे फोन नंबर से ही संबंधित संस्था से पुष्टि करें।",
        "Kannada": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಪಾಸ್‌ಬುಕ್ ಅಥವಾ ಬಿಲ್‌ನಲ್ಲಿ ಮುದ್ರಿಸಲಾದ ಅಧಿಕೃತ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ ಪರಿಶೀಲಿಸಿ."
    },
    "Confirm who really sent this before you respond or share anything.": {
        "English": "Confirm who really sent this before you respond or share any details.",
        "Hindi": "कोई भी उत्तर देने या जानकारी देने से पहले भेजने वाले की सत्यता परखें।",
        "Kannada": "ಯಾವುದೇ ವಿವರ ಹಂಚಿಕೊಳ್ಳುವ ಮೊದಲು ಸಂದೇಶ ಕಳುಹಿಸಿದವರು ಯಾರೆಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."
    },
    "Take your time. Genuine organisations do not rush you or threaten you.": {
        "English": "Take your time. Genuine organisations never rush you or threaten you.",
        "Hindi": "जल्दबाजी न करें। असली संस्थाएं कभी भी तुरंत कार्रवाई का दबाव या धमकी नहीं देतीं।",
        "Kannada": "ಸಮಾಧಾನವಾಗಿ ಯೋಚಿಸಿ. ನಿಜವಾದ ಬ್ಯಾಂಕುಗಳು ಎಂದಿಗೂ ಬೆದರಿಕೆ ಹಾಕಿ ಅವಸರ ಮಾಡುವುದಿಲ್ಲ."
    },
    "Report the message and block the sender, then delete it.": {
        "English": "Report the message and block the sender, then delete it safely.",
        "Hindi": "इस संदेश को 'Report Scam' करके प्रेषक को ब्लॉक करें और मिटा दें।",
        "Kannada": "ಸಂದೇಶವನ್ನು ರಿಪೋರ್ಟ್ ಮಾಡಿ ಕಳುಹಿಸಿದವರನ್ನು ಬ್ಲಾಕ್ ಮಾಡಿ ನಂತರ ಅಳಿಸಿಹಾಕಿ."
    },
    "Stay cautious with messages you were not expecting, even ones that look harmless.": {
        "English": "Stay cautious with unexpected messages, even if they appear harmless at first.",
        "Hindi": "अपेक्षित न होने वाले संदेशों के प्रति हमेशा सतर्क रहें।",
        "Kannada": "ನಿರೀಕ್ಷಿಸದ ಸಂದೇಶಗಳ ಬಗ್ಗೆ ಯಾವಾಗಲೂ ಎಚ್ಚರಿಕೆಯಿಂದಿರಿ."
    }
}

WARNING_TRANSLATIONS = {
    "Warning! This message may be fraudulent. Do not share OTPs, passwords or banking details.": {
        "English": "Warning! This message displays dangerous scam patterns. Do not click links or share secret details.",
        "Hindi": "सावधान! यह संदेश फर्जी हो सकता है। कोई भी लिंक न खोलें और न ही OTP या पासवर्ड साझा करें।",
        "Kannada": "ಎಚ್ಚರಿಕೆ! ಇದು ವಂಚನೆಯ ಸಂದೇಶವಾಗಿರಬಹುದು. ಯಾವುದೇ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ ಅಥವಾ OTP ನೀಡಬೇಡಿ."
    },
    "This message contains some suspicious elements. Verify the sender before responding.": {
        "English": "Caution: This message contains suspicious elements. Verify the sender before taking any action.",
        "Hindi": "सावधानी: इस संदेश में कुछ संदेहास्पद तत्व मिले हैं। किसी भी कार्रवाई से पूर्व पुष्टि करें।",
        "Kannada": "ಎಚ್ಚರಿಕೆ: ಈ ಸಂದೇಶದಲ್ಲಿ ಅನುಮಾನಾಸ್ಪದ ಅಂಶಗಳಿವೆ. ಖಚಿತಪಡಿಸಿಕೊಳ್ಳದೆ ಯಾವುದೇ ಕ್ರಮ ಕೈಗೊಳ್ಳಬೇಡಿ."
    },
    "No major suspicious activity was detected. Stay cautious.": {
        "English": "Safe & Normal: No major suspicious activity was detected. Stay cautious as usual.",
        "Hindi": "सामान्य एवं सुरक्षित: कोई बड़ा संदेहास्पद लक्षण नहीं मिला। सामान्य सतर्कता बनाए रखें।",
        "Kannada": "ಸಾಮಾನ್ಯ ಮತ್ತು ಸುರಕ್ಷಿತ: ಯಾವುದೇ ಪ್ರಮುಖ ಅಪಾಯದ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಎಂದಿನಂತೆ ಜಾಗರೂಕರಾಗಿರಿ."
    }
}

DAILY_SAFETY_TIPS = [
    {
        "English": "Banks never threaten to deactivate your account within hours over SMS. If you receive such a message, ignore it and visit your branch.",
        "Hindi": "बैंक कभी भी SMS द्वारा कुछ ही घंटों में खाता बंद करने की धमकी नहीं देते। ऐसा संदेश आने पर बैंक शाखा में जाकर ही संपर्क करें।",
        "Kannada": "ಬ್ಯಾಂಕ್‌ಗಳು ಎಂದಿಗೂ SMS ಮೂಲಕ ಕೆಲವೇ ಗಂಟೆಗಳಲ್ಲಿ ಖಾತೆ ರದ್ದು ಮಾಡುವುದಾಗಿ ಬೆದರಿಸುವುದಿಲ್ಲ. ಇಂತಹ ಸಂದೇಶ ಬಂದರೆ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ಭೇಟಿ ನೀಡಿ."
    },
    {
        "English": "Never enter your UPI PIN to receive money. UPI PIN is required ONLY to deduct money from your account, never to receive cashback or refunds.",
        "Hindi": "पैसे प्राप्त करने के लिए कभी भी UPI PIN दर्ज न करें। UPI PIN केवल आपके खाते से पैसे कटने के लिए आवश्यक होता है, पैसे आने के लिए नहीं।",
        "Kannada": "ಹಣ ಸ್ವೀಕರಿಸಲು ಎಂದಿಗೂ UPI PIN ನಮೂದಿಸಬೇಡಿ. UPI PIN ಕೇವಲ ನಿಮ್ಮ ಖಾತೆಯಿಂದ ಹಣ ಕಳುಹಿಸಲು ಮಾತ್ರ ಬೇಕಾಗುತ್ತದೆ."
    },
    {
        "English": "Electricity departments never send personal mobile numbers in SMS asking you to call a 'power officer'. Always pay bills via official portals.",
        "Hindi": "बिजली विभाग कभी भी SMS में किसी व्यक्तिगत मोबाइल नंबर पर कॉल करने को नहीं कहता। बिल हमेशा आधिकारिक पोर्टल या काउंटर से ही भरें।",
        "Kannada": "ವಿದ್ಯುತ್ ಇಲಾಖೆಯು SMS ನಲ್ಲಿ ವೈಯಕ್ತಿಕ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನೀಡಿ ಕರೆ ಮಾಡಲು ಹೇಳುವುದಿಲ್ಲ. ಅಧಿಕೃತ ಕೌಂಟರ್ ಅಥವಾ ಆ್ಯಪ್ ಮೂಲಕ ಮಾತ್ರ ಬಿಲ್ ಪಾವತಿಸಿ."
    },
    {
        "English": "If an unknown caller claims to be a police officer or CBI agent on video call, hang up immediately. Police never arrest anyone over WhatsApp.",
        "Hindi": "यदि कोई अनजान व्यक्ति वीडियो कॉल पर पुलिस या CBI अधिकारी बनकर डराए, तो तुरंत कॉल काटें। पुलिस कभी WhatsApp पर अरेस्ट नहीं करती।",
        "Kannada": "ಯಾರಾದರೂ ವಿಡಿಯೋ ಕಾಲ್‌ನಲ್ಲಿ ಪೊಲೀಸ್ ಅಥವಾ ಸಿಬಿಐ ಅಧಿಕಾರಿ ಎಂದು ಕರೆ ಮಾಡಿದರೆ ತಕ್ಷಣ ಕಾಲ್ ಕಟ್ ಮಾಡಿ. ಪೊಲೀಸರು ವಾಟ್ಸಾಪ್‌ನಲ್ಲಿ ಯಾರನ್ನೂ ಬಂಧಿಸುವುದಿಲ್ಲ."
    },
    {
        "English": "Never download screen-sharing apps like AnyDesk or TeamViewer on a stranger's advice. They allow criminals to view your passwords and empty your accounts.",
        "Hindi": "किसी अजनबी के कहने पर AnyDesk या TeamViewer जैसे रिमोट ऐप कभी डाउनलोड न करें। इससे धोखेबाज आपका फोन देखकर पैसे चुरा सकते हैं।",
        "Kannada": "ಅಪರಿಚಿತರ ಮಾತನ್ನು ನಂಬಿ AnyDesk ಅಥವಾ TeamViewer ಆ್ಯಪ್‌ಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಬೇಡಿ. ಇವುಗಳ ಮೂಲಕ ವಂಚಕರು ನಿಮ್ಮ ಬ್ಯಾಂಕಿಂಗ್ ಹಣವನ್ನು ದೋಚುತ್ತಾರೆ."
    }
]

SCAM_LIBRARY_ITEMS = [
    {
        "category": "Banking KYC Scam",
        "title": "SBI / HDFC KYC Expiry Notice",
        "message": "Dear customer, your bank account will be suspended today due to non-updated KYC. Click http://bit.ly/sbi-kyc-verify immediately.",
        "indicators": ["Bank Impersonation", "Artificial Urgency (Today)", "Hidden Shortened Link"],
        "advice": "Banks never send shortened bit.ly links. Update KYC only in branch or official mobile app."
    },
    {
        "category": "Electricity Bill Threat",
        "title": "Tonight 9:30 PM Power Cut Notice",
        "message": "Dear Consumer, your electricity will be disconnected tonight at 9:30 PM from the power office because your previous bill was not updated. Call our officer 9876543210 immediately.",
        "indicators": ["Threat of Utility Cut", "False Urgency (9:30 PM)", "Personal Mobile Number"],
        "advice": "Genuine electricity boards never provide personal mobile numbers in SMS. Verify on your official board website."
    },
    {
        "category": "Fake Job / Task Fraud",
        "title": "Part-Time YouTube Like Work",
        "message": "Part-time job vacancy: Earn ₹2500 per day by giving 5-star ratings on Google and liking YouTube channels. Work 15 minutes from home. WhatsApp now: 9123456789.",
        "indicators": ["Unrealistic Earnings", "Work-from-Home Bait", "Unverified WhatsApp Contact"],
        "advice": "These are structured Ponzi task scams that trick victims into depositing savings into fake crypto accounts."
    },
    {
        "category": "KBC / Lottery Fraud",
        "title": "₹25 Lakh Lucky Winner Alert",
        "message": "Congratulations! You have won ₹25,00,000 in the KBC All-India Lucky Draw. To claim your prize money, send ₹12,500 government processing tax to manager.",
        "indicators": ["Unsolicited Prize", "Demand for Upfront Processing Fee", "Fake Celebrity/Brand Name"],
        "advice": "Legitimate lotteries NEVER ask winners to pay upfront fees to claim prizes. This is 100% fraud."
    }
]


def t(key: str, lang: str = "English") -> str:
    """Safely fetch translation for given key in requested language."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    return lang_dict.get(key, TRANSLATIONS["English"].get(key, key))


def translate_risk_level(level: str, lang: str = "English") -> str:
    """Translate risk level token into localized human text."""
    norm = str(level).upper().strip()
    entry = RISK_LEVEL_TRANSLATIONS.get(norm, RISK_LEVEL_TRANSLATIONS["MEDIUM"])
    return entry.get(lang, entry["English"])


def translate_prediction(prediction: str, lang: str = "English") -> str:
    """Translate prediction token into localized text."""
    norm = str(prediction).upper().strip()
    entry = PREDICTION_TRANSLATIONS.get(norm, PREDICTION_TRANSLATIONS["UNKNOWN"])
    return entry.get(lang, entry["English"])


def translate_url_risk(risk: str, lang: str = "English") -> str:
    """Translate URL risk token into localized text."""
    norm = str(risk).upper().strip()
    entry = URL_RISK_TRANSLATIONS.get(norm, URL_RISK_TRANSLATIONS["UNKNOWN"])
    return entry.get(lang, entry["English"])


def translate_indicator(indicator: str, lang: str = "English") -> str:
    """Translate a risk indicator string if found in dictionary."""
    if indicator in INDICATOR_TRANSLATIONS:
        return INDICATOR_TRANSLATIONS[indicator].get(lang, indicator)
    for k, v in INDICATOR_TRANSLATIONS.items():
        if k.lower() in indicator.lower():
            return v.get(lang, indicator)
    return indicator


def translate_action(action: str, lang: str = "English") -> str:
    """Translate a recommended safety action string if found in dictionary."""
    if action in ACTION_TRANSLATIONS:
        return ACTION_TRANSLATIONS[action].get(lang, action)
    for k, v in ACTION_TRANSLATIONS.items():
        if k.lower() in action.lower():
            return v.get(lang, action)
    return action


def translate_warning(warning: str, lang: str = "English") -> str:
    """Translate a warning sentence if found in dictionary."""
    if warning in WARNING_TRANSLATIONS:
        return WARNING_TRANSLATIONS[warning].get(lang, warning)
    for k, v in WARNING_TRANSLATIONS.items():
        if k.lower() in warning.lower():
            return v.get(lang, warning)
    return warning


def translate_explanation(explanation: str, lang: str = "English", prediction: str = "SCAM") -> str:
    """Provide a fluent localized explanation for the AI model output."""
    if not explanation or lang == "English":
        return explanation or "The message has been analyzed by SilverShield AI's machine learning security engine."
    
    is_scam = "scam" in prediction.lower() or "suspicious" in explanation.lower() or "fraudulent" in explanation.lower()
    
    if lang == "Hindi":
        if is_scam:
            return "इस संदेश में फर्जीवाड़े और धोखाधड़ी से जुड़े संदेहास्पद भाषाई संकेत पाए गए हैं। साइबर अपराधी जल्दबाजी में निर्णय करवाने या गोपनीय जानकारी चुराने हेतु अक्सर ऐसे हथकंडों का उपयोग करते हैं।"
        else:
            return "यह संदेश सामान्य और सुरक्षित बातचीत जैसा प्रतीत होता है। इसमें धोखाधड़ी से जुड़ा कोई प्रमुख संदेहास्पद संकेत नहीं मिला है।"
    elif lang == "Kannada":
        if is_scam:
            return "ಈ ಸಂದೇಶದಲ್ಲಿ ವಂಚನೆ ಮತ್ತು ಅಕ್ರಮ ಕೃತ್ಯಗಳಿಗೆ ಸಂಬಂಧಿಸಿದ ಅನುಮಾನಾಸ್ಪದ ಭಾಷಾ ಮಾದರಿಗಳು ಕಂಡುಬಂದಿವೆ. ಅವಸರದಲ್ಲಿ ತೀರ್ಮಾನ ಕೈಗೊಳ್ಳುವಂತೆ ಮಾಡಲು ಅಥವಾ ರಹಸ್ಯ ವಿವರಗಳನ್ನು ಪಡೆಯಲು ವಂಚಕರು ಇಂತಹ ತಂತ್ರಗಳನ್ನು ಬಳಸುತ್ತಾರೆ."
        else:
            return "ಈ ಸಂದೇಶವು ಸಾಮಾನ್ಯ ಮತ್ತು ಸುರಕ್ಷಿತ ಸಂವಹನದಂತೆ ಕಂಡುಬರುತ್ತದೆ. ಇದರಲ್ಲಿ ಯಾವುದೇ ಪ್ರಮುಖ ವಂಚನೆಯ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ."
            
    return explanation
