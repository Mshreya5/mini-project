"""
SilverShield AI - Reusable UI Components
Provides specialized components for:
- Speech synthesis & Kannada TTS fallback with Play/Stop controls
- Visual Risk Gauge & Threat Indicators
- Recommended Action Cards
- 24/7 Helpline Banner
- Caregiver WhatsApp Alerting
- Interactive Scam Awareness Quiz
- Session Analysis History
"""

import json
import urllib.parse
from datetime import datetime
import streamlit as st

from frontend.locales import (
    LANGUAGES,
    t,
    translate_action,
    translate_indicator,
    translate_risk_level,
    translate_warning,
)
from frontend.styles import ICONS


def render_audio_narrator(text_to_speak: str, lang_code: str, button_label: str = "Listen to Result", font_size: int = 15):
    """
    Render a robust speech narration player with Play and Stop controls.
    - For English: Uses browser speech synthesis (en-IN / en-US).
    - For Kannada: Inspects browser voices for native Kannada (kn-IN).
      If no Kannada voice is available in the browser/OS, delegates to
      Google Text-to-Speech audio stream so authentic Kannada is always spoken.
    - Never sends Kannada text to an English voice.
    - Handles empty text, network delays, and playback errors gracefully.
    """
    clean_text = (text_to_speak or "").strip()
    if not clean_text:
        st.markdown(
            f"<div style='font-size:13px; color:#94A3B8; font-style:italic; padding:4px 0;'>No audio narration available for this content.</div>",
            unsafe_allow_html=True
        )
        return

    escaped_text = json.dumps(clean_text, ensure_ascii=False)
    uid = abs(hash(clean_text[:50])) % 999999
    
    is_kannada = lang_code.lower().startswith("kn")
    is_hindi = lang_code.lower().startswith("hi")
    
    status_playing = "ಧ್ವನಿ ಪ್ಲೇ ಆಗುತ್ತಿದೆ..." if is_kannada else ("आवाज़ सुनाई दे रही है..." if is_hindi else "Reading aloud...")
    status_stopped = "ನಿಲ್ಲಿಸಲಾಗಿದೆ" if is_kannada else ("रोक दिया गया" if is_hindi else "Stopped")
    stop_label = "ನಿಲ್ಲಿಸಿ (Stop)" if is_kannada else ("रोकें (Stop)" if is_hindi else "Stop")
    
    html = f"""
    <div id="narrator_wrap_{uid}" style="display:flex; align-items:center; gap:8px; margin: 6px 0 10px 0; flex-wrap:wrap;">
      <button id="btn_play_{uid}" onclick="ssPlay_{uid}()" style="
          background: linear-gradient(135deg, #0D9488 0%, #0284C7 100%);
          color: #FFFFFF;
          padding: 8px 16px;
          font-size: 14px;
          font-weight: 600;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 7px;
          box-shadow: 0 2px 6px rgba(13, 148, 136, 0.25);
          transition: all 0.15s ease;
          font-family: inherit;">
        {ICONS['speaker']} <span id="lbl_play_{uid}">{button_label}</span>
      </button>
      
      <button id="btn_stop_{uid}" onclick="ssStop_{uid}()" style="
          background: #DC2626;
          color: #FFFFFF;
          padding: 8px 14px;
          font-size: 14px;
          font-weight: 600;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          display: none;
          align-items: center;
          gap: 6px;
          box-shadow: 0 2px 6px rgba(220, 38, 38, 0.25);
          transition: all 0.15s ease;
          font-family: inherit;">
        {ICONS['stop']} <span>{stop_label}</span>
      </button>

      <span id="status_{uid}" style="font-size:12px; color:#64748B; font-weight:500;"></span>

      <script>
      (function() {{
        var text = {escaped_text};
        var langCode = '{lang_code}';
        var isKn = {str(is_kannada).lower()};
        var isHi = {str(is_hindi).lower()};
        var activeAudio = null;
        var isPlaying = false;

        function setUiState(playing) {{
          isPlaying = playing;
          var btnPlay = document.getElementById('btn_play_{uid}');
          var btnStop = document.getElementById('btn_stop_{uid}');
          var status = document.getElementById('status_{uid}');
          if (!btnPlay || !btnStop) return;

          if (playing) {{
            btnPlay.style.opacity = '0.75';
            btnStop.style.display = 'inline-flex';
            if (status) status.innerText = '{status_playing}';
          }} else {{
            btnPlay.style.opacity = '1.0';
            btnStop.style.display = 'none';
            if (status) status.innerText = '';
          }}
        }}

        window.ssStop_{uid} = function() {{
          if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();
          }}
          if (activeAudio) {{
            activeAudio.pause();
            activeAudio.currentTime = 0;
            activeAudio = null;
          }}
          setUiState(false);
        }};

        function findVoice(targetLang) {{
          if (!('speechSynthesis' in window)) return null;
          var voices = window.speechSynthesis.getVoices() || [];
          if (!voices.length) return null;

          var prefix = targetLang.split('-')[0].toLowerCase();
          
          for (var i = 0; i < voices.length; i++) {{
            var v = voices[i];
            if (v.lang && v.lang.toLowerCase() === targetLang.toLowerCase()) {{
              return v;
            }}
          }}
          
          for (var i = 0; i < voices.length; i++) {{
            var v = voices[i];
            if (v.lang && v.lang.toLowerCase().startsWith(prefix)) {{
              return v;
            }}
          }}

          var keywords = isKn ? ['kannada', 'kn', 'sapna', 'gagan'] : (isHi ? ['hindi', 'hi', 'swara', 'madhur'] : ['english', 'en', 'india', 'david']);
          for (var i = 0; i < voices.length; i++) {{
            var name = (voices[i].name || '').toLowerCase();
            for (var k = 0; k < keywords.length; k++) {{
              if (name.indexOf(keywords[k]) !== -1) {{
                return voices[i];
              }}
            }}
          }}
          return null;
        }}

        function playOnlineAudio(langTag, ttsText) {{
          try {{
            var clean = ttsText.replace(/[\\r\\n]+/g, ' ').substring(0, 190);
            var url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=' + encodeURIComponent(langTag) + '&client=tw-ob&q=' + encodeURIComponent(clean);
            activeAudio = new Audio(url);
            activeAudio.crossOrigin = 'anonymous';
            activeAudio.onplay = function() {{ setUiState(true); }};
            activeAudio.onended = function() {{ setUiState(false); }};
            activeAudio.onerror = function() {{
              setUiState(false);
              var st = document.getElementById('status_{uid}');
              if (st) st.innerText = isKn ? 'ಧ್ವನಿ ಸೌಲಭ್ಯ ಲಭ್ಯವಿಲ್ಲ' : 'Voice service temporarily unavailable';
            }};
            activeAudio.play().catch(function(e) {{
              setUiState(false);
            }});
          }} catch(e) {{
            setUiState(false);
          }}
        }}

        function speakUtterance(targetLang, rate, fallbackOnlineTag) {{
          if (!('speechSynthesis' in window)) {{
            if (fallbackOnlineTag) {{
              playOnlineAudio(fallbackOnlineTag, text);
            }} else {{
              alert('Speech synthesis is not supported on this browser.');
            }}
            return;
          }}

          var voice = findVoice(targetLang);
          var utter = new SpeechSynthesisUtterance(text);
          if (voice) {{
            utter.voice = voice;
          }}
          utter.lang = voice && voice.lang ? voice.lang : targetLang;
          utter.rate = rate;

          var speakStarted = false;
          utter.onstart = function() {{
            speakStarted = true;
            setUiState(true);
          }};
          utter.onend = function() {{
            setUiState(false);
          }};
          utter.onerror = function(ev) {{
            setUiState(false);
            if (!speakStarted && fallbackOnlineTag) {{
              playOnlineAudio(fallbackOnlineTag, text);
            }}
          }};

          try {{
            window.speechSynthesis.speak(utter);
            setTimeout(function() {{
              if (!speakStarted && !window.speechSynthesis.speaking && fallbackOnlineTag) {{
                playOnlineAudio(fallbackOnlineTag, text);
              }}
            }}, 400);
          }} catch (err) {{
            if (fallbackOnlineTag) {{
              playOnlineAudio(fallbackOnlineTag, text);
            }} else {{
              setUiState(false);
            }}
          }}
        }}

        window.ssPlay_{uid} = function() {{
          window.ssStop_{uid}();
          if (!text || !text.trim()) return;

          if ('speechSynthesis' in window) {{
            window.speechSynthesis.getVoices();
          }}

          if (isKn) {{
            speakUtterance('kn-IN', 0.88, 'kn');
          }} else if (isHi) {{
            speakUtterance('hi-IN', 0.90, 'hi');
          }} else {{
            speakUtterance('en-IN', 0.92, 'en');
          }}
        }};

        if ('speechSynthesis' in window && window.speechSynthesis.onvoiceschanged !== undefined) {{
          window.speechSynthesis.onvoiceschanged = function() {{
            window.speechSynthesis.getVoices();
          }};
        }}
      }})();
      </script>
    </div>
    """
    st.components.v1.html(html, height=52)


def render_risk_card(risk_level: str, warning_text: str, risk_score: float, lang: str = "English", font_size: int = 15):
    """Render the primary threat alert card based on risk level."""
    norm_level = str(risk_level).upper().strip()
    loc_risk = translate_risk_level(norm_level, lang)
    loc_warn = translate_warning(warning_text, lang)
    
    score_pct = int(min(1.0, max(0.0, risk_score)) * 100)
    
    if norm_level == "HIGH":
        css_class = "alert-high"
        icon_svg = ICONS['shield_alert']
        badge_style = "background:#DC2626; color:white;"
    elif norm_level == "MEDIUM":
        css_class = "alert-med"
        icon_svg = ICONS['alert_triangle']
        badge_style = "background:#D97706; color:white;"
    else:
        css_class = "alert-low"
        icon_svg = ICONS['shield_check']
        badge_style = "background:#10B981; color:white;"
        
    html = f"""
    <div class="{css_class}">
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
        <div style="display:flex; align-items:center; gap:10px;">
          {icon_svg}
          <h2 style="margin:0; font-size:18px;">{loc_risk}</h2>
        </div>
        <div style="padding:4px 12px; border-radius:20px; font-weight:800; font-size:13px; {badge_style}">
          Score: {score_pct}/100
        </div>
      </div>
      <p style="margin:0; font-weight:600; font-size:15px; line-height:1.5;">{loc_warn}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_threat_indicators(indicators: list, lang: str = "English"):
    """Display threat indicators tagged with warning badges."""
    if not indicators:
        st.markdown(f"<p style='color:#64748B; font-size:14px;'>{t('res_no_indicators', lang)}</p>", unsafe_allow_html=True)
        return
        
    for ind in indicators:
        loc_ind = translate_indicator(ind, lang)
        st.markdown(f"""
        <div class="ss-indicator-box">
          <span style="flex-shrink:0; margin-top:1px;">{ICONS['alert_triangle']}</span>
          <span>{loc_ind}</span>
        </div>
        """, unsafe_allow_html=True)


def render_safety_actions(actions: list, lang: str = "English"):
    """Display concrete safety recommendations."""
    if not actions:
        return
        
    for act in actions:
        loc_act = translate_action(act, lang)
        st.markdown(f"""
        <div class="ss-action-box">
          <span style="flex-shrink:0; margin-top:1px;">{ICONS['check_circle']}</span>
          <span>{loc_act}</span>
        </div>
        """, unsafe_allow_html=True)


def render_helpline_banner(lang: str = "English", font_size: int = 15):
    """Render the 1930 National Cyber Crime Helpline CTA."""
    html = f"""
    <div class="ss-helpline-card">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px; flex-wrap:wrap;">
        {ICONS['phone_call']}
        <div>
          <h2 style="margin:0; color:white !important; font-size:18px;">
            {t("sidebar_quick_helpline", lang)}
          </h2>
          <span style="color:rgba(255,255,255,0.85); font-size:12px;">
            Toll-free Government of India Emergency Assistance
          </span>
        </div>
      </div>
      <p style="color:rgba(255,255,255,0.92) !important; margin-bottom:12px; font-size:14px;">
        {t("emer_step3_desc", lang).splitlines()[0]}
      </p>
      <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
        <a href="tel:1930" style="text-decoration:none;">
          <div style="background:white; color:#DC2626; font-size:22px;
                      font-weight:900; border-radius:9px; padding:6px 20px; letter-spacing:1px;
                      display:inline-block; box-shadow:0 2px 8px rgba(0,0,0,0.15);">
            1930
          </div>
        </a>
        <a href="https://cybercrime.gov.in" target="_blank" style="text-decoration:none;">
          <div style="background:rgba(255,255,255,0.18); color:white; border:1px solid white;
                      font-size:13px; font-weight:600; border-radius:8px;
                      padding:8px 16px; display:inline-block;">
            Visit cybercrime.gov.in
          </div>
        </a>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_caregiver_share(helper_name: str, helper_phone: str, message_text: str, risk_level: str, warning_text: str, lang: str = "English"):
    """Render WhatsApp share button with clear confirmation disclosure."""
    name = helper_name.strip() or "Caregiver"
    phone = helper_phone.strip()
    
    if not phone:
        st.markdown(f"""
        <div class="ss-card" style="border-left:4px solid #0D9488;">
          <div style="display:flex; align-items:center; gap:10px;">
            {ICONS['user_caregiver']}
            <div>
              <h4 style="margin:0; font-size:15px;">Caregiver Alerting Setup</h4>
              <p style="margin:0; font-size:13px; color:#64748B;">
                Add your trusted helper's phone number under <b>Settings & Accessibility</b> to enable instant 1-tap WhatsApp alerts.
              </p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    clean_snippet = (message_text[:120] + "...") if len(message_text) > 120 else message_text
    
    wa_msg = (
        f"[SilverShield AI Alert]\n\n"
        f"Hello {name}, I scanned this suspicious message on SilverShield AI and need your guidance:\n\n"
        f"\"{clean_snippet}\"\n\n"
        f"Threat Level: *{risk_level}*\n"
        f"Assessment: {warning_text}\n\n"
        f"Please verify this for me before I take any action."
    )
    encoded = urllib.parse.quote(wa_msg)
    wa_url = f"https://wa.me/{phone}?text={encoded}"
    
    st.markdown(f"""
    <div style="margin: 12px 0;">
      <a href="{wa_url}" target="_blank" style="text-decoration:none; display:block;">
        <div class="ss-wa-btn">
          {ICONS['whatsapp']}
          <span>{t('res_caregiver_share', lang)} ({name})</span>
        </div>
      </a>
      <div style="font-size:12px; color:#64748B; margin-top:4px; text-align:center;">
        {t('res_caregiver_notice', lang)}
      </div>
    </div>
    """, unsafe_allow_html=True)


def log_analysis_history(input_type: str, content: str, risk_level: str, score: float):
    """Store analysis event in session history."""
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []
        
    entry = {
        "id": len(st.session_state.analysis_history) + 1,
        "timestamp": datetime.now().strftime("%d-%b %H:%M"),
        "type": input_type,
        "preview": (content[:80] + "...") if len(content) > 80 else content,
        "risk_level": risk_level,
        "score": round(score, 2)
    }
    st.session_state.analysis_history.insert(0, entry)
    st.session_state.analysis_history = st.session_state.analysis_history[:15]
