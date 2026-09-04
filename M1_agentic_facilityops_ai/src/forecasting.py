import pandas as pd

from sklearn.ensemble import RandomForestRegressor


class EnergyForecaster:

    def __init__(self):

        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )


    def prepare_hourly_data(self, df):
        """
        Aggregate energy consumption
        across all buildings by timestamp.
        """

        hourly_data = (
            df.groupby("timestamp")[
                "meter_reading"
            ]
            .sum()
            .reset_index()
        )

        hourly_data = hourly_data.sort_values(
            "timestamp"
        )

        return hourly_data


    def create_features(self, df):

        data = df.copy()

        data["hour"] = (
            data["timestamp"].dt.hour
        )

        data["day_of_week"] = (
            data["timestamp"].dt.dayofweek
        )

        data["month"] = (
            data["timestamp"].dt.month
        )

        data["day"] = (
            data["timestamp"].dt.day
        )

        return data


    def train(self, df):

        hourly_data = (
            self.prepare_hourly_data(df)
        )

        data = self.create_features(
            hourly_data
        )

        features = data[
            [
                "hour",
                "day_of_week",
                "month",
                "day"
            ]
        ]

        target = data[
            "meter_reading"
        ]

        self.model.fit(
            features,
            target
        )


    def forecast(self, df, periods=24):

        hourly_data = (
            self.prepare_hourly_data(df)
        )

        last_timestamp = (
            hourly_data["timestamp"].max()
        )

        future_timestamps = (
            pd.date_range(
                start=last_timestamp
                + pd.Timedelta(hours=1),
                periods=periods,
                freq="h"
            )
        )

        future_df = pd.DataFrame({
            "timestamp":
            future_timestamps
        })

        future_features = (
            self.create_features(
                future_df
            )
        )

        X_future = future_features[
            [
                "hour",
                "day_of_week",
                "month",
                "day"
            ]
        ]

        predictions = (
            self.model.predict(
                X_future
            )
        )

        future_df[
            "predicted_energy"
        ] = predictions

        return future_df