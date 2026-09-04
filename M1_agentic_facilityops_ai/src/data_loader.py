import pandas as pd


class DataLoader:

    def __init__(self, data_path):

        self.data_path = data_path


    def load_data(self):

        print("Loading Energy Agent dataset...")

        df = pd.read_csv(
            self.data_path
        )

        # Convert timestamp
        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        # Sort data
        df = df.sort_values(
            ["building_id", "timestamp"]
        )

        print(
            f"Dataset loaded successfully: "
            f"{df.shape}"
        )

        return df


    def get_building_data(
        self,
        df,
        building_id
    ):

        building_df = df[
            df["building_id"] == building_id
        ].copy()

        return building_df