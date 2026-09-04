# ==================================================
# SMART FACILITY SYSTEM
# UNIFIED DASHBOARD
# ==================================================


import sys
from pathlib import Path

import streamlit as st
import pandas as pd


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Smart Facility System",
    page_icon="🏢",
    layout="wide"
)


# ==================================================
# PROJECT PATHS
# ==================================================

# Current folder:
# Springboard/smart_facility_system

CURRENT_DIR = Path(__file__).resolve().parent


# Main Springboard folder
SPRINGBOARD_DIR = CURRENT_DIR.parent


# Milestone 1 Project
ENERGY_PROJECT_PATH = (
    SPRINGBOARD_DIR
    / "M1_agentic_facilityops_ai"
)


# Milestone 2 Project
MAINTENANCE_PROJECT_PATH = (
    SPRINGBOARD_DIR
    / "M2_Predictive_Maintenance"
)

# ==================================================
# RESET SRC MODULES
# ==================================================

modules_to_remove = []


for module_name in list(sys.modules.keys()):

    if (
        module_name == "src"
        or module_name.startswith("src.")
    ):

        modules_to_remove.append(
            module_name
        )


for module_name in modules_to_remove:

    del sys.modules[module_name]


# ==================================================
# ADD SMART FACILITY SYSTEM TO PYTHON PATH
# ==================================================

if str(CURRENT_DIR) in sys.path:

    sys.path.remove(
        str(CURRENT_DIR)
    )


sys.path.insert(
    0,
    str(CURRENT_DIR)
)


# ==================================================
# IMPORT CENTRAL AGENT
# ==================================================

from src.smart_facility_agent import (
    SmartFacilityAgent
)


# ==================================================
# LOAD ENERGY DATA
# ==================================================

@st.cache_data
def load_energy_data():

    data_path = (
        ENERGY_PROJECT_PATH
        / "data"
        / "processed"
        / "processed_energy_data.csv"
    )

    print(
        "Loading Energy dataset..."
    )

    df = pd.read_csv(
        data_path
    )

    # Convert timestamp column to datetime
    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    print(
        f"Energy dataset loaded: {df.shape}"
    )

    print(
        f"Timestamp datatype: {df['timestamp'].dtype}"
    )

    return df


# ==================================================
# LOAD MAINTENANCE DATA
# ==================================================

@st.cache_data
def load_maintenance_data():

    data_path = (
        MAINTENANCE_PROJECT_PATH
        / "data"
        / "raw"
        / "ai4i2020.csv"
    )

    print(
        "Loading Maintenance dataset..."
    )

    # Check whether file exists
    if not data_path.exists():

        raise FileNotFoundError(
            f"Maintenance dataset not found:\n{data_path}"
        )

    df = pd.read_csv(
        data_path
    )

    print(
        f"Maintenance dataset loaded: {df.shape}"
    )

    return df


# ==================================================
# INITIALIZE SMART FACILITY AGENT
# ==================================================

@st.cache_resource
def initialize_smart_facility_agent():

    # Maintenance ML model path
    model_path = (
        MAINTENANCE_PROJECT_PATH
        / "models"
        / "maintenance_failure_model.pkl"
    )

    print(
        "Initializing Smart Facility Agent..."
    )

    # Check whether model exists
    if not model_path.exists():

        raise FileNotFoundError(
            f"Maintenance model not found:\n{model_path}"
        )

    # IMPORTANT:
    # SmartFacilityAgent requires
    # maintenance_model_path

    agent = SmartFacilityAgent(
        maintenance_model_path=str(
            model_path
        )
    )

    print(
        "Smart Facility Agent initialized successfully!"
    )

    return agent


# ==================================================
# LOAD DATASETS
# ==================================================

energy_df = load_energy_data()

maintenance_df = load_maintenance_data()


# ==================================================
# INITIALIZE SMART FACILITY AGENT
# ==================================================

smart_facility_agent = (
    initialize_smart_facility_agent()
)


# ==================================================
# DASHBOARD HEADER
# ==================================================

st.title(
    "🏢 Smart Facility System"
)


st.success(
    "Unified Smart Facility System initialized successfully!"
)


# ==================================================
# DATASET OVERVIEW
# ==================================================

st.header(
    "📊 Facility Datasets"
)


col1, col2 = st.columns(2)


# ==================================================
# ENERGY DATASET
# ==================================================

with col1:

    st.subheader(
        "⚡ Energy Dataset"
    )

    st.metric(
        "Total Records",
        f"{len(energy_df):,}"
    )

    st.metric(
        "Total Columns",
        energy_df.shape[1]
    )

    st.success(
        "Energy Agent ready"
    )


# ==================================================
# MAINTENANCE DATASET
# ==================================================

with col2:

    st.subheader(
        "🔧 Maintenance Dataset"
    )

    st.metric(
        "Total Records",
        f"{len(maintenance_df):,}"
    )

    st.metric(
        "Total Columns",
        maintenance_df.shape[1]
    )

    st.success(
        "Maintenance Agent ready"
    )


# ==================================================
# SYSTEM STATUS
# ==================================================

st.divider()


st.header(
    "🤖 Agent Integration Status"
)


status_col1, status_col2, status_col3 = (
    st.columns(3)
)


with status_col1:

    st.success(
        "⚡ Energy Agent Connected"
    )


with status_col2:

    st.success(
        "🔧 Maintenance Agent Connected"
    )


with status_col3:

    st.success(
        "🏢 Smart Facility Agent Ready"
    )


# ==================================================
# PROJECT INFORMATION
# ==================================================

st.divider()


st.caption(
    "Smart Facility System | "
    "Milestone 1: Energy Operations + "
    "Milestone 2: Predictive Maintenance"
)

# ==================================================
# RUN SMART FACILITY ANALYSIS
# ==================================================

st.divider()

st.header(
    "🔍 Run Smart Facility Analysis"
)


# Get available machine IDs
product_ids = (
    maintenance_df["Product ID"]
    .astype(str)
    .unique()
)


# Machine selection
selected_product_id = st.selectbox(
    "Select Machine Product ID",
    product_ids
)


# Get selected machine data
selected_machine = (
    maintenance_df[
        maintenance_df["Product ID"].astype(str)
        == selected_product_id
    ]
)


# Run analysis button
if st.button(
    "🚀 Run Complete Facility Analysis",
    use_container_width=True
):

    with st.spinner(
        "Running Energy and Maintenance Agents..."
    ):

        # selected_machine is already the filtered DataFrame.
        # Extract one machine record as a Pandas Series.
        selected_machine_data = selected_machine.iloc[0]

        results = (
            smart_facility_agent
            .run_complete_analysis(
                energy_df,
                selected_machine_data
            )
        )

    st.success(
        "Facility analysis completed successfully!"
    )


    # ==============================================
    # STORE RESULTS
    # ==============================================

    energy_results = (
        results["energy_results"]
    )

    maintenance_result = (
        results["maintenance_result"]
    )

    facility_insight = (
        results["facility_insight"]
    )


    # ==============================================
    # FACILITY PRIORITY
    # ==============================================

    st.subheader(
        "🏢 Facility Priority"
    )

    priority = (
        facility_insight[
            "facility_priority"
        ]
    )

    if priority == "High":

        st.error(
            f"Priority Level: {priority}"
        )

    elif priority == "Medium":

        st.warning(
            f"Priority Level: {priority}"
        )

    else:

        st.success(
            f"Priority Level: {priority}"
        )

    # ==================================================
    # ENERGY ANALYSIS RESULTS
    # ==================================================

    st.divider()

    st.subheader(
        "⚡ Energy Analysis Results"
    )


    energy_summary = (
        energy_results["summary"]
    )

    peak_usage = (
        energy_results["peak_usage"]
    )

    anomaly_count = (
        energy_results["anomaly_count"]
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Energy Consumption",
            f"{energy_summary['total_energy']:,.2f}"
        )


    with col2:

        st.metric(
            "Average Energy Consumption",
            f"{energy_summary['average_energy']:,.2f}"
        )


    with col3:

        st.metric(
            "Peak Energy Consumption",
            f"{energy_summary['peak_energy']:,.2f}"
        )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Peak Usage Hour",
            f"{peak_usage['peak_hour']}:00"
        )


    with col2:

        st.metric(
            "Energy Anomalies Detected",
            f"{anomaly_count:,}"
        )

    # ==================================================
    # MAINTENANCE ANALYSIS RESULTS
    # ==================================================

    st.divider()

    st.subheader(
        "🔧 Maintenance Analysis Results"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Machine Product ID",
            maintenance_result["product_id"]
        )


    with col2:

        st.metric(
            "Machine Type",
            maintenance_result["machine_type"]
        )


    with col3:

        st.metric(
            "Health Score",
            f"{maintenance_result['health_score']}/100"
        )


    col1, col2, col3 = st.columns(3)


    with col1:

        failure_prediction = (
            maintenance_result[
                "failure_prediction"
            ]
        )

        prediction_text = (
            "Failure Predicted"
            if failure_prediction == 1
            else "No Failure Predicted"
        )

        st.metric(
            "Failure Prediction",
            prediction_text
        )


    with col2:

        failure_probability = (
            maintenance_result[
                "failure_probability"
            ]
        )

        st.metric(
            "Failure Probability",
            f"{failure_probability * 100:.2f}%"
        )


    with col3:

        st.metric(
            "Risk Level",
            maintenance_result["risk_level"]
        )


    # ==============================================
    # HEALTH STATUS
    # ==============================================

    health_status = (
        maintenance_result[
            "health_status"
        ]
    )


    if health_status == "Healthy":

        st.success(
            f"Machine Health Status: {health_status}"
        )

    elif health_status == "Warning":

        st.warning(
            f"Machine Health Status: {health_status}"
        )

    else:

        st.error(
            f"Machine Health Status: {health_status}"
        )


    # ==============================================
    # MAINTENANCE RECOMMENDATION
    # ==============================================

    st.subheader(
        "🛠️ Maintenance Recommendation"
    )


    st.info(
        maintenance_result[
            "recommendation"
        ]
    )

    # ==================================================
    # COMBINED FACILITY INSIGHTS
    # ==================================================

    st.divider()

    st.subheader(
        "💡 Combined Facility Insights"
    )


    # ==============================================
    # INSIGHTS
    # ==============================================

    st.write(
        "### Key Facility Insights"
    )


    for insight in facility_insight["insights"]:

        st.write(
            f"• {insight}"
        )


    # ==============================================
    # COMBINED RECOMMENDATION
    # ==============================================

    st.subheader(
        "🎯 Combined Recommendation"
    )


    st.info(
        facility_insight[
            "combined_recommendation"
        ]
    )

