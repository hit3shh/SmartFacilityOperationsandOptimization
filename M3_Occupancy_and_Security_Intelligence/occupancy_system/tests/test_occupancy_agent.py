"""
Tests for the Occupancy Agent.
"""

import sys
from pathlib import Path

import pandas as pd


# -------------------------------------------------------------------
# Make src/ importable
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))


from occupancy_agent import OccupancyAgent


# -------------------------------------------------------------------
# Test fixture
# -------------------------------------------------------------------

def create_test_dataframe():
    """
    Create a small synthetic occupancy dataset for testing.
    """

    timestamps = pd.date_range(
        start="2024-01-01 09:00:00",
        periods=12,
        freq="30s"
    )

    occupancy = [
        0, 0, 0, 0,
        1, 1,
        2, 2,
        3, 3, 3, 3
    ]

    dataframe = pd.DataFrame({
        "Date": timestamps.strftime("%Y-%m-%d"),
        "Time": timestamps.strftime("%H:%M:%S"),
        "Room_Occupancy_Count": occupancy,

        "S1_Temp": [20.0] * 12,
        "S2_Temp": [20.5] * 12,
        "S3_Temp": [21.0] * 12,
        "S4_Temp": [20.5] * 12,

        "S1_Light": [100.0] * 12,
        "S2_Light": [100.0] * 12,
        "S3_Light": [100.0] * 12,
        "S4_Light": [100.0] * 12,

        "S1_Sound": [30.0] * 12,
        "S2_Sound": [30.0] * 12,
        "S3_Sound": [30.0] * 12,
        "S4_Sound": [30.0] * 12,

        "S5_CO2": [500.0] * 12,
        "S5_CO2_Slope": [0.0] * 12,

        "S6_PIR": [1] * 12,
        "S7_PIR": [1] * 12,
    })

    return dataframe


# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------

def test_agent_initialization():
    """
    Verify that the Occupancy Agent initializes correctly.
    """

    agent = OccupancyAgent()

    assert agent.agent_name == "Occupancy Agent"


def test_occupancy_status():
    """
    Verify VACANT/OCCUPIED classification.
    """

    agent = OccupancyAgent()

    assert agent.get_occupancy_status(0) == "VACANT"
    assert agent.get_occupancy_status(1) == "OCCUPIED"
    assert agent.get_occupancy_status(3) == "OCCUPIED"


def test_current_occupancy():
    """
    Verify retrieval of the latest occupancy count.
    """

    agent = OccupancyAgent()
    dataframe = create_test_dataframe()

    result = agent.get_current_occupancy(dataframe)

    assert result == 3


def test_occupancy_rate():
    """
    Verify percentage of observations where the room was occupied.
    """

    agent = OccupancyAgent()
    dataframe = create_test_dataframe()

    result = agent.calculate_occupancy_rate(dataframe)

    assert round(result, 2) == 66.67


def test_average_occupancy():
    """
    Verify average occupancy calculation.
    """

    agent = OccupancyAgent()
    dataframe = create_test_dataframe()

    result = agent.calculate_average_occupancy(dataframe)

    assert round(result, 2) == 1.5


def test_maximum_occupancy():
    """
    Verify maximum occupancy calculation.
    """

    agent = OccupancyAgent()
    dataframe = create_test_dataframe()

    result = agent.calculate_max_occupancy(dataframe)

    assert result == 3


def test_complete_analysis():
    """
    Verify the complete Occupancy Agent analysis pipeline.
    """

    agent = OccupancyAgent()
    dataframe = create_test_dataframe()

    result = agent.analyze(dataframe)

    assert result["agent"] == "Occupancy Agent"
    assert result["current_occupancy"] == 3
    assert result["current_status"] == "OCCUPIED"

    assert "occupancy_rate_percent" in result
    assert "average_occupancy" in result
    assert "maximum_occupancy" in result
    assert "forecast" in result

    forecast = result["forecast"]

    assert "timestamp" in forecast
    assert "current_occupancy" in forecast
    assert "predicted_next_occupancy" in forecast
    assert "forecast_horizon" in forecast

    assert forecast["current_occupancy"] == 3
    assert forecast["forecast_horizon"] == "30 seconds"

    assert isinstance(
        forecast["predicted_next_occupancy"],
        int
    )

    assert forecast["predicted_next_occupancy"] >= 0

    