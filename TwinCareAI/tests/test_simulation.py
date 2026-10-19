"""TwinCare AI - Unit and Integration Tests for Telemetry Simulation & State Engine."""

import pytest
import pandas as pd
from config import PATIENT_PRESETS
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


@pytest.fixture
def sample_profile():
    return PATIENT_PRESETS["desk_worker"]


def test_telemetry_generation(sample_profile):
    """Test synthetic telemetry generation for expected columns and shape."""
    sim = SyntheticTelemetrySimulator(profile=sample_profile, random_seed=42)
    df = sim.generate_timeline(duration_hours=24, interval_minutes=30)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 48  # 24 hours * 2 samples/hr
    expected_cols = [
        "timestamp", "heart_rate", "blood_pressure_systolic",
        "blood_pressure_diastolic", "spo2", "blood_glucose",
        "temperature", "respiratory_rate", "activity_steps",
        "stress_index", "is_sleep", "is_simulated"
    ]
    for col in expected_cols:
        assert col in df.columns

    # Verify is_simulated flag is consistently True
    assert df["is_simulated"].all()


def test_physiological_ranges(sample_profile):
    """Verify that generated vitals fall within biologically possible bounds."""
    sim = SyntheticTelemetrySimulator(profile=sample_profile, random_seed=42)
    df = sim.generate_timeline(duration_hours=24, interval_minutes=15)

    assert (df["heart_rate"] >= 35).all() and (df["heart_rate"] <= 210).all()
    assert (df["blood_pressure_systolic"] >= 70).all() and (df["blood_pressure_systolic"] <= 220).all()
    assert (df["spo2"] >= 80).all() and (df["spo2"] <= 100).all()
    assert (df["blood_glucose"] >= 50).all() and (df["blood_glucose"] <= 350).all()


def test_twin_state_evaluation(sample_profile):
    """Test digital twin state evaluation and stability score calculation."""
    sim = SyntheticTelemetrySimulator(profile=sample_profile, random_seed=42)
    df = sim.generate_timeline(duration_hours=24, interval_minutes=30)

    engine = DigitalTwinStateEngine(profile=sample_profile)
    state = engine.evaluate_current_state(df)

    assert "vitals" in state
    assert "stability_index" in state
    assert 0.0 <= state["stability_index"] <= 100.0
    assert "resilience_tier" in state
    assert state["is_simulated"] is True

    # Check all 5 sub-scores
    sub_scores = state["sub_scores"]
    assert "Cardiovascular" in sub_scores
    assert "Respiratory / O2" in sub_scores
    assert "Metabolic Regulation" in sub_scores
    assert "Circadian / Sleep" in sub_scores
    assert "Autonomic Resilience" in sub_scores


def test_anomaly_injection(sample_profile):
    """Test acute anomaly injection and alert detection."""
    sim = SyntheticTelemetrySimulator(profile=sample_profile, random_seed=42)
    df_normal = sim.generate_timeline(duration_hours=24, inject_anomaly=False)
    df_anomaly = sim.generate_timeline(
        duration_hours=24,
        inject_anomaly=True,
        anomaly_type="Tachycardia Spike",
    )

    # Anomaly dataframe should have higher max heart rate
    assert df_anomaly["heart_rate"].max() > df_normal["heart_rate"].max()

    engine = DigitalTwinStateEngine(profile=sample_profile)
    state = engine.evaluate_current_state(df_anomaly)
    # Check that anomaly list caught the event
    assert len(state["anomalies"]) > 0


def test_visualizer_figures(sample_profile):
    """Ensure all Plotly figures render without error."""
    sim = SyntheticTelemetrySimulator(profile=sample_profile, random_seed=42)
    df = sim.generate_timeline(duration_hours=24, interval_minutes=30)
    engine = DigitalTwinStateEngine(profile=sample_profile)
    state = engine.evaluate_current_state(df)

    fig1 = plot_cardiovascular_telemetry(df)
    fig2 = plot_metabolic_glycemic_curve(df)
    fig3 = plot_respiratory_spo2(df)
    fig4 = plot_stability_gauge(state["stability_index"], state["resilience_tier"])
    fig5 = plot_organ_radar(state["sub_scores"])
    fig6 = plot_circadian_activity_hr(df)

    assert fig1 is not None
    assert fig2 is not None
    assert fig3 is not None
    assert fig4 is not None
    assert fig5 is not None
    assert fig6 is not None
