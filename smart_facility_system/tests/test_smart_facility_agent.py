import sys
from pathlib import Path


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
# DATA PATH
# ==================================================

MAINTENANCE_MODEL_PATH = (
    SPRINGBOARD_PATH
    / "M2_Predictive_Maintenance"
    / "models"
    / "maintenance_failure_model.pkl"
)


# ==================================================
# CREATE AGENT
# ==================================================

def create_agent():

    return SmartFacilityAgent(
        maintenance_model_path=
        str(MAINTENANCE_MODEL_PATH)
    )


# ==================================================
# PYTEST TESTS
# ==================================================

def test_smart_facility_agent_initialization():

    agent = create_agent()

    assert agent is not None

    assert hasattr(
        agent,
        "energy_agent"
    )

    assert hasattr(
        agent,
        "maintenance_agent"
    )


def test_smart_facility_agent_methods():

    agent = create_agent()

    assert callable(
        agent.run_energy_analysis
    )

    assert callable(
        agent.analyze_machine
    )

    assert callable(
        agent.get_maintenance_summary
    )

    assert callable(
        agent.generate_facility_insight
    )

    assert callable(
        agent.run_complete_analysis
    )


def test_facility_insight_generation():

    agent = create_agent()

    # Lightweight mock results representing
    # the output structure expected by the agent.

    energy_results = {

        "summary": {

            "total_energy": 1000.0

        },

        "peak_usage": {

            "peak_hour": 14

        },

        "anomaly_count": 5

    }


    maintenance_result = {

        "product_id": "TestMachine",

        "risk_level": "Low"

    }


    result = (
        agent.generate_facility_insight(
            energy_results,
            maintenance_result
        )
    )


    assert isinstance(
        result,
        dict
    )

    assert "facility_priority" in result

    assert "insights" in result

    assert "combined_recommendation" in result

    assert isinstance(
        result["insights"],
        list
    )

    assert len(
        result["insights"]
    ) > 0


# ==================================================
# OCCUPANCY INTEGRATION TEST
# ==================================================

def test_occupancy_analysis_integration(
    monkeypatch
):

    import pandas as pd
    import occupancy_agent


    # Replace the expensive forecasting call
    # used by OccupancyAgent.
    def mock_forecast_with_details(dataframe):

        return {
            "timestamp": "test_timestamp",
            "current_occupancy": int(
                dataframe[
                    "Room_Occupancy_Count"
                ].iloc[-1]
            ),
            "predicted_next_occupancy": 1,
            "forecast_horizon": "30 seconds"
        }


    monkeypatch.setattr(
        occupancy_agent,
        "forecast_with_details",
        mock_forecast_with_details
    )


    # Create unified agent
    agent = create_agent()


    # Small test dataset
    occupancy_df = pd.DataFrame({

        "Room_Occupancy_Count": [
            0,
            1,
            1
        ]

    })


    # Run through the unified agent
    result = (
        agent.run_occupancy_analysis(
            occupancy_df
        )
    )


    # ----------------------------------------------
    # RESULT CHECKS
    # ----------------------------------------------

    assert isinstance(
        result,
        dict
    )

    assert result["agent"] == (
        "Occupancy Agent"
    )

    assert result["current_occupancy"] == 1

    assert result["current_status"] == (
        "OCCUPIED"
    )

    assert result["occupancy_rate_percent"] == (
        66.67
    )

    assert result["average_occupancy"] == (
        0.67
    )

    assert result["maximum_occupancy"] == 1

    assert "forecast" in result

    assert (
        result["forecast"]
        ["predicted_next_occupancy"]
        == 1
    )

# ==================================================
# SECURITY INTEGRATION TEST
# ==================================================

def test_security_analysis_integration():

    # Create unified agent
    agent = create_agent()

    # Simple security event
    event = {
        "log_id": "TEST-001",
        "timestamp": "2026-01-19 03:00:01",
        "session_id": "test-session",
        "user_id": "human_operator_10",
        "agent_type": "human",
        "action": "READ",
        "resource": "database_quality_control",
        "resource_type": "database",
        "human_present": 1,
        "emergency_flag": 0,
        "location": "server_room",
        "previous_action": "LOGIN",
        "production_state": "RUNNING",
        "shift_id": "night",
        "correlation_id": None,
    }

    # Run through unified agent
    result = agent.analyze_security_event(event)

    # ----------------------------------------------
    # RESULT CHECKS
    # ----------------------------------------------

    assert isinstance(
        result,
        dict
    )

    assert result["log_id"] == "TEST-001"

    assert result["user_id"] == (
        "human_operator_10"
    )

    assert "risk_score" in result

    assert "is_anomaly" in result

    assert "severity" in result

    assert "reasons" in result

    assert isinstance(
        result["reasons"],
        list
    )


