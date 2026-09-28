"""
Tests for SecurityDetector.
"""

import sys
from pathlib import Path

import pytest

# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parents[1] / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from security_detector import SecurityDetector


@pytest.fixture
def detector():
    """Create a SecurityDetector instance."""
    return SecurityDetector()


def test_detector_loads(detector):
    """Test that the trained detector loads successfully."""

    assert detector.model is not None
    assert detector.threshold == 0.9
    assert len(detector.features) == 8


def test_detector_prediction_structure(detector):
    """Test the structure of a prediction result."""

    features = {
        "events_last_5min": 1,
        "authorization_mismatch": False,
        "home_zone_mismatch": False,
        "is_off_hours": False,
        "transition_log_frequency_train": 8.0,
        "transition_is_rare_train": False,
        "human_present": False,
        "emergency_flag": False,
    }

    result = detector.predict(features)

    assert "risk_score" in result
    assert "is_anomaly" in result
    assert "threshold" in result

    assert 0.0 <= result["risk_score"] <= 1.0
    assert isinstance(result["is_anomaly"], bool)
    assert result["threshold"] == 0.9


def test_detector_handles_missing_features(detector):
    """Test that missing features receive default values."""

    result = detector.predict({})

    assert "risk_score" in result
    assert "is_anomaly" in result
    assert 0.0 <= result["risk_score"] <= 1.0