"""TwinCare AI - High-End Interactive Telemetry Visualizer Module.

Provides luminous biotech charts, clinical safety bands,
and multi-system radar/gauge representations in Dark (Cyber Pink & Neon Orchid)
and Light (Rose Quartz & Berry) theme modes.
"""

from typing import Dict
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _apply_theme(
    fig: go.Figure,
    title: str = "",
    height: int = 390,
    is_dark: bool = True,
    theme_key: str = "dark",
    **kwargs,
) -> go.Figure:
    """Apply consistent theme styling across Plotly charts."""
    is_dark_mode = is_dark or theme_key == "dark" or "pink" in theme_key

    if is_dark_mode:
        paper_bg = "rgba(22, 11, 34, 0.85)"
        plot_bg = "rgba(14, 7, 23, 0.95)"
        title_color = "#FDF2F8"
        font_color = "#E9D5FF"
        grid_color = "rgba(255, 42, 133, 0.12)"
        line_color = "rgba(255, 42, 133, 0.28)"
        legend_bg = "rgba(24, 11, 36, 0.85)"
        legend_border = "rgba(255, 42, 133, 0.30)"
        legend_font = "#FDF2F8"
        hover_bg = "#200E2E"
        hover_border = "#FF2A85"
        hover_font = "#FFFFFF"
    else:
        paper_bg = "#FFFFFF"
        plot_bg = "#FFF5F7"
        title_color = "#831843"
        font_color = "#475569"
        grid_color = "#FCE7F3"
        line_color = "#FBCFE8"
        legend_bg = "#FFFFFF"
        legend_border = "#FBCFE8"
        legend_font = "#831843"
        hover_bg = "#FFFFFF"
        hover_border = "#E11D48"
        hover_font = "#1E293B"

    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "font": {"size": 15, "color": title_color, "family": "Plus Jakarta Sans, sans-serif"},
            "x": 0.02,
            "xanchor": "left",
        },
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        margin={"l": 50, "r": 25, "t": 55, "b": 40},
        height=height,
        font={"color": font_color, "family": "Plus Jakarta Sans, sans-serif", "size": 12},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1.0,
            "bgcolor": legend_bg,
            "bordercolor": legend_border,
            "borderwidth": 1,
            "font": {"size": 11, "color": legend_font},
        },
        xaxis={
            "gridcolor": grid_color,
            "zerolinecolor": grid_color,
            "showline": True,
            "linecolor": line_color,
            "tickfont": {"size": 11, "color": font_color},
        },
        yaxis={
            "gridcolor": grid_color,
            "zerolinecolor": grid_color,
            "showline": True,
            "linecolor": line_color,
            "tickfont": {"size": 11, "color": font_color},
        },
        hoverlabel={
            "bgcolor": hover_bg,
            "font_size": 12,
            "font_family": "Plus Jakarta Sans, sans-serif",
            "bordercolor": hover_border,
            "font_color": hover_font,
        },
    )
    return fig


def plot_cardiovascular_telemetry(
    df: pd.DataFrame,
    is_dark: bool = True,
    theme_key: str = "dark",
    **kwargs,
) -> go.Figure:
    """Generate high-contrast dual chart for Heart Rate and Blood Pressure."""
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.55, 0.45],
        subplot_titles=("Heart Rate Telemetry (BPM)", "Vascular Blood Pressure (mmHg)"),
    )

    is_dark_mode = is_dark or theme_key == "dark" or "pink" in theme_key

    # Shaded Sleep Intervals Background
    sleep_intervals = []
    in_sleep = False
    start_t = None
    for _, row in df.iterrows():
        if row["is_sleep"] and not in_sleep:
            in_sleep = True
            start_t = row["timestamp"]
        elif not row["is_sleep"] and in_sleep:
            in_sleep = False
            sleep_intervals.append((start_t, row["timestamp"]))
    if in_sleep:
        sleep_intervals.append((start_t, df.iloc[-1]["timestamp"]))

    if is_dark_mode:
        sleep_color = "rgba(168, 85, 247, 0.14)"
        sleep_anno = "#C084FC"
        hr_band_color = "rgba(255, 42, 133, 0.07)"
        hr_color = "#FF2A85"
        hr_fill = "rgba(255, 42, 133, 0.14)"
        sys_color = "#FB7185"
        dia_color = "#C084FC"
    else:
        sleep_color = "rgba(217, 70, 239, 0.08)"
        sleep_anno = "#A855F7"
        hr_band_color = "rgba(225, 29, 72, 0.06)"
        hr_color = "#E11D48"
        hr_fill = "rgba(225, 29, 72, 0.08)"
        sys_color = "#BE185D"
        dia_color = "#9333EA"

    for idx, (start_s, end_s) in enumerate(sleep_intervals):
        fig.add_vrect(
            x0=start_s,
            x1=end_s,
            fillcolor=sleep_color,
            line_width=0,
            layer="below",
            annotation_text="🌙 Nocturnal Sleep" if idx == 0 else None,
            annotation_position="top left",
            annotation_font={"size": 10, "color": sleep_anno},
        )

    # Threshold band for normal HR (60 - 100 BPM)
    fig.add_hrect(
        y0=60,
        y1=100,
        fillcolor=hr_band_color,
        line_width=0,
        layer="below",
        row=1,
        col=1,
    )

    # Trace: Heart Rate
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["heart_rate"],
            mode="lines",
            name="Heart Rate",
            line={"color": hr_color, "width": 2.5},
            fill="tozeroy",
            fillcolor=hr_fill,
            hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>Heart Rate: <b>%{y:.1f} BPM</b><extra></extra>",
        ),
        row=1,
        col=1,
    )

    # Trace: Systolic BP
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["blood_pressure_systolic"],
            mode="lines",
            name="Systolic BP",
            line={"color": sys_color, "width": 2.2},
            hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>Systolic: <b>%{y:.1f} mmHg</b><extra></extra>",
        ),
        row=2,
        col=1,
    )

    # Trace: Diastolic BP
    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["blood_pressure_diastolic"],
            mode="lines",
            name="Diastolic BP",
            line={"color": dia_color, "width": 2.0, "dash": "dash"},
            hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>Diastolic: <b>%{y:.1f} mmHg</b><extra></extra>",
        ),
        row=2,
        col=1,
    )

    # Normal Systolic reference line (120 mmHg)
    fig.add_hline(
        y=120,
        line_dash="dot",
        line_color="rgba(239, 68, 68, 0.5)",
        annotation_text="Normal Max Sys (120)",
        annotation_position="bottom right",
        annotation_font_size=10,
        row=2,
        col=1,
    )

    _apply_theme(fig, title="Cardiovascular & Vascular Dynamics", height=430, is_dark=is_dark_mode, theme_key=theme_key)
    fig.update_yaxes(title_text="BPM", row=1, col=1)
    fig.update_yaxes(title_text="mmHg", row=2, col=1)
    return fig


def plot_metabolic_glycemic_curve(
    df: pd.DataFrame,
    is_dark: bool = True,
    theme_key: str = "dark",
    **kwargs,
) -> go.Figure:
    """Generate blood glucose curve with post-prandial meal thresholds."""
    fig = go.Figure()
    is_dark_mode = is_dark or theme_key == "dark" or "pink" in theme_key

    if is_dark_mode:
        fasting_color = "rgba(255, 42, 133, 0.08)"
        anno_col = "#FF2A85"
        line_col = "#F43F5E"
        glu_color = "#D946EF"
        glu_fill = "rgba(217, 70, 239, 0.14)"
    else:
        fasting_color = "rgba(225, 29, 72, 0.06)"
        anno_col = "#E11D48"
        line_col = "#BE185D"
        glu_color = "#DB2777"
        glu_fill = "rgba(219, 39, 119, 0.08)"

    # Normal fasting envelope (70 - 100 mg/dL)
    fig.add_hrect(
        y0=70,
        y1=100,
        fillcolor=fasting_color,
        line_width=0,
        layer="below",
        annotation_text="Target Fasting Envelope (70-100)",
        annotation_position="top left",
        annotation_font={"size": 10, "color": anno_col},
    )

    # Post-prandial threshold line (140 mg/dL)
    fig.add_hline(
        y=140,
        line_dash="dash",
        line_color=line_col,
        annotation_text="Post-Meal Threshold (140 mg/dL)",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color=line_col,
    )

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["blood_glucose"],
            mode="lines",
            name="Blood Glucose",
            line={"color": glu_color, "width": 2.5},
            fill="tozeroy",
            fillcolor=glu_fill,
            hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>Glucose: <b>%{y:.1f} mg/dL</b><extra></extra>",
        )
    )

    _apply_theme(fig, title="Metabolic Telemetry: Blood Glucose Dynamics", height=340, is_dark=is_dark_mode, theme_key=theme_key)
    fig.update_yaxes(title_text="mg/dL", range=[50, max(180, df["blood_glucose"].max() + 15)])
    return fig


def plot_respiratory_spo2(
    df: pd.DataFrame,
    is_dark: bool = True,
    theme_key: str = "dark",
    **kwargs,
) -> go.Figure:
    """Generate SpO2 oxygenation chart with clinical safety boundary."""
    fig = go.Figure()
    is_dark_mode = is_dark or theme_key == "dark" or "pink" in theme_key

    # Warning band below 95%
    fig.add_hrect(
        y0=88,
        y1=95,
        fillcolor="rgba(239, 68, 68, 0.10)",
        line_width=0,
        layer="below",
        annotation_text="Desaturation Threshold (< 95%)",
        annotation_position="bottom left",
        annotation_font={"size": 10, "color": "#EF4444"},
    )

    # Optimal band (95 - 100%)
    optimal_color = "rgba(255, 42, 133, 0.06)" if is_dark_mode else "rgba(225, 29, 72, 0.05)"
    fig.add_hrect(
        y0=95,
        y1=100,
        fillcolor=optimal_color,
        line_width=0,
        layer="below",
    )

    spo2_color = "#38BDF8" if is_dark_mode else "#0284C7"

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["spo2"],
            mode="lines+markers",
            marker={"size": 4.5, "color": spo2_color},
            name="SpO2 Saturation",
            line={"color": spo2_color, "width": 2.2},
            hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>SpO2: <b>%{y:.1f}%</b><extra></extra>",
        )
    )

    _apply_theme(fig, title="Blood Oxygen Saturation (SpO2 %)", height=340, is_dark=is_dark_mode, theme_key=theme_key)
    fig.update_yaxes(title_text="SpO2 (%)", range=[min(88, df["spo2"].min() - 2), 101])
    return fig


def plot_stability_gauge(
    score: float,
    tier_name: str,
    is_dark: bool = True,
    theme_key: str = "dark",
    **kwargs,
) -> go.Figure:
    """Generate high-contrast gauge for Homeostasis Stability."""
    is_dark_mode = is_dark or theme_key == "dark" or "pink" in theme_key

    if is_dark_mode:
        number_color = "#FFFFFF"
        bar_color = "#FF2A85"
        bg_color = "rgba(32, 14, 46, 0.85)"
        border_col = "rgba(255, 42, 133, 0.3)"
    else:
        number_color = "#831843"
        bar_color = "#E11D48"
        bg_color = "#FFF5F7"
        border_col = "#FBCFE8"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "suffix": "%",
                "font": {"size": 38, "color": number_color, "family": "Plus Jakarta Sans, sans-serif"},
            },
            title={
                "text": f"<b>Homeostasis Stability</b><br><span style='font-size:12px;color:{bar_color};'>{tier_name}</span>",
                "font": {"size": 14, "color": "#E9D5FF" if is_dark_mode else "#64748B"},
            },
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": border_col},
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": bg_color,
                "borderwidth": 1,
                "bordercolor": border_col,
                "steps": [
                    {"range": [0, 50], "color": "rgba(239, 68, 68, 0.25)"},
                    {"range": [50, 70], "color": "rgba(245, 158, 11, 0.25)"},
                    {"range": [70, 85], "color": "rgba(168, 85, 247, 0.25)" if is_dark_mode else "rgba(217, 70, 239, 0.20)"},
                    {"range": [85, 100], "color": "rgba(255, 42, 133, 0.30)" if is_dark_mode else "rgba(225, 29, 72, 0.25)"},
                ],
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin={"l": 25, "r": 25, "t": 45, "b": 15},
        height=250,
    )
    return fig


def plot_organ_radar(
    sub_scores: Dict[str, float],
    is_dark: bool = True,
    theme_key: str = "dark",
    **kwargs,
) -> go.Figure:
    """Generate radar/spider chart showing multi-system physiological balance."""
    categories = list(sub_scores.keys())
    values = list(sub_scores.values())

    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    is_dark_mode = is_dark or theme_key == "dark" or "pink" in theme_key

    if is_dark_mode:
        radar_color = "#FF2A85"
        radar_fill = "rgba(255, 42, 133, 0.25)"
        polar_bg = "rgba(22, 11, 34, 0.85)"
        grid_color = "rgba(255, 42, 133, 0.18)"
        label_color = "#FDF2F8"
    else:
        radar_color = "#E11D48"
        radar_fill = "rgba(225, 29, 72, 0.18)"
        polar_bg = "#FFF5F7"
        grid_color = "#FBCFE8"
        label_color = "#831843"

    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            name="Virtual Twin State",
            line={"color": radar_color, "width": 2.5},
            fillcolor=radar_fill,
        )
    )

    fig.update_layout(
        polar={
            "bgcolor": polar_bg,
            "radialaxis": {
                "visible": True,
                "range": [0, 100],
                "color": "#94A3B8" if is_dark_mode else "#64748B",
                "gridcolor": grid_color,
            },
            "angularaxis": {
                "color": label_color,
                "gridcolor": grid_color,
            },
        },
        paper_bgcolor="rgba(0,0,0,0)",
        margin={"l": 35, "r": 35, "t": 35, "b": 25},
        height=270,
        showlegend=False,
    )
    return fig


def plot_circadian_activity_hr(
    df: pd.DataFrame,
    is_dark: bool = True,
    theme_key: str = "dark",
    **kwargs,
) -> go.Figure:
    """Generate correlation chart comparing daily activity steps and heart rate response."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    is_dark_mode = is_dark or theme_key == "dark" or "pink" in theme_key

    if is_dark_mode:
        bar_color = "rgba(168, 85, 247, 0.55)"
        hr_line_color = "#FF2A85"
    else:
        bar_color = "rgba(244, 63, 94, 0.35)"
        hr_line_color = "#E11D48"

    fig.add_trace(
        go.Bar(
            x=df["timestamp"],
            y=df["activity_steps"],
            name="Activity Steps",
            marker_color=bar_color,
            hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>Steps: <b>%{y}</b><extra></extra>",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["heart_rate"],
            name="Heart Rate",
            line={"color": hr_line_color, "width": 2.2},
            hovertemplate="<b>%{x|%b %d, %H:%M}</b><br>Heart Rate: <b>%{y:.1f} BPM</b><extra></extra>",
        ),
        secondary_y=True,
    )

    _apply_theme(fig, title="Activity Exertion vs Heart Rate Response", height=340, is_dark=is_dark_mode, theme_key=theme_key)
    fig.update_yaxes(title_text="Steps / Interval", secondary_y=False)
    fig.update_yaxes(title_text="Heart Rate (BPM)", secondary_y=True)
    return fig
