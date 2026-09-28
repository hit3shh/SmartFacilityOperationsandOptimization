"""
Occupancy Agent

Provides occupancy status, occupancy analytics, and
next-step occupancy forecasting for the Smart Facility
Operations system.
"""

import pandas as pd

from occupancy_forecasting import (
    forecast_with_details,
)


class OccupancyAgent:
    """
    Agent responsible for occupancy intelligence.

    Responsibilities:
    - Analyze current occupancy
    - Determine occupancy status
    - Calculate basic occupancy KPIs
    - Forecast next-step occupancy
    """

    def __init__(self):
        """Initialize the Occupancy Agent."""
        self.agent_name = "Occupancy Agent"

    # ----------------------------------------------------------------
    # Current occupancy
    # ----------------------------------------------------------------

    def get_current_occupancy(self, dataframe):
        """
        Return the latest observed occupancy count.
        """

        if dataframe.empty:
            raise ValueError(
                "Cannot analyze an empty occupancy dataset."
            )

        return int(
            dataframe["Room_Occupancy_Count"].iloc[-1]
        )

    # ----------------------------------------------------------------
    # Occupancy status
    # ----------------------------------------------------------------

    def get_occupancy_status(self, occupancy_count):
        """
        Convert occupancy count into an operational status.
        """

        if occupancy_count <= 0:
            return "VACANT"

        return "OCCUPIED"

    # ----------------------------------------------------------------
    # Occupancy rate
    # ----------------------------------------------------------------

    def calculate_occupancy_rate(self, dataframe):
        """
        Calculate the percentage of observations where
        the room was occupied.
        """

        if dataframe.empty:
            raise ValueError(
                "Cannot calculate occupancy rate "
                "from an empty dataset."
            )

        occupied = (
            dataframe["Room_Occupancy_Count"] > 0
        ).sum()

        total = len(dataframe)

        return (occupied / total) * 100

    # ----------------------------------------------------------------
    # Average occupancy
    # ----------------------------------------------------------------

    def calculate_average_occupancy(self, dataframe):
        """
        Calculate average observed occupancy.
        """

        if dataframe.empty:
            raise ValueError(
                "Cannot calculate average occupancy "
                "from an empty dataset."
            )

        return float(
            dataframe["Room_Occupancy_Count"].mean()
        )

    # ----------------------------------------------------------------
    # Maximum occupancy
    # ----------------------------------------------------------------

    def calculate_max_occupancy(self, dataframe):
        """
        Return maximum observed occupancy.
        """

        if dataframe.empty:
            raise ValueError(
                "Cannot calculate maximum occupancy "
                "from an empty dataset."
            )

        return int(
            dataframe["Room_Occupancy_Count"].max()
        )

    # ----------------------------------------------------------------
    # Forecasting
    # ----------------------------------------------------------------

    def forecast_next_occupancy(self, dataframe):
        """
        Forecast occupancy for the next 30-second interval.
        """

        return forecast_with_details(dataframe)

    # ----------------------------------------------------------------
    # Complete analysis
    # ----------------------------------------------------------------

    def analyze(self, dataframe):
        """
        Perform a complete occupancy analysis.

        Returns
        -------
        dict
            Operational occupancy intelligence.
        """

        if dataframe.empty:
            raise ValueError(
                "Cannot analyze an empty occupancy dataset."
            )

        current_occupancy = self.get_current_occupancy(
            dataframe
        )

        status = self.get_occupancy_status(
            current_occupancy
        )

        occupancy_rate = self.calculate_occupancy_rate(
            dataframe
        )

        average_occupancy = (
            self.calculate_average_occupancy(dataframe)
        )

        max_occupancy = self.calculate_max_occupancy(
            dataframe
        )

        forecast = self.forecast_next_occupancy(
            dataframe
        )

        return {
            "agent": self.agent_name,
            "current_occupancy": current_occupancy,
            "current_status": status,
            "occupancy_rate_percent": round(
                occupancy_rate,
                2
            ),
            "average_occupancy": round(
                average_occupancy,
                2
            ),
            "maximum_occupancy": max_occupancy,
            "forecast": forecast,
        }


# --------------------------------------------------------------------
# Simple standalone test
# --------------------------------------------------------------------

if __name__ == "__main__":

    print(
        f"{OccupancyAgent.__name__} module loaded successfully."
    )
    