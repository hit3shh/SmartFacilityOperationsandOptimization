import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class AnomalyDetector:

    def __init__(self, contamination=0.02):

        self.contamination = contamination

        self.scaler = StandardScaler()

        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=42,
            n_estimators=100,
            n_jobs=-1
        )


    def prepare_features(self, df):

        features = df[
            [
                "meter_reading",
                "hour",
                "air_temperature",
                "dew_temperature"
            ]
        ].copy()

        features = features.fillna(
            features.median()
        )

        return features


    def detect(self, df):

        data = df.copy()

        features = self.prepare_features(
            data
        )

        scaled_features = (
            self.scaler.fit_transform(
                features
            )
        )

        predictions = (
            self.model.fit_predict(
                scaled_features
            )
        )

        data["anomaly"] = predictions

        data["is_anomaly"] = (
            data["anomaly"] == -1
        )

        return data


    def get_anomalies(self, df):

        anomaly_df = self.detect(df)

        return anomaly_df[
            anomaly_df["is_anomaly"]
        ]