"""TwinCare AI - Configuration and Clinical Thresholds Module.

Defines global constants, clinical reference ranges for telemetry,
patient preset templates, visual themes, and background styles.
"""

# Application Metadata
APP_NAME = "TwinCare AI"
APP_SUBTITLE = "Healthcare Digital Twin & Dynamic Telemetry Analytics"
APP_VERSION = ""

# Mandatory Academic & Non-Medical Disclaimer
DISCLAIMER_TEXT = (
    "TwinCare AI is an experimental hackathon prototype demonstrating "
    "digital twin computational modeling on synthetic telemetry data. "
    "This system does NOT provide clinical diagnoses, medical advice, or validated prognosis. "
    "All telemetry values, patient models, and risk trends are 100% synthetically simulated "
    "for academic evaluation and proof-of-concept testing."
)

# Background Styles & Color Themes (Simple Dark / Light Mode)
THEMES = {
    "dark": {
        "name": "🌙 Dark Theme",
        "is_dark": True,
        "css_bg": (
            "background-color: #0E0717 !important; "
            "background-image: "
            "radial-gradient(ellipse 90% 60% at 50% -10%, rgba(255, 42, 133, 0.22), transparent), "
            "radial-gradient(circle at 90% 85%, rgba(168, 85, 247, 0.20), transparent 45%), "
            "linear-gradient(rgba(255, 42, 133, 0.045) 1px, transparent 1px), "
            "linear-gradient(90deg, rgba(255, 42, 133, 0.045) 1px, transparent 1px) !important; "
            "background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px !important;"
        ),
        "card_bg": "linear-gradient(145deg, rgba(32, 14, 46, 0.90) 0%, rgba(18, 9, 28, 0.95) 100%)",
        "sidebar_bg": "linear-gradient(180deg, #160B22 0%, #0C0614 100%)",
        "sidebar_brand_box": "background: linear-gradient(135deg, #FF2A85 0%, #9333EA 100%); color:#FFFFFF; border-radius:14px; padding:16px; margin-bottom:16px; box-shadow:0 6px 20px rgba(255, 42, 133, 0.35);",
        "accent_primary": "#FF2A85",
        "accent_secondary": "#C084FC",
        "accent_violet": "#A855F7",
        "accent_glow": "rgba(255, 42, 133, 0.40)",
        "accent_ring": "rgba(255, 42, 133, 0.25)",
        "btn_gradient": "linear-gradient(135deg, #FF2A85 0%, #9333EA 100%)",
        "chart_paper": "rgba(22, 11, 34, 0.82)",
        "chart_plot": "rgba(14, 7, 23, 0.92)",
        "chart_grid": "rgba(255, 42, 133, 0.10)",
        "text_primary": "#FDF2F8",
        "text_secondary": "#E9D5FF",
        "text_muted": "#A855F7",
        "border": "rgba(255, 42, 133, 0.28)",
        "border_subtle": "rgba(255, 255, 255, 0.08)",
        "input_bg": "#200E2E",
        "input_text": "#FFFFFF",
        "input_border": "rgba(255, 42, 133, 0.40)",
        "label_color": "#FCE7F3",
        "header_title_color": "#FF2A85",
        "shadow": "0 10px 30px rgba(0, 0, 0, 0.5), 0 0 15px rgba(255, 42, 133, 0.12)",
    },
    "light": {
        "name": "☀️ Light Theme",
        "is_dark": False,
        "css_bg": (
            "background-color: #FFF5F7 !important; "
            "background-image: "
            "radial-gradient(ellipse 90% 55% at 50% -10%, rgba(244, 63, 94, 0.15), transparent), "
            "radial-gradient(circle at 90% 90%, rgba(217, 70, 239, 0.12), transparent 50%), "
            "linear-gradient(rgba(251, 207, 216, 0.45) 1px, transparent 1px), "
            "linear-gradient(90deg, rgba(251, 207, 216, 0.45) 1px, transparent 1px) !important; "
            "background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px !important;"
        ),
        "card_bg": "#FFFFFF",
        "sidebar_bg": "linear-gradient(180deg, #FFF0F4 0%, #FDF2F8 100%)",
        "sidebar_brand_box": "background: linear-gradient(135deg, #E11D48 0%, #BE185D 100%); color:#FFFFFF; border-radius:14px; padding:16px; margin-bottom:16px; box-shadow:0 6px 20px rgba(225, 29, 72, 0.25);",
        "accent_primary": "#E11D48",
        "accent_secondary": "#9333EA",
        "accent_violet": "#A855F7",
        "accent_glow": "rgba(225, 29, 72, 0.35)",
        "accent_ring": "rgba(225, 29, 72, 0.20)",
        "btn_gradient": "linear-gradient(135deg, #E11D48 0%, #DB2777 100%)",
        "chart_paper": "#FFFFFF",
        "chart_plot": "#FFF5F7",
        "chart_grid": "#FCE7F3",
        "text_primary": "#1E293B",
        "text_secondary": "#475569",
        "text_muted": "#831843",
        "border": "#FBCFE8",
        "border_subtle": "#FDE2ED",
        "input_bg": "#FFFFFF",
        "input_text": "#1E293B",
        "input_border": "#F472B6",
        "label_color": "#831843",
        "header_title_color": "#E11D48",
        "shadow": "0 8px 24px rgba(225, 29, 72, 0.08), 0 1px 3px rgba(0, 0, 0, 0.04)",
    },
}

BACKGROUND_THEMES = THEMES

# Default Color Palette
THEME_COLORS = {
    "cyan": "#0284C7",
    "blue": "#2563EB",
    "indigo": "#4F46E5",
    "purple": "#7C3AED",
    "coral": "#EF4444",
    "rose": "#E11D48",
    "emerald": "#059669",
    "mint": "#10B981",
    "amber": "#D97706",
    "gold": "#F59E0B",
}

# Physiological Reference Bands (Established General Guidelines for Simulated Baselining)
PHYSIOLOGICAL_THRESHOLDS = {
    "heart_rate": {
        "unit": "BPM",
        "low_warning": 50,
        "normal_min": 60,
        "normal_max": 100,
        "elevated_max": 115,
        "high_warning": 125,
        "label": "Heart Rate",
        "icon": "❤️",
        "accent": "#EF4444",
        "gradient": "linear-gradient(135deg, #EF4444, #F87171)",
    },
    "blood_pressure_systolic": {
        "unit": "mmHg",
        "low_warning": 90,
        "normal_min": 90,
        "normal_max": 120,
        "elevated_max": 129,
        "stage1_max": 139,
        "high_warning": 140,
        "label": "Systolic BP",
        "icon": "🩺",
        "accent": "#4F46E5",
        "gradient": "linear-gradient(135deg, #4F46E5, #6366F1)",
    },
    "blood_pressure_diastolic": {
        "unit": "mmHg",
        "low_warning": 60,
        "normal_min": 60,
        "normal_max": 80,
        "elevated_max": 89,
        "high_warning": 90,
        "label": "Diastolic BP",
    },
    "spo2": {
        "unit": "%",
        "critical_min": 88,
        "warning_min": 92,
        "normal_min": 95,
        "normal_max": 100,
        "label": "Blood Oxygen (SpO2)",
        "icon": "🫁",
        "accent": "#0284C7",
        "gradient": "linear-gradient(135deg, #0284C7, #38BDF8)",
    },
    "glucose": {
        "unit": "mg/dL",
        "hypo_warning": 70,
        "fasting_min": 70,
        "fasting_max": 99,
        "pre_diabetic_max": 125,
        "post_prandial_max": 140,
        "hyper_warning": 180,
        "label": "Blood Glucose",
        "icon": "🩸",
        "accent": "#D97706",
        "gradient": "linear-gradient(135deg, #D97706, #F59E0B)",
    },
    "temperature": {
        "unit": "°F",
        "hypo_warning": 96.0,
        "normal_min": 97.7,
        "normal_max": 99.5,
        "fever_warning": 100.4,
        "label": "Body Temperature",
        "icon": "🌡️",
        "accent": "#059669",
        "gradient": "linear-gradient(135deg, #059669, #10B981)",
    },
    "respiratory_rate": {
        "unit": "breaths/min",
        "normal_min": 12,
        "normal_max": 20,
        "elevated_max": 24,
        "label": "Respiration Rate",
    },
}

# Virtual Patient Presets for Quick Demonstration
PATIENT_PRESETS = {
    "athlete": {
        "name": "Alex Mercer (High Endurance Athlete)",
        "patient_id": "TWIN-ATH-101",
        "age": 26,
        "gender": "Male",
        "activity_level": "High (Athletic)",
        "sleep_hours": 8.5,
        "baseline_hr": 52,
        "baseline_bp_sys": 110,
        "baseline_bp_dia": 70,
        "baseline_glucose": 82,
        "stress_level": "Low",
        "notes": "Low resting heart rate, high heart rate variability (HRV), rapid post-exercise recovery.",
    },
    "desk_worker": {
        "name": "Sarah Chen (Desk Professional - Elevated Stress)",
        "patient_id": "TWIN-DSK-204",
        "age": 37,
        "gender": "Female",
        "activity_level": "Sedentary",
        "sleep_hours": 5.5,
        "baseline_hr": 82,
        "baseline_bp_sys": 126,
        "baseline_bp_dia": 82,
        "baseline_glucose": 96,
        "stress_level": "High",
        "notes": "Chronic sleep deficit, high cognitive stress, diurnal sympathetic tone elevation.",
    },
    "senior_monitor": {
        "name": "Robert Miller (Senior - Hypertensive Telemetry)",
        "patient_id": "TWIN-SR-309",
        "age": 69,
        "gender": "Male",
        "activity_level": "Light (Walking)",
        "sleep_hours": 6.8,
        "baseline_hr": 74,
        "baseline_bp_sys": 136,
        "baseline_bp_dia": 86,
        "baseline_glucose": 108,
        "stress_level": "Moderate",
        "notes": "Arterial stiffness simulation, mild nocturnal hypertension dipping deficit.",
    },
    "custom": {
        "name": "Custom Virtual Patient",
        "patient_id": "TWIN-CUSTOM-001",
        "age": 42,
        "gender": "Other / Unspecified",
        "activity_level": "Moderate",
        "sleep_hours": 7.0,
        "baseline_hr": 72,
        "baseline_bp_sys": 120,
        "baseline_bp_dia": 80,
        "baseline_glucose": 90,
        "stress_level": "Moderate",
        "notes": "User-configured digital twin parameters for scenario stress testing.",
    },
}

# Activity level scaling factors for physiological model
ACTIVITY_LEVEL_MAP = {
    "Sedentary": {"step_multiplier": 0.4, "hr_boost": 0, "resilience_boost": 0.90},
    "Light (Walking)": {"step_multiplier": 0.7, "hr_boost": 2, "resilience_boost": 0.95},
    "Moderate": {"step_multiplier": 1.0, "hr_boost": 5, "resilience_boost": 1.00},
    "High (Athletic)": {"step_multiplier": 1.5, "hr_boost": 8, "resilience_boost": 1.10},
}
