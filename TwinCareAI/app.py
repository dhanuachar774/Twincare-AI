"""TwinCare AI — Healthcare Digital Twin & Risk Analytics Dashboard.

Phase 1 Prototype: Demonstrates synthetic physiological telemetry simulation,
dynamic digital twin state evaluation, multi-organ homeostasis indices,
and interactive hospital-grade visualizations.

DISCLAIMER: Synthetically simulated telemetry only. Not for clinical diagnosis.
"""

import streamlit as st
import pandas as pd
from config import (
    APP_NAME,
    APP_SUBTITLE,
    APP_VERSION,
    PATIENT_PRESETS,
    BACKGROUND_THEMES,
)
from modules.simulator import SyntheticTelemetrySimulator
from modules.twin_state import DigitalTwinStateEngine
from modules.visualizer import (
    plot_cardiovascular_telemetry,
    plot_metabolic_glycemic_curve,
    plot_respiratory_spo2,
    plot_stability_gauge,
    plot_organ_radar,
    plot_circadian_activity_hr,
)
from modules.components import (
    render_html,
    inject_custom_css,
    render_disclaimer_banner,
    render_twin_command_hero,
    render_vital_cards,
    render_anomaly_alerts,
)

# 1. Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} — Healthcare Digital Twin",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme Selector (Simple Dark / Light Mode)
theme_option = st.sidebar.radio(
    "🌓 Theme Mode:",
    options=["🌙 Dark Theme", "☀️ Light Theme"],
    index=0,
    horizontal=True,
    help="Toggle between Dark (Cyber Pink & Neon Orchid) and Light (Rose Quartz & Berry) theme.",
)
selected_theme_key = "dark" if "Dark" in theme_option else "light"
theme_cfg = BACKGROUND_THEMES[selected_theme_key]
is_dark = theme_cfg.get("is_dark", True)

# Inject dynamic theme styling
inject_custom_css(selected_theme_key)

# 2. Sidebar: Virtual Patient & Simulation Controls
sidebar_brand_box = theme_cfg.get(
    "sidebar_brand_box",
    "background: linear-gradient(135deg, #FF2A85 0%, #9333EA 100%); color:#FFFFFF; border-radius:14px; padding:16px; margin-bottom:16px;",
)
accent_primary = theme_cfg.get("accent_primary", "#FF2A85")
sidebar_sub_color = theme_cfg.get("text_secondary", "#E9D5FF" if is_dark else "#475569")

with st.sidebar:
    render_html(
        f"""
        <div style="{sidebar_brand_box}">
            <div style="font-size:1.45rem; font-weight:800; color:#FFFFFF; display:flex; align-items:center; gap:8px;">
                <span>🧬</span> {APP_NAME}
            </div>
            <div style="font-size:0.75rem; color:{sidebar_sub_color}; margin-top:3px; line-height:1.35;">
                {APP_SUBTITLE}
            </div>
        </div>
        """
    )

st.sidebar.markdown("### 👤 Virtual Patient Configuration")

# Preset Selector
preset_keys = list(PATIENT_PRESETS.keys())
preset_labels = [PATIENT_PRESETS[k]["name"] for k in preset_keys]

selected_preset_label = st.sidebar.selectbox(
    "Clinical Cohort Archetype:",
    options=preset_labels,
    index=1,  # Default to Desk Worker
    help="Quickly load pre-calibrated digital twin profiles representing typical physiological cohorts.",
)

preset_key = preset_keys[preset_labels.index(selected_preset_label)]
preset_data = PATIENT_PRESETS[preset_key]

# Virtual Patient Parameters
patient_id = st.sidebar.text_input("Patient Identifier", value=preset_data["patient_id"])
col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    age = st.number_input("Age (Years)", min_value=18, max_value=99, value=int(preset_data["age"]), step=1)
with col_sb2:
    gender = st.selectbox("Biological Sex", options=["Female", "Male", "Other"], index=0 if preset_data["gender"] == "Female" else 1)

activity_level = st.sidebar.selectbox(
    "🏃 Activity Level",
    options=["Sedentary", "Light (Walking)", "Moderate", "High (Athletic)"],
    index=["Sedentary", "Light (Walking)", "Moderate", "High (Athletic)"].index(preset_data["activity_level"]),
)

sleep_hours = st.sidebar.slider(
    "🌙 Sleep Duration (Hours / Day)",
    min_value=4.0,
    max_value=11.0,
    value=float(preset_data["sleep_hours"]),
    step=0.5,
    help="Daily average sleep window. Low sleep significantly impacts nocturnal dipping and autonomic balance.",
)

stress_level = st.sidebar.select_slider(
    "⚡ Perceived Stress Level",
    options=["Low", "Moderate", "High"],
    value=preset_data["stress_level"],
)

with st.sidebar.expander("⚙️ Calibrate Baseline Vitals", expanded=False):
    baseline_hr = st.slider("Resting Heart Rate (BPM)", 45, 110, int(preset_data["baseline_hr"]))
    baseline_bp_sys = st.slider("Systolic BP (mmHg)", 85, 160, int(preset_data["baseline_bp_sys"]))
    baseline_bp_dia = st.slider("Diastolic BP (mmHg)", 55, 105, int(preset_data["baseline_bp_dia"]))
    baseline_glucose = st.slider("Fasting Blood Glucose (mg/dL)", 65, 140, int(preset_data["baseline_glucose"]))

# Telemetry Controls
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Telemetry Stream Controls")

col_t1, col_t2 = st.sidebar.columns(2)
with col_t1:
    sim_duration_option = st.selectbox(
        "Time Horizon:",
        options=["Last 12 Hours", "Last 24 Hours", "Last 48 Hours", "Last 7 Days"],
        index=1,
        help="Simulated patient observation duration.",
    )
with col_t2:
    sim_resolution_option = st.selectbox(
        "Sensor Interval:",
        options=["15 Minutes", "30 Minutes", "60 Minutes"],
        index=0,
        help="Wearable biometric sampling frequency.",
    )

duration_hours_map = {
    "Last 12 Hours": 12,
    "Last 24 Hours": 24,
    "Last 48 Hours": 48,
    "Last 7 Days": 168,
}
duration_hours = duration_hours_map[sim_duration_option]

resolution_map = {
    "15 Minutes": 15,
    "30 Minutes": 30,
    "60 Minutes": 60,
}
interval_minutes = resolution_map[sim_resolution_option]

# Live Anomaly Injection for Hackathon Demos
inject_anomaly = st.sidebar.checkbox(
    "Simulate Acute Anomaly",
    value=False,
    help="Inject a transient physiological perturbation to demonstrate the digital twin's dynamic response live.",
)
anomaly_type = "Tachycardia Spike"
if inject_anomaly:
    anomaly_type = st.sidebar.selectbox(
        "Anomaly Archetype:",
        options=[
            "Tachycardia Spike",
            "Hypertensive Episode",
            "Nocturnal Hypoxemia",
            "Post-prandial Spike",
        ],
    )

# Simulation Seed
if "sim_seed" not in st.session_state:
    st.session_state.sim_seed = 42

if st.sidebar.button("🔄 Resimulate Telemetry", use_container_width=True):
    st.session_state.sim_seed = (st.session_state.sim_seed + 7) % 1000
    st.rerun()

# 3. Build Active Profile
active_profile = {
    "name": preset_data["name"] if preset_key != "custom" else f"Patient {patient_id}",
    "patient_id": patient_id,
    "age": age,
    "gender": gender,
    "activity_level": activity_level,
    "sleep_hours": sleep_hours,
    "stress_level": stress_level,
    "baseline_hr": baseline_hr,
    "baseline_bp_sys": baseline_bp_sys,
    "baseline_bp_dia": baseline_bp_dia,
    "baseline_glucose": baseline_glucose,
}

# 4. Run Telemetry Engine
simulator = SyntheticTelemetrySimulator(profile=active_profile, random_seed=st.session_state.sim_seed)
telemetry_df = simulator.generate_timeline(
    duration_hours=duration_hours,
    interval_minutes=interval_minutes,
    inject_anomaly=inject_anomaly,
    anomaly_type=anomaly_type,
)

# 5. Evaluate Digital Twin Current State
state_engine = DigitalTwinStateEngine(profile=active_profile)
twin_state = state_engine.evaluate_current_state(telemetry_df)

# 6. Main Dashboard Interface
# Header Section Styling
accent_primary = theme_cfg.get("accent_primary", "#FF2A85")
accent_secondary = theme_cfg.get("accent_secondary", "#A855F7")
header_title_color = theme_cfg.get("header_title_color", "#FF2A85")
header_sub_color = theme_cfg.get("text_secondary", "#E9D5FF" if is_dark else "#475569")
header_box_bg = f"background:{theme_cfg.get('card_bg')}; border:1px solid {theme_cfg.get('border')}; box-shadow:{theme_cfg.get('shadow')};"
header_box_text = theme_cfg.get("text_primary", "#FFFFFF")

col_head1, col_head2 = st.columns([0.65, 0.35])
with col_head1:
    render_html(
        f"""
        <div style="margin-bottom:12px;">
            <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.12em; color:{accent_primary}; font-weight:700; margin-bottom:4px; display:flex; align-items:center; gap:6px;">
                <span style="color:{accent_primary};">●</span> VIRTUAL PHYSIOLOGICAL TELEMETRY LAB
            </div>
            <h1 style="margin:0; font-size:2.5rem; font-weight:800; letter-spacing:-0.03em; color:{header_title_color}; line-height:1.15; display:flex; align-items:center; gap:10px;">
                <span>🧬</span> {APP_NAME}
            </h1>
            <p style="color:{header_sub_color}; font-size:0.95rem; margin-top:5px; margin-bottom:0;">
                {APP_SUBTITLE}
            </p>
        </div>
        """
    )
with col_head2:
    render_html(
        f"""
        <div style="text-align:right; padding-top:8px;">
            <div style="display:inline-block; {header_box_bg} border-radius:12px; padding:10px 16px; text-align:right;">
                <div style="font-family:'JetBrains Mono', monospace; font-size:0.70rem; color:{'#64748B' if not is_dark else '#94A3B8'}; text-transform:uppercase; letter-spacing:0.06em;">
                    Biometric Telemetry Stream <span style="color:#059669; font-weight:700;">● Active</span>
                </div>
                <div style="font-size:0.86rem; font-weight:700; color:{header_box_text}; margin-top:3px;">
                    {len(telemetry_df)} Time Samples &nbsp;|&nbsp; {duration_hours}h Horizon ({interval_minutes}m step)
                </div>
            </div>
        </div>
        """
    )

# Mandatory Academic & Non-Medical Disclaimer Ribbon
render_disclaimer_banner()

# Unified High-Tech Digital Twin Command Hero Bar
render_twin_command_hero(active_profile, twin_state, is_dark=is_dark, theme_key=selected_theme_key)

# Live Vital Telemetry KPI Cards with High-Contrast Accent Strips
stream_title_color = theme_cfg.get("text_primary", "#FFFFFF")
stream_sub_color = theme_cfg.get("text_secondary", "#94A3B8")
render_html(
    f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin:16px 0 10px 0;">
        <div style="font-size:1.05rem; font-weight:700; color:{stream_title_color}; letter-spacing:-0.01em;">
            ⚡ Virtual Patient Live Telemetry Stream
        </div>
        <div style="font-size:0.75rem; color:{stream_sub_color};">
            Auto-synchronized with Circadian Phase
        </div>
    </div>
    """
)
render_vital_cards(twin_state["vitals"])

# Main Dashboard Navigation Tabs
tab_telemetry, tab_risk, tab_data, tab_guide = st.tabs([
    "📈 Time-Series Telemetry",
    "🧬 Physiological Stability & Risk",
    "📋 Raw Telemetry Data & Export",
    "🎯 Presentation & Architecture Guide",
])

# -------------------------------------------------------------
# TAB 1: Time-Series Telemetry
# -------------------------------------------------------------
with tab_telemetry:
    render_html(
        f"""
        <div style="margin-bottom:8px;">
            <strong style="font-size:1.05rem; color:{stream_title_color};">Interactive Continuous Telemetry Stream</strong>
            <p style="color:{stream_sub_color}; font-size:0.84rem; margin:2px 0 14px 0;">
                Displays continuous multi-sensor traces with shaded nocturnal sleep recovery bands and clinical safety boundaries.
            </p>
        </div>
        """
    )

    # Chart 1: Cardiovascular (HR + BP)
    fig_cv = plot_cardiovascular_telemetry(telemetry_df, is_dark=is_dark, theme_key=selected_theme_key)
    st.plotly_chart(fig_cv, use_container_width=True)

    col_chart_a, col_chart_b = st.columns(2)
    with col_chart_a:
        # Chart 2: Blood Glucose
        fig_glucose = plot_metabolic_glycemic_curve(telemetry_df, is_dark=is_dark, theme_key=selected_theme_key)
        st.plotly_chart(fig_glucose, use_container_width=True)

    with col_chart_b:
        # Chart 3: Blood Oxygen (SpO2)
        fig_spo2 = plot_respiratory_spo2(telemetry_df, is_dark=is_dark, theme_key=selected_theme_key)
        st.plotly_chart(fig_spo2, use_container_width=True)

    # Chart 4: Activity vs Heart Rate
    fig_activity = plot_circadian_activity_hr(telemetry_df, is_dark=is_dark, theme_key=selected_theme_key)
    st.plotly_chart(fig_activity, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: Physiological Stability & Risk Analytics
# -------------------------------------------------------------
with tab_risk:
    render_html(
        f"""
        <div style="margin-bottom:8px;">
            <strong style="font-size:1.05rem; color:{stream_title_color};">Multi-System Homeostatic Resilience Analysis</strong>
            <p style="color:{stream_sub_color}; font-size:0.84rem; margin:2px 0 14px 0;">
                Quantitative mathematical indices tracking physiological variance across five core biological subsystems.
            </p>
        </div>
        """
    )

    col_risk1, col_risk2 = st.columns([0.45, 0.55])
    with col_risk1:
        st.markdown("##### Homeostasis Stability Gauge")
        fig_gauge = plot_stability_gauge(
            twin_state["stability_index"],
            twin_state["resilience_tier"],
            is_dark=is_dark,
            theme_key=selected_theme_key,
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("##### Multi-Organ System Balance Radar")
        fig_radar = plot_organ_radar(twin_state["sub_scores"], is_dark=is_dark, theme_key=selected_theme_key)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_risk2:
        st.markdown("##### Subsystem Stability Breakdown")
        for sub_name, score_val in twin_state["sub_scores"].items():
            col_s1, col_s2 = st.columns([0.42, 0.58])
            with col_s1:
                st.write(f"**{sub_name}**")
            with col_s2:
                st.progress(int(score_val) / 100, text=f"{score_val}%")

        st.markdown("##### Detected Telemetry Anomalies & Events")
        render_anomaly_alerts(twin_state["anomalies"], is_dark=is_dark)

        st.markdown("##### Digital Twin Observations")
        st.info(
            f"**Circadian Dipping Assessment:** Under current profile parameters (sleep: {sleep_hours} hrs, "
            f"activity: {activity_level}), the virtual twin models a ~14% resting heart rate dip during nocturnal "
            f"sleep. Current perceived stress level ('{stress_level}') produces an estimated baseline autonomic "
            f"variance factor of ±{5 if stress_level == 'Low' else (10 if stress_level == 'Moderate' else 18)}%."
        )

# -------------------------------------------------------------
# TAB 3: Raw Telemetry Data & Export
# -------------------------------------------------------------
with tab_data:
    render_html(
        f"""
        <div style="margin-bottom:8px;">
            <strong style="font-size:1.05rem; color:{stream_title_color};">Telemetry Dataset Inspection & Export</strong>
            <p style="color:{stream_sub_color}; font-size:0.84rem; margin:2px 0 14px 0;">
                Inspect every synthetic reading generated by the simulation engine. Tagged with <code>is_simulated = True</code>.
            </p>
        </div>
        """
    )

    st.dataframe(
        telemetry_df.style.format({
            "heart_rate": "{:.1f}",
            "blood_pressure_systolic": "{:.1f}",
            "blood_pressure_diastolic": "{:.1f}",
            "spo2": "{:.1f}",
            "blood_glucose": "{:.1f}",
            "temperature": "{:.2f}",
            "respiratory_rate": "{:.1f}",
            "stress_index": "{:.1f}",
        }),
        use_container_width=True,
        height=320,
    )

    col_stat1, col_stat2 = st.columns([0.65, 0.35])
    with col_stat1:
        st.markdown("##### Descriptive Statistics (Simulated Stream)")
        st.dataframe(
            telemetry_df[[
                "heart_rate", "blood_pressure_systolic", "blood_pressure_diastolic",
                "spo2", "blood_glucose", "temperature"
            ]].describe().round(2),
            use_container_width=True,
        )

    with col_stat2:
        st.markdown("##### Export Telemetry Stream")
        st.write("Export synthetic readings for external validation or future ML pipeline ingestion.")
        csv_data = telemetry_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Telemetry (CSV)",
            data=csv_data,
            file_name=f"twincare_synthetic_telemetry_{patient_id}.csv",
            mime="text/csv",
            use_container_width=True,
        )

# -------------------------------------------------------------
# TAB 4: Presentation & Architecture Guide (For Hackathon Pitch)
# -------------------------------------------------------------
with tab_guide:
    st.markdown("#### Hackathon Presentation & Technical Architecture Guide")
    st.markdown(
        """
        Welcome to **TwinCare AI**! As an AIML engineering student presenting this project to hackathon judges,
        use the structured guide below to explain the system architecture, mathematical models, and development roadmap.
        """
    )

    with st.expander("🎯 1. 60-Second Elevator Pitch for Judges", expanded=True):
        st.markdown(
            """
            > *"Judges, chronic illness management and acute patient deterioration are often caught too late because wearable data is analyzed in fragmented silos. **TwinCare AI** introduces a **Healthcare Digital Twin** framework that models multi-organ physiological state in real time.
            >
            > In Phase 1, we established a modular computational twin architecture: it generates circadian-synchronized telemetry, monitors continuous deviations across 5 physiological subsystems, and computes an aggregate Homeostatic Stability Index. In Phase 2, we integrate predictive ML risk estimators trained on the official hackathon problem statement."*
            """
        )

    with st.expander("⚙️ 2. Core Mathematical & Physiological Formulations", expanded=False):
        st.markdown(
            """
            - **Circadian Harmonic Modeling:**
              $$HR(t) = HR_{base} + A_{circ} \\cdot \\cos\\left(\\frac{2\\pi (t_{hour} - 16)}{24}\\right) + \\Delta_{exercise} - \\Delta_{nocturnal} + \\epsilon$$
              Biomarkers follow a 24-hour diurnal phase peaking in late afternoon and reaching nadir during deep nocturnal sleep.
            - **Post-prandial Glycemic Surges:**
              Modeled using an asymmetric exponential impulse curve:
              $$G(t) = G_{base} + \\sum_{m \\in Meals} \\Delta G_m \\cdot \\left(\\frac{t - t_m}{\\tau}\\right) e^{1 - \\frac{t - t_m}{\\tau}}$$
            - **Homeostasis Stability Score:**
              A multi-attribute heuristic risk equation weighted across Cardiovascular ($30\\%$), Respiratory/Oxygenation ($25\\%$), Metabolic Regulation ($20\\%$), Circadian Restoration ($15\\%$), and Autonomic Stress ($10\\%$).
            """
        )

    with st.expander("🗺️ 3. Roadmap: Phase 1 vs. Phase 2", expanded=True):
        st.markdown(
            """
            | Phase | Status | Key Deliverables |
            | :--- | :--- | :--- |
            | **Phase 1** | **Completed** | Clean modular architecture, synthetic telemetry engine with circadian rhythms, virtual patient profile configuration, interactive Plotly dashboard, digital twin current state evaluation, rigorous disclaimers. |
            | **Phase 2** | *Upcoming* | Ingestion of official hackathon dataset, Scikit-learn predictive risk model, cross-validation & ROC-AUC evaluation metrics, what-if counterfactual scenario simulation (digital twin intervention forecasting). |
            """
        )

    with st.expander("🛡️ 4. Clinical Safety & Ethical Compliance Checklist", expanded=False):
        st.markdown(
            """
            - **Zero Diagnostic Claims:** The tool explicitly states it is an architectural prototype and does not provide clinical diagnoses.
            - **Transparent Simulated Flags:** Every record in the database and data stream contains `is_simulated = True`.
            - **Auditability:** Modular codebase separated into simulation, state analytics, visualization, and presentation layers.
            """
        )
