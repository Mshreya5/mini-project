"""
SilverShield AI - Elegant Purple, White & Lavender Design System
Theme specifications:
- Background: #F8F7FC
- Primary Purple: #7653B5
- Deep Purple: #49316F
- Light Lavender: #EDE5FA
- Cards: #FFFFFF
- Main Text: #292438
- Secondary Text: #777185
- Borders: #E6E0EF
"""

def get_css(font_size: int = 15, high_contrast: bool = False) -> str:
    fs = font_size
    
    if high_contrast:
        bg = "#0B0814"
        card_bg = "#151026"
        card_border = "#B39DDB"
        txt_main = "#FFFFFF"
        txt_sub = "#EDE5FA"
        accent = "#B39DDB"
        accent_deep = "#FFFFFF"
        lavender_bg = "#261C40"
        input_bg = "#151026"
        input_border = "#B39DDB"
        btn_primary_bg = "#B39DDB"
        btn_primary_txt = "#0B0814"
        
        hi_bg = "#380606"; hi_border = "#FF6B6B"; hi_txt = "#FFFFFF"
        med_bg = "#332200"; med_border = "#FCD34D"; med_txt = "#FFFFFF"
        low_bg = "#002E18"; low_border = "#34D399"; low_txt = "#FFFFFF"
    else:
        bg = "#F8F7FC"
        card_bg = "#FFFFFF"
        card_border = "#E6E0EF"
        txt_main = "#292438"
        txt_sub = "#777185"
        accent = "#7653B5"
        accent_deep = "#49316F"
        lavender_bg = "#EDE5FA"
        input_bg = "#FFFFFF"
        input_border = "#E6E0EF"
        btn_primary_bg = "#7653B5"
        btn_primary_txt = "#FFFFFF"
        
        hi_bg = "#FEF2F2"; hi_border = "#EF4444"; hi_txt = "#991B1B"
        med_bg = "#FFFBEB"; med_border = "#F59E0B"; med_txt = "#92400E"
        low_bg = "#ECFDF5"; low_border = "#10B981"; low_txt = "#065F46"

    h1_size = 25 if fs <= 15 else (27 if fs <= 17 else 29)
    h2_size = 19 if fs <= 15 else (21 if fs <= 17 else 23)
    h3_size = 16 if fs <= 15 else (17 if fs <= 17 else 18)
    btn_size = 14 if fs <= 15 else (15 if fs <= 17 else 16)

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=Noto+Sans+Kannada:wght@400;500;600;700&display=swap');

    *, *::before, *::after {{
        box-sizing: border-box !important;
    }}

    html, body {{
        overflow-x: hidden !important;
        width: 100% !important;
        max-width: 100vw !important;
    }}

    /* Hide the left sidebar and default Streamlit header */
    [data-testid="stSidebar"], 
    [data-testid="collapsedControl"], 
    header[data-testid="stHeader"] {{
        display: none !important;
    }}

    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', 'Noto Sans Kannada', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: {bg} !important;
        color: {txt_main} !important;
    }}

    /* Main Container */
    .block-container {{
        max-width: 1060px !important;
        width: 100% !important;
        padding-left: clamp(1rem, 3vw, 2.5rem) !important;
        padding-right: clamp(1rem, 3vw, 2.5rem) !important;
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }}

    /* Top Brand Header Bar */
    .ss-header-card {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 18px;
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 1px 4px rgba(73, 49, 111, 0.04);
    }}

    /* Typography Hierarchy */
    p, span, label, li {{
        font-size: {fs}px !important;
        line-height: 1.55 !important;
        color: {txt_main} !important;
        word-break: break-word !important;
    }}

    h1 {{
        font-size: {h1_size}px !important;
        font-weight: 800 !important;
        color: {accent_deep} !important;
        letter-spacing: -0.3px !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.3rem !important;
        line-height: 1.25 !important;
    }}

    h2 {{
        font-size: {h2_size}px !important;
        font-weight: 700 !important;
        color: {accent_deep} !important;
        letter-spacing: -0.2px !important;
        margin-top: 1.1rem !important;
        margin-bottom: 0.4rem !important;
        line-height: 1.3 !important;
    }}

    h3 {{
        font-size: {h3_size}px !important;
        font-weight: 700 !important;
        color: {accent_deep} !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
        line-height: 1.35 !important;
    }}

    /* Buttons - All States */
    div.stButton > button,
    div.stButton > button:focus,
    div.stButton > button:active,
    div.stButton > button:focus-visible,
    div.stButton > button:focus:not(:active) {{
        min-height: 38px !important;
        padding: 8px 18px !important;
        font-size: {btn_size}px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: 1.5px solid {card_border} !important;
        background-color: {card_bg} !important;
        background: {card_bg} !important;
        color: {accent_deep} !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 2px rgba(73, 49, 111, 0.04) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        outline: none !important;
    }}

    div.stButton > button:hover {{
        border-color: {accent} !important;
        color: {accent_deep} !important;
        background-color: {lavender_bg} !important;
        background: {lavender_bg} !important;
        box-shadow: 0 2px 6px rgba(118, 83, 181, 0.15) !important;
    }}

    div.stButton > button:active,
    div.stButton > button:focus {{
        border-color: {accent} !important;
        color: {accent_deep} !important;
        background-color: {lavender_bg} !important;
        background: {lavender_bg} !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(118, 83, 181, 0.25) !important;
    }}

    div.stButton > button[kind="primary"],
    div.stButton > button[kind="primary"]:focus,
    div.stButton > button[kind="primary"]:active,
    div.stButton > button[kind="primary"]:focus:not(:active) {{
        background: {btn_primary_bg} !important;
        background-color: {btn_primary_bg} !important;
        color: {btn_primary_txt} !important;
        border: 1.5px solid {accent} !important;
        box-shadow: 0 2px 6px rgba(118, 83, 181, 0.25) !important;
        outline: none !important;
    }}

    div.stButton > button[kind="primary"]:hover {{
        background: #5D3E96 !important;
        background-color: #5D3E96 !important;
        color: #FFFFFF !important;
        border-color: #5D3E96 !important;
        box-shadow: 0 4px 10px rgba(118, 83, 181, 0.35) !important;
    }}

    /* Popover Trigger Buttons (3-dots & Settings) */
    div[data-testid="stPopover"] > button,
    div[data-testid="stPopover"] > button:focus,
    div[data-testid="stPopover"] > button:active,
    div[data-testid="stPopover"] > button:focus-visible,
    div[data-testid="stPopover"] > button:focus:not(:active),
    div[data-testid="stPopover"] > button[aria-expanded="true"] {{
        min-height: 38px !important;
        width: 38px !important;
        padding: 0 !important;
        border-radius: 8px !important;
        font-size: 19px !important;
        font-weight: 700 !important;
        border: 1.5px solid {card_border} !important;
        background: {card_bg} !important;
        background-color: {card_bg} !important;
        color: {accent_deep} !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.15s ease !important;
        outline: none !important;
        box-shadow: 0 1px 2px rgba(73, 49, 111, 0.04) !important;
    }}

    div[data-testid="stPopover"] > button:hover,
    div[data-testid="stPopover"] > button:focus,
    div[data-testid="stPopover"] > button:active,
    div[data-testid="stPopover"] > button[aria-expanded="true"] {{
        border-color: {accent} !important;
        background: {lavender_bg} !important;
        background-color: {lavender_bg} !important;
        color: {accent_deep} !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(118, 83, 181, 0.25) !important;
    }}

    /* Popover Content Container (Settings & Navigation) */
    [data-testid="stPopoverBody"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid #D8CBEF !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(73, 49, 111, 0.18) !important;
        padding: 16px 18px !important;
        max-height: 80vh !important;
        overflow-y: auto !important;
        color: {txt_main} !important;
    }}

    [data-testid="stPopoverBody"] * {{
        color: {txt_main} !important;
    }}

    [data-testid="stPopoverBody"] p,
    [data-testid="stPopoverBody"] span,
    [data-testid="stPopoverBody"] label,
    [data-testid="stPopoverBody"] h1,
    [data-testid="stPopoverBody"] h2,
    [data-testid="stPopoverBody"] h3,
    [data-testid="stPopoverBody"] h4 {{
        color: {txt_main} !important;
    }}

    /* Popover Navigation Item Buttons */
    [data-testid="stPopoverBody"] div.stButton > button,
    [data-testid="stPopoverBody"] div.stButton > button:focus,
    [data-testid="stPopoverBody"] div.stButton > button:active,
    [data-testid="stPopoverBody"] div.stButton > button:focus:not(:active) {{
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 9px 14px !important;
        margin-bottom: 5px !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        border: 1px solid {card_border} !important;
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: {txt_main} !important;
        width: 100% !important;
        min-height: 38px !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    [data-testid="stPopoverBody"] div.stButton > button:hover {{
        background-color: {lavender_bg} !important;
        background: {lavender_bg} !important;
        border-color: {accent} !important;
        color: {accent_deep} !important;
        font-weight: 600 !important;
    }}

    [data-testid="stPopoverBody"] div.stButton > button[kind="primary"],
    [data-testid="stPopoverBody"] div.stButton > button[kind="primary"]:focus,
    [data-testid="stPopoverBody"] div.stButton > button[kind="primary"]:active,
    [data-testid="stPopoverBody"] div.stButton > button[kind="primary"]:focus:not(:active) {{
        background-color: {lavender_bg} !important;
        background: {lavender_bg} !important;
        border: 1.5px solid {accent} !important;
        color: {accent_deep} !important;
        font-weight: 700 !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* BaseWeb Popover / Dropdown Portal Menus */
    div[data-baseweb="popover"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1.5px solid #D8CBEF !important;
        box-shadow: 0 10px 30px rgba(73, 49, 111, 0.18) !important;
        z-index: 999999 !important;
    }}

    div[data-baseweb="popover"] * {{
        background-color: transparent !important;
        background: transparent !important;
        color: {txt_main} !important;
    }}

    div[data-baseweb="popover"] span {{
        color: {txt_main} !important;
    }}

    div[data-baseweb="menu"], ul[role="listbox"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }}

    li[role="option"], div[role="option"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: {txt_main} !important;
        padding: 10px 14px !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.12s ease !important;
    }}

    li[role="option"] *, div[role="option"] * {{
        color: {txt_main} !important;
        background-color: transparent !important;
        background: transparent !important;
    }}

    li[role="option"]:hover,
    li[role="option"]:focus,
    li[role="option"]:active,
    li[role="option"][aria-selected="true"],
    li[role="option"][data-highlighted="true"],
    div[role="option"]:hover,
    div[role="option"]:focus,
    div[role="option"]:active,
    div[role="option"][aria-selected="true"],
    div[role="option"][data-highlighted="true"] {{
        background-color: {lavender_bg} !important;
        background: {lavender_bg} !important;
        color: {accent_deep} !important;
        font-weight: 600 !important;
    }}

    li[role="option"]:hover *,
    li[role="option"]:focus *,
    li[role="option"]:active *,
    li[role="option"][aria-selected="true"] *,
    li[role="option"][data-highlighted="true"] *,
    div[role="option"]:hover *,
    div[role="option"]:focus *,
    div[role="option"]:active *,
    div[role="option"][aria-selected="true"] *,
    div[role="option"][data-highlighted="true"] * {{
        color: {accent_deep} !important;
    }}

    /* Selectbox Main Field */
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid {card_border} !important;
        border-radius: 8px !important;
        color: {txt_main} !important;
    }}

    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="select"] > div:focus-within {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px rgba(118, 83, 181, 0.15) !important;
    }}

    /* Eliminate black background on dropdown arrow / indicators */
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] svg,
    div[data-baseweb="select"] [role="button"],
    div[data-baseweb="select"] [data-baseweb="icon"] {{
        background-color: transparent !important;
        background: transparent !important;
        color: {accent_deep} !important;
        fill: {accent_deep} !important;
    }}

    /* Tooltips */
    div[data-baseweb="tooltip"],
    div[role="tooltip"] {{
        background-color: {accent_deep} !important;
        background: {accent_deep} !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        padding: 5px 9px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(73, 49, 111, 0.25) !important;
    }}

    div[data-baseweb="tooltip"] *,
    div[role="tooltip"] * {{
        color: #FFFFFF !important;
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* Form Inputs */
    textarea, input[type="text"] {{
        background-color: {input_bg} !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 8px !important;
        font-size: {fs}px !important;
        color: {txt_main} !important;
        padding: 9px 13px !important;
        transition: border-color 0.15s ease !important;
    }}

    textarea:focus, input[type="text"]:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 3px rgba(118, 83, 181, 0.15) !important;
        outline: none !important;
    }}

    .stTextArea textarea {{
        min-height: 95px !important;
    }}

    /* Clean Card Layout */
    .ss-card {{
        background: {card_bg};
        border: 1.5px solid {card_border};
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(73, 49, 111, 0.04);
        transition: box-shadow 0.15s ease, border-color 0.15s ease;
    }}

    .ss-card:hover {{
        box-shadow: 0 4px 12px rgba(73, 49, 111, 0.08);
        border-color: #D3C8E5;
    }}

    /* Hero / Welcome Card */
    .ss-welcome-card {{
        background: linear-gradient(135deg, #FAF7FF 0%, #EDE5FA 100%);
        border: 1.5px solid #D8CBEF;
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 18px;
        color: {txt_main} !important;
        box-shadow: 0 2px 8px rgba(73, 49, 111, 0.05);
    }}

    /* Badges */
    .ss-badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 9px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }}

    .ss-badge-purple {{
        background: {lavender_bg};
        color: {accent_deep} !important;
        border: 1px solid #D8CBEF;
    }}

    .ss-badge-teal {{
        background: #ECFDF5;
        color: #065F46 !important;
        border: 1px solid #A7F3D0;
    }}

    /* Threat Alert Banners */
    .alert-high {{
        background: {hi_bg};
        border-left: 4px solid {hi_border};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
    }}

    .alert-med {{
        background: {med_bg};
        border-left: 4px solid {med_border};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
    }}

    .alert-low {{
        background: {low_bg};
        border-left: 4px solid {low_border};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
    }}

    /* Threat Indicators & Action Items */
    .ss-action-box {{
        background: {low_bg};
        border: 1px solid {low_border};
        border-radius: 8px;
        padding: 9px 12px;
        margin-bottom: 6px;
        font-size: {fs}px !important;
        font-weight: 500;
        color: {low_txt} !important;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }}

    .ss-indicator-box {{
        background: {hi_bg};
        border: 1px solid {hi_border};
        border-radius: 8px;
        padding: 9px 12px;
        margin-bottom: 6px;
        font-size: {fs}px !important;
        font-weight: 500;
        color: {hi_txt} !important;
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }}

    /* WhatsApp Button */
    .ss-wa-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background-color: #25D366;
        color: #FFFFFF !important;
        padding: 9px 16px;
        font-size: {btn_size}px;
        font-weight: 700;
        border-radius: 8px;
        text-decoration: none;
        width: 100%;
        box-shadow: 0 2px 6px rgba(37, 211, 102, 0.25);
        transition: all 0.15s ease;
    }}

    .ss-wa-btn:hover {{
        background-color: #1EBE5D;
        color: #FFFFFF !important;
    }}

    /* Helpline Banner */
    .ss-helpline-card {{
        background: linear-gradient(135deg, #B91C1C 0%, #DC2626 100%);
        border-radius: 10px;
        padding: 14px 18px;
        color: #FFFFFF !important;
        margin-top: 14px;
    }}

    .ss-helpline-card * {{
        color: #FFFFFF !important;
    }}

    /* Quiz Card */
    .ss-quiz-card {{
        background: {card_bg};
        border: 1.5px solid {card_border};
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }}

    .ss-quiz-correct {{
        background: {low_bg};
        border-left: 3px solid {low_border};
        padding: 9px 12px;
        border-radius: 6px;
        margin-top: 6px;
        font-weight: 500;
        font-size: {fs}px;
    }}

    .ss-quiz-incorrect {{
        background: {hi_bg};
        border-left: 3px solid {hi_border};
        padding: 9px 12px;
        border-radius: 6px;
        margin-top: 6px;
        font-weight: 500;
        font-size: {fs}px;
    }}
    </style>
    """

ICONS = {
    "shield_main": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "shield_check": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>',
    "shield_alert": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
    "lock": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "globe": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "message": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "alert_triangle": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#EF4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "check_circle": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "phone_call": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.61 3.4 2 2 0 0 1 3.6 1.22h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 8.82a16 16 0 0 0 6.29 6.29l.96-.96a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "speaker": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>',
    "stop": '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>',
    "whatsapp": '<svg width="16" height="16" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>',
    "brain": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-2.04z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-2.04z"/></svg>',
    "user_caregiver": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>',
    "bulb": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="9" y1="18" x2="15" y2="18"/><line x1="10" y1="22" x2="14" y2="22"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/></svg>',
    "settings": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#49316F" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "book": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    "home": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7653B5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "dots": '<svg width="18" height="18" viewBox="0 0 24 24" fill="#49316F"><circle cx="12" cy="5" r="2.2"/><circle cx="12" cy="12" r="2.2"/><circle cx="12" cy="19" r="2.2"/></svg>'
}
