# 🧬 TwinCare AI — Healthcare Digital Twin & Risk Analytics

> **Phase 1 Hackathon Prototype:** Continuous synthetic telemetry simulation, dynamic physiological state estimation, multi-organ homeostasis indices, and interactive clinical telemetry dashboard.

---

## ⚠️ Important Academic & Hackathon Disclaimer
> **NON-MEDICAL PROTOTYPE & SIMULATED DATA ONLY:**
> TwinCare AI is an experimental engineering and digital-twin computational prototype created for hackathon demonstration. **It does NOT provide medical diagnoses, treatment recommendations, clinical prognosis, or medical advice.**
> All patient records, telemetry time series, vital signs, and anomaly spikes are **100% synthetically simulated** through physiological circadian mathematical models. Every row generated is tagged with `is_simulated = True`.

---

## 📌 Project Overview
Wearable devices (smartwatches, optical PPG sensors, continuous glucose monitors) produce vast amounts of biometric data. However, this data is usually displayed in isolated charts without an integrated model of how human organ systems interact.

**TwinCare AI** constructs a **Virtual Healthcare Digital Twin**—a computational software representation of an individual's physiological state. It models:
1. **Circadian Rhythm Cycles**: 24-hour diurnal harmonic oscillations for heart rate, blood pressure, and core body temperature.
2. **Sleep & Nocturnal Dipping**: Physiological vagal recovery modeling during nocturnal sleep windows.
3. **Metabolic Post-Prandial Glycemia**: Non-linear impulse-response curves representing carbohydrate digestion and glucose clearance.
4. **Physical Exertion & Sympathetic Tone**: Dynamic elevation in heart rate, respiration, and blood pressure with proportional step counts.
5. **Systemic Homeostasis Stability Index (0 - 100%)**: Multi-system weighted balance evaluation across Cardiovascular, Respiratory, Metabolic, Sleep, and Autonomic Resilience.

---

## 🏗️ Project Architecture & File Structure

```text
TwinCareAI/
├── .gitignore                    # Git exclusions (virtualenvs, cache, logs)
├── requirements.txt              # Project dependencies
├── README.md                     # Documentation, Windows setup, hackathon guide
├── config.py                     # App settings, theme palette, clinical thresholds & presets
├── app.py                        # Main Streamlit web application entry point
├── modules/
│   ├── __init__.py               # Package marker
│   ├── simulator.py              # Synthetic circadian & telemetry simulation engine
│   ├── twin_state.py             # Digital Twin state evaluator & multi-organ scoring
│   ├── visualizer.py             # Hospital telemetry dark-themed Plotly charts
│   └── components.py             # Reusable UI cards, profile chip, disclaimer banner
└── tests/
    └── test_simulation.py        # Automated unit and integration tests (100% passing)
```

---

## 🚀 Setup & Run Instructions (Windows PowerShell)

### Step 1: Open Terminal in Project Directory
Open **PowerShell** or Command Prompt and ensure you are in the project folder:
```powershell
cd c:\Users\Apple\Desktop\TwinCareAI
```

### Step 2: (Optional but Recommended) Create & Activate a Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```
*(If PowerShell blocks script execution, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Run Automated Tests
Verify all synthetic simulation engines and digital twin state calculators pass:
```powershell
python -m pytest tests/
```

### Step 5: Launch the Interactive Dashboard
```powershell
streamlit run app.py
```
Streamlit will automatically open in your default browser at:
👉 **`http://localhost:8501`**

---

## 💡 How to Demo This Project to Hackathon Judges

When presenting as a solo AIML engineering student, follow this 4-step pitch structure:

### 1. The Hook (Problem Statement)
> *"Judges, wearables produce gigabytes of health telemetry, but clinicians and patients only see static retrospective charts. When biometric signals drift, there is no real-time computational model that evaluates how organs impact each other. We built **TwinCare AI** to bring digital twin engineering to preventive health analytics."*

### 2. Live Interactive Walkthrough
- **Select a Patient Archetype**: Switch between *High Endurance Athlete*, *Desk Professional (Elevated Stress)*, and *Senior Citizen (Hypertension)*. Show how the digital twin baseline parameters adapt instantly.
- **Explain the Physiological Graphs**:
  - Show the **Cardiovascular Telemetry**: Point out the shaded sleep periods and how the heart rate dips naturally (circadian rhythm) while day-time activity produces exertion spikes.
  - Show the **Metabolic Curve**: Highlight the 3 post-prandial meal spikes (Breakfast, Lunch, Dinner) showing how glucose rises and safely clears within 2-3 hours.
  - Show the **SpO2 Telemetry**: Illustrate the hospital safety boundary band (<95%).
- **Demonstrate Anomaly Injection**: Toggle **"Simulate Acute Anomaly"** (e.g. *Tachycardia Spike* or *Nocturnal Hypoxemia*). Watch the **Homeostasis Stability Index Gauge** drop from *Optimal* to *Mild Strain* or *High Variance*, and point out the alert card under *Detected Telemetry Anomalies*.

### 3. Architecture & Engineering Highlights
- **Mathematical rigor**: Show how the simulation uses cosine diurnal harmonics, non-linear post-prandial exponential surges, and Gaussian sensor noise instead of flat random numbers.
- **Safety & Ethics First**: Emphasize that all data is strictly labeled as synthetic (`is_simulated = True`) and bounded by clear non-diagnostic academic disclaimers.

### 4. Roadmap to Phase 2
- **Phase 1 (Current)**: Foundation telemetry engine, virtual patient calibration, digital twin state computation, and hospital dark telemetry dashboard.
- **Phase 2 (Upcoming)**: Training machine learning models on the official hackathon competition dataset, integrating Scikit-learn predictive risk scoring, and counterfactual simulation (e.g. *"What happens to the digital twin if the patient gets 8 hours of sleep instead of 5?"*).

---

## 📊 Technical Stack
- **Python 3.12**
- **Streamlit**: Modern interactive web interface
- **Pandas & NumPy**: Telemetry generation, vector math, time-series operations
- **Plotly**: Telemetry charts with shaded bands, gauge indicators, and multi-system radar plots
- **Scikit-learn**: Prepared for Phase 2 predictive modeling
- **Pytest**: Automated test suite for simulation validation
