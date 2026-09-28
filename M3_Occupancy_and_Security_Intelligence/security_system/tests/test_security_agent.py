"""
Tests for SecurityAgent.
"""

import sys
from pathlib import Path

import pytest

# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parents[1] / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from security_agent import SecurityAgent


@pytest.fixture
def agent():
    """Create a SecurityAgent instance."""
    return SecurityAgent()


def test_agent_loads(agent):
    """Test that the Security Agent loads successfully."""

    assert agent.detector is not None
    assert len(agent.agent_profiles) == 67
    assert len(agent.transition_frequency_map) == 84


def test_agent_analyzes_event(agent):
    """Test that the agent can analyze a security event."""

    event = {
        "log_id": "test_000001",
        "timestamp": "2026-01-05T10:00:00",
        "user_id": "human_operator_01",
        "agent_type": "human",
        "action": "read_sensor",
        "resource": "sensor_force_a1",
        "location": "zone_assembly_a",
        "previous_action": "read_database",
        "human_present": True,
        "emergency_flag": False,
    }

    result = agent.analyze_event(event)

    assert "risk_score" in result
    assert "is_anomaly" in result
    assert "severity" in result
    assert "reasons" in result
    assert "features" in result

    assert 0.0 <= result["risk_score"] <= 1.0
    assert isinstance(result["is_anomaly"], bool)


def test_agent_detects_known_anomaly(agent):
    """Test the agent using a known anomalous security pattern."""

    event = {
        "log_id": "test_anomaly_000001",
        "timestamp": "2026-01-19T03:00:01",
        "user_id": "human_operator_10",
        "agent_type": "human",
        "action": "read_database",
        "resource": "database_quality_control",
        "location": "zone_server_room",
        "previous_action": "read_sensor",
        "human_present": True,
        "emergency_flag": False,
    }

    result = agent.analyze_event(event)

    assert result["risk_score"] >= 0.9
    assert result["is_anomaly"] is True
    assert result["severity"] in ["MEDIUM", "HIGH"]


def test_alert_history(agent):
    """Test that detected anomalies are stored in alert history."""

    event = {
        "log_id": "test_anomaly_000002",
        "timestamp": "2026-01-19T03:00:01",
        "user_id": "human_operator_10",
        "agent_type": "human",
        "action": "read_database",
        "resource": "database_quality_control",
        "location": "zone_server_room",
        "previous_action": "read_sensor",
        "human_present": True,
        "emergency_flag": False,
    }

    result = agent.analyze_event(event)

    alerts = agent.get_alert_history()

    if result["is_anomaly"]:
        assert len(alerts) >= 1
        assert alerts[-1]["log_id"] == "test_anomaly_000002"


def test_clear_alert_history(agent):
    """Test clearing the alert history."""

    agent.alert_history.append({"log_id": "test_alert"})

    assert len(agent.get_alert_history()) == 1

    agent.clear_alert_history()

    assert len(agent.get_alert_history()) == 0