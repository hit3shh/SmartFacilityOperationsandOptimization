import pandas as pd


class EnergyAnalytics:

    def calculate_summary(self, df):
        """
        Calculate overall energy consumption metrics.
        """

        total_energy = df["meter_reading"].sum()

        average_energy = df["meter_reading"].mean()

        peak_energy = df["meter_reading"].max()

        return {
            "total_energy": total_energy,
            "average_energy": average_energy,
            "peak_energy": peak_energy
        }


    def hourly_consumption(self, df):
        """
        Calculate average energy consumption by hour.
        """

        hourly_data = (
            df.groupby("hour")["meter_reading"]
            .mean()
            .reset_index()
        )

        return hourly_data


    def daily_consumption(self, df):
        """
        Calculate total energy consumption per day.
        """

        data = df.copy()

        data["date"] = data["timestamp"].dt.date

        daily_data = (
            data.groupby("date")["meter_reading"]
            .sum()
            .reset_index()
        )

        return daily_data


    def building_consumption(self, df):
        """
        Calculate total energy consumption for each building.
        """

        building_data = (
            df.groupby("building_id")["meter_reading"]
            .sum()
            .reset_index()
            .sort_values(
                by="meter_reading",
                ascending=False
            )
        )

        return building_data


    def peak_usage_period(self, df):
        """
        Identify the hour with the highest average energy consumption.
        """

        hourly_data = self.hourly_consumption(df)

        peak_row = hourly_data.loc[
            hourly_data["meter_reading"].idxmax()
        ]

        return {
            "peak_hour": int(peak_row["hour"]),
            "average_energy": peak_row["meter_reading"]
        }