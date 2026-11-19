"""
SilverShield AI - Secure AI-Powered Elderly Digital Safety Companion
Member 1: Frontend and Accessibility
"""

import streamlit as st
import json
import urllib.parse
import requests

from frontend.locales import LANGUAGES, TRANSLATIONS

st.set_page_config(
    page_title="SilverShield AI | Senior Digital Safety Companion",
    page_icon="https://img.icons8.com/color/48/shield.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

for key, default in {
    "font_size_choice": "Large (22px)",
    "high_contrast": False,
    "language": "English",
    "helper_name": "",
    "helper_relation": "",
    "helper_phone": "",
    "message_input": "",
    "chat_history": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

BACKEND_ASSESS_URL = "http://127.0.0.1:8000/api/v1/assess"
BACKEND_HEALTH_URL = "http://127.0.0.1:8000/health"

font_size_map = {"Standard (18px)": 18, "Large (22px)": 22, "Extra Large (26px)": 26}
fs = font_size_map.get(st.session_state.font_size_choice, 22)

if st.session_state.high_contrast:
    bg      = "#0D0D0D"; card_bg = "#1A1A1A"; txt    = "#FFFFFF"
    accent  = "#FFD700"; border  = "#FFFFFF"; sbg    = "#050505"
    hi_bg   = "#3D0000"; me_bg   = "#3D2E00"; lo_bg  = "#003320"
    hi_bdr  = "#FF4444"; me_bdr  = "#FFC107"; lo_bdr = "#22C55E"
    btn_bg  = "#FFD700"; btn_txt = "#000000"
    inp_bg  = "#1A1A1A"; inp_bdr = "#FFD700"
else:
    bg      = "#F0F4F8"; card_bg = "#FFFFFF"; txt    = "#1A2E44"
    accent  = "#1565C0"; border  = "#CBD5E1"; sbg    = "#0F3460"
    hi_bg   = "#FFF0F0"; me_bg   = "#FFFBEB"; lo_bg  = "#F0FFF4"
    hi_bdr  = "#DC2626"; me_bdr  = "#D97706"; lo_bdr = "#16A34A"
    btn_bg  = "#1565C0"; btn_txt = "#FFFFFF"
    inp_bg  = "#FFFFFF"; inp_bdr = "#94A3B8"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

*, *::before, *::after {{ box-sizing: border-box !important; }}

html, body {{
    overflow-x: hidden !important;
    width: 100% !important;
    max-width: 100vw !important;
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: {bg} !important;
    color: {txt} !important;
}}

/* ── Kill ALL Streamlit horizontal overflow sources ── */
.stApp, .stApp > div, section.main, section.main > div,
.block-container, [data-testid="stAppViewContainer"],
[data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {{
    max-width: 100% !important;
    overflow-x: hidden !important;
}}

.stApp {{ background-color: {bg} !important; }}

.block-container {{
    max-width: 100% !important;
    width: 100% !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}}

/* ── Streamlit columns: prevent overflow, allow wrap ── */
[data-testid="stHorizontalBlock"] {{
    flex-wrap: wrap !important;
    gap: 10px !important;
    width: 100% !important;
    overflow-x: hidden !important;
}}
[data-testid="stHorizontalBlock"] > div {{
    min-width: 140px !important;
    flex: 1 1 140px !important;
    overflow: hidden !important;
}}

p, span, label, li {{
    font-size: {fs}px !important;
    line-height: 1.75 !important;
    color: {txt} !important;
    word-break: break-word !important;
    overflow-wrap: anywhere !important;
}}
h1 {{
    font-size: {fs+14}px !important;
    font-weight: 800 !important; color: {accent} !important;
    margin-bottom: 6px !important; line-height: 1.2 !important;
    word-break: break-word !important;
}}
h2 {{
    font-size: {fs+8}px !important;
    font-weight: 700 !important; color: {accent} !important;
    line-height: 1.3 !important; word-break: break-word !important;
}}
h3 {{
    font-size: {fs+4}px !important;
    font-weight: 700 !important; color: {txt} !important;
    line-height: 1.35 !important; word-break: break-word !important;
}}

/* ── Buttons ── */
div.stButton > button {{
    min-height: 54px !important;
    padding: 10px 14px !important;
    font-size: {fs}px !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    border: 2px solid {border} !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    background-color: {card_bg} !important;
    color: {txt} !important;
    width: 100% !important;
    max-width: 100% !important;
    white-space: normal !important;
    word-break: break-word !important;
    overflow-wrap: anywhere !important;
    text-align: center !important;
    line-height: 1.4 !important;
    display: block !important;
    overflow: hidden !important;
}}
div.stButton > button:hover {{
    border-color: {accent} !important;
    color: {accent} !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}}
div.stButton > button[kind="primary"] {{
    background-color: {btn_bg} !important;
    color: {btn_txt} !important;
    border: 2px solid {btn_bg} !important;
}}
div.stButton > button[kind="primary"]:hover {{
    opacity: 0.88 !important; color: {btn_txt} !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background-color: {sbg} !important;
    border-right: 3px solid {accent};
}}
[data-testid="stSidebar"] > div {{
    overflow-x: hidden !important;
    width: 100% !important;
}}
[data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}
[data-testid="stSidebar"] .stRadio label {{
    font-size: {fs}px !important;
    padding: 6px 0 !important;
    white-space: normal !important;
    word-break: break-word !important;
}}

/* ── All custom HTML blocks: never overflow ── */
.ss-card, .ss-hero, .ss-rules-grid, .ss-rule-card,
.alert-high, .alert-med, .alert-low,
.ss-action-item, .ss-indicator, .ss-tip-card,
.ss-helpline, .ss-info-box, .ss-wa-btn,
.ss-status-online, .ss-status-offline {{
    max-width: 100% !important;
    overflow-x: hidden !important;
    word-break: break-word !important;
    overflow-wrap: anywhere !important;
    box-sizing: border-box !important;
}}

.ss-card {{
    background-color: {card_bg};
    border: 1.5px solid {border};
    border-radius: 16px;
    padding: 22px 20px;
    margin-bottom: 18px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    width: 100%;
}}

.ss-hero {{
    background: linear-gradient(135deg, {accent} 0%, #0D47A1 100%);
    border-radius: 16px;
    padding: 28px 22px;
    margin-bottom: 22px;
    width: 100%;
}}
.ss-hero h1, .ss-hero h2, .ss-hero p, .ss-hero span {{ color: #FFFFFF !important; }}
.ss-hero-inner {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}}

/* ── Rule cards: CSS grid that truly responds ── */
.ss-rules-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 18px;
    width: 100%;
}}
.ss-rule-card {{
    background-color: {card_bg};
    border-radius: 14px;
    padding: 22px 18px;
    border-top: 6px solid;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    text-align: center;
    width: 100%;
}}

.alert-high {{
    background-color: {hi_bg}; border-left: 8px solid {hi_bdr};
    border-radius: 12px; padding: 18px 16px;
    margin: 14px 0; width: 100%;
}}
.alert-med {{
    background-color: {me_bg}; border-left: 8px solid {me_bdr};
    border-radius: 12px; padding: 18px 16px;
    margin: 14px 0; width: 100%;
}}
.alert-low {{
    background-color: {lo_bg}; border-left: 8px solid {lo_bdr};
    border-radius: 12px; padding: 18px 16px;
    margin: 14px 0; width: 100%;
}}
.alert-inner {{
    display: flex; align-items: flex-start; gap: 10px;
    flex-wrap: wrap; margin-bottom: 8px;
}}
.alert-inner svg {{ flex-shrink: 0; margin-top: 2px; }}

.ss-action-item {{
    background-color: {lo_bg}; border: 1.5px solid {lo_bdr};
    border-radius: 10px; padding: 11px 14px; margin-bottom: 8px;
    font-size: {fs-1}px !important;
    color: {txt} !important; font-weight: 600;
    display: flex; align-items: flex-start; gap: 8px; width: 100%;
}}
.ss-action-item svg {{ flex-shrink: 0; margin-top: 2px; }}
.ss-indicator {{
    background-color: {hi_bg}; border: 1.5px solid {hi_bdr};
    border-radius: 10px; padding: 11px 14px; margin-bottom: 8px;
    font-size: {fs-1}px !important;
    color: {hi_bdr} !important; font-weight: 600;
    display: flex; align-items: flex-start; gap: 8px; width: 100%;
}}
.ss-indicator svg {{ flex-shrink: 0; margin-top: 2px; }}

.ss-tip-card {{
    background-color: {card_bg}; border: 1.5px solid {border};
    border-radius: 14px; padding: 18px 16px;
    margin-bottom: 14px; display: flex; gap: 14px; align-items: flex-start;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05); width: 100%;
    flex-wrap: wrap;
}}
.ss-tip-icon {{
    flex-shrink: 0; width: 52px; height: 52px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
}}
.ss-tip-body {{ flex: 1; min-width: 0; }}

.ss-helpline {{
    background: linear-gradient(135deg, #7B0000 0%, #C62828 100%);
    border-radius: 14px; padding: 22px 18px;
    margin-top: 18px; width: 100%;
}}
.ss-helpline * {{ color: #FFFFFF !important; }}
.ss-helpline-inner {{
    display: flex; align-items: center; gap: 10px;
    flex-wrap: wrap; margin-bottom: 10px;
}}
.ss-helpline-number {{
    display: flex; align-items: center; gap: 14px;
    flex-wrap: wrap; margin-top: 12px;
}}

.ss-status-online {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {lo_bg}; border: 1.5px solid {lo_bdr};
    border-radius: 30px; padding: 6px 14px;
    font-weight: 700; font-size: {fs-2}px !important;
    color: {lo_bdr} !important; margin-bottom: 14px;
    max-width: 100%;
}}
.ss-status-offline {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {me_bg}; border: 1.5px solid {me_bdr};
    border-radius: 30px; padding: 6px 14px;
    font-weight: 700; font-size: {fs-2}px !important;
    color: {me_bdr} !important; margin-bottom: 14px;
    max-width: 100%;
}}

textarea, input[type="text"] {{
    background-color: {inp_bg} !important; border: 2px solid {inp_bdr} !important;
    border-radius: 10px !important; font-size: {fs}px !important;
    color: {txt} !important; padding: 12px !important;
    width: 100% !important; max-width: 100% !important;
    box-sizing: border-box !important;
}}
.stTextArea textarea {{ min-height: 140px !important; }}
.stCheckbox label {{ font-size: {fs}px !important; }}
.stSelectbox div[data-baseweb="select"] {{
    font-size: {fs}px !important; border-radius: 10px !important;
}}

.ss-wa-btn {{
    display: flex; align-items: center; justify-content: center; gap: 10px;
    background-color: #25D366; color: white !important;
    padding: 14px 20px;
    font-size: {fs}px; font-weight: 700;
    border-radius: 12px; cursor: pointer; width: 100%;
    box-shadow: 0 3px 12px rgba(37,211,102,0.3);
    text-decoration: none; flex-wrap: wrap;
    box-sizing: border-box;
}}

.ss-brand {{
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0 6px 0; overflow: hidden;
}}
.ss-brand-text {{ min-width: 0; overflow: hidden; }}

.ss-info-box {{
    display: flex; align-items: flex-start; gap: 10px;
    background-color: {card_bg}; border: 1.5px solid {border};
    border-left: 6px solid {accent}; border-radius: 12px;
    padding: 16px 16px;
    margin-top: 8px; width: 100%;
}}
.ss-info-box svg {{ flex-shrink: 0; margin-top: 2px; }}
.ss-info-box p {{ min-width: 0; }}
</style>
""", unsafe_allow_html=True)

# ── SVG ICONS ──
ICONS = {
    "shield":  '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "lock":    '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "clock":   '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "people":  '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "police":  '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "bulb":    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2"><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
    "bank":    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>',
    "phone":   '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>',
    "speaker": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>',
    "whatsapp":'<svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>',
    "check":   '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>',
    "warn":    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "user":    '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "bot":     '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><line x1="12" y1="7" x2="12" y2="11"/><line x1="8" y1="15" x2="8.01" y2="15"/><line x1="16" y1="15" x2="16.01" y2="15"/></svg>',
    "gear":    '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "call":    '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.22h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.82a16 16 0 0 0 6.29 6.29l.96-.96a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "info":    '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{accent}" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
}


def render_audio_narrator(text_to_speak: str, lang_code: str, button_label: str = "Read this aloud"):
    escaped = json.dumps(text_to_speak, ensure_ascii=False)
    uid = abs(hash(text_to_speak[:30])) % 99999
    html = f"""
    <div style="margin:12px 0;">
      <button onclick="ssSpeak{uid}()" style="
          background-color:#1565C0;color:white;
          padding:clamp(10px,14px,16px) clamp(16px,22px,26px);
          font-size:clamp(13px,{fs}px,{fs+1}px);font-weight:700;
          border:none;border-radius:12px;cursor:pointer;
          display:inline-flex;align-items:center;gap:10px;
          box-shadow:0 3px 10px rgba(21,101,192,0.3);
          max-width:100%;white-space:normal;word-break:break-word;">
        {ICONS['speaker']} {button_label}
      </button>
      <script>
      function ssSpeak{uid}(){{
        if(!('speechSynthesis' in window)){{ alert('Audio not supported in this browser.'); return; }}
        window.speechSynthesis.cancel();
        var u=new SpeechSynthesisUtterance({escaped});
        u.lang='{lang_code}';u.rate=0.85;u.pitch=1.0;
        window.speechSynthesis.speak(u);
      }}
      </script>
    </div>"""
    st.components.v1.html(html, height=68)


def check_backend_health():
    try:
        r = requests.get(BACKEND_HEALTH_URL, timeout=1.5)
        return r.status_code == 200
    except Exception:
        return False


def run_local_fallback_assessment(message: str, lang: str):
    from backend.risk_engine import RiskAggregationEngine
    from backend.warning_generator import WarningGenerator
    from backend.integrations import IntegrationClient
    engine = RiskAggregationEngine()
    urls = IntegrationClient.extract_urls(message)
    has_url = len(urls) > 0
    tl = message.lower()
    is_scam = any(w in tl for w in ["blocked","suspended","kyc","otp","police","arrest","lottery","won","crore"])
    is_sus  = any("bit.ly" in u or "tinyurl" in u or "192.168" in u for u in urls)
    ml_pred = "SCAM" if is_scam else "LEGITIMATE"
    ml_conf = 0.88 if is_scam else 0.92
    url_risk = "SUSPICIOUS" if is_sus else ("SAFE" if has_url else "NO_URL")
    assessment = engine.aggregate_risk(
        message=message, ml_prediction=ml_pred, ml_confidence=ml_conf,
        ml_triggers=["Keyword Scam Pattern Detected"] if is_scam else [],
        ml_available=True, url_risk=url_risk,
        url_indicators=["Shortened / Masked URL"] if is_sus else [],
        urls_found=urls, url_available=True)
    overall_risk = assessment["overall_risk"]
    indicators   = assessment["risk_indicators"]
    warning  = WarningGenerator.generate_warning(overall_risk, indicators, lang)
    actions  = WarningGenerator.generate_recommended_actions(
        overall_risk, indicators, has_url=has_url, message_text=message, language=lang)
    return {
        "overall_risk": overall_risk.value, "message_prediction": ml_pred,
        "url_risk": url_risk, "risk_indicators": indicators,
        "warning": warning, "recommended_actions": actions,
        "risk_score": assessment["composite_score"],
        "module_status": {"ml_service": "STANDALONE_FALLBACK", "url_service": "STANDALONE_FALLBACK"}
    }


# ── SIDEBAR ──
with st.sidebar:
    st.markdown(f"""
    <div class="ss-brand">
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#FFD700" stroke-width="2.2" style="flex-shrink:0;">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
      <div class="ss-brand-text">
        <div style="font-size:clamp(16px,{fs+2}px,{fs+4}px);font-weight:800;color:#FFFFFF;white-space:nowrap;">SilverShield AI</div>
        <div style="font-size:clamp(11px,{fs-4}px,{fs-2}px);color:#CBD5E1;">Digital Safety Companion</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown(f"<div style='font-size:clamp(11px,{fs-3}px,{fs-1}px);font-weight:700;color:#94A3B8;letter-spacing:1px;margin-bottom:8px;'>LANGUAGE</div>", unsafe_allow_html=True)
    selected_language = st.selectbox(
        "Language", ["English", "Hindi", "Kannada"],
        index=["English", "Hindi", "Kannada"].index(st.session_state.language),
        label_visibility="collapsed"
    )
    st.session_state.language = selected_language
    t = TRANSLATIONS[selected_language]
    current_lang_code = LANGUAGES[selected_language]

    st.divider()
    st.markdown(f"<div style='font-size:clamp(11px,{fs-3}px,{fs-1}px);font-weight:700;color:#94A3B8;letter-spacing:1px;margin-bottom:8px;'>MENU</div>", unsafe_allow_html=True)
    nav_labels = {
        "home":     t["home"],
        "check":    t["check_message"],
        "tips":     t["safety_tips"],
        "helper":   t["trusted_helper"],
        "bot":      t["safety_bot"],
        "settings": t["settings"]
    }
    selected_page_label = st.radio("Menu", list(nav_labels.values()), label_visibility="collapsed")
    page_key = [k for k, v in nav_labels.items() if v == selected_page_label][0]

    st.divider()
    st.markdown(f"<div style='font-size:clamp(11px,{fs-3}px,{fs-1}px);font-weight:700;color:#94A3B8;letter-spacing:1px;margin-bottom:8px;'>ACCESSIBILITY</div>", unsafe_allow_html=True)
    st.session_state.high_contrast = st.toggle("High Contrast Mode", value=st.session_state.high_contrast)
    st.markdown(f"<div style='font-size:clamp(11px,{fs-4}px,{fs-2}px);color:#94A3B8;margin-top:14px;line-height:1.6;'>If you feel worried about a message, pause and ask someone you trust.</div>", unsafe_allow_html=True)


# ── HOME ──
if page_key == "home":
    st.markdown(f"""
    <div class="ss-hero">
      <div class="ss-hero-inner">
        {ICONS['shield']}
        <div style="flex:1;min-width:200px;">
          <h1 style="color:white!important;margin:0 0 6px 0;">{t["welcome_hero"]}</h1>
          <p style="color:rgba(255,255,255,0.88)!important;margin:0;font-size:clamp(14px,{fs+1}px,{fs+3}px);">{t["welcome_sub"]}</p>
        </div>
      </div>
      <p style="color:rgba(255,255,255,0.9)!important;margin:0;font-size:clamp(14px,{fs}px,{fs+1}px);">{t["welcome_desc"]}</p>
    </div>
    """, unsafe_allow_html=True)

    render_audio_narrator(f"{t['welcome_hero']}. {t['welcome_sub']}. {t['welcome_desc']}", current_lang_code)

    st.markdown(f"<h2 style='margin-bottom:18px;'>{t['card_rules_title']}</h2>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ss-rules-grid">
      <div class="ss-rule-card" style="border-top-color:#DC2626;">
        <div style="margin-bottom:12px;">{ICONS['lock']}</div>
        <div style="font-size:clamp(10px,{fs-4}px,{fs-2}px);font-weight:800;color:#DC2626;letter-spacing:1px;margin-bottom:6px;">RULE 1</div>
        <h3 style="color:{txt}!important;margin-bottom:8px;">{t['rule_1_title']}</h3>
        <p style="color:{txt}!important;margin:0;">{t['rule_1_desc']}</p>
      </div>
      <div class="ss-rule-card" style="border-top-color:#D97706;">
        <div style="margin-bottom:12px;">{ICONS['clock']}</div>
        <div style="font-size:clamp(10px,{fs-4}px,{fs-2}px);font-weight:800;color:#D97706;letter-spacing:1px;margin-bottom:6px;">RULE 2</div>
        <h3 style="color:{txt}!important;margin-bottom:8px;">{t['rule_2_title']}</h3>
        <p style="color:{txt}!important;margin:0;">{t['rule_2_desc']}</p>
      </div>
      <div class="ss-rule-card" style="border-top-color:#16A34A;">
        <div style="margin-bottom:12px;">{ICONS['people']}</div>
        <div style="font-size:clamp(10px,{fs-4}px,{fs-2}px);font-weight:800;color:#16A34A;letter-spacing:1px;margin-bottom:6px;">RULE 3</div>
        <h3 style="color:{txt}!important;margin-bottom:8px;">{t['rule_3_title']}</h3>
        <p style="color:{txt}!important;margin:0;">{t['rule_3_desc']}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ss-info-box">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="{accent}" stroke-width="2.5" style="flex-shrink:0;margin-top:2px;">
        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <p style="margin:0;font-weight:600;">Tip: Select <b>Check a Message</b> from the left menu to verify any suspicious SMS or WhatsApp message you received.</p>
    </div>
    """, unsafe_allow_html=True)


# ── CHECK A MESSAGE ──
elif page_key == "check":
    st.markdown(f"<h1>{t['check_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:clamp(14px,{fs}px,{fs+1}px);margin-bottom:18px;'>{t['check_subtitle']}</p>", unsafe_allow_html=True)

    is_live_backend = check_backend_health()
    if is_live_backend:
        st.markdown(f'<div class="ss-status-online"><svg width="10" height="10" viewBox="0 0 10 10"><circle cx="5" cy="5" r="5" fill="#16A34A"/></svg>{t["backend_connected"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ss-status-offline"><svg width="10" height="10" viewBox="0 0 10 10"><circle cx="5" cy="5" r="5" fill="#D97706"/></svg>{t["backend_fallback"]}</div>', unsafe_allow_html=True)

    st.markdown(f"<h3 style='margin-bottom:12px;'>{t['sample_prompts_label']}</h3>", unsafe_allow_html=True)

    samples = [
        (t["sample_sbi"],   "URGENT: Your SBI netbanking account is suspended due to expired KYC. Update immediately at http://bit.ly/sbi-kyc-verify to prevent permanent block."),
        (t["sample_otp"],   "Your one time password (OTP) is 748291. Share this with the bank executive on call to cancel unauthorized debit of Rs 15,000."),
        (t["sample_power"], "Dear consumer, your electricity connection will be disconnected tonight at 9:30 PM because previous bill was unpaid. Call officer immediately at 9876543210."),
        (t["sample_legit"], "Hi Grandma, I have reached home safely from college. See you for dinner at 8 PM!"),
    ]

    for i, (label, msg) in enumerate(samples):
        if st.button(label, key=f"sample_{i}", use_container_width=True):
            st.session_state.message_input = msg
            st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    user_message = st.text_area(
        t["message_box_label"],
        value=st.session_state.message_input,
        placeholder=t["message_box_placeholder"],
        height=150
    )

    check_clicked = st.button(t["btn_check"], type="primary", use_container_width=True)
    if st.button(t["btn_clear"], use_container_width=True):
        st.session_state.message_input = ""
        st.rerun()

    if check_clicked:
        clean_text = user_message.strip()
        if not clean_text:
            st.warning("Please paste or type a message first.")
        else:
            with st.spinner("Analyzing message safety..."):
                assessment_data = None
                if is_live_backend:
                    try:
                        resp = requests.post(BACKEND_ASSESS_URL,
                            json={"message": clean_text, "language": selected_language}, timeout=4.0)
                        if resp.status_code == 200:
                            assessment_data = resp.json()
                    except Exception as e:
                        st.warning(f"Could not reach live backend: {e}. Using standalone mode.")
                if not assessment_data:
                    assessment_data = run_local_fallback_assessment(clean_text, selected_language)

            risk_level = assessment_data.get("overall_risk", "MEDIUM")
            warning    = assessment_data.get("warning", "")
            actions    = assessment_data.get("recommended_actions", [])
            indicators = assessment_data.get("risk_indicators", [])
            risk_score = assessment_data.get("risk_score", 0.5)

            st.markdown("---")

            if risk_level == "HIGH":
                icon_svg = f'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="{hi_bdr}" stroke-width="2.5" style="flex-shrink:0;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
                st.markdown(f"""
                <div class="alert-high">
                  <div class="alert-inner">{icon_svg}<h2 style="color:{hi_bdr}!important;margin:0;">{t['risk_high_title']}</h2></div>
                  <p style="font-size:clamp(14px,{fs+1}px,{fs+2}px);font-weight:700;color:{txt}!important;margin:0;">{warning}</p>
                </div>""", unsafe_allow_html=True)
            elif risk_level == "MEDIUM":
                icon_svg = f'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="{me_bdr}" stroke-width="2.5" style="flex-shrink:0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
                st.markdown(f"""
                <div class="alert-med">
                  <div class="alert-inner">{icon_svg}<h2 style="color:{me_bdr}!important;margin:0;">{t['risk_med_title']}</h2></div>
                  <p style="font-size:clamp(14px,{fs+1}px,{fs+2}px);font-weight:700;color:{txt}!important;margin:0;">{warning}</p>
                </div>""", unsafe_allow_html=True)
            else:
                icon_svg = f'<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="{lo_bdr}" stroke-width="2.5" style="flex-shrink:0;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
                st.markdown(f"""
                <div class="alert-low">
                  <div class="alert-inner">{icon_svg}<h2 style="color:{lo_bdr}!important;margin:0;">{t['risk_low_title']}</h2></div>
                  <p style="font-size:clamp(14px,{fs+1}px,{fs+2}px);font-weight:700;color:{txt}!important;margin:0;">{warning}</p>
                </div>""", unsafe_allow_html=True)

            render_audio_narrator(f"{warning}. " + " ".join(actions), current_lang_code, button_label=t["read_aloud_btn"])

            st.markdown(f"<h3 style='margin-top:18px;margin-bottom:10px;'>{t['actions_title']}</h3>", unsafe_allow_html=True)
            for action in actions:
                st.markdown(f'<div class="ss-action-item">{ICONS["check"]} <span>{action}</span></div>', unsafe_allow_html=True)

            if indicators:
                st.markdown(f"<h3 style='margin-top:18px;margin-bottom:10px;'>{t['indicators_title']}</h3>", unsafe_allow_html=True)
                for ind in indicators:
                    st.markdown(f'<div class="ss-indicator">{ICONS["warn"]} <span>{ind}</span></div>', unsafe_allow_html=True)

            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            helper_phone = st.session_state.helper_phone.strip()
            helper_name  = st.session_state.helper_name.strip() or "Caregiver"
            if helper_phone:
                encoded_msg = urllib.parse.quote(
                    f"{t['helper_whatsapp_msg']}\n\n\"{clean_text[:120]}...\"\n\nResult: {risk_level} Risk.\nWarning: {warning}")
                wa_url = f"https://wa.me/{helper_phone}?text={encoded_msg}"
                st.markdown(f"""
                <a href="{wa_url}" target="_blank" style="text-decoration:none;display:block;">
                  <div class="ss-wa-btn">{ICONS['whatsapp']} Alert {helper_name} via WhatsApp</div>
                </a>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ss-info-box">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{me_bdr}" stroke-width="2.5" style="flex-shrink:0;margin-top:2px;">
                    <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  <p style="margin:0;font-weight:600;">Add your trusted family member's phone number under <b>Trusted Helper</b> in the menu to alert them in one tap.</p>
                </div>""", unsafe_allow_html=True)

            with st.expander(t["technical_details"]):
                st.write("**Overall Risk Level:**", risk_level)
                st.write("**Risk Score (0.0 to 1.0):**", round(risk_score, 4))
                st.write("**ML Classification (Member 2):**", assessment_data.get("message_prediction"))
                st.write("**URL Threat Level (Member 3):**", assessment_data.get("url_risk"))
                st.write("**Module Status:**", assessment_data.get("module_status"))
                st.json(assessment_data)


# ── SCAM AWARENESS ──
elif page_key == "tips":
    st.markdown(f"<h1>{t['tips_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:clamp(14px,{fs}px,{fs+1}px);margin-bottom:22px;'>{t['tips_sub']}</p>", unsafe_allow_html=True)

    scams = [
        (t["scam_1_title"], t["scam_1_desc"], ICONS["police"], "#DC2626"),
        (t["scam_2_title"], t["scam_2_desc"], ICONS["bulb"],   "#D97706"),
        (t["scam_3_title"], t["scam_3_desc"], ICONS["bank"],   "#1565C0"),
        (t["scam_4_title"], t["scam_4_desc"], ICONS["phone"],  "#7C3AED"),
    ]
    for title, desc, icon, color in scams:
        st.markdown(f"""
        <div class="ss-tip-card">
          <div class="ss-tip-icon" style="background:{color}18;">{icon}</div>
          <div class="ss-tip-body">
            <h3 style="color:{color}!important;margin:0 0 8px 0;">{title}</h3>
            <p style="margin:0;">{desc}</p>
          </div>
        </div>""", unsafe_allow_html=True)

    render_audio_narrator(". ".join(f"{t}: {d}" for t, d, _, __ in scams), current_lang_code)


# ── TRUSTED HELPER ──
elif page_key == "helper":
    st.markdown(f"<h1>{t['helper_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:clamp(14px,{fs}px,{fs+1}px);margin-bottom:22px;'>{t['helper_sub']}</p>", unsafe_allow_html=True)

    with st.form("helper_form"):
        h_name  = st.text_input(t["helper_name"],    value=st.session_state.helper_name)
        h_rel   = st.text_input(t["helper_relation"], value=st.session_state.helper_relation)
        h_phone = st.text_input(t["helper_phone"],    value=st.session_state.helper_phone,
                                placeholder="e.g. 919876543210 (with country code)")
        save_btn = st.form_submit_button("Save Details", type="primary")

    if save_btn:
        st.session_state.helper_name     = h_name.strip()
        st.session_state.helper_relation = h_rel.strip()
        st.session_state.helper_phone    = h_phone.strip()
        st.success(t["helper_saved"])

    st.divider()

    if st.session_state.helper_name:
        st.markdown(f"""
        <div class="ss-card">
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:12px;flex-wrap:wrap;">
            <div style="width:52px;height:52px;background:{accent}18;border-radius:50%;
                 display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              {ICONS['user']}
            </div>
            <div>
              <h3 style="margin:0;">{st.session_state.helper_name}</h3>
              <p style="margin:0;color:#64748B;">{st.session_state.helper_relation or 'Relationship not specified'}</p>
            </div>
          </div>
          <p style="margin:0;"><b>Contact:</b> {st.session_state.helper_phone or 'No number provided'}</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="ss-card">
          <p style="margin:0;color:#64748B;">No helper added yet. Fill in the form above to save your trusted contact.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="ss-helpline">
      <div class="ss-helpline-inner">
        {ICONS['call']}
        <h2 style="color:white!important;margin:0;">{t['emergency_helpline_title']}</h2>
      </div>
      <p style="color:rgba(255,255,255,0.9)!important;margin-bottom:0;">{t['emergency_helpline_desc']}</p>
      <div class="ss-helpline-number">
        <a href="tel:1930" style="text-decoration:none;">
          <div style="background:white;color:#C62828;font-size:clamp(28px,{fs+12}px,{fs+16}px);
               font-weight:900;border-radius:12px;padding:12px 28px;
               display:inline-block;letter-spacing:3px;">1930</div>
        </a>
        <span style="color:rgba(255,255,255,0.85);font-size:clamp(12px,{fs-2}px,{fs}px);">Toll-Free, 24 hours, 7 days</span>
      </div>
    </div>""", unsafe_allow_html=True)


# ── AI COMPANION ──
elif page_key == "bot":
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;flex-wrap:wrap;">
      {ICONS['bot']}
      <h1 style="margin:0;">AI Safety Companion</h1>
    </div>
    <p style="font-size:clamp(14px,{fs}px,{fs+1}px);margin-bottom:22px;">Ask any question about staying safe on your phone or internet.</p>
    """, unsafe_allow_html=True)

    sample_questions = [
        "What should I do if someone calls asking for my OTP?",
        "Someone sent a link saying my electricity will be cut. Is it real?",
        "A caller says they are from Mumbai Police on video call. What should I do?",
        "Can a stranger steal my money if I install AnyDesk?",
    ]

    st.markdown(f"<h3 style='margin-bottom:12px;'>Common questions — tap to ask:</h3>", unsafe_allow_html=True)
    for i, sq in enumerate(sample_questions):
        if st.button(sq, key=f"sq_{i}", use_container_width=True):
            st.session_state.bot_input = sq

    user_query = st.text_input("Type or choose your question:", value=st.session_state.get("bot_input", ""))

    if st.button("Ask Companion", type="primary"):
        if not user_query.strip():
            st.warning("Please enter a question.")
        else:
            q = user_query.lower()
            if any(w in q for w in ["otp", "pin", "password"]):
                ans = "Never share your OTP or PIN with anyone. Banks and police never ask for your secret code. If someone on a call is asking for it, hang up immediately and dial 1930."
            elif any(w in q for w in ["electricity", "power", "bill"]):
                ans = "This is a very common scam. Scammers send fake disconnection threats to create panic. Do not call numbers in the SMS. Pay your electricity bill only through your official electricity board app or office."
            elif any(w in q for w in ["police", "cbi", "arrest", "video call"]):
                ans = "This is the Digital Arrest scam. Police or judges never hold trials or ask for money over WhatsApp or video calls. Immediately disconnect the call and dial 1930."
            elif any(w in q for w in ["anydesk", "teamviewer", "screen share"]):
                ans = "Never install AnyDesk or TeamViewer if a stranger asks you to. These apps let fraudsters see your screen, watch you enter passwords, and steal your money."
            else:
                ans = "Take your time. If a message or caller is asking for money, passwords, or threatening you, stop and show it to your trusted family member. You do not have to act in a rush."

            st.markdown(f"""
            <div class="ss-card" style="border-left:6px solid {accent};margin-top:14px;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap;">
                {ICONS['bot']}
                <h3 style="margin:0;">SilverShield Companion Answer</h3>
              </div>
              <p style="margin:0;font-size:clamp(14px,{fs}px,{fs+1}px);">{ans}</p>
            </div>""", unsafe_allow_html=True)
            render_audio_narrator(ans, current_lang_code)


# ── SETTINGS ──
elif page_key == "settings":
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;flex-wrap:wrap;">
      {ICONS['gear']}
      <h1 style="margin:0;">{t['settings_title']}</h1>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<h3 style='margin-top:22px;margin-bottom:12px;'>{t['font_size_label']}</h3>", unsafe_allow_html=True)
    chosen_size = st.radio(
        "Font Size",
        ["Standard (18px)", "Large (22px)", "Extra Large (26px)"],
        index=["Standard (18px)", "Large (22px)", "Extra Large (26px)"].index(st.session_state.font_size_choice)
    )
    if chosen_size != st.session_state.font_size_choice:
        st.session_state.font_size_choice = chosen_size
        st.rerun()

    st.divider()
    st.markdown(f"<h3 style='margin-bottom:12px;'>{t['contrast_label']}</h3>", unsafe_allow_html=True)
    hc_val = st.toggle("Enable High Contrast Mode (WCAG AAA)", value=st.session_state.high_contrast)
    if hc_val != st.session_state.high_contrast:
        st.session_state.high_contrast = hc_val
        st.rerun()

    st.divider()
    if st.button(t["restore_defaults"]):
        st.session_state.font_size_choice = "Large (22px)"
        st.session_state.high_contrast    = False
        st.session_state.language         = "English"
        st.rerun()
