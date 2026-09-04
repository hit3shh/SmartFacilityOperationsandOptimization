import joblib
import pandas as pd


class MaintenancePredictor:

    def __init__(
        self,
        model_path
    ):

        self.model = joblib.load(
            model_path
        )


    def prepare_features(
        self,
        machine_data
    ):

        features = pd.DataFrame([{
            "Air temperature [K]": machine_data[
                "Air temperature [K]"
            ],

            "Process temperature [K]": machine_data[
                "Process temperature [K]"
            ],

            "Rotational speed [rpm]": machine_data[
                "Rotational speed [rpm]"
            ],

            "Torque [Nm]": machine_data[
                "Torque [Nm]"
            ],

            "Tool wear [min]": machine_data[
                "Tool wear [min]"
            ],

            "Type_L": int(
                machine_data["Type"] == "L"
            ),

            "Type_M": int(
                machine_data["Type"] == "M"
            )
        }])

        return features


    def predict_failure(
        self,
        machine_data
    ):

        features = self.prepare_features(
            machine_data
        )

        prediction = self.model.predict(
            features
        )[0]

        probability = self.model.predict_proba(
            features
        )[0][1]

        return {
            "failure_prediction": int(
                prediction
            ),
            "failure_probability": round(
                probability * 100,
                2
            )
        }