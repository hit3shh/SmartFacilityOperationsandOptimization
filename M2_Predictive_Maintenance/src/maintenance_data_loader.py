import pandas as pd


class MaintenanceDataLoader:

    def __init__(self, data_path):

        self.data_path = data_path


    def load_data(self):

        print(
            "Loading Predictive Maintenance dataset..."
        )

        df = pd.read_csv(
            self.data_path
        )

        print(
            f"Dataset loaded successfully: {df.shape}"
        )

        return df


    def get_machine_data(
        self,
        df,
        product_id
    ):

        machine_df = df[
            df["Product ID"] == product_id
        ].copy()

        return machine_df