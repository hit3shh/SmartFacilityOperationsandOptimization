import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_loader import DataLoader


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="FacilityOps AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ------------------------------
       MAIN APPLICATION
    ------------------------------ */

    .stApp {
        background-color: #F5F7FA;
        color: #1F2937;
    }


    /* Main content area */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }


    /* ------------------------------
       TEXT
    ------------------------------ */

    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }

    p, span, label {
        color: #374151;
    }


    /* ------------------------------
       MAIN TITLES
    ------------------------------ */

    .main-title {
        font-size: 46px;
        font-weight: 700;
        color: #111827 !important;
        margin-bottom: 8px;
    }


    .subtitle {
        font-size: 17px;
        color: #6B7280 !important;
        margin-bottom: 30px;
    }


    .section-title {
        font-size: 25px;
        font-weight: 650;
        color: #111827 !important;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ------------------------------
       METRIC CARDS
    ------------------------------ */

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }


    div[data-testid="stMetricLabel"] {
        color: #6B7280 !important;
        font-weight: 600;
    }


    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 700;
    }


    /* ------------------------------
       SIDEBAR
    ------------------------------ */

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }


    section[data-testid="stSidebar"] * {
        color: #1F2937;
    }


    /* ------------------------------
       BUTTONS
    ------------------------------ */

    .stButton > button {
        background-color: #2563EB;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 10px;
    }


    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white !important;
    }


    /* ------------------------------
       INPUT BOXES
    ------------------------------ */

    .stTextInput input {
        background-color: white !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB;
        border-radius: 8px;
    }


    /* ------------------------------
       DATAFRAME
    ------------------------------ */

    div[data-testid="stDataFrame"] {
        border: 1px solid #E5E7EB;
        border-radius: 10px;
    }


    /* ------------------------------
       ALERT BOXES
    ------------------------------ */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ------------------------------
       LOGIN
    ------------------------------ */

    .login-title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        color: #111827 !important;
        margin-top: 40px;
    }


    .login-subtitle {
        text-align: center;
        color: #6B7280 !important;
        font-size: 17px;
        margin-bottom: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SESSION STATE
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Energy Dashboard"


# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_energy_data():

    loader = DataLoader(
        "data/processed/processed_energy_data.csv"
    )

    df = loader.load_data()

    return df


# ==================================================
# LOGIN PAGE
# ==================================================

def login_page():

    st.markdown(
        '<div class="login-title">⚡ FacilityOps AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Smart Facility Energy Intelligence Platform'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(
        [1, 1.2, 1]
    )

    with col2:

        st.markdown("### 🔐 Sign In")

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        login_button = st.button(
            "Sign In to FacilityOps AI",
            use_container_width=True
        )

        if login_button:

            if username == "admin" and password == "admin":

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login successful!")

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

        st.caption(
            "Demo credentials: admin / admin"
        )


# ==================================================
# SIDEBAR
# ==================================================

def sidebar(df):

    with st.sidebar:

        st.markdown(
            "## 🏢 FacilityOps AI"
        )

        st.caption(
            "Smart Facility Intelligence"
        )

        st.divider()

        st.markdown(
            "### Navigation"
        )

        page = st.radio(
            "",
            [
                "⚡ Energy Dashboard",
                "🤖 Energy Agent",
                "📊 Anomaly Analytics"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown(
            "### 🔍 Monitoring Filters"
        )

        building_ids = sorted(
            df["building_id"].unique()
        )

        selected_building = st.selectbox(
            "Select Building",
            ["All Buildings"] + building_ids
        )

        st.caption(
            f"Logged in as: {st.session_state.username}"
        )

        st.divider()

        if st.button(
            "Sign Out",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.rerun()

    return page, selected_building


# ==================================================
# FILTER DATA
# ==================================================

def filter_data(df, building_id):

    if building_id == "All Buildings":

        return df.copy()

    return df[
        df["building_id"] == building_id
    ].copy()


# ==================================================
# ENERGY DASHBOARD
# ==================================================

def energy_dashboard(df):

    st.markdown(
        '<div class="main-title">'
        '⚡ Energy Intelligence & Monitoring Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered monitoring and analysis of facility energy consumption'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    total_energy = df["meter_reading"].sum()

    average_energy = df["meter_reading"].mean()

    peak_energy = df["meter_reading"].max()

    avg_temperature = df["air_temperature"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Consumption",
        f"{total_energy:,.0f}"
    )

    col2.metric(
        "Average Energy",
        f"{average_energy:,.2f}"
    )

    col3.metric(
        "Peak Energy",
        f"{peak_energy:,.2f}"
    )

    col4.metric(
        "Average Temperature",
        f"{avg_temperature:,.1f} °C"
    )

    st.divider()

    # --------------------------------------------------
    # PERFORMANCE OPTIMIZATION
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📈 Energy Consumption'
        '</div>',
        unsafe_allow_html=True
    )

    # Aggregate by timestamp
    energy_timeline = (
        df.groupby("timestamp")[
            "meter_reading"
        ]
        .mean()
        .reset_index()
    )

    # Limit displayed data for faster chart rendering
    chart_data = energy_timeline.tail(1000)

    fig = px.line(
        chart_data,
        x="timestamp",
        y="meter_reading",
        title="Energy Consumption Timeline"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🌡️ Temperature Monitoring'
        '</div>',
        unsafe_allow_html=True
    )

    temperature_data = (
        df.groupby("timestamp")[
            "air_temperature"
        ]
        .mean()
        .reset_index()
    )

    temperature_chart = (
        temperature_data.tail(1000)
    )

    fig_temp = px.line(
        temperature_chart,
        x="timestamp",
        y="air_temperature",
        title="Average Air Temperature"
    )

    fig_temp.update_layout(
        height=400
    )

    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )

    # --------------------------------------------------
    # ENERGY BY HOUR
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '⏰ Hourly Energy Pattern'
        '</div>',
        unsafe_allow_html=True
    )

    hourly_data = (
        df.groupby("hour")[
            "meter_reading"
        ]
        .mean()
        .reset_index()
    )

    fig_hour = px.bar(
        hourly_data,
        x="hour",
        y="meter_reading",
        title="Average Energy Consumption by Hour"
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )


# ==================================================
# ENERGY AGENT PAGE
# ==================================================

def energy_agent_page(df):

    st.markdown(
        '<div class="main-title">'
        '🤖 Energy Agent'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered analysis of energy patterns and facility consumption'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # CALCULATE ANALYSIS
    # --------------------------------------------------

    mean_energy = df[
        "meter_reading"
    ].mean()

    std_energy = df[
        "meter_reading"
    ].std()

    high_energy_threshold = (
        mean_energy + std_energy
    )

    high_energy_events = df[
        df["meter_reading"]
        > high_energy_threshold
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "High Energy Threshold",
        f"{high_energy_threshold:,.2f}"
    )

    col2.metric(
        "High Energy Events",
        len(high_energy_events)
    )

    st.divider()

    # --------------------------------------------------
    # AI RECOMMENDATION
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '⚠️ AI Recommendation'
        '</div>',
        unsafe_allow_html=True
    )

    peak_hour_data = (
        df.groupby("hour")[
            "meter_reading"
        ]
        .mean()
    )

    peak_hour = peak_hour_data.idxmax()

    st.warning(
        "High energy consumption patterns were detected."
    )

    st.info(
        f"💡 Recommendation: Investigate HVAC, "
        f"lighting and equipment usage around "
        f"{peak_hour}:00, which shows the highest "
        f"average energy demand."
    )

    st.divider()

    # --------------------------------------------------
    # HIGH ENERGY EVENTS
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📊 High Energy Events'
        '</div>',
        unsafe_allow_html=True
    )

    columns_to_display = [
        "building_id",
        "timestamp",
        "meter_reading",
        "air_temperature"
    ]

    available_columns = [
        col
        for col in columns_to_display
        if col in high_energy_events.columns
    ]

    st.dataframe(
        high_energy_events[
            available_columns
        ].head(100),
        use_container_width=True
    )


# ==================================================
# ANOMALY ANALYTICS PAGE
# ==================================================

def anomaly_page(df):

    st.markdown(
        '<div class="main-title">'
        '📊 Anomaly Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Detection of abnormal energy consumption patterns'
        '</div>',
        unsafe_allow_html=True
    )

    mean_energy = df[
        "meter_reading"
    ].mean()

    std_energy = df[
        "meter_reading"
    ].std()

    anomaly_threshold = (
        mean_energy + 2 * std_energy
    )

    anomalies = df[
        df["meter_reading"]
        > anomaly_threshold
    ].copy()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Records",
        f"{len(df):,}"
    )

    col2.metric(
        "Anomalies Detected",
        f"{len(anomalies):,}"
    )

    col3.metric(
        "Anomaly Threshold",
        f"{anomaly_threshold:,.2f}"
    )

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '🚨 Detected Anomalies'
        '</div>',
        unsafe_allow_html=True
    )

    if len(anomalies) > 0:

        anomaly_chart_data = (
            anomalies.tail(1000)
        )

        fig = px.scatter(
            anomaly_chart_data,
            x="timestamp",
            y="meter_reading",
            color="building_id",
            title="Energy Consumption Anomalies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            anomalies.head(100),
            use_container_width=True
        )

    else:

        st.success(
            "No significant anomalies detected."
        )


# ==================================================
# MAIN APPLICATION
# ==================================================

def main():

    # ----------------------------------------------
    # LOGIN CHECK
    # ----------------------------------------------

    if not st.session_state.logged_in:

        login_page()

        return

    # ----------------------------------------------
    # LOAD DATA AFTER LOGIN
    # ----------------------------------------------

    with st.spinner(
        "Loading facility energy data..."
    ):

        df = load_energy_data()

    # ----------------------------------------------
    # SIDEBAR
    # ----------------------------------------------

    page, selected_building = sidebar(
        df
    )

    # ----------------------------------------------
    # FILTER DATA
    # ----------------------------------------------

    filtered_df = filter_data(
        df,
        selected_building
    )

    # ----------------------------------------------
    # ROUTING
    # ----------------------------------------------

    if page == "⚡ Energy Dashboard":

        energy_dashboard(
            filtered_df
        )

    elif page == "🤖 Energy Agent":

        energy_agent_page(
            filtered_df
        )

    elif page == "📊 Anomaly Analytics":

        anomaly_page(
            filtered_df
        )


# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":

    main()