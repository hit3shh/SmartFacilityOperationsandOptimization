class MaintenanceAlerts:

    def generate_alert(
        self,
        health_score,
        health_status,
        prediction_result
    ):

        failure_prediction = (
            prediction_result[
                "failure_prediction"
            ]
        )

        failure_probability = (
            prediction_result[
                "failure_probability"
            ]
        )


        # Critical risk
        if (
            failure_prediction == 1
            or failure_probability >= 70
            or health_score <= 40
        ):

            return {
                "risk_level": "Critical",
                "message": (
                    "High probability of machine failure "
                    "or critical machine health condition detected."
                ),
                "recommendation": (
                    "Schedule immediate maintenance inspection "
                    "and check the machine before continued operation."
                )
            }


        # High risk
        elif (
            failure_probability >= 40
            or health_score <= 60
        ):

            return {
                "risk_level": "High",
                "message": (
                    "Machine is showing signs of increased "
                    "failure risk."
                ),
                "recommendation": (
                    "Schedule preventive maintenance and "
                    "inspect major operating components."
                )
            }


        # Medium risk
        elif (
            failure_probability >= 15
            or health_score <= 80
        ):

            return {
                "risk_level": "Medium",
                "message": (
                    "Machine condition requires monitoring."
                ),
                "recommendation": (
                    "Continue monitoring sensor readings and "
                    "plan maintenance if conditions worsen."
                )
            }


        # Low risk
        else:

            return {
                "risk_level": "Low",
                "message": (
                    "Machine is operating within normal conditions."
                ),
                "recommendation": (
                    "No immediate maintenance action is required. "
                    "Continue regular monitoring."
                )
            }