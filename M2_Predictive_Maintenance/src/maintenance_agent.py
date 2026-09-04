from src.maintenance_analytics import MaintenanceAnalytics
from src.health_scoring import HealthScoring
from src.maintenance_predictor import MaintenancePredictor
from src.maintenance_alerts import MaintenanceAlerts


class MaintenanceAgent:

    def __init__(
        self,
        model_path
    ):

        self.analytics = (
            MaintenanceAnalytics()
        )

        self.health_scoring = (
            HealthScoring()
        )

        self.predictor = (
            MaintenancePredictor(
                model_path
            )
        )

        self.alerts = (
            MaintenanceAlerts()
        )


    def analyze_machine(
        self,
        machine_data
    ):

        # Calculate health score
        health_score = (
            self.health_scoring
            .calculate_health_score(
                machine_data
            )
        )


        # Get health status
        health_status = (
            self.health_scoring
            .get_health_status(
                health_score
            )
        )


        # Predict failure
        prediction_result = (
            self.predictor
            .predict_failure(
                machine_data
            )
        )


        # Generate maintenance alert
        alert_result = (
            self.alerts
            .generate_alert(
                health_score,
                health_status,
                prediction_result
            )
        )


        return {
            "product_id": machine_data[
                "Product ID"
            ],

            "machine_type": machine_data[
                "Type"
            ],

            "health_score": health_score,

            "health_status": health_status,

            "failure_prediction": prediction_result[
                "failure_prediction"
            ],

            "failure_probability": prediction_result[
                "failure_probability"
            ],

            "risk_level": alert_result[
                "risk_level"
            ],

            "message": alert_result[
                "message"
            ],

            "recommendation": alert_result[
                "recommendation"
            ]
        }


    def get_dataset_summary(
        self,
        df
    ):

        return self.analytics.get_summary(
            df
        )


    def get_machine_type_analysis(
        self,
        df
    ):

        return (
            self.analytics
            .get_machine_type_analysis(
                df
            )
        )


    def get_failure_type_analysis(
        self,
        df
    ):

        return (
            self.analytics
            .get_failure_type_analysis(
                df
            )
        )