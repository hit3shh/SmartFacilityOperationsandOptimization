class HealthScoring:

    def calculate_health_score(
        self,
        machine_data
    ):

        score = 100


        # Tool wear
        tool_wear = machine_data[
            "Tool wear [min]"
        ]

        if tool_wear > 200:
            score -= 30

        elif tool_wear > 150:
            score -= 20

        elif tool_wear > 100:
            score -= 10


        # Torque
        torque = machine_data[
            "Torque [Nm]"
        ]

        if torque > 60:
            score -= 20

        elif torque > 50:
            score -= 10


        # Process temperature
        process_temp = machine_data[
            "Process temperature [K]"
        ]

        if process_temp > 315:
            score -= 15


        # Rotational speed
        rotational_speed = machine_data[
            "Rotational speed [rpm]"
        ]

        if rotational_speed > 2200:
            score -= 15


        # Ensure score stays between 0 and 100
        score = max(
            0,
            min(
                score,
                100
            )
        )

        return score


    def get_health_status(
        self,
        score
    ):

        if score >= 81:
            return "Healthy"

        elif score >= 61:
            return "Warning"

        elif score >= 41:
            return "Poor"

        else:
            return "Critical"