"""TwinCare AI - Digital Twin State & Risk Analytics Engine.

Computes the real-time physiological snapshot, multi-organ homeostasis indices,
and simulated anomaly alerts from synthetic telemetry.

DISCLAIMER: All scores and tiers are heuristic digital-twin simulation markers
designed for engineering research and hackathon demonstration only.
Not intended for clinical diagnosis.
"""

from typing import Dict, Any, List
import pandas as pd
from config import PHYSIOLOGICAL_THRESHOLDS


class DigitalTwinStateEngine:
    """Evaluates the virtual patient's current digital twin state."""

    def __init__(self, profile: Dict[str, Any]):
        self.profile = profile

    def evaluate_current_state(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Evaluate the latest reading and overall window stability.

        Parameters:
            df: pd.DataFrame containing simulated telemetry series.

        Returns:
            Dict containing current vitals, status flags, sub-system scores,
            and overall stability index.
        """
        if df.empty:
            raise ValueError("Telemetry dataframe cannot be empty.")

        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest

        # 1. Individual Vital Status & Deviations
        vitals_status = {}

        # Heart Rate
        hr = float(latest["heart_rate"])
        hr_cfg = PHYSIOLOGICAL_THRESHOLDS["heart_rate"]
        if hr < hr_cfg["low_warning"]:
            hr_tag, hr_color = "Low (Bradycardia)", "amber"
        elif hr <= hr_cfg["normal_max"]:
            hr_tag, hr_color = "Normal", "emerald"
        elif hr <= hr_cfg["elevated_max"]:
            hr_tag, hr_color = "Elevated", "amber"
        else:
            hr_tag, hr_color = "High (Tachycardia)", "rose"

        vitals_status["heart_rate"] = {
            "value": hr,
            "unit": hr_cfg["unit"],
            "delta": round(hr - float(prev["heart_rate"]), 1),
            "status": hr_tag,
            "color": hr_color,
            "normal_range": f"{hr_cfg['normal_min']} - {hr_cfg['normal_max']} {hr_cfg['unit']}",
        }

        # Blood Pressure
        sys_bp = float(latest["blood_pressure_systolic"])
        dia_bp = float(latest["blood_pressure_diastolic"])
        bp_sys_cfg = PHYSIOLOGICAL_THRESHOLDS["blood_pressure_systolic"]
        bp_dia_cfg = PHYSIOLOGICAL_THRESHOLDS["blood_pressure_diastolic"]

        if sys_bp < bp_sys_cfg["normal_max"] and dia_bp < bp_dia_cfg["normal_max"]:
            bp_tag, bp_color = "Normal", "emerald"
        elif sys_bp <= bp_sys_cfg["elevated_max"] and dia_bp < bp_dia_cfg["normal_max"]:
            bp_tag, bp_color = "Elevated", "amber"
        elif sys_bp <= bp_sys_cfg["stage1_max"] or (80 <= dia_bp <= 89):
            bp_tag, bp_color = "Stage 1 Elevated", "amber"
        else:
            bp_tag, bp_color = "Stage 2 Elevated", "rose"

        vitals_status["blood_pressure"] = {
            "systolic": sys_bp,
            "diastolic": dia_bp,
            "display": f"{int(sys_bp)}/{int(dia_bp)}",
            "unit": "mmHg",
            "delta": f"{round(sys_bp - float(prev['blood_pressure_systolic']), 1)} sys",
            "status": bp_tag,
            "color": bp_color,
            "normal_range": "< 120/80 mmHg",
        }

        # SpO2
        spo2 = float(latest["spo2"])
        spo2_cfg = PHYSIOLOGICAL_THRESHOLDS["spo2"]
        if spo2 >= spo2_cfg["normal_min"]:
            spo2_tag, spo2_color = "Optimal", "emerald"
        elif spo2 >= spo2_cfg["warning_min"]:
            spo2_tag, spo2_color = "Mildly Reduced", "amber"
        else:
            spo2_tag, spo2_color = "Hypoxemia Alert", "rose"

        vitals_status["spo2"] = {
            "value": spo2,
            "unit": spo2_cfg["unit"],
            "delta": round(spo2 - float(prev["spo2"]), 1),
            "status": spo2_tag,
            "color": spo2_color,
            "normal_range": "95 - 100 %",
        }

        # Glucose
        glucose = float(latest["blood_glucose"])
        glu_cfg = PHYSIOLOGICAL_THRESHOLDS["glucose"]
        if glucose < glu_cfg["hypo_warning"]:
            glu_tag, glu_color = "Hypoglycemic", "rose"
        elif glucose <= glu_cfg["fasting_max"]:
            glu_tag, glu_color = "Normal Fasting", "emerald"
        elif glucose <= glu_cfg["post_prandial_max"]:
            glu_tag, glu_color = "Normal Post-meal", "cyan"
        elif glucose <= glu_cfg["hyper_warning"]:
            glu_tag, glu_color = "Elevated Spike", "amber"
        else:
            glu_tag, glu_color = "Hyperglycemic Spike", "rose"

        vitals_status["blood_glucose"] = {
            "value": glucose,
            "unit": glu_cfg["unit"],
            "delta": round(glucose - float(prev["blood_glucose"]), 1),
            "status": glu_tag,
            "color": glu_color,
            "normal_range": "70 - 140 mg/dL",
        }

        # Temperature
        temp = float(latest["temperature"])
        temp_cfg = PHYSIOLOGICAL_THRESHOLDS["temperature"]
        if temp < temp_cfg["normal_min"]:
            temp_tag, temp_color = "Low", "cyan"
        elif temp <= temp_cfg["normal_max"]:
            temp_tag, temp_color = "Normal (Afebrile)", "emerald"
        else:
            temp_tag, temp_color = "Elevated (Fever)", "rose"

        vitals_status["temperature"] = {
            "value": temp,
            "unit": temp_cfg["unit"],
            "delta": round(temp - float(prev["temperature"]), 2),
            "status": temp_tag,
            "color": temp_color,
            "normal_range": "97.7 - 99.5 °F",
        }

        # 2. Multi-System Stability Indices (0 - 100 Scale)
        # Cardiovascular Score
        cv_penalty = 0.0
        if hr > 100:
            cv_penalty += min(40.0, (hr - 100) * 1.5)
        elif hr < 55:
            cv_penalty += min(20.0, (55 - hr) * 1.2)
        if sys_bp > 120:
            cv_penalty += min(40.0, (sys_bp - 120) * 1.2)
        cv_score = max(20.0, round(100.0 - cv_penalty, 1))

        # Respiratory / Oxygenation Score
        resp_penalty = 0.0
        if spo2 < 95.0:
            resp_penalty += (95.0 - spo2) * 8.0
        resp_score = max(25.0, round(100.0 - resp_penalty, 1))

        # Metabolic Regulation Score
        meta_penalty = 0.0
        if glucose > 130:
            meta_penalty += min(50.0, (glucose - 130) * 0.8)
        elif glucose < 70:
            meta_penalty += (70 - glucose) * 1.5
        metabolic_score = max(25.0, round(100.0 - meta_penalty, 1))

        # Circadian & Sleep Restoration Score
        sleep_hours = self.profile.get("sleep_hours", 7.0)
        sleep_penalty = 0.0
        if sleep_hours < 7.0:
            sleep_penalty += (7.0 - sleep_hours) * 12.0
        elif sleep_hours > 9.5:
            sleep_penalty += (sleep_hours - 9.5) * 5.0
        circadian_score = max(30.0, round(100.0 - sleep_penalty, 1))

        # Autonomic / Stress Resilience
        stress_val = float(latest["stress_index"])
        autonomic_score = max(20.0, round(100.0 - (stress_val * 0.75), 1))

        sub_scores = {
            "Cardiovascular": cv_score,
            "Respiratory / O2": resp_score,
            "Metabolic Regulation": metabolic_score,
            "Circadian / Sleep": circadian_score,
            "Autonomic Resilience": autonomic_score,
        }

        # 3. Overall Homeostasis Stability Index (Weighted Blend)
        weights = {
            "Cardiovascular": 0.30,
            "Respiratory / O2": 0.25,
            "Metabolic Regulation": 0.20,
            "Circadian / Sleep": 0.15,
            "Autonomic Resilience": 0.10,
        }
        stability_index = round(
            sum(sub_scores[k] * weights[k] for k in sub_scores), 1
        )

        # Classify Overall Resilience Tier
        if stability_index >= 85.0:
            resilience_tier = "Optimal Homeostasis"
            tier_badge = "Stable"
            tier_color = "emerald"
            summary_desc = (
                "All synthetic vital signs fall within expected homeostatic tolerance. "
                "Circadian regulation and cardiovascular telemetry show healthy nocturnal recovery."
            )
        elif stability_index >= 70.0:
            resilience_tier = "Mild Physiological Deviation"
            tier_badge = "Mild Strain"
            tier_color = "amber"
            summary_desc = (
                "Mild deviation detected in cardiovascular or sleep metrics. "
                "Digital twin reflects elevated daytime sympathetic tone or modest sleep deficit."
            )
        elif stability_index >= 50.0:
            resilience_tier = "Moderate Physiological Strain"
            tier_badge = "Attention"
            tier_color = "amber"
            summary_desc = (
                "Noticeable multi-system variance. Simulated cardiovascular or glycemic metrics "
                "frequently exceed baseline thresholds."
            )
        else:
            resilience_tier = "High Physiological Stress"
            tier_badge = "High Variance"
            tier_color = "rose"
            summary_desc = (
                "Significant telemetry variance across multiple simulated physiological subsystems. "
                "Virtual twin flags multiple threshold crossings."
            )

        # 4. Detected Synthetic Anomalies in Timeline Window
        anomalies = self._detect_window_anomalies(df)

        return {
            "timestamp": latest["timestamp"],
            "vitals": vitals_status,
            "stability_index": stability_index,
            "resilience_tier": resilience_tier,
            "tier_badge": tier_badge,
            "tier_color": tier_color,
            "summary_desc": summary_desc,
            "sub_scores": sub_scores,
            "anomalies": anomalies,
            "is_simulated": True,
        }

    def _detect_window_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identify significant excursions or episodes across the simulated window."""
        anomalies = []

        # Peak Heart Rate event
        max_hr_row = df.loc[df["heart_rate"].idxmax()]
        if max_hr_row["heart_rate"] > 110:
            anomalies.append({
                "type": "Elevated Heart Rate Peak",
                "timestamp": max_hr_row["timestamp"],
                "value": f"{max_hr_row['heart_rate']} BPM",
                "severity": "Warning" if max_hr_row["heart_rate"] < 130 else "Alert",
                "context": "Simulated physical exertion or adrenergic spike",
            })

        # Systolic BP excursion
        max_bp_row = df.loc[df["blood_pressure_systolic"].idxmax()]
        if max_bp_row["blood_pressure_systolic"] > 135:
            anomalies.append({
                "type": "Systolic BP Excursion",
                "timestamp": max_bp_row["timestamp"],
                "value": f"{int(max_bp_row['blood_pressure_systolic'])}/{int(max_bp_row['blood_pressure_diastolic'])} mmHg",
                "severity": "Warning",
                "context": "Transient vascular pressure elevation in simulated timeline",
            })

        # SpO2 Drop
        min_spo2_row = df.loc[df["spo2"].idxmin()]
        if min_spo2_row["spo2"] < 94.0:
            anomalies.append({
                "type": "Oxygen Saturation Dip",
                "timestamp": min_spo2_row["timestamp"],
                "value": f"{min_spo2_row['spo2']}% SpO2",
                "severity": "Alert" if min_spo2_row["spo2"] < 92.0 else "Warning",
                "context": "Simulated nocturnal desaturation or transient ventilation variance",
            })

        # Glucose Spike
        max_glu_row = df.loc[df["blood_glucose"].idxmax()]
        if max_glu_row["blood_glucose"] > 140:
            anomalies.append({
                "type": "Post-prandial Glucose Surge",
                "timestamp": max_glu_row["timestamp"],
                "value": f"{max_glu_row['blood_glucose']} mg/dL",
                "severity": "Info",
                "context": "Post-meal glycemic excursion within simulated carbohydrate metabolism",
            })

        return anomalies
