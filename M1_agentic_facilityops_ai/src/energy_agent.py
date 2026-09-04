from src.analytics import EnergyAnalytics
from src.anomaly_detector import AnomalyDetector
from src.forecasting import EnergyForecaster
from src.recommendations import RecommendationEngine


class EnergyAgent:

    def __init__(self):

        self.analytics = EnergyAnalytics()

        self.anomaly_detector = AnomalyDetector()

        self.forecaster = EnergyForecaster()

        self.recommendation_engine = (
            RecommendationEngine()
        )


    def run_analysis(self, df):

        print("Energy Agent started...")


        # -----------------------------
        # ENERGY ANALYTICS
        # -----------------------------

        summary = (
            self.analytics.calculate_summary(df)
        )

        hourly_consumption = (
            self.analytics.hourly_consumption(df)
        )

        daily_consumption = (
            self.analytics.daily_consumption(df)
        )

        building_consumption = (
            self.analytics.building_consumption(df)
        )

        peak_usage = (
            self.analytics.peak_usage_period(df)
        )


        # -----------------------------
        # ANOMALY DETECTION
        # -----------------------------

        anomaly_result = (
            self.anomaly_detector.detect(df)
        )

        anomaly_count = (
            anomaly_result["is_anomaly"]
            .sum()
        )


        # -----------------------------
        # FORECASTING
        # -----------------------------

        self.forecaster.train(df)

        forecast_df = (
            self.forecaster.forecast(
                df,
                periods=24
            )
        )


        # -----------------------------
        # RECOMMENDATIONS
        # -----------------------------

        recommendations = (
            self.recommendation_engine
            .generate_recommendations(
                df=df,
                summary=summary,
                anomaly_count=anomaly_count,
                forecast_df=forecast_df,
                peak_usage=peak_usage
            )
        )


        # -----------------------------
        # RETURN COMPLETE RESULTS
        # -----------------------------

        results = {

            "summary": summary,

            "hourly_consumption":
                hourly_consumption,

            "daily_consumption":
                daily_consumption,

            "building_consumption":
                building_consumption,

            "peak_usage":
                peak_usage,

            "anomaly_data":
                anomaly_result,

            "anomaly_count":
                anomaly_count,

            "forecast":
                forecast_df,

            "recommendations":
                recommendations
        }


        print("Energy Agent analysis completed.")

        return results