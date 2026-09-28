# ==================================================
# SMART FACILITY SYSTEM
# UNIFIED MULTI-AGENT DASHBOARD
# ==================================================

import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Smart Facility System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.20);
    }
    .hero {
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(30,136,229,.14), rgba(0,188,212,.10));
        border: 1px solid rgba(30,136,229,.18);
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0 0 .25rem 0; font-size: 2.2rem; }
    .hero p { margin: 0; opacity: .78; font-size: 1rem; }
    .section-card {
        padding: 1rem 1.1rem;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,.18);
        background: rgba(128,128,128,.035);
        margin-bottom: .8rem;
    }
    .insight-card {
        padding: .9rem 1rem;
        border-radius: 13px;
        border-left: 4px solid #1e88e5;
        background: rgba(30,136,229,.07);
        margin: .45rem 0;
    }
    .recommendation-card {
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid rgba(0,188,212,.25);
        background: rgba(0,188,212,.07);
        margin: .5rem 0;
    }
    .small-muted { opacity: .68; font-size: .82rem; }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# PROJECT PATHS
# ==================================================

CURRENT_DIR = Path(__file__).resolve().parent

SPRINGBOARD_DIR = CURRENT_DIR.parent

ENERGY_PROJECT_PATH = (
    SPRINGBOARD_DIR
    / "M1_agentic_facilityops_ai"
)

MAINTENANCE_PROJECT_PATH = (
    SPRINGBOARD_DIR
    / "M2_Predictive_Maintenance"
)

M3_PROJECT_PATH = (
    SPRINGBOARD_DIR
    / "M3_Occupancy_and_Security_Intelligence"
)

OCCUPANCY_PROJECT_PATH = (
    M3_PROJECT_PATH
    / "occupancy_system"
)

SECURITY_PROJECT_PATH = (
    M3_PROJECT_PATH
    / "security_system"
)

M4_PROJECT_PATH = (
    SPRINGBOARD_DIR
    / "M4_Cost_Optimization"
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
# DATA LOADERS
# ==================================================

@st.cache_data
def load_energy_preview():

    """
    Load only the columns required for
    dashboard-level Energy visualization.

    The complete Energy dataset is loaded only
    when an actual Energy Agent analysis is run.
    """

    data_path = (
        ENERGY_PROJECT_PATH
        / "data"
        / "processed"
        / "processed_energy_data.csv"
    )

    if not data_path.exists():

        raise FileNotFoundError(
            f"Energy dataset not found:\n{data_path}"
        )

    df = pd.read_csv(
        data_path,
        usecols=[
            "timestamp",
            "meter_reading",
            "building_id",
            "site_id"
        ]
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df


@st.cache_data
def load_energy_full():

    """
    Load the complete Energy dataset.

    This is intentionally NOT called during
    normal page navigation.
    """

    data_path = (
        ENERGY_PROJECT_PATH
        / "data"
        / "processed"
        / "processed_energy_data.csv"
    )

    if not data_path.exists():

        raise FileNotFoundError(
            f"Energy dataset not found:\n{data_path}"
        )

    df = pd.read_csv(
        data_path
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df


@st.cache_data
def load_maintenance_data():

    data_path = (
        MAINTENANCE_PROJECT_PATH
        / "data"
        / "raw"
        / "ai4i2020.csv"
    )

    if not data_path.exists():

        raise FileNotFoundError(
            f"Maintenance dataset not found:\n{data_path}"
        )

    return pd.read_csv(
        data_path
    )


@st.cache_data
def load_occupancy_data():

    data_path = (
        OCCUPANCY_PROJECT_PATH
        / "data"
        / "raw"
        / "Occupancy_Estimation.csv"
    )

    if not data_path.exists():

        raise FileNotFoundError(
            f"Occupancy dataset not found:\n{data_path}"
        )

    return pd.read_csv(
        data_path
    )


@st.cache_data
def load_security_data():

    data_path = (
        SECURITY_PROJECT_PATH
        / "data"
        / "raw"
        / "access_logs_final.csv"
    )

    if not data_path.exists():

        raise FileNotFoundError(
            f"Security dataset not found:\n{data_path}"
        )

    df = pd.read_csv(
        data_path
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df


@st.cache_data
def load_cost_data():

    data_path = (
        M4_PROJECT_PATH
        / "data"
        / "operational_costs.csv"
    )

    if not data_path.exists():
        raise FileNotFoundError(
            f"Cost dataset not found:\n{data_path}"
        )

    df = pd.read_csv(data_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


# ==================================================
# SMART FACILITY AGENT
# ==================================================

@st.cache_resource
def initialize_smart_facility_agent():

    model_path = (
        MAINTENANCE_PROJECT_PATH
        / "models"
        / "maintenance_failure_model.pkl"
    )

    if not model_path.exists():

        raise FileNotFoundError(
            f"Maintenance model not found:\n{model_path}"
        )

    return SmartFacilityAgent(
        maintenance_model_path=str(
            model_path
        )
    )


def get_smart_facility_agent():

    return initialize_smart_facility_agent()


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def show_agent_status(
    title,
    description
):

    with st.container(border=True):

        st.subheader(
            title
        )

        st.caption(
            description
        )

        st.success(
            "Connected"
        )


def show_priority(
    priority
):

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


def safe_percentage(
    numerator,
    denominator
):

    if denominator == 0:

        return 0.0

    return (
        numerator
        / denominator
        * 100
    )


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title(
    "🏢 Smart Facility"
)

st.sidebar.caption(
    "Agentic AI Operations Platform"
)


page = st.sidebar.radio(
    "Navigate to Module",
    [
        "🏠 Executive Overview",
        "⚡ Energy Agent",
        "🔧 Maintenance Agent",
        "🏢 Occupancy Agent",
        "🔐 Security Agent",
        "💰 Cost Optimization",
        "🤖 Facility Intelligence"
    ]
)


st.sidebar.divider()


st.sidebar.subheader(
    "Project Progress"
)

st.sidebar.write(
    "✅ M1 — Energy Intelligence"
)

st.sidebar.write(
    "✅ M2 — Predictive Maintenance"
)

st.sidebar.write(
    "✅ M3 — Occupancy & Security"
)


st.sidebar.divider()

st.sidebar.caption(
    "Smart Facility System"
)

st.sidebar.caption(
    "M1 • M2 • M3"
)


# ==================================================
# EXECUTIVE OVERVIEW
# ==================================================

if page == "🏠 Executive Overview":

    st.markdown(
        """
        <div class="hero">
            <h1>🏢 Smart Facility Operations Center</h1>
            <p>Unified Agentic AI platform for intelligent facility operations,
            optimization and executive decision support.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        "M1–M4 integrated: Energy • Maintenance • Occupancy • Security • Cost Optimization"
    )

    st.subheader("🧭 Facility Command Center")

    c1, c2, c3, c4, c5 = st.columns(5)

    cards = [
        ("⚡", "Energy", "M1", "Monitoring + anomalies"),
        ("🔧", "Maintenance", "M2", "Failure prediction"),
        ("🏢", "Occupancy", "M3", "Usage + forecasting"),
        ("🔐", "Security", "M3", "Anomaly detection"),
        ("💰", "Cost", "M4", "Budget + savings"),
    ]

    for col, (icon, name, milestone, desc) in zip(
        [c1, c2, c3, c4, c5], cards
    ):
        with col:
            st.markdown(
                f"""
                <div class="section-card">
                    <div style="font-size:1.35rem">{icon}</div>
                    <b>{name}</b>
                    <div class="small-muted">{milestone} · {desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()
    st.subheader("💰 M4 Cost Snapshot")

    try:
        overview_agent = get_smart_facility_agent()
        cost = overview_agent.run_cost_analysis()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Operational Cost", f"₹{cost['total_operational_cost']:,.0f}")
        k2.metric("Budget", f"₹{cost['total_budget']:,.0f}")
        k3.metric("Budget Variance", f"₹{cost['budget_variance']:,.0f}")
        k4.metric("Potential Savings", f"₹{cost['potential_savings']:,.0f}")

        if cost["budget_status"] == "Over Budget":
            st.warning(
                f"⚠️ Current budget position: ₹{abs(cost['budget_variance']):,.0f} "
                f"above allocation. Estimated savings opportunity: "
                f"₹{cost['potential_savings']:,.0f}."
            )
        else:
            st.success("✅ Operational expenditure is within the allocated budget.")

    except Exception:
        st.info("M4 cost snapshot is unavailable until the cost dataset is configured.")

    st.divider()
    st.subheader("🧠 How the Agentic System Works")

    st.markdown(
        """
        <div class="section-card">
        <b>Facility Data</b> → Energy, equipment, occupancy, access and cost data
        <br><br>↓<br><br>
        <b>Specialized AI Agents</b> → Domain-specific analysis
        <br><br>↓<br><br>
        <b>Smart Facility Agent</b> → Cross-agent orchestration
        <br><br>↓<br><br>
        <b>Facility Intelligence</b> → Priorities, savings opportunities and actions
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "💡 Each agent remains modular, while the orchestration layer combines "
        "their outputs for facility-level decision support."
    )

    st.subheader("📊 Connected Data Sources")

    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("Energy", "M1")
    d1.caption("ASHRAE building energy")
    d2.metric("Maintenance", "M2")
    d2.caption("AI4I equipment data")
    d3.metric("Occupancy", "M3")
    d3.caption("Room occupancy data")
    d4.metric("Security", "M3")
    d4.caption("Access-control logs")
    d5.metric("Cost", "M4")
    d5.caption("Operational cost data")



# ==================================================
# ENERGY AGENT
# ==================================================

elif page == "⚡ Energy Agent":

    st.title(
        "⚡ Energy Intelligence"
    )

    st.caption(
        "Milestone 1 — Energy monitoring, analytics and anomaly detection"
    )


    # ------------------------------------------------
    # LIGHTWEIGHT PREVIEW
    # ------------------------------------------------

    energy_df = load_energy_preview()


    st.header(
        "📊 Energy Overview"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Records",
            f"{len(energy_df):,}"
        )


    with col2:

        st.metric(
            "Buildings",
            energy_df[
                "building_id"
            ].nunique()
        )


    with col3:

        st.metric(
            "Sites",
            energy_df[
                "site_id"
            ].nunique()
        )


    with col4:

        st.metric(
            "Peak Reading",
            f"{energy_df['meter_reading'].max():,.2f}"
        )


    # ------------------------------------------------
    # ENERGY TREND
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "📈 Energy Consumption Trend"
    )


    energy_trend = (
        energy_df
        .set_index("timestamp")
        ["meter_reading"]
        .resample("1h")
        .mean()
        .dropna()
    )


    st.line_chart(
        energy_trend,
        height=350
    )


    # ------------------------------------------------
    # BASIC ANALYTICS
    # ------------------------------------------------

    st.subheader(
        "🔍 Energy Analytics"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Average Consumption",
            f"{energy_df['meter_reading'].mean():,.2f}"
        )


    with col2:

        st.metric(
            "Maximum Consumption",
            f"{energy_df['meter_reading'].max():,.2f}"
        )


    with col3:

        st.metric(
            "Minimum Consumption",
            f"{energy_df['meter_reading'].min():,.2f}"
        )


    # ------------------------------------------------
    # ACTUAL AGENT
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "🤖 Energy Agent"
    )


    st.write(
        "Run the complete Energy Agent pipeline for "
        "analytics, anomaly detection and recommendations."
    )


    if st.button(
        "🚀 Run Energy Agent Analysis",
        use_container_width=True
    ):

        with st.spinner(
            "Energy Agent analyzing facility data..."
        ):

            full_energy_df = (
                load_energy_full()
            )

            agent = (
                get_smart_facility_agent()
            )

            energy_results = (
                agent.run_energy_analysis(
                    full_energy_df
                )
            )


        st.success(
            "Energy Agent analysis completed."
        )


        summary = (
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
                "Total Energy",
                f"{summary['total_energy']:,.2f}"
            )


        with col2:

            st.metric(
                "Average Energy",
                f"{summary['average_energy']:,.2f}"
            )


        with col3:

            st.metric(
                "Peak Energy",
                f"{summary['peak_energy']:,.2f}"
            )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Peak Usage Hour",
                f"{peak_usage['peak_hour']}:00"
            )


        with col2:

            st.metric(
                "Energy Anomalies",
                f"{anomaly_count:,}"
            )


# ==================================================
# MAINTENANCE AGENT
# ==================================================

elif page == "🔧 Maintenance Agent":

    st.title(
        "🔧 Predictive Maintenance"
    )

    st.caption(
        "Milestone 2 — Equipment health monitoring and failure prediction"
    )


    maintenance_df = (
        load_maintenance_data()
    )


    # ------------------------------------------------
    # DATASET OVERVIEW
    # ------------------------------------------------

    st.header(
        "📊 Equipment Overview"
    )


    failure_count = int(
        maintenance_df[
            "Machine failure"
        ].sum()
    )


    failure_rate = safe_percentage(
        failure_count,
        len(maintenance_df)
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Records",
            f"{len(maintenance_df):,}"
        )


    with col2:

        st.metric(
            "Failures",
            f"{failure_count:,}"
        )


    with col3:

        st.metric(
            "Failure Rate",
            f"{failure_rate:.2f}%"
        )


    with col4:

        st.metric(
            "Machine Types",
            maintenance_df[
                "Type"
            ].nunique()
        )


    # ------------------------------------------------
    # FAILURE CHART
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "📊 Failure Distribution"
    )


    failure_distribution = (
        maintenance_df[
            "Machine failure"
        ]
        .value_counts()
        .sort_index()
    )


    failure_distribution.index = [
        "No Failure"
        if value == 0
        else "Failure"
        for value in failure_distribution.index
    ]


    st.bar_chart(
        failure_distribution,
        height=300
    )


    # ------------------------------------------------
    # MACHINE ANALYSIS
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "🔍 Individual Machine Analysis"
    )


    product_ids = (
        maintenance_df[
            "Product ID"
        ]
        .astype(str)
        .unique()
    )


    selected_product_id = st.selectbox(
        "Select Machine",
        product_ids
    )


    selected_machine = (
        maintenance_df[
            maintenance_df[
                "Product ID"
            ].astype(str)
            == selected_product_id
        ]
        .iloc[0]
    )


    if st.button(
        "🚀 Analyze Machine",
        use_container_width=True
    ):

        with st.spinner(
            "Maintenance Agent analyzing machine..."
        ):

            agent = (
                get_smart_facility_agent()
            )

            maintenance_result = (
                agent.analyze_machine(
                    selected_machine
                )
            )


        st.success(
            "Machine analysis completed."
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Product ID",
                maintenance_result[
                    "product_id"
                ]
            )


        with col2:

            st.metric(
                "Health Score",
                f"{maintenance_result['health_score']}/100"
            )


        with col3:

            st.metric(
                "Risk Level",
                maintenance_result[
                    "risk_level"
                ]
            )


        col1, col2, col3 = st.columns(3)


        with col1:

            prediction = (
                maintenance_result[
                    "failure_prediction"
                ]
            )

            prediction_text = (
                "Failure Predicted"
                if prediction == 1
                else "No Failure Predicted"
            )

            st.metric(
                "Prediction",
                prediction_text
            )


        with col2:

            probability = (
                maintenance_result[
                    "failure_probability"
                ]
            )

            st.metric(
                "Failure Probability",
                f"{probability * 100:.2f}%"
            )


        with col3:

            st.metric(
                "Machine Type",
                maintenance_result[
                    "machine_type"
                ]
            )


        st.subheader(
            "🛠️ Maintenance Recommendation"
        )

        st.info(
            maintenance_result[
                "recommendation"
            ]
        )


# ==================================================
# OCCUPANCY AGENT
# ==================================================

elif page == "🏢 Occupancy Agent":

    st.title(
        "🏢 Occupancy Intelligence"
    )

    st.caption(
        "Milestone 3 — Occupancy analytics and forecasting"
    )


    occupancy_df = (
        load_occupancy_data()
    )


    # ------------------------------------------------
    # PREPARE TIMESTAMP
    # ------------------------------------------------

    occupancy_chart_df = (
        occupancy_df.copy()
    )


    occupancy_chart_df["Timestamp"] = (
        pd.to_datetime(
            occupancy_chart_df["Date"].astype(str)
            + " "
            + occupancy_chart_df["Time"].astype(str),
            errors="coerce"
        )
    )


    occupancy_chart_df = (
        occupancy_chart_df
        .dropna(
            subset=["Timestamp"]
        )
        .sort_values("Timestamp")
    )


    # ------------------------------------------------
    # KPIs
    # ------------------------------------------------

    current_occupancy = int(
        occupancy_df[
            "Room_Occupancy_Count"
        ].iloc[-1]
    )


    occupancy_rate = (
        (
            occupancy_df[
                "Room_Occupancy_Count"
            ] > 0
        )
        .mean()
        * 100
    )


    average_occupancy = (
        occupancy_df[
            "Room_Occupancy_Count"
        ]
        .mean()
    )


    maximum_occupancy = int(
        occupancy_df[
            "Room_Occupancy_Count"
        ]
        .max()
    )


    st.header(
        "📊 Occupancy Overview"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Records",
            f"{len(occupancy_df):,}"
        )


    with col2:

        st.metric(
            "Current Occupancy",
            current_occupancy
        )


    with col3:

        st.metric(
            "Occupancy Rate",
            f"{occupancy_rate:.2f}%"
        )


    with col4:

        st.metric(
            "Maximum Occupancy",
            maximum_occupancy
        )


    # ------------------------------------------------
    # OCCUPANCY TREND
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "📈 Occupancy Trend"
    )


    occupancy_trend = (
        occupancy_chart_df
        .set_index("Timestamp")
        ["Room_Occupancy_Count"]
        .resample("5min")
        .mean()
        .dropna()
    )


    st.line_chart(
        occupancy_trend,
        height=350
    )


    # ------------------------------------------------
    # BASIC ANALYTICS
    # ------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Average Occupancy",
            f"{average_occupancy:.2f}"
        )


    with col2:

        current_status = (
            "OCCUPIED"
            if current_occupancy > 0
            else "VACANT"
        )

        st.metric(
            "Current Status",
            current_status
        )


    # ------------------------------------------------
    # OCCUPANCY AGENT
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "🤖 Occupancy Agent"
    )


    if st.button(
        "🚀 Run Occupancy Agent Analysis",
        use_container_width=True
    ):

        with st.spinner(
            "Occupancy Agent analyzing room activity..."
        ):

            agent = (
                get_smart_facility_agent()
            )

            occupancy_results = (
                agent.run_occupancy_analysis(
                    occupancy_df
                )
            )


        st.success(
            "Occupancy analysis completed."
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Current Occupancy",
                occupancy_results[
                    "current_occupancy"
                ]
            )


        with col2:

            st.metric(
                "Status",
                occupancy_results[
                    "current_status"
                ]
            )


        with col3:

            st.metric(
                "Average Occupancy",
                occupancy_results[
                    "average_occupancy"
                ]
            )


        forecast = (
            occupancy_results[
                "forecast"
            ]
        )


        st.subheader(
            "🔮 Occupancy Forecast"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Current",
                forecast[
                    "current_occupancy"
                ]
            )


        with col2:

            st.metric(
                "Predicted Next",
                forecast[
                    "predicted_next_occupancy"
                ]
            )


        with col3:

            st.metric(
                "Forecast Horizon",
                forecast[
                    "forecast_horizon"
                ]
            )


# ==================================================
# SECURITY AGENT
# ==================================================

elif page == "🔐 Security Agent":

    st.title(
        "🔐 Security Intelligence"
    )

    st.caption(
        "Milestone 3 — Access monitoring and behavioral anomaly detection"
    )


    security_df = (
        load_security_data()
    )


    # ------------------------------------------------
    # SECURITY KPIs
    # ------------------------------------------------

    anomaly_count = int(
        security_df[
            "is_anomaly"
        ].sum()
    )


    anomaly_rate = safe_percentage(
        anomaly_count,
        len(security_df)
    )


    unique_users = (
        security_df[
            "user_id"
        ].nunique()
    )


    unique_locations = (
        security_df[
            "location"
        ].nunique()
    )


    st.header(
        "📊 Security Overview"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Security Events",
            f"{len(security_df):,}"
        )


    with col2:

        st.metric(
            "Anomalies",
            f"{anomaly_count:,}"
        )


    with col3:

        st.metric(
            "Anomaly Rate",
            f"{anomaly_rate:.2f}%"
        )


    with col4:

        st.metric(
            "Locations",
            f"{unique_locations:,}"
        )


    # ------------------------------------------------
    # ANOMALY DISTRIBUTION
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "🚨 Anomaly Distribution"
    )


    anomaly_types = (
        security_df[
            security_df["is_anomaly"] == 1
        ]
        ["anomaly_type"]
        .fillna("Unknown")
        .value_counts()
    )


    if not anomaly_types.empty:

        st.bar_chart(
            anomaly_types,
            height=350
        )


    # ------------------------------------------------
    # USER / EVENT ANALYTICS
    # ------------------------------------------------

    st.subheader(
        "📈 Security Activity"
    )


    security_trend = (
        security_df
        .set_index("timestamp")
        .resample("1h")
        .size()
        .rename("Events")
    )


    st.line_chart(
        security_trend,
        height=300
    )


    # ------------------------------------------------
    # EVENT INVESTIGATION
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "🔍 Security Event Investigation"
    )


    anomalous_events = (
        security_df[
            security_df["is_anomaly"] == 1
        ]
        .sort_values(
            "timestamp",
            ascending=False
        )
    )


    if anomalous_events.empty:

        st.info(
            "No anomalous events available."
        )

    else:

        event_ids = (
            anomalous_events[
                "log_id"
            ]
            .astype(str)
            .tolist()
        )


        selected_log_id = st.selectbox(
            "Select Anomalous Event",
            event_ids
        )


        selected_event_df = (
            anomalous_events[
                anomalous_events[
                    "log_id"
                ].astype(str)
                == selected_log_id
            ]
        )


        selected_event = (
            selected_event_df
            .iloc[0]
            .to_dict()
        )


        # Convert timestamp to string so
        # SecurityAgent receives a clean value.
        if pd.notna(
            selected_event.get(
                "timestamp"
            )
        ):

            selected_event["timestamp"] = (
                str(
                    selected_event[
                        "timestamp"
                    ]
                )
            )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "User",
                str(
                    selected_event.get(
                        "user_id",
                        "Unknown"
                    )
                )
            )

            st.metric(
                "Action",
                str(
                    selected_event.get(
                        "action",
                        "Unknown"
                    )
                )
            )


        with col2:

            st.metric(
                "Resource",
                str(
                    selected_event.get(
                        "resource",
                        "Unknown"
                    )
                )
            )

            st.metric(
                "Location",
                str(
                    selected_event.get(
                        "location",
                        "Unknown"
                    )
                )
            )


        with col3:

            st.metric(
                "Anomaly Type",
                str(
                    selected_event.get(
                        "anomaly_type",
                        "Unknown"
                    )
                )
            )

            st.metric(
                "Agent Type",
                str(
                    selected_event.get(
                        "agent_type",
                        "Unknown"
                    )
                )
            )


        if st.button(
            "🚨 Analyze Selected Event",
            use_container_width=True
        ):

            with st.spinner(
                "Security Agent analyzing event..."
            ):

                agent = (
                    get_smart_facility_agent()
                )

                security_result = (
                    agent.analyze_security_event(
                        selected_event
                    )
                )


            st.success(
                "Security event analysis completed."
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Risk Score",
                    f"{security_result['risk_score']:.4f}"
                )


            with col2:

                status = (
                    "ANOMALY"
                    if security_result[
                        "is_anomaly"
                    ]
                    else "NORMAL"
                )

                st.metric(
                    "Assessment",
                    status
                )


            with col3:

                st.metric(
                    "Severity",
                    security_result[
                        "severity"
                    ]
                )


            st.subheader(
                "🔎 Detection Reasons"
            )


            reasons = (
                security_result[
                    "reasons"
                ]
            )


            if reasons:

                for reason in reasons:

                    st.write(
                        f"• {reason}"
                    )

            else:

                st.write(
                    "No specific reasons reported."
                )


    # ------------------------------------------------
    # RECENT ALERTS
    # ------------------------------------------------

    st.divider()

    st.subheader(
        "📋 Recent Security Alerts"
    )


    display_columns = [
        "timestamp",
        "user_id",
        "action",
        "resource",
        "location",
        "anomaly_type"
    ]


    available_columns = [
        column
        for column in display_columns
        if column in anomalous_events.columns
    ]


    st.dataframe(
        anomalous_events[
            available_columns
        ].head(20),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# COST OPTIMIZATION AGENT - M4
# ==================================================

elif page == "💰 Cost Optimization":

    st.markdown(
        """
        <div class="hero">
            <h1>💰 Cost Optimization Center</h1>
            <p>Operational expenditure, budget compliance,
            savings opportunities and explainable ROI.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        cost_df = load_cost_data()
        agent = get_smart_facility_agent()

        with st.spinner("Cost Optimization Agent analyzing expenditure..."):
            cost_results = agent.run_cost_analysis()

        st.subheader("📌 Executive Cost Indicators")

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Operational Cost", f"₹{cost_results['total_operational_cost']:,.0f}")
        k2.metric("Allocated Budget", f"₹{cost_results['total_budget']:,.0f}")
        k3.metric("Variance", f"₹{cost_results['budget_variance']:,.0f}")
        k4.metric("Potential Savings", f"₹{cost_results['potential_savings']:,.0f}")

        if cost_results["budget_status"] == "Over Budget":
            st.error(
                f"🔴 OVER BUDGET — ₹{abs(cost_results['budget_variance']):,.0f} above allocation."
            )
        else:
            st.success(f"🟢 Budget status: {cost_results['budget_status']}")

        st.divider()
        st.subheader("📈 Monthly Cost vs Budget")

        cost_cols = [
            "energy_cost", "maintenance_cost", "water_cost",
            "vendor_cost", "labor_cost", "other_cost"
        ]

        monthly = cost_df.copy()
        monthly["total_cost"] = monthly[cost_cols].sum(axis=1)

        st.line_chart(
            monthly[["date", "total_cost", "budget"]].set_index("date"),
            height=330
        )

        st.caption(
            "When total cost stays above the budget line, expenditure is "
            "higher than planned for that period."
        )

        left, right = st.columns([1.2, 1])

        with left:
            st.subheader("💸 Cost Breakdown")
            breakdown = cost_results["cost_breakdown"]

            breakdown_df = pd.DataFrame(
                {
                    "Category": [
                        k.replace("_cost", "").replace("_", " ").title()
                        for k in breakdown
                    ],
                    "Cost": list(breakdown.values())
                }
            ).set_index("Category")

            st.bar_chart(breakdown_df, height=350)

        with right:
            st.subheader("🔎 Cost Drivers")
            total = cost_results["total_operational_cost"]

            for category, value in breakdown.items():
                share = safe_percentage(value, total)
                st.markdown(
                    f"""
                    <div class="section-card">
                        <b>{category.replace('_cost','').replace('_',' ').title()}</b>
                        <br>₹{value:,.0f} · {share:.1f}% of total cost
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()
        st.subheader("💡 Identified Savings Opportunities")

        for i, opportunity in enumerate(
            cost_results["savings_opportunities"], 1
        ):
            with st.container(border=True):
                a, b, c = st.columns([1.1, 1, 2.2])

                with a:
                    st.markdown(f"### {i}. {opportunity['area']}")
                    st.caption(
                        f"Current cost: ₹{opportunity['current_cost']:,.0f}"
                    )

                with b:
                    st.metric(
                        "Potential Saving",
                        f"₹{opportunity['estimated_savings']:,.0f}"
                    )

                with c:
                    st.markdown("**Recommended action**")
                    st.write(opportunity["action"])

        st.divider()
        st.subheader("📈 Optimization ROI")

        roi = cost_results["roi"]
        r1, r2, r3 = st.columns(3)

        r1.metric("Estimated Savings", f"₹{roi['estimated_annual_savings']:,.0f}")
        r2.metric(
            "Estimated Implementation Cost",
            f"₹{roi['estimated_implementation_cost']:,.0f}"
        )
        r3.metric("Estimated ROI", f"{roi['estimated_roi_percent']:.0f}%")

        st.caption(
            "ROI is an estimate based on the project's optimization assumptions; "
            "it is not a measured financial return."
        )

        st.subheader("🤖 Explainable AI Recommendations")

        for rec in cost_results["recommendations"]:
            st.markdown(
                f"""
                <div class="recommendation-card">
                    🧠 {rec}
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.expander("📖 How the Cost Optimization Agent works"):
            st.markdown(
                """
                **1. Analyze** — aggregate operational expenditure.

                **2. Compare** — compare actual cost against budget.

                **3. Identify** — find high-impact optimization areas.

                **4. Estimate** — calculate potential savings.

                **5. Evaluate** — estimate ROI from optimization initiatives.

                **6. Recommend** — convert the analysis into facility-manager actions.
                """
            )

        with st.expander("📄 View operational cost data"):
            st.dataframe(
                cost_df,
                use_container_width=True,
                hide_index=True
            )

    except Exception as exc:
        st.error(f"Cost Optimization Agent error: {exc}")


# ==================================================
# FACILITY INTELLIGENCE - M4 EXECUTIVE DASHBOARD
# ==================================================

elif page == "🤖 Facility Intelligence":

    st.markdown(
        """
        <div class="hero">
            <h1>🤖 Facility Intelligence Dashboard</h1>
            <p>Cross-agent orchestration for executive-level facility decisions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "This is the M4 decision-support layer: specialized agents are "
        "coordinated into one facility-level view."
    )

    maintenance_df = load_maintenance_data()
    occupancy_df = load_occupancy_data()
    security_df = load_security_data()

    product_ids = maintenance_df["Product ID"].astype(str).unique()

    selected_product_id = st.selectbox(
        "⚙️ Select machine",
        product_ids
    )

    selected_machine = maintenance_df[
        maintenance_df["Product ID"].astype(str) == selected_product_id
    ].iloc[0]

    anomalous_events = (
        security_df[
            security_df["is_anomaly"] == 1
        ]
        .sort_values("timestamp", ascending=False)
    )

    selected_security_event = None

    if not anomalous_events.empty:

        event_ids = anomalous_events["log_id"].astype(str).tolist()

        selected_security_log = st.selectbox(
            "🔐 Select security event",
            event_ids
        )

        selected_security_event = anomalous_events[
            anomalous_events["log_id"].astype(str) == selected_security_log
        ].iloc[0].to_dict()

        if pd.notna(selected_security_event.get("timestamp")):
            selected_security_event["timestamp"] = str(
                selected_security_event["timestamp"]
            )

    st.divider()

    run = st.button(
        "🚀 Run Complete Facility Intelligence",
        use_container_width=True,
        type="primary"
    )

    if run:

        with st.spinner(
            "Coordinating Energy, Maintenance, Occupancy, Security and Cost agents..."
        ):

            agent = get_smart_facility_agent()

            energy_results = agent.run_energy_analysis(
                load_energy_full()
            )

            maintenance_result = agent.analyze_machine(
                selected_machine
            )

            occupancy_results = agent.run_occupancy_analysis(
                occupancy_df
            )

            security_result = None

            if selected_security_event:
                security_result = agent.analyze_security_event(
                    selected_security_event
                )

            cost_results = agent.run_cost_analysis()

            facility_insight = agent.generate_facility_insight(
                energy_results,
                maintenance_result,
                cost_results
            )

            st.session_state["facility_results"] = {
                "energy": energy_results,
                "maintenance": maintenance_result,
                "occupancy": occupancy_results,
                "security": security_result,
                "cost": cost_results,
                "insight": facility_insight
            }

    results = st.session_state.get("facility_results")

    if results:

        energy_results = results["energy"]
        maintenance_result = results["maintenance"]
        occupancy_results = results["occupancy"]
        security_result = results["security"]
        cost_results = results["cost"]
        facility_insight = results["insight"]

        st.subheader("🎯 Facility Decision Summary")

        p1, p2, p3, p4, p5 = st.columns(5)

        p1.metric(
            "Priority",
            facility_insight["facility_priority"]
        )
        p2.metric(
            "Energy Anomalies",
            f"{energy_results['anomaly_count']:,}"
        )
        p3.metric(
            "Machine Risk",
            maintenance_result["risk_level"]
        )
        p4.metric(
            "Potential Savings",
            f"₹{cost_results['potential_savings']:,.0f}"
        )
        p5.metric(
            "Budget",
            cost_results["budget_status"]
        )

        st.divider()
        st.subheader("🧠 Cross-Agent Intelligence")

        for insight in facility_insight["insights"]:
            st.markdown(
                f"""
                <div class="insight-card">
                    {insight}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("🎯 Recommended Facility Action")

        st.markdown(
            f"""
            <div class="recommendation-card">
                <b>Priority: {facility_insight['facility_priority']}</b>
                <br><br>
                {facility_insight['combined_recommendation']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()
        st.subheader("📊 Agent Scorecards")

        a1, a2 = st.columns(2)

        with a1:
            with st.container(border=True):
                st.markdown("### ⚡ Energy")
                summary = energy_results["summary"]
                st.metric("Total Energy", f"{summary['total_energy']:,.2f}")
                st.metric("Peak Energy", f"{summary['peak_energy']:,.2f}")
                st.caption(
                    f"{energy_results['anomaly_count']:,} anomalies detected"
                )

        with a2:
            with st.container(border=True):
                st.markdown("### 🔧 Maintenance")
                st.metric(
                    "Machine",
                    maintenance_result["product_id"]
                )
                st.metric(
                    "Health Score",
                    f"{maintenance_result['health_score']}/100"
                )
                st.caption(
                    f"Risk: {maintenance_result['risk_level']}"
                )

        a3, a4 = st.columns(2)

        with a3:
            with st.container(border=True):
                st.markdown("### 🏢 Occupancy")
                st.metric(
                    "Current",
                    occupancy_results["current_occupancy"]
                )
                st.metric(
                    "Maximum",
                    occupancy_results["maximum_occupancy"]
                )
                st.caption(
                    f"Predicted next: "
                    f"{occupancy_results['forecast']['predicted_next_occupancy']}"
                )

        with a4:
            with st.container(border=True):
                st.markdown("### 🔐 Security")

                if security_result:
                    status = (
                        "ANOMALY"
                        if security_result["is_anomaly"]
                        else "NORMAL"
                    )

                    st.metric("Assessment", status)
                    st.metric(
                        "Severity",
                        security_result["severity"]
                    )
                else:
                    st.info("No security event selected.")

        st.divider()
        st.subheader("💰 Financial Intelligence")

        f1, f2, f3 = st.columns(3)

        f1.metric(
            "Operational Cost",
            f"₹{cost_results['total_operational_cost']:,.0f}"
        )
        f2.metric(
            "Budget Variance",
            f"₹{cost_results['budget_variance']:,.0f}"
        )
        f3.metric(
            "Potential Savings",
            f"₹{cost_results['potential_savings']:,.0f}"
        )

        st.caption(
            "Potential savings are estimated optimization opportunities, "
            "not guaranteed financial outcomes."
        )

        st.subheader("🛠️ Action Plan")

        for i, recommendation in enumerate(
            cost_results["recommendations"], 1
        ):
            st.markdown(
                f"""
                <div class="recommendation-card">
                    <b>Action {i}</b><br>
                    {recommendation}
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.expander("🔬 Explain the facility intelligence logic"):
            st.markdown(
                """
                **Energy Agent** → consumption, peaks and anomalies

                **Maintenance Agent** → equipment health and failure risk

                **Occupancy Agent** → current utilization and forecast

                **Security Agent** → access anomalies and severity

                **Cost Optimization Agent** → expenditure, budget, savings and ROI

                **Smart Facility Agent** → coordinates these outputs and
                produces facility priority and recommendations.
                """
            )

    else:
        st.info(
            "👆 Select the analysis inputs and click "
            "**Run Complete Facility Intelligence** to generate the executive view."
        )



# ==================================================
# COMBINED FACILITY AGENT
# ==================================================

elif page == "🤖 Combined Facility Agent":

    st.title(
        "🤖 Combined Facility Intelligence"
    )

    st.caption(
        "Unified operational view across Energy, Maintenance, Occupancy and Security"
    )


    st.info(
        "This workflow intentionally runs only when you click "
        "the analysis button because it coordinates multiple agents."
    )


    # ------------------------------------------------
    # LOAD SMALLER DATASETS
    # ------------------------------------------------

    maintenance_df = (
        load_maintenance_data()
    )

    occupancy_df = (
        load_occupancy_data()
    )

    security_df = (
        load_security_data()
    )


    # ------------------------------------------------
    # MACHINE
    # ------------------------------------------------

    st.header(
        "⚙️ Analysis Configuration"
    )


    product_ids = (
        maintenance_df[
            "Product ID"
        ]
        .astype(str)
        .unique()
    )


    selected_product_id = st.selectbox(
        "Select Machine",
        product_ids
    )


    selected_machine = (
        maintenance_df[
            maintenance_df[
                "Product ID"
            ].astype(str)
            == selected_product_id
        ]
        .iloc[0]
    )


    # ------------------------------------------------
    # SECURITY EVENT
    # ------------------------------------------------

    anomalous_events = (
        security_df[
            security_df["is_anomaly"] == 1
        ]
        .sort_values(
            "timestamp",
            ascending=False
        )
    )


    selected_security_event = None


    if not anomalous_events.empty:

        security_event_ids = (
            anomalous_events[
                "log_id"
            ]
            .astype(str)
            .tolist()
        )


        selected_security_log = st.selectbox(
            "Select Security Event",
            security_event_ids
        )


        selected_security_event = (
            anomalous_events[
                anomalous_events[
                    "log_id"
                ].astype(str)
                == selected_security_log
            ]
            .iloc[0]
            .to_dict()
        )


        if pd.notna(
            selected_security_event.get(
                "timestamp"
            )
        ):

            selected_security_event[
                "timestamp"
            ] = str(
                selected_security_event[
                    "timestamp"
                ]
            )


    # ------------------------------------------------
    # RUN BUTTON
    # ------------------------------------------------

    st.divider()


    if st.button(
        "🚀 Run Combined Facility Analysis",
        use_container_width=True
    ):

        with st.spinner(
            "Running Energy, Maintenance, Occupancy and Security Agents..."
        ):

            agent = (
                get_smart_facility_agent()
            )


            # ----------------------------------------
            # ENERGY
            # ----------------------------------------

            energy_df = (
                load_energy_full()
            )


            energy_results = (
                agent.run_energy_analysis(
                    energy_df
                )
            )


            # ----------------------------------------
            # MAINTENANCE
            # ----------------------------------------

            maintenance_result = (
                agent.analyze_machine(
                    selected_machine
                )
            )


            # ----------------------------------------
            # OCCUPANCY
            # ----------------------------------------

            occupancy_results = (
                agent.run_occupancy_analysis(
                    occupancy_df
                )
            )


            # ----------------------------------------
            # SECURITY
            # ----------------------------------------

            security_result = None


            if selected_security_event:

                security_result = (
                    agent.analyze_security_event(
                        selected_security_event
                    )
                )


            # ----------------------------------------
            # EXISTING FACILITY INSIGHT
            # ----------------------------------------

            facility_insight = (
                agent.generate_facility_insight(
                    energy_results,
                    maintenance_result,
                    agent.run_cost_analysis()
                )
            )


        st.success(
            "Combined facility analysis completed successfully."
        )


        # ==================================================
        # FACILITY PRIORITY
        # ==================================================

        st.header(
            "🏢 Facility Priority"
        )


        show_priority(
            facility_insight[
                "facility_priority"
            ]
        )


        # ==================================================
        # AGENT RESULTS
        # ==================================================

        st.divider()

        st.header(
            "🤖 Agent Results"
        )


        # ------------------------------------------------
        # ENERGY
        # ------------------------------------------------

        with st.expander(
            "⚡ Energy Agent",
            expanded=True
        ):

            summary = (
                energy_results[
                    "summary"
                ]
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Total Energy",
                    f"{summary['total_energy']:,.2f}"
                )


            with col2:

                st.metric(
                    "Average Energy",
                    f"{summary['average_energy']:,.2f}"
                )


            with col3:

                st.metric(
                    "Energy Anomalies",
                    f"{energy_results['anomaly_count']:,}"
                )


        # ------------------------------------------------
        # MAINTENANCE
        # ------------------------------------------------

        with st.expander(
            "🔧 Maintenance Agent",
            expanded=True
        ):

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Machine",
                    maintenance_result[
                        "product_id"
                    ]
                )


            with col2:

                st.metric(
                    "Health Score",
                    f"{maintenance_result['health_score']}/100"
                )


            with col3:

                st.metric(
                    "Risk Level",
                    maintenance_result[
                        "risk_level"
                    ]
                )


            st.info(
                maintenance_result[
                    "recommendation"
                ]
            )


        # ------------------------------------------------
        # OCCUPANCY
        # ------------------------------------------------

        with st.expander(
            "🏢 Occupancy Agent",
            expanded=True
        ):

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Current Occupancy",
                    occupancy_results[
                        "current_occupancy"
                    ]
                )


            with col2:

                st.metric(
                    "Occupancy Rate",
                    f"{occupancy_results['occupancy_rate_percent']:.2f}%"
                )


            with col3:

                st.metric(
                    "Maximum Occupancy",
                    occupancy_results[
                        "maximum_occupancy"
                    ]
                )


            forecast = (
                occupancy_results[
                    "forecast"
                ]
            )


            st.write(
                "### Next-Step Forecast"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Current",
                    forecast[
                        "current_occupancy"
                    ]
                )


            with col2:

                st.metric(
                    "Predicted Next",
                    forecast[
                        "predicted_next_occupancy"
                    ]
                )


        # ------------------------------------------------
        # SECURITY
        # ------------------------------------------------

        with st.expander(
            "🔐 Security Agent",
            expanded=True
        ):

            if security_result:

                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Risk Score",
                        f"{security_result['risk_score']:.4f}"
                    )


                with col2:

                    security_status = (
                        "ANOMALY"
                        if security_result[
                            "is_anomaly"
                        ]
                        else "NORMAL"
                    )


                    st.metric(
                        "Assessment",
                        security_status
                    )


                with col3:

                    st.metric(
                        "Severity",
                        security_result[
                            "severity"
                        ]
                    )


                st.write(
                    "### Detection Reasons"
                )


                for reason in (
                    security_result["reasons"]
                ):

                    st.write(
                        f"• {reason}"
                    )

            else:

                st.info(
                    "No security event selected."
                )


        # ==================================================
        # FACILITY INSIGHTS
        # ==================================================

        st.divider()

        st.header(
            "💡 Facility-Level Insights"
        )


        for insight in (
            facility_insight[
                "insights"
            ]
        ):

            st.write(
                f"• {insight}"
            )


        st.subheader(
            "🎯 Combined Recommendation"
        )


        st.info(
            facility_insight[
                "combined_recommendation"
            ]
        )


        # ==================================================
        # M3 OPERATIONAL SUMMARY
        # ==================================================

        st.divider()

        st.header(
            "📌 M3 Operational Summary"
        )


        security_status = (
            "Anomaly Detected"
            if (
                security_result
                and security_result[
                    "is_anomaly"
                ]
            )
            else "No Anomaly Detected"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Current Occupancy",
                occupancy_results[
                    "current_occupancy"
                ]
            )


        with col2:

            st.metric(
                "Next Occupancy",
                occupancy_results[
                    "forecast"
                ][
                    "predicted_next_occupancy"
                ]
            )


        with col3:

            st.metric(
                "Security",
                security_status
            )



