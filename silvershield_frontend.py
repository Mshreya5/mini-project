"""
SilverShield AI - Secure AI-Powered Elderly Digital Safety Companion
Clean, elegant, modern light-theme application with Purple + White + Lavender palette.
Navigation is powered exclusively by a top-right Three-Dot Menu (⋮) with zero emojis.
"""

from __future__ import annotations

import json
import logging
import re
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from frontend.locales import (
    DAILY_SAFETY_TIPS,
    LANGUAGES,
    SCAM_LIBRARY_ITEMS,
    TRANSLATIONS,
    t,
    translate_action,
    translate_explanation,
    translate_indicator,
    translate_prediction,
    translate_risk_level,
    translate_url_risk,
    translate_warning,
)
from frontend.styles import ICONS, get_css
from frontend.components import (
    log_analysis_history,
    render_audio_narrator,
    render_caregiver_share,
    render_helpline_banner,
    render_risk_card,
    render_safety_actions,
    render_threat_indicators,
)

logger = logging.getLogger("silvershield.frontend")

st.set_page_config(
    page_title="SilverShield AI | Senior Digital Safety Companion",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DEFAULTS = {
    "font_size_choice": "Standard (15px)",
    "high_contrast": False,
    "language": "English",
    "helper_name": "",
    "helper_relation": "",
    "helper_phone": "",
    "message_input": "",
    "url_input": "",
    "daily_tip_idx": 0,
    "analysis_history": [],
    "quiz_submitted": False,
    "quiz_answers": {},
    "active_nav": "nav_dashboard",
    "last_message_result": None,
    "last_url_result": None,
    "auth_token": "",
    "auth_user": None,
}

for k, val in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = val

FONT_MAP = {
    "Compact (14px)": 14,
    "Standard (15px)": 15,
    "Large (17px)": 17,
}
current_fs = FONT_MAP.get(st.session_state.font_size_choice, 15)
lang = st.session_state.language
lang_code = LANGUAGES.get(lang, "en-IN")

st.markdown(get_css(font_size=current_fs, high_contrast=st.session_state.high_contrast), unsafe_allow_html=True)

BACKEND_BASE_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
BACKEND_HEALTH_URL = f"{BACKEND_BASE_URL}/health"
BACKEND_ANALYZE_URL = f"{BACKEND_BASE_URL}/api/v1/analyze"
URL_SERVICE_URL = os.environ.get("URL_SERVICE_URL", "http://127.0.0.1:8002/analyze-url")
SCAM_SERVICE_URL = os.environ.get("SCAM_SERVICE_URL", "http://127.0.0.1:8001/predict")


def check_live_backend() -> bool:
    try:
        parsed = urllib.parse.urlparse(BACKEND_BASE_URL)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        with socket.create_connection((host, port), timeout=0.2):
            return True
    except Exception:
        return False


def run_integrated_analysis(message_text: str, url_override: Optional[str] = None) -> Dict[str, Any]:
    is_live = check_live_backend()
    if is_live:
        try:
            payload = {
                "message": message_text.strip(),
                "url": url_override.strip() if url_override else None,
                "language": lang,
                "consent_given": True,
            }
            resp = requests.post(BACKEND_ANALYZE_URL, json=payload, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                data["source"] = "live_api"
                return data
        except Exception as e:
            logger.warning("Live API call failed: %s; falling back to direct engine.", e)

    from ai_module.src.predict import predict_message
    from url_analysis.analyzer import analyze_url
    from app.clients.scam_detector import parse_message_payload
    from app.clients.url_analyzer import parse_url_payload
    from app.core.models import RemoteCallResult, ModuleState
    from app.core.orchestrator import RiskAggregator
    from app.schemas import AnalyzeRequest
    from app.settings import Settings, get_risk_config

    class InProcessScamClient:
        def analyze(self, msg: str):
            res = predict_message(msg)
            analysis = parse_message_payload(res)
            return RemoteCallResult(state=ModuleState.OK, data=analysis, latency_ms=12)

    class InProcessUrlClient:
        def analyze(self, target_url: str):
            res = analyze_url(target_url)
            u_dict = {
                "url": res.url,
                "url_found": res.url_found,
                "suspicious": res.suspicious,
                "risk_score": res.risk_score,
                "risk_indicators": res.risk_indicators,
                "explanation": res.explanation
            }
            payload = {"results": [u_dict]}
            analysis = parse_url_payload(payload, target_url)
            return RemoteCallResult(state=ModuleState.OK, data=analysis, latency_ms=8)

    cfg = get_risk_config()
    aggregator = RiskAggregator(
        scam_client=InProcessScamClient(),
        url_client=InProcessUrlClient(),
        config=cfg,
        settings=Settings()
    )

    req = AnalyzeRequest(
        message=message_text.strip(),
        url=url_override.strip() if url_override else None,
        language=lang,
        consent_given=True
    )
    result = aggregator.aggregate(req)

    clean_indicators = []
    if result.scam_analysis and result.scam_analysis.indicators:
        clean_indicators.extend(result.scam_analysis.indicators)
    if result.url_analysis and result.url_analysis.indicators:
        clean_indicators.extend(result.url_analysis.indicators)

    raw_conf = result.scam_analysis.confidence if result.scam_analysis else None
    if raw_conf is not None and raw_conf > 1.0:
        raw_conf = raw_conf / 100.0

    return {
        "overall_risk_score": result.score,
        "overall_risk_level": result.level.value,
        "is_scam": result.scam_analysis.is_scam if result.scam_analysis else False,
        "message_prediction": result.scam_analysis.prediction if result.scam_analysis else "UNKNOWN",
        "message_confidence": raw_conf,
        "url_risk": result.url_analysis.risk_level if result.url_analysis else "NOT_APPLICABLE",
        "url_score": result.url_analysis.raw_score if result.url_analysis else 0,
        "risk_score": result.score / 100.0,
        "warning": result.action_advice.warning_message if result.action_advice else "Stay cautious.",
        "explanation": result.explanation or "Analysis completed by SilverShield AI safety engine.",
        "risk_indicators": clean_indicators,
        "recommended_actions": result.action_advice.recommended_actions if result.action_advice else [
            "Do not click unknown links or share credentials.",
            "Verify suspicious messages with a trusted family member."
        ],
        "source": "local_engine"
    }


def run_standalone_url_analysis(target_url: str) -> Dict[str, Any]:
    clean_url = target_url.strip()
    try:
        with socket.create_connection(("127.0.0.1", 8002), timeout=0.08):
            resp = requests.post(URL_SERVICE_URL, json={"url": clean_url}, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                data["source"] = "url_api"
                return data
    except Exception:
        pass

    from url_analysis.analyzer import analyze_url
    ar = analyze_url(clean_url)
    return {
        "url": ar.url,
        "url_found": ar.url_found,
        "suspicious": ar.suspicious,
        "risk_score": ar.risk_score,
        "risk_indicators": ar.risk_indicators,
        "explanation": ar.explanation,
        "source": "local_analyzer"
    }


nav_sections = [
    ("nav_dashboard", t("nav_dashboard", lang), ICONS['home']),
    ("nav_message_checker", t("nav_message_checker", lang), ICONS['message']),
    ("nav_url_checker", t("nav_url_checker", lang), ICONS['globe']),
    ("nav_awareness", t("nav_awareness", lang), ICONS['shield_check']),
    ("nav_safety_guide", t("nav_safety_guide", lang), ICONS['book']),
    ("nav_settings", t("nav_settings", lang), ICONS['settings']),
    ("nav_account", t("nav_account", lang), ICONS['lock']),
]

header_col1, header_col2 = st.columns([8, 2], vertical_alignment="center")

with header_col1:
    is_live = check_live_backend()
    status_text = t("system_status_live", lang) if is_live else t("system_status_fallback", lang)
    status_badge = "ss-badge-teal" if is_live else "ss-badge-purple"
    
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding:6px 0;">
      <div style="display:flex; align-items:center; gap:8px;">
        {ICONS['shield_main']}
        <span style="font-size:19px; font-weight:800; color:#49316F; letter-spacing:-0.4px;">SilverShield AI</span>
      </div>
      <span style="color:#D8CBEF; font-size:13px;">|</span>
      <span style="font-size:13px; color:#777185; font-weight:500;">{t('app_tagline', lang)}</span>
      <span class="ss-badge {status_badge}" style="margin-left:6px;">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

with header_col2:
    btn_sub_c1, btn_sub_c2 = st.columns([1, 1], vertical_alignment="center")
    
    with btn_sub_c1:
        is_set_active = (st.session_state.active_nav == "nav_settings")
        if st.button("Settings", key="quick_top_settings_btn", type="primary" if is_set_active else "secondary", use_container_width=True):
            st.session_state.active_nav = "nav_settings"
            st.rerun()

    with btn_sub_c2:
        with st.popover("⋮", use_container_width=True):
            st.markdown(f"<div style='font-size:11px; font-weight:700; color:#49316F; text-transform:uppercase; margin-bottom:8px; letter-spacing:0.4px;'>Menu Options</div>", unsafe_allow_html=True)
            for nav_key, nav_title, nav_icon in nav_sections:
                is_active = (st.session_state.active_nav == nav_key)
                
                n_c1, n_c2 = st.columns([1, 6], vertical_alignment="center")
                with n_c1:
                    st.markdown(f"<div style='display:flex; align-items:center; justify-content:center; padding-top:4px;'>{nav_icon}</div>", unsafe_allow_html=True)
                with n_c2:
                    if st.button(nav_title, key=f"popnav_{nav_key}", type="primary" if is_active else "secondary", use_container_width=True):
                        st.session_state.active_nav = nav_key
                        st.rerun()


if st.session_state.active_nav == "nav_dashboard":
    st.markdown(f"""
    <div class="ss-welcome-card">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
        <div>
          <span class="ss-badge ss-badge-purple" style="margin-bottom:6px;">AI-Powered Protection</span>
          <h1 style="color:#49316F !important; margin:4px 0 6px 0; font-size:23px;">{t('dash_hero_title', lang)}</h1>
          <p style="color:#292438 !important; font-size:14px; margin:0; max-width:860px; line-height:1.55;">
            {t('dash_hero_sub', lang)}
          </p>
        </div>
      </div>
    </div>
    <p style="font-size:clamp(14px,{fs}px,{fs+1}px);margin-bottom:22px;">Ask any question about staying safe on your phone or internet.</p>
    """, unsafe_allow_html=True)

    narrator_col, cta_col = st.columns([1, 2], vertical_alignment="center")
    with narrator_col:
        welcome_speech = f"{t('dash_hero_title', lang)}. {t('dash_hero_sub', lang)}"
        render_audio_narrator(welcome_speech, lang_code, button_label=t("msg_btn_narrate", lang), font_size=current_fs)
    with cta_col:
        cta1, cta2 = st.columns(2)
        with cta1:
            if st.button("Check a Message Now", key="dash_cta_msg", type="primary", use_container_width=True):
                st.session_state.active_nav = "nav_message_checker"
                st.rerun()
        with cta2:
            if st.button("Inspect a Web Link", key="dash_cta_url", use_container_width=True):
                st.session_state.active_nav = "nav_url_checker"
                st.rerun()

    st.markdown(f"<h2 style='font-size:18px; margin-top:20px; margin-bottom:12px;'>{t('dash_actions_heading', lang)}</h2>", unsafe_allow_html=True)
    
    card_row1_col1, card_row1_col2 = st.columns(2)
    
    with card_row1_col1:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #7653B5; min-height:165px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              {ICONS['message']}
              <h3 style="margin:0; font-size:15px; color:#49316F;">{t('dash_action_msg_title', lang)}</h3>
            </div>
            <p style="color:#777185; font-size:13px; margin:0 0 12px 0; line-height:1.45;">
              Scan suspicious WhatsApp texts, bank alerts, electricity notices, or lottery claims using machine learning. Get instant explanations and safety advice.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("dash_action_msg_btn", lang), key="btn_dash_msg_explore", type="primary", use_container_width=True):
            st.session_state.active_nav = "nav_message_checker"
            st.rerun()

    with card_row1_col2:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #49316F; min-height:165px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              {ICONS['globe']}
              <h3 style="margin:0; font-size:15px; color:#49316F;">{t('dash_action_url_title', lang)}</h3>
            </div>
            <p style="color:#777185; font-size:13px; margin:0 0 12px 0; line-height:1.45;">
              Inspect unfamiliar links and web addresses before you click. Detect lookalike phishing domains, deceptive IP URLs, brand impersonation, and hidden redirects.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(t("dash_action_url_btn", lang), key="btn_dash_url_explore", use_container_width=True):
            st.session_state.active_nav = "nav_url_checker"
            st.rerun()

    card_row2_col1, card_row2_col2 = st.columns(2)

    with card_row2_col1:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #0D9488; min-height:165px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              {ICONS['shield_check']}
              <h3 style="margin:0; font-size:15px; color:#0D9488;">{t('dash_action_aware_title', lang)}</h3>
            </div>
            <p style="color:#777185; font-size:13px; margin:0 0 12px 0; line-height:1.45;">
              Explore real-world case studies of digital arrest calls, fake KYC updates, lottery prize traps, and task frauds. Learn simple defenses to stay completely secure.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Awareness", key="btn_dash_aware_explore", use_container_width=True):
            st.session_state.active_nav = "nav_awareness"
            st.rerun()

    with card_row2_col2:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #DC2626; min-height:165px; display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              {ICONS['book']}
              <h3 style="margin:0; font-size:15px; color:#DC2626;">Elderly Safety Guide & Quiz</h3>
            </div>
            <p style="color:#777185; font-size:13px; margin:0 0 12px 0; line-height:1.45;">
              Learn practical emergency protocols if an OTP was shared or money was sent. Test your fraud detection readiness with an interactive 4-question scam quiz.
            </p>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Safety Guide", key="btn_dash_guide_explore", use_container_width=True):
            st.session_state.active_nav = "nav_safety_guide"
            st.rerun()

    tip_idx = st.session_state.daily_tip_idx % len(DAILY_SAFETY_TIPS)
    current_tip = DAILY_SAFETY_TIPS[tip_idx].get(lang, DAILY_SAFETY_TIPS[tip_idx]["English"])

    st.markdown(f"""
    <div class="ss-card" style="background:#FAF7FF; border:1px solid #D8CBEF; margin-top:14px;">
      <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
        {ICONS['bulb']}
        <span style="font-size:11px; font-weight:700; color:#7653B5; text-transform:uppercase; letter-spacing:0.4px;">
          {t('dash_tip_badge', lang)}
        </span>
      </div>
      <p style="font-weight:600; font-size:14px; margin:0; color:#49316F; line-height:1.5;">
        {current_tip}
      </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(t("dash_tip_next_btn", lang), key="btn_next_tip"):
        st.session_state.daily_tip_idx = (st.session_state.daily_tip_idx + 1) % len(DAILY_SAFETY_TIPS)
        st.rerun()

    st.markdown(f"<h2 style='font-size:17px; margin-top:20px; margin-bottom:12px;'>{t('dash_rules_heading', lang)}</h2>", unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3px solid #DC2626; text-align:center; min-height:145px;">
          <div style="display:flex; justify-content:center; margin-bottom:6px;">{ICONS['lock']}</div>
          <span style="font-size:11px; font-weight:700; color:#DC2626; letter-spacing:0.4px;">RULE 1</span>
          <h3 style="margin:4px 0; font-size:14px; color:#49316F;">{t('rule_1_title', lang)}</h3>
          <p style="font-size:12.5px; color:#777185; margin:0; line-height:1.45;">{t('rule_1_desc', lang)}</p>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3px solid #D97706; text-align:center; min-height:145px;">
          <div style="display:flex; justify-content:center; margin-bottom:6px;">{ICONS['alert_triangle']}</div>
          <span style="font-size:11px; font-weight:700; color:#D97706; letter-spacing:0.4px;">RULE 2</span>
          <h3 style="margin:4px 0; font-size:14px; color:#49316F;">{t('rule_2_title', lang)}</h3>
          <p style="font-size:12.5px; color:#777185; margin:0; line-height:1.45;">{t('rule_2_desc', lang)}</p>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3px solid #10B981; text-align:center; min-height:145px;">
          <div style="display:flex; justify-content:center; margin-bottom:6px;">{ICONS['user_caregiver']}</div>
          <span style="font-size:11px; font-weight:700; color:#10B981; letter-spacing:0.4px;">RULE 3</span>
          <h3 style="margin:4px 0; font-size:14px; color:#49316F;">{t('rule_3_title', lang)}</h3>
          <p style="font-size:12.5px; color:#777185; margin:0; line-height:1.45;">{t('rule_3_desc', lang)}</p>
        </div>
        """, unsafe_allow_html=True)

    render_helpline_banner(lang, current_fs)


elif st.session_state.active_nav == "nav_message_checker":
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">
      {ICONS['message']}
      <h1 style="margin:0; font-size:22px; color:#49316F;">{t('msg_title', lang)}</h1>
    </div>
    <p style="color:#777185; font-size:13.5px; margin-bottom:14px;">{t('msg_subtitle', lang)}</p>
    """, unsafe_allow_html=True)

    st.markdown(f"<span style='font-size:12px; font-weight:700; color:#777185;'>{t('msg_sample_label', lang)}</span>", unsafe_allow_html=True)
    sample_cols = st.columns(3)
    samples = [
        ("Bank KYC Threat", "URGENT: Your SBI netbanking account is suspended due to expired KYC. Update immediately at http://bit.ly/sbi-kyc-verify to prevent permanent block."),
        ("Electricity Cutoff", "Dear consumer, your electricity connection will be disconnected tonight at 9:30 PM because previous bill was unpaid. Call power officer immediately at 9876543210."),
        ("Legitimate Family", "Hi Grandma, reached home safely from college. Dad said we will go out for dinner together at 8 PM!"),
    ]
    for i, (s_label, s_text) in enumerate(samples):
        with sample_cols[i]:
            if st.button(s_label, key=f"smp_{i}", use_container_width=True):
                st.session_state.message_input = s_text
                st.rerun()

    user_msg = st.text_area(
        t("msg_input_label", lang),
        value=st.session_state.message_input,
        placeholder=t("msg_placeholder", lang),
        key="main_msg_textarea",
        height=95
    )

    btn_c1, btn_c2 = st.columns([4, 1])
    with btn_c1:
        analyze_clicked = st.button(t("msg_btn_analyze", lang), type="primary", use_container_width=True)
    with btn_c2:
        clear_clicked = st.button(t("msg_btn_clear", lang), use_container_width=True)

    if clear_clicked:
        st.session_state.message_input = ""
        st.session_state.last_message_result = None
        st.rerun()

    if analyze_clicked:
        if not user_msg.strip():
            st.warning(t("msg_input_required", lang))
        else:
            with st.spinner(t("msg_analyzing", lang)):
                result = run_integrated_analysis(user_msg)
                st.session_state.last_message_result = result
                
                log_analysis_history(
                    input_type="Message",
                    content=user_msg.strip(),
                    risk_level=result.get("overall_risk_level", "SAFE"),
                    score=result.get("risk_score", 0.0)
                )

    res = st.session_state.last_message_result
    if res:
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='font-size:18px; color:#49316F;'>{t('msg_results_heading', lang)}</h2>", unsafe_allow_html=True)

        overall_risk = res.get("overall_risk_level", "SAFE")
        warning = res.get("warning", "")
        risk_score = res.get("risk_score", 0.0)
        prediction = res.get("message_prediction", "UNKNOWN")
        confidence = res.get("message_confidence")
        explanation = res.get("explanation", "")
        indicators = res.get("risk_indicators", [])
        actions = res.get("recommended_actions", [])

        render_risk_card(overall_risk, warning, risk_score, lang=lang, font_size=current_fs)

        narration_text = f"{translate_warning(warning, lang)}. " + " ".join(translate_action(a, lang) for a in actions[:3])
        render_audio_narrator(narration_text, lang_code, button_label=t("msg_btn_narrate", lang), font_size=current_fs)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="ss-card" style="padding:12px; text-align:center;">
              <span style="font-size:11px; font-weight:700; color:#777185; text-transform:uppercase; letter-spacing:0.3px;">{t('res_prediction', lang)}</span>
              <div style="font-size:16px; font-weight:800; color:#7653B5; margin-top:3px;">
                {translate_prediction(prediction, lang)}
              </div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            conf_str = f"{int(confidence * 100)}%" if confidence is not None else "N/A"
            st.markdown(f"""
            <div class="ss-card" style="padding:12px; text-align:center;">
              <span style="font-size:11px; font-weight:700; color:#777185; text-transform:uppercase; letter-spacing:0.3px;">{t('res_confidence', lang)}</span>
              <div style="font-size:16px; font-weight:800; color:#49316F; margin-top:3px;">
                {conf_str}
              </div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="ss-card" style="padding:12px; text-align:center;">
              <span style="font-size:11px; font-weight:700; color:#777185; text-transform:uppercase; letter-spacing:0.3px;">{t('res_risk_score', lang)}</span>
              <div style="font-size:16px; font-weight:800; color:#B45309; margin-top:3px;">
                {round(risk_score, 2)} / 1.00
              </div>
            </div>
            """, unsafe_allow_html=True)

        localized_exp = translate_explanation(explanation, lang=lang, prediction=prediction)
        st.markdown(f"""
        <div class="ss-card" style="border-left:3.5px solid #7653B5; background:#FAF7FF;">
          <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
            {ICONS['brain']}
            <h3 style="margin:0; color:#49316F !important; font-size:14px;">{t('res_explanation_title', lang)}</h3>
          </div>
          <p style="margin:0; font-size:13.5px; line-height:1.55; color:#292438;">
            {localized_exp}
          </p>
        </div>
        """, unsafe_allow_html=True)

        ind_col, act_col = st.columns(2)
        with ind_col:
            st.markdown(f"<h3 style='font-size:15px; color:#49316F;'>{t('res_indicators_title', lang)}</h3>", unsafe_allow_html=True)
            render_threat_indicators(indicators, lang=lang)

        with act_col:
            st.markdown(f"<h3 style='font-size:15px; color:#49316F;'>{t('res_actions_title', lang)}</h3>", unsafe_allow_html=True)
            render_safety_actions(actions, lang=lang)

        render_caregiver_share(
            helper_name=st.session_state.helper_name,
            helper_phone=st.session_state.helper_phone,
            message_text=user_msg,
            risk_level=overall_risk,
            warning_text=translate_warning(warning, lang),
            lang=lang
        )


elif st.session_state.active_nav == "nav_url_checker":
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">
      {ICONS['globe']}
      <h1 style="margin:0; font-size:22px; color:#49316F;">{t('url_title', lang)}</h1>
    </div>
    <p style="color:#777185; font-size:13.5px; margin-bottom:14px;">{t('url_subtitle', lang)}</p>
    """, unsafe_allow_html=True)

    st.markdown(f"<span style='font-size:12px; font-weight:700; color:#777185;'>{t('url_sample_label', lang)}</span>", unsafe_allow_html=True)
    u_cols = st.columns(3)
    u_samples = [
        ("Fake Bank Site", "http://sbi-kyc-verification.top/login.php"),
        ("Shortened Link", "http://bit.ly/claim-lottery-gift"),
        ("Official Portal", "https://onlinesbi.sbi"),
    ]
    for i, (u_lbl, u_val) in enumerate(u_samples):
        with u_cols[i]:
            if st.button(u_lbl, key=f"usmp_{i}", use_container_width=True):
                st.session_state.url_input = u_val
                st.rerun()

    user_url = st.text_input(
        t("url_input_label", lang),
        value=st.session_state.url_input,
        placeholder="https://example.com/verify-account",
        key="main_url_input"
    )

    u_btn_c1, u_btn_c2 = st.columns([4, 1])
    with u_btn_c1:
        u_analyze_clicked = st.button(t("url_btn_analyze", lang), type="primary", use_container_width=True)
    with u_btn_c2:
        u_clear_clicked = st.button(t("msg_btn_clear", lang), key="u_clear", use_container_width=True)

    if u_clear_clicked:
        st.session_state.url_input = ""
        st.session_state.last_url_result = None
        st.rerun()

    if u_analyze_clicked:
        if not user_url.strip():
            st.warning(t("url_input_required", lang))
        else:
            with st.spinner(t("url_analyzing", lang)):
                url_res = run_standalone_url_analysis(user_url.strip())
                st.session_state.last_url_result = url_res
                
                risk_lvl = "HIGH" if url_res.get("risk_score", 0) >= 3 else ("MEDIUM" if url_res.get("suspicious") else "LOW")
                log_analysis_history(
                    input_type="URL",
                    content=user_url.strip(),
                    risk_level=risk_lvl,
                    score=min(1.0, url_res.get("risk_score", 0) / 4.0)
                )

    u_res = st.session_state.last_url_result
    if u_res:
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='font-size:18px; color:#49316F;'>{t('url_res_heading', lang)}</h2>", unsafe_allow_html=True)

        is_suspicious = u_res.get("suspicious", False)
        risk_score = u_res.get("risk_score", 0)
        analyzed_url = u_res.get("url", "")
        url_indicators = u_res.get("risk_indicators", [])
        explanation = u_res.get("explanation", "")

        if risk_score >= 3:
            url_level = "HIGH"
            level_banner_class = "alert-high"
            level_text = translate_url_risk("MALICIOUS", lang)
        elif is_suspicious or risk_score >= 1:
            url_level = "MEDIUM"
            level_banner_class = "alert-med"
            level_text = translate_url_risk("SUSPICIOUS", lang)
        else:
            url_level = "LOW"
            level_banner_class = "alert-low"
            level_text = translate_url_risk("SAFE", lang)

        st.markdown(f"""
        <div class="{level_banner_class}">
          <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
              {ICONS['globe']}
              <div>
                <h2 style="margin:0; font-size:17px;">{level_text}</h2>
                <span style="font-size:13px; color:#49316F;">Target: {analyzed_url}</span>
              </div>
            </div>
            <div style="padding:4px 10px; border-radius:14px; background:rgba(0,0,0,0.06); font-weight:700; font-size:12px;">
              Risk Points: {risk_score}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        loc_explanation = translate_explanation(explanation, lang=lang, prediction="scam" if risk_score >= 1 else "safe")
        render_audio_narrator(f"{level_text}. {loc_explanation}", lang_code, button_label=t("msg_btn_narrate", lang), font_size=current_fs)

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.markdown(f"<h3 style='font-size:15px; color:#49316F;'>{t('url_res_indicators', lang)}</h3>", unsafe_allow_html=True)
            if url_indicators:
                for u_ind in url_indicators:
                    loc_u_ind = translate_indicator(u_ind, lang)
                    st.markdown(f"""
                    <div class="ss-indicator-box">
                      <span style="flex-shrink:0;">{ICONS['alert_triangle']}</span>
                      <span>{loc_u_ind}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ss-action-box">
                  <span style="flex-shrink:0;">{ICONS['check_circle']}</span>
                  <span>{t('res_no_indicators', lang)}</span>
                </div>
                """, unsafe_allow_html=True)

        with col_u2:
            st.markdown(f"<h3 style='font-size:15px; color:#49316F;'>{t('url_res_explanation', lang)}</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="ss-card" style="border-left:3.5px solid #7653B5; font-size:13.5px; line-height:1.55; background:#FAF7FF;">
              <p style="margin:0; color:#292438;">{loc_explanation}</p>
            </div>
            """, unsafe_allow_html=True)


elif st.session_state.active_nav == "nav_awareness":
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">
      {ICONS['shield_check']}
      <h1 style="margin:0; font-size:22px; color:#49316F;">{t('aware_title', lang)}</h1>
    </div>
    <p style="color:#777185; font-size:13.5px; margin-bottom:14px;">{t('aware_subtitle', lang)}</p>
    """, unsafe_allow_html=True)

    aware_items = [
        ("scam_otp_title", "scam_otp_desc", "#DC2626", ICONS['lock']),
        ("scam_bank_title", "scam_bank_desc", "#D97706", ICONS['alert_triangle']),
        ("scam_lottery_title", "scam_lottery_desc", "#7653B5", ICONS['bulb']),
        ("scam_digital_arrest_title", "scam_digital_arrest_desc", "#49316F", ICONS['phone_call']),
    ]

    a_c1, a_c2 = st.columns(2)
    for idx, (t_key, d_key, color, icon) in enumerate(aware_items):
        target = a_c1 if idx % 2 == 0 else a_c2
        with target:
            st.markdown(f"""
            <div class="ss-card" style="border-top:3.5px solid {color}; min-height:140px;">
              <div style="display:flex; align-items:center; gap:6px; margin-bottom:6px;">
                {icon}
                <h3 style="margin:0; font-size:15px; color:{color};">{t(t_key, lang)}</h3>
              </div>
              <p style="color:#777185; font-size:13px; margin:0; line-height:1.5;">
                {t(d_key, lang)}
              </p>
            </div>
            """, unsafe_allow_html=True)


elif st.session_state.active_nav == "nav_safety_guide":
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">
      {ICONS['book']}
      <h1 style="margin:0; font-size:22px; color:#49316F;">{t('guide_title', lang)}</h1>
    </div>
    <p style="color:#777185; font-size:13.5px; margin-bottom:14px;">{t('guide_subtitle', lang)}</p>
    """, unsafe_allow_html=True)

    tab_guide_emer, tab_guide_quiz = st.tabs([
        t("guide_tab_emergency", lang),
        t("guide_tab_quiz", lang)
    ])

    with tab_guide_emer:
        scenarios = [
            (t("emer_step1_title", lang), t("emer_step1_desc", lang), "#7653B5"),
            (t("emer_step2_title", lang), t("emer_step2_desc", lang), "#D97706"),
            (t("emer_step3_title", lang), t("emer_step3_desc", lang), "#DC2626"),
        ]
        for s_title, s_desc, color in scenarios:
            st.markdown(f"""
            <div class="ss-card" style="border-left:3.5px solid {color}; margin-bottom:12px;">
              <h3 style="color:{color} !important; margin:0 0 4px 0; font-size:14.5px;">{s_title}</h3>
              <p style="margin:0; font-size:13px; white-space:pre-line; line-height:1.55; color:#292438;">
                {s_desc}
              </p>
            </div>
            """, unsafe_allow_html=True)
        render_helpline_banner(lang, current_fs)

    with tab_guide_quiz:
        st.markdown(f"<h2 style='font-size:17px; color:#49316F;'>{t('quiz_title', lang)}</h2>", unsafe_allow_html=True)
        
        quiz_list = [
            {
                "id": "q1",
                "q": t("quiz_q1", lang),
                "options": [t("quiz_q1_o1", lang), t("quiz_q1_o2", lang), t("quiz_q1_o3", lang)],
                "correct": 1,
                "exp": t("quiz_q1_exp", lang)
            },
            {
                "id": "q2",
                "q": t("quiz_q2", lang),
                "options": [t("quiz_q2_o1", lang), t("quiz_q2_o2", lang), t("quiz_q2_o3", lang)],
                "correct": 1,
                "exp": t("quiz_q2_exp", lang)
            },
            {
                "id": "q3",
                "q": t("quiz_q3", lang),
                "options": [t("quiz_q3_o1", lang), t("quiz_q3_o2", lang), t("quiz_q3_o3", lang)],
                "correct": 1,
                "exp": t("quiz_q3_exp", lang)
            },
        ]

        q_score = 0
        with st.form("quick_quiz_form"):
            for q_idx, item in enumerate(quiz_list):
                st.markdown(f"""
                <div class="ss-quiz-card">
                  <div style="font-weight:700; font-size:13.5px; margin-bottom:6px; color:#49316F;">
                    {q_idx+1}. {item['q']}
                  </div>
                </div>
                """, unsafe_allow_html=True)
                ans = st.radio(
                    f"Answer {q_idx+1}",
                    item["options"],
                    key=f"quiz_radio_{item['id']}",
                    label_visibility="collapsed"
                )
                st.session_state.quiz_answers[item["id"]] = item["options"].index(ans)

            quiz_submit = st.form_submit_button(t("quiz_btn_check", lang), type="primary")

        if quiz_submit or st.session_state.quiz_submitted:
            st.session_state.quiz_submitted = True
            for item in quiz_list:
                user_sel = st.session_state.quiz_answers.get(item["id"])
                if user_sel == item["correct"]:
                    q_score += 1
                    st.markdown(f"""
                    <div class="ss-quiz-correct">
                      <b>Correct: {item['q']}</b><br/>
                      <span style="color:#065F46;">{item['exp']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ss-quiz-incorrect">
                      <b>Incorrect: {item['q']}</b><br/>
                      <span style="color:#991B1B;">{item['exp']}</span>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="ss-card" style="text-align:center; margin-top:14px; border-top:3.5px solid #7653B5;">
              <h2 style="font-size:17px; margin:4px 0; color:#49316F;">{t('quiz_score_prefix', lang)} {q_score} / {len(quiz_list)}</h2>
            </div>
            """, unsafe_allow_html=True)

            if st.button(t("quiz_btn_reset", lang)):
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {}
                st.rerun()


elif st.session_state.active_nav == "nav_settings":
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">
      {ICONS['settings']}
      <h1 style="margin:0; font-size:22px; color:#49316F;">{t('set_title', lang)}</h1>
    </div>
    <p style="color:#777185; font-size:13.5px; margin-bottom:14px;">{t('set_subtitle', lang)}</p>
    """, unsafe_allow_html=True)

    set_col1, set_col2 = st.columns(2)

    with set_col1:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #7653B5;">
          <h3 style="margin-top:0; font-size:15px; color:#49316F;">Visual & Language Preferences</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<span style='font-size:12px; font-weight:700; color:#49316F; text-transform:uppercase;'>{t('sidebar_language_label', lang)}</span>", unsafe_allow_html=True)
        lang_options = ["English", "Hindi", "Kannada"]
        lang_labels = {"English": "English", "Hindi": "हिन्दी (Hindi)", "Kannada": "ಕನ್ನಡ (Kannada)"}
        selected_lang = st.selectbox(
            "Language Selector",
            lang_options,
            index=lang_options.index(st.session_state.language),
            format_func=lambda x: lang_labels.get(x, x),
            key="set_lang_selectbox"
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        st.markdown(f"<span style='font-size:12px; font-weight:700; color:#49316F; text-transform:uppercase;'>{t('set_font_size_label', lang)}</span>", unsafe_allow_html=True)
        fs_choices = ["Compact (14px)", "Standard (15px)", "Large (17px)"]
        chosen_fs = st.radio(
            "Font Size Selection",
            fs_choices,
            index=fs_choices.index(st.session_state.font_size_choice) if st.session_state.font_size_choice in fs_choices else 1,
            key="set_fs_radio"
        )
        if chosen_fs != st.session_state.font_size_choice:
            st.session_state.font_size_choice = chosen_fs
            st.rerun()

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        st.markdown(f"<span style='font-size:12px; font-weight:700; color:#49316F; text-transform:uppercase;'>{t('set_contrast_label', lang)}</span>", unsafe_allow_html=True)
        hc_val = st.toggle("WCAG AAA High Contrast", value=st.session_state.high_contrast, key="set_hc_toggle")
        if hc_val != st.session_state.high_contrast:
            st.session_state.high_contrast = hc_val
            st.rerun()

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #10B981;">
          <h3 style="margin-top:0; font-size:15px; color:#49316F;">Account & Authentication Status</h3>
          <p style="font-size:12.5px; color:#777185; margin:0 0 10px 0;">
            {"Logged in: " + st.session_state.auth_user.get('email', '') if st.session_state.auth_user else "Running in Secure Guest Mode. Create an account to sync caregiver and consent settings."}
          </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manage Account & Security" if st.session_state.auth_user else "Sign In / Create Account", key="btn_go_account_from_settings", type="primary", use_container_width=True):
            st.session_state.active_nav = "nav_account"
            st.rerun()

    with set_col2:
        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #49316F;">
          <h3 style="margin-top:0; font-size:15px; color:#49316F;">{t('set_helper_heading', lang)}</h3>
          <p style="font-size:12.5px; color:#777185; margin:0 0 10px 0;">{t('set_helper_desc', lang)}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("full_helper_form"):
            h_name = st.text_input(t("set_helper_name", lang), value=st.session_state.helper_name, placeholder="e.g. Ramesh / Priya")
            h_phone = st.text_input(t("set_helper_phone", lang), value=st.session_state.helper_phone, placeholder="919876543210")
            if st.form_submit_button(t("set_helper_save_btn", lang), type="primary"):
                st.session_state.helper_name = h_name.strip()
                st.session_state.helper_phone = re.sub(r"[^\d]", "", h_phone.strip())
                st.success(t("set_helper_saved_msg", lang))

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #0D9488;">
          <h3 style="margin-top:0; font-size:15px; color:#0D9488;">{t('set_history_heading', lang)}</h3>
          <p style="font-size:12.5px; color:#777185; margin:0 0 8px 0;">{t('set_history_desc', lang)}</p>
        </div>
        """, unsafe_allow_html=True)

        hist = st.session_state.analysis_history
        if hist:
            for h_item in hist[:6]:
                st.markdown(f"""
                <div style='font-size:12.5px; padding:6px 8px; border-bottom:1px solid #E6E0EF; display:flex; justify-content:space-between;'>
                  <span><b>[{h_item['type']}]</b> {h_item['preview']}</span>
                  <span style='color:#7653B5; font-weight:700;'>{h_item['risk_level']}</span>
                </div>
                """, unsafe_allow_html=True)
            if st.button(t("set_history_clear_btn", lang), key="btn_clear_hist_full"):
                st.session_state.analysis_history = []
                st.rerun()
        else:
            st.caption(t("set_history_empty", lang))

        render_helpline_banner(lang, current_fs)


elif st.session_state.active_nav == "nav_account":
    from app.database import authenticate_user, register_user, get_consent_record, save_consent_update, update_caregiver
    from security.auth_rules import validate_password_strength, invalidate_token
    from security.consent import get_elderly_transparency_notices

    st.markdown(f"""
    <div class="ss-welcome-card" style="border-left: 4px solid #7653B5;">
      <h2 style="color:#49316F !important; margin:0 0 6px 0; font-size:20px;">
        {t('nav_account', lang)} — Senior & Family Security Center
      </h2>
      <p style="color:#292438 !important; font-size:13.5px; margin:0;">
        Powered by OWASP-recommended Argon2id memory-hard password verification, sliding-window rate limiting, and granular privacy consent.
      </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.auth_user is not None:
        user = st.session_state.auth_user
        acc_col1, acc_col2 = st.columns([1, 1])

        with acc_col1:
            st.markdown(f"""
            <div class="ss-card" style="border-top:3.5px solid #10B981;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0; font-size:16px; color:#49316F;">Profile & Session State</h3>
                <span class="ss-badge ss-badge-teal">Active Session</span>
              </div>
              <div style="margin-top:12px; font-size:13.5px; line-height:1.8;">
                <div><b>Email:</b> {user.get('email')}</div>
                <div><b>User ID:</b> <code>{user.get('id')}</code></div>
                <div><b>Account Role:</b> {str(user.get('role', 'senior')).capitalize()}</div>
                <div><b>Authentication:</b> <span style="color:#0D9488; font-weight:600;">Argon2id (64MB Hardened)</span></div>
                <div><b>Token Security:</b> <span style="color:#7653B5; font-weight:600;">JWT HMAC-SHA256</span></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            if st.button("Log Out of Session", key="btn_auth_logout", type="secondary", use_container_width=True):
                if st.session_state.auth_token:
                    invalidate_token(st.session_state.auth_token)
                st.session_state.auth_token = ""
                st.session_state.auth_user = None
                st.success("You have been securely logged out.")
                st.rerun()

        with acc_col2:
            st.markdown(f"""
            <div class="ss-card" style="border-top:3.5px solid #7653B5;">
              <h3 style="margin-top:0; font-size:16px; color:#49316F;">Caregiver & Family Contact</h3>
              <p style="font-size:13px; color:#777185; margin:0 0 10px 0;">
                Designated contact for emergency notifications and scam alerts.
              </p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("account_caregiver_form"):
                acc_c_name = st.text_input("Caregiver Name", value=user.get("helper_name") or st.session_state.helper_name, placeholder="e.g. Ramesh")
                acc_c_phone = st.text_input("Caregiver Phone (with country code)", value=user.get("helper_phone") or st.session_state.helper_phone, placeholder="919876543210")
                if st.form_submit_button("Save Caregiver Details", type="primary"):
                    clean_phone = re.sub(r"[^\d]", "", acc_c_phone.strip())
                    update_caregiver(user["id"], acc_c_name.strip(), clean_phone)
                    st.session_state.helper_name = acc_c_name.strip()
                    st.session_state.helper_phone = clean_phone
                    user["helper_name"] = acc_c_name.strip()
                    user["helper_phone"] = clean_phone
                    st.session_state.auth_user = user
                    st.success("Caregiver information updated securely.")

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ss-card" style="border-top:3.5px solid #0D9488;">
          <h3 style="margin-top:0; font-size:16px; color:#49316F;">Granular Privacy & Consent Controls</h3>
          <p style="font-size:13px; color:#777185; margin:0 0 12px 0;">
            Manage how your safety scans and data are handled in full compliance with DPDP & GDPR data rights.
          </p>
        </div>
        """, unsafe_allow_html=True)

        user_consent = get_consent_record(user["id"])
        c_prefs = user_consent.preferences

        with st.form("account_consent_form"):
            c1_val = st.checkbox("Immediate In-Memory Message Analysis (Essential for scam detection)", value=c_prefs.consent_message_analysis)
            c2_val = st.checkbox("Save Scan Risk Ratings (Stores only risk ratings; never stores your raw SMS or message text)", value=c_prefs.consent_save_history)
            c3_val = st.checkbox("Share Anonymous Threat Signals (Aggregated statistics to improve safety defenses)", value=c_prefs.consent_analytics)
            c4_val = st.checkbox("Designated Caregiver Sharing (Send high-risk alert details to your caregiver)", value=c_prefs.consent_caregiver_sharing)

            if st.form_submit_button("Update Consent Preferences", type="primary"):
                updated_consent = save_consent_update(
                    user["id"],
                    {
                        "consent_message_analysis": c1_val,
                        "consent_save_history": c2_val,
                        "consent_analytics": c3_val,
                        "consent_caregiver_sharing": c4_val,
                    }
                )
                st.success("Consent preferences updated and logged in privacy audit trail.")
                st.rerun()

    else:
        auth_tab_login, auth_tab_register, auth_tab_privacy = st.tabs(["Sign In", "Create Account", "Privacy Rights & Disclosures"])

        with auth_tab_login:
            st.markdown(f"""
            <div class="ss-card" style="border-top:3.5px solid #7653B5; max-width:560px; margin:10px auto;">
              <h3 style="margin:0 0 8px 0; color:#49316F; font-size:17px;">Sign In to SilverShield AI</h3>
              <p style="font-size:13px; color:#777185; margin:0 0 14px 0;">
                Access your personalized safety settings, saved caregiver alert contacts, and privacy preferences.
              </p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("auth_login_form"):
                log_email = st.text_input("Email Address", placeholder="senior@example.com")
                log_pass = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("Sign In", type="primary", use_container_width=True)

                if submit_login:
                    u, err = authenticate_user(log_email.strip(), log_pass)
                    if err:
                        st.error(err)
                    else:
                        from security.auth_rules import create_token
                        token = create_token(subject=u["id"], secret_key="silvershield_ai_jwt_production_secret_key_minimum_32_bytes")
                        st.session_state.auth_token = token
                        st.session_state.auth_user = u
                        if u.get("helper_name"):
                            st.session_state.helper_name = u["helper_name"]
                        if u.get("helper_phone"):
                            st.session_state.helper_phone = u["helper_phone"]
                        st.success("Successfully logged in! Session secured.")
                        st.rerun()

        with auth_tab_register:
            st.markdown(f"""
            <div class="ss-card" style="border-top:3.5px solid #10B981; max-width:560px; margin:10px auto;">
              <h3 style="margin:0 0 8px 0; color:#49316F; font-size:17px;">Create a New Safety Account</h3>
              <p style="font-size:13px; color:#777185; margin:0 0 14px 0;">
                Your password is protected using memory-hard Argon2id hashing with unique random salts.
              </p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("auth_register_form"):
                reg_email = st.text_input("Email Address", placeholder="senior@example.com")
                reg_pass = st.text_input("Password (min 8 characters, letters and numbers)", type="password", placeholder="Create a strong password")
                reg_role = st.selectbox("I am a:", ["Senior Citizen", "Family Caregiver / Relative"])
                submit_register = st.form_submit_button("Create Account", type="primary", use_container_width=True)

                if submit_register:
                    role_key = "caregiver" if "Caregiver" in reg_role else "senior"
                    u, err = register_user(reg_email.strip(), reg_pass, role=role_key)
                    if err:
                        st.error(err)
                    else:
                        from security.auth_rules import create_token
                        token = create_token(subject=u["id"], secret_key="silvershield_ai_jwt_production_secret_key_minimum_32_bytes")
                        st.session_state.auth_token = token
                        st.session_state.auth_user = u
                        st.success("Account created successfully! Session is now active.")
                        st.rerun()

        with auth_tab_privacy:
            st.markdown(f"""
            <div class="ss-card" style="border-top:3.5px solid #0D9488; margin-top:10px;">
              <h3 style="margin:0 0 8px 0; color:#0D9488; font-size:16px;">Plain-Language Elderly Privacy Disclosures</h3>
              <p style="font-size:13px; color:#777185; margin:0 0 12px 0;">
                SilverShield AI adheres to strict Privacy-by-Design and elderly-friendly transparency standards.
              </p>
            </div>
            """, unsafe_allow_html=True)

            from security.consent import ConsentPreferences, get_elderly_transparency_notices
            notices = get_elderly_transparency_notices(ConsentPreferences())
            for n in notices:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E6E0EF; border-radius:8px; padding:12px 14px; margin-bottom:8px;">
                  <div style="font-weight:700; color:#49316F; font-size:14px; margin-bottom:4px;">{n['title']}</div>
                  <div style="color:#292438; font-size:13px; line-height:1.5;">{n['notice']}</div>
                </div>
                """, unsafe_allow_html=True)

