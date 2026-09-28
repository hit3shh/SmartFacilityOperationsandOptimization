"""
Security Anomaly Detector

Loads the trained Random Forest model and provides
anomaly-risk predictions for security events.
"""

import json
from pathlib import Path

import joblib
import pandas as pd


class SecurityDetector:
    """Detect anomalous security events using the trained model."""

    def __init__(self, model_path=None, metadata_path=None):
        base_dir = Path(__file__).resolve().parents[1]

        if model_path is None:
            model_path = (
                base_dir
                / "models"
                / "security_anomaly_random_forest.joblib"
            )

        if metadata_path is None:
            metadata_path = (
                base_dir
                / "models"
                / "security_model_metadata.json"
            )

        self.model_path = Path(model_path)
        self.metadata_path = Path(metadata_path)

        self.model = joblib.load(self.model_path)

        with open(self.metadata_path, "r") as file:
            self.metadata = json.load(file)

        self.threshold = self.metadata["threshold"]
        self.features = self.metadata["features"]

    def predict(self, features):
        """
        Predict whether a security event is anomalous.

        Parameters
        ----------
        features : dict
            Dictionary containing the trained model features.

        Returns
        -------
        dict
            Prediction result containing risk score and alert status.
        """

        feature_data = {
            feature: features.get(feature, 0)
            for feature in self.features
        }

        input_df = pd.DataFrame([feature_data])

        probability = float(
            self.model.predict_proba(input_df)[0][1]
        )

        is_anomaly = probability >= self.threshold

        return {
            "risk_score": probability,
            "is_anomaly": is_anomaly,
            "threshold": self.threshold
        }