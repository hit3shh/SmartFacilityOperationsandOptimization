import sys
import importlib
from pathlib import Path

import pandas as pd


# ==================================================
# PROJECT PATHS
# ==================================================

CURRENT_DIR = Path(__file__).resolve().parent

SMART_FACILITY_PATH = CURRENT_DIR.parent

SPRINGBOARD_PATH = SMART_FACILITY_PATH.parent


# Add Smart Facility System to path
sys.path.insert(
    0,
    str(SMART_FACILITY_PATH)
)


# ==================================================
# IMPORT SMART FACILITY AGENT
# ==================================================

from src.smart_facility_agent import (
    SmartFacilityAgent
)


# ==================================================
# DATA PATHS
# ==================================================

ENERGY_DATA_PATH = (
    SPRINGBOARD_PATH
    / "M1_agentic_facilityops_ai"
    / "data"
    / "processed"
    / "processed_energy_data.csv"
)


MAINTENANCE_DATA_PATH = (
    SPRINGBOARD_PATH
    / "M2_Predictive_Maintenance"
    / "data"
    / "raw"
    / "ai4i2020.csv"
)


MAINTENANCE_MODEL_PATH = (
    SPRINGBOARD_PATH
    / "M2_Predictive_Maintenance"
    / "models"
    / "maintenance_failure_model.pkl"
)


# ==================================================
# LOAD DATA
# ==================================================

print(
    "\nLoading Energy dataset..."
)

energy_df = pd.read_csv(
    ENERGY_DATA_PATH
)

energy_df["timestamp"] = pd.to_datetime(
    energy_df["timestamp"]
)

print(
    "Energy dataset loaded:",
    energy_df.shape
)


print(
    "\nLoading Maintenance dataset..."
)

maintenance_df = pd.read_csv(
    MAINTENANCE_DATA_PATH
)

print(
    "Maintenance dataset loaded:",
    maintenance_df.shape
)


# ==================================================
# SELECT MACHINE
# ==================================================

machine_data = (
    maintenance_df
    .sample(
        1,
        random_state=42
    )
    .iloc[0]
)


print(
    "\nSelected Machine:"
)

print(
    machine_data["Product ID"]
)


# ==================================================
# INITIALIZE SMART FACILITY AGENT
# ==================================================

print(
    "\nInitializing Smart Facility Agent..."
)

agent = SmartFacilityAgent(
    maintenance_model_path=
    str(MAINTENANCE_MODEL_PATH)
)


# ==================================================
# RUN COMPLETE ANALYSIS
# ==================================================

print(
    "\nRunning Complete Facility Analysis..."
)

results = agent.run_complete_analysis(
    energy_df,
    machine_data
)


# ==================================================
# DISPLAY ENERGY RESULTS
# ==================================================

print(
    "\n========== ENERGY RESULTS =========="
)

energy_results = results[
    "energy_results"
]

print(
    "\nEnergy Summary:"
)

for key, value in energy_results[
    "summary"
].items():

    print(
        f"{key}: {value}"
    )


print(
    "\nPeak Usage:"
)

print(
    energy_results[
        "peak_usage"
    ]
)


print(
    "\nEnergy Anomalies:"
)

print(
    energy_results[
        "anomaly_count"
    ]
)


# ==================================================
# DISPLAY MAINTENANCE RESULTS
# ==================================================

print(
    "\n========== MAINTENANCE RESULTS =========="
)

maintenance_result = results[
    "maintenance_result"
]

for key, value in maintenance_result.items():

    print(
        f"{key}: {value}"
    )


# ==================================================
# DISPLAY COMBINED FACILITY INSIGHT
# ==================================================

print(
    "\n========== FACILITY INSIGHT =========="
)

facility_insight = results[
    "facility_insight"
]


print(
    "\nFacility Priority:"
)

print(
    facility_insight[
        "facility_priority"
    ]
)


print(
    "\nInsights:"
)

for insight in facility_insight[
    "insights"
]:

    print(
        f"- {insight}"
    )


print(
    "\nCombined Recommendation:"
)

print(
    facility_insight[
        "combined_recommendation"
    ]
)


print(
    "\n========== INTEGRATION TEST COMPLETED =========="
)