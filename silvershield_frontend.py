
import streamlit as st
import re
import json

st.set_page_config(
    page_title="SilverShield AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SETTINGS ----------------

if "large_text" not in st.session_state:
    st.session_state.large_text = True

if "high_contrast" not in st.session_state:
    st.session_state.high_contrast = False

if "helper_name" not in st.session_state:
    st.session_state.helper_name = ""

if "helper_phone" not in st.session_state:
    st.session_state.helper_phone = ""

if "chat" not in st.session_state:
    st.session_state.chat = []

if "checked_count" not in st.session_state:
    st.session_state.checked_count = 0

# ---------------- LANGUAGES ----------------

LANGUAGES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Kannada": "kn-IN"
}

WORDS = {
    "English": {
        "welcome": "Welcome to SilverShield AI",
        "tagline": "Stay safe online. Take your time.",
        "intro": "Simple help for staying safe when using your phone or the internet.",
        "home": "Home",
        "check": "Check a Message",
        "tips": "Safety Tips",
        "helper": "Trusted Helper",
        "assistant": "AI Assistant",
        "settings": "Easy Reading",
        "language": "Language",
        "larger": "Use larger text",
        "contrast": "High contrast",
        "message_title": "Check a Message",
        "message_help": "Paste a message below. We will look for common warning signs.",
        "message_placeholder": "Paste your text message here...",
        "check_button": "Check Message",
        "clear": "Clear",
        "safe_note": "Not sure? It is okay to ask someone you trust.",
        "audio": "Read this aloud",
        "question": "What would you like help with?",
        "send": "Ask",
        "helper_intro": "Save the details of a family member or trusted person.",
        "name": "Name",
        "phone": "Phone number",
        "save": "Save Details",
        "saved": "Trusted person saved for this session.",
        "assistant_intro": "Hello. You can ask me about online safety. I will use simple words.",
        "disclaimer": "Student project demo. This is not connected to a live AI model."
    },
    "Hindi": {
        "welcome": "SilverShield AI में आपका स्वागत है",
        "tagline": "इंटरनेट पर सुरक्षित रहें। आराम से समय लें।",
        "intro": "मोबाइल और इंटरनेट का सुरक्षित उपयोग करने में आसान मदद।",
        "home": "मुख्य पृष्ठ",
        "check": "संदेश जाँचें",
        "tips": "सुरक्षा सुझाव",
        "helper": "भरोसेमंद व्यक्ति",
        "assistant": "AI सहायक",
        "settings": "आसान पढ़ाई",
        "language": "भाषा",
        "larger": "बड़े अक्षर",
        "contrast": "गहरा रंग",
        "message_title": "संदेश जाँचें",
        "message_help": "संदेश यहाँ डालें। हम खतरे के सामान्य संकेत देखेंगे।",
        "message_placeholder": "अपना संदेश यहाँ डालें...",
        "check_button": "संदेश जाँचें",
        "clear": "हटाएँ",
        "safe_note": "शक हो तो किसी भरोसेमंद व्यक्ति से मदद लें।",
        "audio": "यह सुनें",
        "question": "आपको किस बारे में मदद चाहिए?",
        "send": "पूछें",
        "helper_intro": "परिवार के किसी सदस्य या भरोसेमंद व्यक्ति की जानकारी रखें।",
        "name": "नाम",
        "phone": "फ़ोन नंबर",
        "save": "जानकारी सहेजें",
        "saved": "जानकारी इस सत्र के लिए सहेजी गई।",
        "assistant_intro": "नमस्ते। आप इंटरनेट सुरक्षा के बारे में पूछ सकते हैं।",
        "disclaimer": "यह छात्र परियोजना का डेमो है। यह लाइव AI मॉडल से जुड़ा नहीं है।"
    },
    "Kannada": {
        "welcome": "SilverShield AI ಗೆ ಸ್ವಾಗತ",
        "tagline": "ಆನ್‌ಲೈನ್‌ನಲ್ಲಿ ಸುರಕ್ಷಿತವಾಗಿರಿ. ನಿಧಾನವಾಗಿ ಮಾಡಿ.",
        "intro": "ಮೊಬೈಲ್ ಮತ್ತು ಇಂಟರ್ನೆಟ್ ಅನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ಬಳಸಲು ಸರಳ ಸಹಾಯ.",
        "home": "ಮುಖಪುಟ",
        "check": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "tips": "ಸುರಕ್ಷತಾ ಸಲಹೆಗಳು",
        "helper": "ನಂಬಿಕೆಯ ವ್ಯಕ್ತಿ",
        "assistant": "AI ಸಹಾಯಕ",
        "settings": "ಸುಲಭ ಓದು",
        "language": "ಭಾಷೆ",
        "larger": "ದೊಡ್ಡ ಅಕ್ಷರಗಳು",
        "contrast": "ಹೆಚ್ಚಿನ ಕಾಂಟ್ರಾಸ್ಟ್",
        "message_title": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "message_help": "ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಹಾಕಿ. ಅಪಾಯದ ಸಾಮಾನ್ಯ ಸೂಚನೆಗಳನ್ನು ಪರಿಶೀಲಿಸುತ್ತೇವೆ.",
        "message_placeholder": "ನಿಮ್ಮ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಹಾಕಿ...",
        "check_button": "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
        "clear": "ಅಳಿಸಿ",
        "safe_note": "ಸಂದೇಹವಿದ್ದರೆ, ನೀವು ನಂಬುವ ವ್ಯಕ್ತಿಯ ಸಹಾಯ ಕೇಳಿ.",
        "audio": "ಇದನ್ನು ಕೇಳಿ",
        "question": "ನಿಮಗೆ ಯಾವ ಸಹಾಯ ಬೇಕು?",
        "send": "ಕೇಳಿ",
        "helper_intro": "ಕುಟುಂಬದ ಸದಸ್ಯರ ಅಥವಾ ನಂಬಿಕೆಯ ವ್ಯಕ್ತಿಯ ವಿವರಗಳನ್ನು ಉಳಿಸಿ.",
        "name": "ಹೆಸರು",
        "phone": "ದೂರವಾಣಿ ಸಂಖ್ಯೆ",
        "save": "ವಿವರಗಳನ್ನು ಉಳಿಸಿ",
        "saved": "ಈ ಸೆಷನ್‌ಗಾಗಿ ವಿವರಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ.",
        "assistant_intro": "ನಮಸ್ಕಾರ. ಆನ್‌ಲೈನ್ ಸುರಕ್ಷತೆ ಬಗ್ಗೆ ನೀವು ಕೇಳಬಹುದು.",
        "disclaimer": "ಇದು ವಿದ್ಯಾರ್ಥಿ ಯೋಜನೆಯ ಮಾದರಿ. ನೈಜ AI ಮಾದರಿಗೆ ಸಂಪರ್ಕಿಸಿಲ್ಲ."
    }
}

# ---------------- DESIGN ----------------

font_size = 21 if st.session_state.large_text else 17
background = "#FFFFFF" if st.session_state.high_contrast else "#F2F7FC"
foreground = "#111111" if st.session_state.high_contrast else "#153B5B"

st.markdown(f"""
<style>
.stApp {{
    background: {background};
    color: {foreground};
}}
html, body, [class*="css"] {{
    font-size: {font_size}px !important;
}}
h1, h2, h3 {{
    color: #064B78;
}}
h1 {{ font-size: 36px !important; }}
h2 {{ font-size: 29px !important; }}
p, label, li {{
    line-height: 1.6 !important;
}}
div.stButton > button {{
    min-height: 48px;
    font-size: 18px !important;
    border-radius: 9px;
    border: 1px solid #17699B;
}}
div.stButton > button[kind="primary"] {{
    background: #075B8D;
    color: white;
}}
[data-testid="stSidebar"] {{
    background: #07385F;
}}
[data-testid="stSidebar"] * {{
    color: white;
}}
[data-testid="stMetric"] {{
    background: white;
    padding: 16px;
    border: 1px solid #C8DFEF;
    border-radius: 12px;
}}
.info-card {{
    background: white;
    border: 1px solid #C8DFEF;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 12px;
}}
.welcome-card {{
    background: #DDF1FF;
    border: 1px solid #B7DDF5;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 18px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- AUDIO ----------------

def read_aloud(text, language):
    speech_text = json.dumps(text, ensure_ascii=False)
    speech_language = LANGUAGES[language]

    st.components.v1.html(
        f"""
        <button onclick="speakPage()"
        style="background:#075B8D;color:white;padding:12px 18px;
        border:0;border-radius:8px;font-size:18px;cursor:pointer;">
        {WORDS[language]["audio"]}
        </button>
        <script>
        function speakPage() {{
            if (!("speechSynthesis" in window)) {{
                alert("Audio is not supported by this browser.");
                return;
            }}
            window.speechSynthesis.cancel();
            const message = new SpeechSynthesisUtterance({speech_text});
            message.lang = "{speech_language}";
            message.rate = 0.85;
            window.speechSynthesis.speak(message);
        }}
        </script>
        """,
        height=60
    )

# ---------------- MESSAGE CHECKER ----------------

def find_warnings(message):
    checks = [
        (r"\b(otp|verification code|one time password)\b",
         "The message mentions a code. Never share your OTP."),
        (r"\b(password|pin|cvv|bank details)\b",
         "It mentions private account details. Keep these secret."),
        (r"\b(won a prize|lottery winner|claim your prize)\b",
         "Unexpected prize offers can be scams. Verify them first."),
        (r"\b(send money|transfer money|pay immediately|urgent payment)\b",
         "It pressures you to pay. Pause and verify before paying."),
        (r"\b(account blocked|account suspended|bank account frozen)\b",
         "This may be a frightening warning. Contact your bank through its official number."),
        (r"\b(click here|verify now|claim now)\b",
         "It asks you to click or act quickly. Check the sender first."),
        (r"\b(remote access|install this app|screen sharing)\b",
         "Be careful if a stranger asks to control your phone.")
    ]

    return [
        explanation for pattern, explanation in checks
        if re.search(pattern, message, re.IGNORECASE)
    ]

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## SilverShield AI")
    st.caption("Your digital safety companion")
    st.divider()

    language = st.selectbox(
        "Language / भाषा / ಭಾಷೆ",
        ["English", "Hindi", "Kannada"]
    )

    t = WORDS[language]

    page = st.radio(
        "Menu",
        [
            t["home"],
            t["check"],
            t["tips"],
            t["helper"],
            t["assistant"],
            t["settings"]
        ]
    )

    st.divider()
    st.write("Need help?")
    st.write("Take your time. You can ask someone you trust.")

# Match translated menu labels to page names
pages = {
    WORDS[lang][key]: key
    for lang in WORDS
    for key in ["home", "check", "tips", "helper", "assistant", "settings"]
}
current_page = pages[page]

# ---------------- HOME ----------------

if current_page == "home":
    st.markdown(f"""
    <div class="welcome-card">
        <h1>{t["welcome"]}</h1>
        <h2>{t["tagline"]}</h2>
        <p>{t["intro"]}</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("### Check a Message")
        st.write("Find warning signs in a text or email.")
        st.markdown("### Safety Tips")
        st.write("Learn simple ways to protect your money and information.")

    with right:
        st.markdown("### Trusted Helper")
        st.write("Keep a trusted person's contact details handy.")
        st.markdown("### AI Assistant")
        st.write("Ask questions about online safety in simple words.")

    st.divider()
    st.subheader("Three things to remember")

    st.markdown("""
    <div class="info-card">
    <b>Keep your OTP private.</b><br>
    Never tell your code to a caller or stranger.
    </div>
    <div class="info-card">
    <b>Do not rush.</b><br>
    A message asking for urgent payment may be suspicious.
    </div>
    <div class="info-card">
    <b>Ask someone you trust.</b><br>
    You do not have to deal with a worrying message alone.
    </div>
    """, unsafe_allow_html=True)

    read_aloud(t["intro"], language)
    st.caption(t["disclaimer"])

# ---------------- CHECK MESSAGE ----------------

elif current_page == "check":
    st.title(t["message_title"])
    st.write(t["message_help"])

    message = st.text_area(
        t["message_placeholder"],
        height=180,
        key="message_input"
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        check_clicked = st.button(
            t["check_button"],
            type="primary",
            use_container_width=True
        )

    with col2:
        if st.button(t["clear"], use_container_width=True):
            st.session_state.message_input = ""
            st.rerun()

    if check_clicked:
        if not message.strip():
            st.warning("Please paste a message first.")
        else:
            st.session_state.checked_count += 1
            warnings = find_warnings(message)

            if warnings:
                st.warning("Please be careful. We found possible warning signs.")
                for warning in warnings:
                    st.markdown(f"- {warning}")
                st.info(
                    "Do not pay or share private details yet. Verify the request "
                    "with the real organisation using its official contact details."
                )
            else:
                st.info(
                    "No common warning signs were found. This does not prove "
                    "the message is safe. Check the sender before taking action."
                )

    st.info(t["safe_note"])
    read_aloud(t["safe_note"], language)
    st.caption(t["disclaimer"])

# ---------------- SAFETY TIPS ----------------

elif current_page == "tips":
    st.title(t["tips"])

    lessons = [
        ("Keep your OTP private",
         "Never share a one-time code with a caller or stranger."),
        ("Be careful with bank calls",
         "If a caller asks for your PIN or password, end the call and contact your bank using its official number."),
        ("Check links first",
         "Do not open unexpected links. Visit the official website yourself."),
        ("Check before paying",
         "Make sure you know who will receive your money before sending it."),
        ("Be careful with prizes",
         "Unexpected prizes that ask for money or private details may be a scam."),
        ("Ask for help",
         "If you are unsure, pause and ask someone you trust.")
    ]

    for title, explanation in lessons:
        st.markdown(
            f"""
            <div class="info-card">
                <h3>{title}</h3>
                <p>{explanation}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    read_aloud(" ".join(title + ". " + text for title, text in lessons), language)

# ---------------- TRUSTED HELPER ----------------

elif current_page == "helper":
    st.title(t["helper"])
    st.write(t["helper_intro"])

    with st.form("helper_form"):
        name = st.text_input(t["name"], value=st.session_state.helper_name)
        phone = st.text_input(t["phone"], value=st.session_state.helper_phone)
        submitted = st.form_submit_button(t["save"], type="primary")

    if submitted:
        st.session_state.helper_name = name.strip()
        st.session_state.helper_phone = phone.strip()
        st.success(t["saved"])

    st.divider()
    st.subheader("Your trusted person")

    if st.session_state.helper_name:
        st.markdown("### " + st.session_state.helper_name)
        if st.session_state.helper_phone:
            st.write("Phone: " + st.session_state.helper_phone)
    else:
        st.write("No trusted person added yet.")

    st.caption(
        "Demo note: these details stay in the current app session. "
        "They are not permanently saved or sent to anyone."
    )

# ---------------- AI ASSISTANT DEMO ----------------

elif current_page == "assistant":
    st.title(t["assistant"])
    st.write(t["assistant_intro"])

    st.markdown("""
    <div class="info-card">
    You can ask questions such as:
    <ul>
    <li>Is this message suspicious?</li>
    <li>How can I keep my bank account safe?</li>
    <li>What should I do if someone asks for my OTP?</li>
    <li>How can I avoid online payment scams?</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        t["question"],
        placeholder="Type your question here..."
    )

    if st.button(t["send"], type="primary"):
        if not question.strip():
            st.warning("Please type a question.")
        else:
            q = question.lower()

            if any(word in q for word in ["otp", "code", "pin", "password"]):
                answer = (
                    "Keep your OTP, PIN and password private. "
                    "Do not share them with a caller or stranger."
                )
            elif any(word in q for word in ["money", "payment", "bank", "transfer"]):
                answer = (
                    "Do not rush to send money. Check the recipient and contact "
                    "your bank using its official number if you are unsure."
                )
            elif any(word in q for word in ["link", "message", "scam", "suspicious"]):
                answer = (
                    "Do not open unknown links or reply with private details. "
                    "Check the sender and ask someone you trust if you are unsure."
                )
            else:
                answer = (
                    "I am a simple demo assistant, so I may not know the answer. "
                    "Pause if you feel unsure and ask someone you trust."
                )

            st.markdown("### Answer")
            st.write(answer)
            read_aloud(answer, language)

    st.caption(t["disclaimer"])

# ---------------- ACCESSIBILITY ----------------

elif current_page == "settings":
    st.title(t["settings"])
    st.write("Choose the settings that make this page easier for you.")

    st.session_state.large_text = st.toggle(
        t["larger"],
        value=st.session_state.large_text
    )

    st.session_state.high_contrast = st.toggle(
        t["contrast"],
        value=st.session_state.high_contrast
    )

    st.divider()
    st.subheader("Audio")

    read_aloud(
        "Welcome to SilverShield AI. Take your time. "
        "If something feels wrong, stop and ask someone you trust.",
        language
    )

    st.caption(
        "Audio depends on your browser and the voices installed on your device. "
        "Hindi and Kannada voices may not be available on every device."
    )

    if st.button("Restore default settings"):
        st.session_state.large_text = True
        st.session_state.high_contrast = False
        st.rerun()
