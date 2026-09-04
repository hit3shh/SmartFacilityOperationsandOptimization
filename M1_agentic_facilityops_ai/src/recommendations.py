class RecommendationEngine:

    def generate_recommendations(
        self,
        df,
        summary,
        anomaly_count,
        forecast_df,
        peak_usage
    ):

        recommendations = []


        # ----------------------------------
        # 1. ANOMALY RECOMMENDATION
        # ----------------------------------

        if anomaly_count > 0:

            anomaly_percentage = (
                anomaly_count / len(df)
            ) * 100


            if anomaly_percentage >= 2:

                recommendations.append({
                    "priority": "High",
                    "category": "Energy Anomaly",
                    "message": (
                        f"{anomaly_count} unusual energy "
                        f"consumption events were detected "
                        f"({anomaly_percentage:.2f}% of records). "
                        "Inspect HVAC systems, electrical equipment, "
                        "and unexpected load patterns."
                    )
                })


        # ----------------------------------
        # 2. NIGHT-TIME ENERGY WASTAGE
        # ----------------------------------

        night_data = df[
            (df["hour"] < 6)
            | (df["hour"] >= 22)
        ]


        night_consumption = (
            night_data["meter_reading"]
            .mean()
        )


        average_consumption = (
            summary["average_energy"]
        )


        if night_consumption > (
            average_consumption * 0.80
        ):

            recommendations.append({
                "priority": "Medium",
                "category": "Night Energy Usage",
                "message": (
                    "Energy consumption remains relatively high "
                    "during non-working hours. Consider optimizing "
                    "lighting schedules, HVAC operation, and "
                    "standby equipment."
                )
            })


        # ----------------------------------
        # 3. PEAK USAGE RECOMMENDATION
        # ----------------------------------

        recommendations.append({
            "priority": "Medium",
            "category": "Peak Demand",
            "message": (
                f"Peak energy usage occurs around "
                f"{peak_usage['peak_hour']:02d}:00. "
                "Consider load shifting or scheduling "
                "non-critical operations outside peak hours."
            )
        })


        # ----------------------------------
        # 4. FORECAST RECOMMENDATION
        # ----------------------------------

        forecast_peak = (
            forecast_df[
                "predicted_energy"
            ].max()
        )


        forecast_average = (
            forecast_df[
                "predicted_energy"
            ].mean()
        )


        if forecast_peak > (
            forecast_average * 1.10
        ):

            recommendations.append({
                "priority": "Medium",
                "category": "Forecast Alert",
                "message": (
                    f"Forecasted energy demand may reach "
                    f"{forecast_peak:.2f}. Prepare facility "
                    "systems for increased demand and review "
                    "peak-load management strategies."
                )
            })


        # ----------------------------------
        # 5. DEFAULT RECOMMENDATION
        # ----------------------------------

        if not recommendations:

            recommendations.append({
                "priority": "Low",
                "category": "Monitoring",
                "message": (
                    "Energy consumption appears stable. "
                    "Continue monitoring energy usage and "
                    "review periodic efficiency trends."
                )
            })


        return recommendations