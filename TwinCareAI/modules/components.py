"""TwinCare AI - Modern Healthcare UI Components & Styling Module.

Supports Dark (Cyber Pink & Neon Orchid) and Light (Rose Quartz & Berry) themes
with glassmorphic cards, vivid telemetry badges, and interactive controls.
"""

import textwrap
from typing import Dict, Any, List
import streamlit as st
from config import DISCLAIMER_TEXT, THEMES, BACKGROUND_THEMES


def render_html(html_str: str):
    """Safely render HTML without Markdown converting indented lines to code blocks."""
    clean = textwrap.dedent(html_str).strip()
    clean = "\n".join(line for line in clean.splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


def inject_custom_css(theme_key: str = "dark", **kwargs):
    """Inject modern clinical CSS with full theme synchronization across all Streamlit widgets."""
    themes_map = THEMES if THEMES else BACKGROUND_THEMES
    theme_cfg = themes_map.get(theme_key, themes_map.get("dark", list(themes_map.values())[0]))
    is_dark = theme_cfg.get("is_dark", False)
    bg_css = theme_cfg["css_bg"]
    card_bg = theme_cfg["card_bg"]
    sidebar_bg = theme_cfg.get("sidebar_bg", "#FFFFFF")
    border_color = theme_cfg["border"]
    text_primary = theme_cfg["text_primary"]
    text_secondary = theme_cfg["text_secondary"]
    shadow = theme_cfg.get("shadow", "0 6px 20px rgba(0,0,0,0.06)")

    # Dynamic Theme Tokens
    accent_primary = theme_cfg.get("accent_primary", "#FF2A85" if is_dark else "#E11D48")
    accent_secondary = theme_cfg.get("accent_secondary", "#A855F7" if is_dark else "#9333EA")
    accent_glow = theme_cfg.get("accent_glow", "rgba(255, 42, 133, 0.40)" if is_dark else "rgba(225, 29, 72, 0.35)")
    btn_gradient = theme_cfg.get("btn_gradient", "linear-gradient(135deg, #FF2A85 0%, #9333EA 100%)" if is_dark else "linear-gradient(135deg, #E11D48 0%, #DB2777 100%)")
    input_bg = theme_cfg.get("input_bg", "#200E2E" if is_dark else "#FFFFFF")
    input_text = theme_cfg.get("input_text", "#FFFFFF" if is_dark else "#1E293B")
    input_border = theme_cfg.get("input_border", "rgba(255, 42, 133, 0.40)" if is_dark else "#F472B6")
    label_color = theme_cfg.get("label_color", "#FCE7F3" if is_dark else "#831843")

    if is_dark:
        badge_emerald = "background: rgba(16, 185, 129, 0.18); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.45);"
        badge_cyan = "background: rgba(255, 42, 133, 0.18); color: #FF66AA; border: 1px solid rgba(255, 42, 133, 0.45);"
        badge_amber = "background: rgba(245, 158, 11, 0.20); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.45);"
        badge_rose = "background: rgba(244, 63, 94, 0.22); color: #FB7185; border: 1px solid rgba(244, 63, 94, 0.50);"
        tab_list_bg = "background: rgba(24, 11, 36, 0.85) !important; border: 1px solid rgba(255, 42, 133, 0.20) !important;"
        card_val_color = "#FFFFFF"
        icon_box_bg = "background: rgba(255, 42, 133, 0.12); border: 1px solid rgba(255, 42, 133, 0.25);"
    else:
        badge_emerald = "background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0;"
        badge_cyan = "background: #FDF2F8; color: #DB2777; border: 1px solid #FBCFE8;"
        badge_amber = "background: #FFFBEB; color: #D97706; border: 1px solid #FDE68A;"
        badge_rose = "background: #FFF1F2; color: #E11D48; border: 1px solid #FECDD3;"
        tab_list_bg = "background: #FCE7F3 !important; border: 1px solid #FBCFE8 !important;"
        card_val_color = "#1E293B"
        icon_box_bg = "background: #FFF1F5; border: 1px solid #FBCFE8;"

    tab_active_css = (
        f"background: {btn_gradient} !important; "
        f"color: #FFFFFF !important; border: 1px solid {accent_primary} !important; "
        f"box-shadow: 0 4px 18px {accent_glow} !important;"
    )

    render_html(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* App Background */
        .stApp {{
            {bg_css}
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: {text_primary} !important;
        }}

        /* Clean Themed Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {'#FCE7F3' if not is_dark else 'rgba(14, 7, 23, 0.8)'};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {btn_gradient};
            border-radius: 999px;
        }}

        /* Widget Labels - High contrast & theme matched */
        label[data-testid="stWidgetLabel"],
        label[data-testid="stWidgetLabel"] p,
        label[data-testid="stWidgetLabel"] span,
        .stSelectbox label, 
        .stTextInput label, 
        .stNumberInput label, 
        .stSlider label,
        .stRadio label,
        div[data-testid="stMarkdownContainer"] p {{
            color: {label_color} !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
        }}

        /* Text Input & Number Input Fields */
        div[data-baseweb="input"],
        div[data-baseweb="input"] > input,
        div[data-baseweb="base-input"] {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {input_border} !important;
            border-radius: 10px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 500 !important;
        }}

        div[data-baseweb="input"]:focus-within {{
            border-color: {accent_primary} !important;
            box-shadow: 0 0 0 2px {accent_glow} !important;
        }}

        /* Selectboxes */
        div[data-baseweb="select"] > div {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border: 1px solid {input_border} !important;
            border-radius: 10px !important;
            font-weight: 500 !important;
        }}

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div {{
            color: {input_text} !important;
        }}

        div[data-baseweb="select"] svg {{
            fill: {input_text} !important;
        }}

        div[data-baseweb="select"]:focus-within {{
            border-color: {accent_primary} !important;
            box-shadow: 0 0 0 2px {accent_glow} !important;
        }}

        /* Selectbox Popover Dropdown */
        div[data-baseweb="popover"],
        ul[role="listbox"] {{
            background-color: {input_bg} !important;
            border: 1px solid {input_border} !important;
            border-radius: 12px !important;
            box-shadow: {shadow} !important;
        }}

        li[role="option"] {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            font-size: 0.86rem !important;
            padding: 9px 14px !important;
            transition: all 0.15s ease !important;
        }}

        li[role="option"]:hover,
        li[aria-selected="true"] {{
            background: {accent_glow} !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }}

        /* Radio Buttons */
        div[data-testid="stRadio"] div[role="radiogroup"] {{
            background: {card_bg} !important;
            padding: 6px 10px !important;
            border-radius: 12px !important;
            border: 1px solid {border_color} !important;
            display: flex !important;
            gap: 12px !important;
        }}

        div[data-testid="stRadio"] label span {{
            color: {text_primary} !important;
            font-weight: 700 !important;
        }}

        /* Number Input Step Buttons */
        div[data-testid="stNumberInput"] button {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {input_border} !important;
            border-radius: 8px !important;
        }}

        div[data-testid="stNumberInput"] button:hover {{
            background-color: {accent_glow} !important;
            color: #FFFFFF !important;
        }}

        /* Checkbox & Radio Labels */
        div[data-testid="stCheckbox"] label span {{
            color: {text_primary} !important;
            font-weight: 600 !important;
        }}

        /* Slider Thumb & Track */
        .stSlider [data-baseweb="slider"] div[role="slider"] {{
            background-color: {accent_primary} !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 0 10px {accent_glow} !important;
        }}

        /* Expanders */
        [data-testid="stExpander"] {{
            background: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 14px !important;
            margin-bottom: 12px !important;
        }}

        [data-testid="stExpander"] summary {{
            color: {text_primary} !important;
            font-weight: 700 !important;
        }}

        /* Streamlit Tab Overrides */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px !important;
            {tab_list_bg}
            padding: 6px 10px !important;
            border-radius: 14px !important;
            backdrop-filter: blur(12px) !important;
            margin-bottom: 20px !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 42px !important;
            padding: 0 20px !important;
            background: transparent !important;
            border-radius: 10px !important;
            color: {text_secondary} !important;
            font-weight: 600 !important;
            font-size: 0.90rem !important;
            border: 1px solid transparent !important;
            transition: all 0.25s ease !important;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            color: {text_primary} !important;
        }}

        .stTabs [aria-selected="true"] {{
            {tab_active_css}
        }}

        .stTabs [data-baseweb="tab-highlight"] {{
            display: none !important;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background: {sidebar_bg} !important;
            border-right: 1px solid {border_color} !important;
        }}

        /* Cards */
        .telemetry-card {{
            background: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: {shadow} !important;
            position: relative;
            overflow: hidden;
            transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
            min-height: 156px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .telemetry-card:hover {{
            transform: translateY(-4px);
            border-color: {accent_primary} !important;
            box-shadow: 0 16px 36px {accent_glow} !important;
        }}

        /* Top Accent Strips */
        .card-top-strip {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
        }}

        .strip-hr {{ background: linear-gradient(90deg, #FF2A85, #FB7185); }}
        .strip-bp {{ background: linear-gradient(90deg, #A855F7, #C084FC); }}
        .strip-spo2 {{ background: linear-gradient(90deg, #0284C7, #38BDF8); }}
        .strip-glucose {{ background: linear-gradient(90deg, #F43F5E, #FB7185); }}
        .strip-temp {{ background: linear-gradient(90deg, #059669, #10B981); }}

        /* Card Header */
        .card-header-flex {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
        }}

        .card-icon-pill {{
            display: flex;
            align-items: center;
            gap: 7px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: {text_secondary};
        }}

        .icon-circle {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.90rem;
            {icon_box_bg}
        }}

        /* Card Value */
        .card-val-container {{
            margin: 4px 0 10px 0;
            display: flex;
            align-items: baseline;
            gap: 6px;
        }}

        .card-val {{
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -0.02em;
            color: {card_val_color} !important;
            font-feature-settings: "tnum";
            font-variant-numeric: tabular-nums;
        }}

        .card-unit {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {text_secondary};
        }}

        /* Card Footer */
        .card-footer-flex {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.74rem;
            color: {text_secondary};
            border-top: 1px solid {'#FCE7F3' if not is_dark else 'rgba(255, 255, 255, 0.06)'};
            padding-top: 8px;
            margin-top: 4px;
        }}

        /* Badges */
        .badge-pill {{
            font-size: 0.68rem;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 9999px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .badge-emerald {{ {badge_emerald} }}
        .badge-cyan {{ {badge_cyan} }}
        .badge-amber {{ {badge_amber} }}
        .badge-rose {{ {badge_rose} }}

        /* Command Hero Card */
        .twin-hero-card {{
            background: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 18px;
            padding: 22px 26px;
            margin-bottom: 22px;
            box-shadow: {shadow} !important;
            position: relative;
            overflow: hidden;
        }}

        .pulse-beacon {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: {accent_primary};
            box-shadow: 0 0 10px {accent_primary};
            margin-right: 7px;
            animation: beacon-pulse 1.8s infinite ease-in-out;
        }}

        @keyframes beacon-pulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.35); opacity: 0.55; }}
        }}

        /* Disclaimer Ribbon */
        .disclaimer-ribbon {{
            background: {'#FFFBEB' if not is_dark else 'rgba(25, 12, 38, 0.75)'};
            border-left: 4px solid #F59E0B;
            border-radius: 10px;
            padding: 12px 18px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 14px;
            font-size: 0.82rem;
            color: {'#92400E' if not is_dark else '#E2E8F0'};
            border: 1px solid {'#FDE68A' if not is_dark else 'rgba(245, 158, 11, 0.3)'};
            border-left-width: 4px;
        }}

        /* Primary Button */
        .stButton button {{
            background: {btn_gradient} !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            box-shadow: 0 4px 16px {accent_glow} !important;
            transition: all 0.25s ease !important;
        }}

        .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px {accent_glow} !important;
            color: #FFFFFF !important;
        }}
        </style>
        """
    )


def render_disclaimer_banner(*args, **kwargs):
    """Render the academic & non-medical compliance banner."""
    render_html(
        f"""
        <div class="disclaimer-ribbon">
            <span style="font-size:1.35rem; line-height:1;">🛡️</span>
            <div>
                <strong style="text-transform:uppercase; letter-spacing:0.04em;">Hackathon Research & Prototype Disclaimer:</strong>
                <span> {DISCLAIMER_TEXT}</span>
            </div>
        </div>
        """
    )


def render_twin_command_hero(profile: Dict[str, Any], state: Dict[str, Any], is_dark: bool = True, theme_key: str = "dark", **kwargs):
    """Render high-end Bio-Digital Twin Command Center hero card synchronized with active theme."""
    themes_map = THEMES if THEMES else BACKGROUND_THEMES
    theme_cfg = themes_map.get(theme_key, themes_map.get("dark" if is_dark else "light", list(themes_map.values())[0]))
    accent_primary = theme_cfg.get("accent_primary", "#FF2A85" if is_dark else "#E11D48")
    accent_secondary = theme_cfg.get("accent_secondary", "#A855F7" if is_dark else "#9333EA")
    accent_glow = theme_cfg.get("accent_glow", "rgba(255, 42, 133, 0.35)" if is_dark else "rgba(225, 29, 72, 0.3)")
    title_color = theme_cfg.get("text_primary", "#FFFFFF" if is_dark else "#1E293B")
    sub_color = theme_cfg.get("text_secondary", "#E9D5FF" if is_dark else "#64748B")
    border_color = theme_cfg.get("border", "rgba(255, 42, 133, 0.25)")
    card_bg = theme_cfg.get("card_bg", "rgba(32, 14, 46, 0.9)")

    patient_id = profile.get("patient_id", "TWIN-001")
    name = profile.get("name", "Virtual Patient")
    age = profile.get("age", 35)
    gender = profile.get("gender", "Female")
    act = profile.get("activity_level", "Moderate")
    sleep = profile.get("sleep_hours", 7.0)
    stress = profile.get("stress_level", "Moderate")

    score = state.get("stability_index", 90.0)
    tier = state.get("resilience_tier", "Optimal")
    badge = state.get("tier_badge", "Stable")
    color = state.get("tier_color", "emerald")

    score_box_bg = f"background: {card_bg}; border: 1px solid {border_color};"

    render_html(
        f"""
        <div class="twin-hero-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
                <div style="flex:1; min-width:280px;">
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                        <span class="pulse-beacon"></span>
                        <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.10em; color:{accent_primary}; font-weight:700;">
                            DIGITAL TWIN INSTANCE SYNCHRONIZED
                        </span>
                        <span style="font-size:0.68rem; background:{accent_glow}; color:#FFFFFF; padding:2px 8px; border-radius:999px; font-weight:700;">
                            LIVE BIO-TELEMETRY
                        </span>
                    </div>
                    <div style="margin:0; font-size:1.85rem; font-weight:800; color:{title_color}; letter-spacing:-0.01em; line-height:1.2;">
                        {name}
                    </div>
                    <div style="display:flex; align-items:center; gap:12px; margin-top:6px; flex-wrap:wrap; font-size:0.84rem; color:{sub_color}; font-family:'JetBrains Mono', monospace;">
                        <span>ID: <strong style="color:{accent_primary};">{patient_id}</strong></span>
                        <span>•</span>
                        <span>Age: <strong style="color:{title_color};">{age}</strong></span>
                        <span>•</span>
                        <span>Sex: <strong style="color:{title_color};">{gender}</strong></span>
                    </div>
                    <div style="display:flex; gap:8px; margin-top:14px; flex-wrap:wrap;">
                        <span class="badge-pill badge-cyan">🏃 Activity: {act}</span>
                        <span class="badge-pill badge-amber">🌙 Sleep: {sleep}h / day</span>
                        <span class="badge-pill badge-rose">⚡ Stress: {stress}</span>
                    </div>
                </div>
                <div style="{score_box_bg} border-radius:14px; padding:16px 20px; min-width:260px; text-align:right;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em; color:{sub_color}; font-weight:600;">
                            Homeostatic Balance
                        </span>
                        <span class="badge-pill badge-{color}">{badge}</span>
                    </div>
                    <div style="display:flex; align-items:baseline; justify-content:flex-end; gap:4px;">
                        <span style="font-size:2.5rem; font-weight:800; color:{accent_primary}; line-height:1; font-feature-settings:'tnum';">
                            {score}
                        </span>
                        <span style="font-size:1.1rem; color:{sub_color}; font-weight:600;">%</span>
                    </div>
                    <div style="width:100%; height:7px; background:rgba(0,0,0,0.2); border-radius:999px; overflow:hidden; margin:8px 0 6px 0; border:1px solid {border_color};">
                        <div style="width:{score}%; height:100%; background:linear-gradient(90deg, {accent_primary} 0%, {accent_secondary} 100%); border-radius:999px;"></div>
                    </div>
                    <div style="font-size:0.75rem; color:{sub_color}; text-align:right;">
                        Tier: <strong style="color:{title_color};">{tier}</strong>
                    </div>
                </div>
            </div>
        </div>
        """
    )


def render_vital_cards(vitals: Dict[str, Any], *args, **kwargs):
    """Render 5-column live telemetry cards with high-contrast accent strips."""
    cols = st.columns(5)

    # 1. Heart Rate
    hr = vitals.get("heart_rate", {})
    delta_hr = hr.get("delta", 0)
    delta_hr_str = f"▲ +{delta_hr}" if delta_hr > 0 else (f"▼ {delta_hr}" if delta_hr < 0 else "— 0.0")
    with cols[0]:
        render_html(
            f"""
            <div class="telemetry-card">
                <div class="card-top-strip strip-hr"></div>
                <div>
                    <div class="card-header-flex">
                        <div class="card-icon-pill">
                            <span class="icon-circle">❤️</span>
                            <span>Heart Rate</span>
                        </div>
                        <span class="badge-pill badge-{hr.get('color', 'emerald')}">{hr.get('status', 'Normal')}</span>
                    </div>
                    <div class="card-val-container">
                        <span class="card-val">{hr.get('value', '--')}</span>
                        <span class="card-unit">BPM</span>
                    </div>
                </div>
                <div class="card-footer-flex">
                    <span style="color:#FF2A85; font-weight:700;">{delta_hr_str}</span>
                    <span>Ref: {hr.get('normal_range', '60-100')}</span>
                </div>
            </div>
            """
        )

    # 2. Blood Pressure
    bp = vitals.get("blood_pressure", {})
    with cols[1]:
        render_html(
            f"""
            <div class="telemetry-card">
                <div class="card-top-strip strip-bp"></div>
                <div>
                    <div class="card-header-flex">
                        <div class="card-icon-pill">
                            <span class="icon-circle">🩺</span>
                            <span>Pressure</span>
                        </div>
                        <span class="badge-pill badge-{bp.get('color', 'emerald')}">{bp.get('status', 'Normal')}</span>
                    </div>
                    <div class="card-val-container">
                        <span class="card-val">{bp.get('display', '--')}</span>
                        <span class="card-unit">mmHg</span>
                    </div>
                </div>
                <div class="card-footer-flex">
                    <span style="color:#A855F7; font-weight:700;">Δ {bp.get('delta', '0 sys')}</span>
                    <span>Ref: &lt;120/80</span>
                </div>
            </div>
            """
        )

    # 3. SpO2
    spo2 = vitals.get("spo2", {})
    delta_spo2 = spo2.get("delta", 0)
    delta_spo2_str = f"▲ +{delta_spo2}%" if delta_spo2 > 0 else (f"▼ {delta_spo2}%" if delta_spo2 < 0 else "— 0.0%")
    with cols[2]:
        render_html(
            f"""
            <div class="telemetry-card">
                <div class="card-top-strip strip-spo2"></div>
                <div>
                    <div class="card-header-flex">
                        <div class="card-icon-pill">
                            <span class="icon-circle">🫁</span>
                            <span>Oxygen</span>
                        </div>
                        <span class="badge-pill badge-{spo2.get('color', 'emerald')}">{spo2.get('status', 'Optimal')}</span>
                    </div>
                    <div class="card-val-container">
                        <span class="card-val">{spo2.get('value', '--')}</span>
                        <span class="card-unit">%</span>
                    </div>
                </div>
                <div class="card-footer-flex">
                    <span style="color:#0284C7; font-weight:700;">{delta_spo2_str}</span>
                    <span>Ref: 95-100%</span>
                </div>
            </div>
            """
        )

    # 4. Blood Glucose
    glu = vitals.get("blood_glucose", {})
    delta_glu = glu.get("delta", 0)
    delta_glu_str = f"▲ +{delta_glu}" if delta_glu > 0 else (f"▼ {delta_glu}" if delta_glu < 0 else "— 0.0")
    with cols[3]:
        render_html(
            f"""
            <div class="telemetry-card">
                <div class="card-top-strip strip-glucose"></div>
                <div>
                    <div class="card-header-flex">
                        <div class="card-icon-pill">
                            <span class="icon-circle">🩸</span>
                            <span>Glucose</span>
                        </div>
                        <span class="badge-pill badge-{glu.get('color', 'emerald')}">{glu.get('status', 'Normal')}</span>
                    </div>
                    <div class="card-val-container">
                        <span class="card-val">{glu.get('value', '--')}</span>
                        <span class="card-unit">mg/dL</span>
                    </div>
                </div>
                <div class="card-footer-flex">
                    <span style="color:#F43F5E; font-weight:700;">{delta_glu_str}</span>
                    <span>Ref: 70-140</span>
                </div>
            </div>
            """
        )

    # 5. Temperature
    temp = vitals.get("temperature", {})
    delta_temp = temp.get("delta", 0)
    delta_temp_str = f"▲ +{delta_temp}°" if delta_temp > 0 else (f"▼ {delta_temp}°" if delta_temp < 0 else "— 0.0°")
    with cols[4]:
        render_html(
            f"""
            <div class="telemetry-card">
                <div class="card-top-strip strip-temp"></div>
                <div>
                    <div class="card-header-flex">
                        <div class="card-icon-pill">
                            <span class="icon-circle">🌡️</span>
                            <span>Temp</span>
                        </div>
                        <span class="badge-pill badge-{temp.get('color', 'emerald')}">{temp.get('status', 'Normal')}</span>
                    </div>
                    <div class="card-val-container">
                        <span class="card-val">{temp.get('value', '--')}</span>
                        <span class="card-unit">°F</span>
                    </div>
                </div>
                <div class="card-footer-flex">
                    <span style="color:#059669; font-weight:700;">{delta_temp_str}</span>
                    <span>Ref: 97.7-99.5</span>
                </div>
            </div>
            """
        )


def render_anomaly_alerts(anomalies: List[Dict[str, Any]], is_dark: bool = False, *args, **kwargs):
    """Render simulated telemetry anomalies in stylish alert cards."""
    if not anomalies:
        render_html(
            f"""
            <div style="background:{'#ECFDF5' if not is_dark else 'rgba(16, 185, 129, 0.1)'};
                        border-left:4px solid #059669; border-radius:10px; padding:14px 18px; margin-bottom:12px;
                        border:1px solid {'#A7F3D0' if not is_dark else 'rgba(16, 185, 129, 0.2)'}; border-left-width:4px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1.1rem; color:#059669;">✓</span>
                    <strong style="color:#059669; font-size:0.88rem;">Optimal Homeostasis: Zero Critical Excursions</strong>
                </div>
                <div style="font-size:0.82rem; color:{'#475569' if not is_dark else '#94A3B8'}; margin-top:4px;">
                    All synthetic telemetry points remain within target physiological baseline tolerances.
                </div>
            </div>
            """
        )
        return

    for alert in anomalies:
        sev = alert.get("severity", "Info")
        border_col = "#EF4444" if sev == "Alert" else ("#F59E0B" if sev == "Warning" else "#0284C7")
        bg_col = "#FEF2F2" if (not is_dark and sev == "Alert") else ("#FFFBEB" if not is_dark and sev == "Warning" else "#F0F9FF") if not is_dark else "rgba(255, 71, 87, 0.12)"
        t_str = alert.get("timestamp").strftime("%b %d, %H:%M") if hasattr(alert.get("timestamp"), "strftime") else str(alert.get("timestamp"))

        render_html(
            f"""
            <div style="background:{bg_col}; border-left:4px solid {border_col}; border-radius:10px; padding:12px 16px; margin-bottom:10px;
                        border:1px solid {border_col}44; border-left-width:4px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:{'#0F172A' if not is_dark else '#FFFFFF'}; font-size:0.88rem;">
                        {alert.get('type')} — <span style="color:{border_col};">{alert.get('value')}</span>
                    </strong>
                    <span style="font-size:0.75rem; color:#64748B; font-family:'JetBrains Mono', monospace;">{t_str}</span>
                </div>
                <div style="font-size:0.82rem; color:{'#334155' if not is_dark else '#CBD5E1'}; margin-top:3px;">
                    {alert.get('context')}
                </div>
            </div>
            """
        )


def render_patient_profile_header(profile: Dict[str, Any], *args, **kwargs):
    """Compatibility wrapper."""
    pass


def render_twin_state_overview(state: Dict[str, Any], *args, **kwargs):
    """Compatibility wrapper."""
    pass
