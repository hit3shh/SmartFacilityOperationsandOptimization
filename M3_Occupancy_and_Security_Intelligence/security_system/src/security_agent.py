"""
Security Agent

Processes security access events, engineers behavioral/security
features, and uses the trained SecurityDetector to generate
risk assessments and security alerts.
"""

import json
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path

from security_detector import SecurityDetector


class SecurityAgent:
    """Agent for security event monitoring and anomaly detection."""

    def __init__(
        self,
        detector=None,
        profiles_path=None,
        transition_frequency_path=None
    ):
        base_dir = Path(__file__).resolve().parents[1]

        # Load detector
        self.detector = detector or SecurityDetector()

        # Default paths
        if profiles_path is None:
            profiles_path = (
                base_dir
                / "data"
                / "raw"
                / "agent_profiles.json"
            )

        if transition_frequency_path is None:
            transition_frequency_path = (
                base_dir
                / "models"
                / "security_transition_frequency.json"
            )

        self.profiles_path = Path(profiles_path)
        self.transition_frequency_path = Path(
            transition_frequency_path
        )

        # Load agent profiles
        with open(self.profiles_path, "r") as file:
            self.agent_profiles = json.load(file)

        # Authorization map
        self.authorization_map = {
            profile["entity_id"]: set(
                profile.get("authorized_resources", [])
            )
            for profile in self.agent_profiles
        }

        # Home-zone map
        self.home_zone_map = {
            profile["entity_id"]: profile.get("home_zone")
            for profile in self.agent_profiles
        }

        # Load training transition frequencies
        with open(
            self.transition_frequency_path, "r"
        ) as file:
            self.transition_frequency_map = json.load(file)

        # Maintain recent event timestamps per user
        self.user_event_history = defaultdict(deque)

        # Store generated alerts
        self.alert_history = []

    def _events_last_5min(self, user_id, timestamp):
        """Count recent events for a user within five minutes."""

        history = self.user_event_history[user_id]

        cutoff = timestamp - timedelta(minutes=5)

        while history and history[0] < cutoff:
            history.popleft()

        history.append(timestamp)

        return len(history)

    def _build_features(self, event):
        """Build model features from a raw security event."""

        timestamp = event["timestamp"]

        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        user_id = event["user_id"]
        resource = event["resource"]
        location = event["location"]
        action = event["action"]

        # Recent activity
        events_last_5min = self._events_last_5min(
            user_id,
            timestamp
        )

        # Authorization check
        authorized_resources = self.authorization_map.get(
            user_id,
            set()
        )

        authorization_mismatch = (
            resource not in authorized_resources
        )

        # Home-zone check
        home_zone = self.home_zone_map.get(user_id)

        if home_zone is None:
            home_zone_mismatch = False
        else:
            home_zone_mismatch = (
                home_zone != location
            )

        # Off-hours
        hour = timestamp.hour

        is_off_hours = (
            hour < 6 or hour >= 22
        )

        # Action transition
        previous_action = event.get(
            "previous_action",
            "NONE"
        )

        action_transition = (
            str(previous_action)
            + " -> "
            + str(action)
        )

        transition_count = int(
            self.transition_frequency_map.get(
                action_transition,
                0
            )
        )

        transition_log_frequency = (
            __import__("math").log1p(
                transition_count
            )
        )

        transition_is_rare = (
            transition_count <= 10
        )

        return {
            "events_last_5min": events_last_5min,
            "authorization_mismatch": authorization_mismatch,
            "home_zone_mismatch": home_zone_mismatch,
            "is_off_hours": is_off_hours,
            "transition_log_frequency_train":
                transition_log_frequency,
            "transition_is_rare_train":
                transition_is_rare,
            "human_present": bool(
                event.get("human_present", False)
            ),
            "emergency_flag": bool(
                event.get("emergency_flag", False)
            )
        }

    def _generate_reasons(self, features):
        """Generate human-readable reasons for an alert."""

        reasons = []

        if features["authorization_mismatch"]:
            reasons.append(
                "Unauthorized resource access"
            )

        if features["home_zone_mismatch"]:
            reasons.append(
                "Access outside home zone"
            )

        if features["is_off_hours"]:
            reasons.append(
                "Off-hours activity"
            )

        if features["transition_is_rare_train"]:
            reasons.append(
                "Rare action transition"
            )

        if features["events_last_5min"] >= 5:
            reasons.append(
                "High recent activity frequency"
            )

        if features["emergency_flag"]:
            reasons.append(
                "Emergency flag active"
            )

        return reasons

    def _determine_severity(self, features, result):
        """Determine operational alert severity."""

        if not result["is_anomaly"]:
            return "NORMAL"

        if (
            features["authorization_mismatch"]
            or features["emergency_flag"]
        ):
            return "HIGH"

        if features["is_off_hours"]:
            return "MEDIUM"

        return "MEDIUM"

    def analyze_event(self, event):
        """
        Analyze a single security event.

        Returns a security assessment containing
        risk score, anomaly status, features and alert details.
        """

        features = self._build_features(event)

        result = self.detector.predict(features)

        reasons = self._generate_reasons(features)

        severity = self._determine_severity(
            features,
            result
        )

        assessment = {
            "log_id": event.get("log_id"),
            "timestamp": event.get("timestamp"),
            "user_id": event.get("user_id"),
            "agent_type": event.get("agent_type"),
            "action": event.get("action"),
            "resource": event.get("resource"),
            "location": event.get("location"),
            "risk_score": result["risk_score"],
            "is_anomaly": result["is_anomaly"],
            "threshold": result["threshold"],
            "severity": severity,
            "reasons": reasons,
            "features": features
        }

        if result["is_anomaly"]:
            self.alert_history.append(assessment)

        return assessment

    def get_alert_history(self):
        """Return all generated security alerts."""

        return list(self.alert_history)

    def clear_alert_history(self):
        """Clear stored security alerts."""

        self.alert_history.clear()