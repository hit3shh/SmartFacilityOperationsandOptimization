from src.data_loader import DataLoader
from src.analytics import EnergyAnalytics
from src.anomaly_detector import AnomalyDetector
from src.forecasting import EnergyForecaster
from src.recommendations import RecommendationEngine


DATA_PATH = (
    "data/processed/"
    "energy_agent_dataset.csv"
)


# ---------------------------------
# LOAD DATA
# ---------------------------------

loader = DataLoader(DATA_PATH)

df = loader.load_data()


# ---------------------------------
# ANALYTICS
# ---------------------------------

analytics = EnergyAnalytics()

summary = (
    analytics.calculate_summary(df)
)

peak_usage = (
    analytics.peak_usage_period(df)
)


# ---------------------------------
# ANOMALY DETECTION
# ---------------------------------

detector = AnomalyDetector()

anomaly_df = (
    detector.detect(df)
)

anomaly_count = (
    anomaly_df["is_anomaly"]
    .sum()
)


# ---------------------------------
# FORECASTING
# ---------------------------------

forecaster = EnergyForecaster()

forecaster.train(df)

forecast_df = (
    forecaster.forecast(
        df,
        periods=24
    )
)


# ---------------------------------
# RECOMMENDATIONS
# ---------------------------------

engine = RecommendationEngine()

recommendations = (
    engine.generate_recommendations(
        df=df,
        summary=summary,
        anomaly_count=anomaly_count,
        forecast_df=forecast_df,
        peak_usage=peak_usage
    )
)


print(
    "\n--- ENERGY AGENT RECOMMENDATIONS ---"
)


for i, recommendation in enumerate(
    recommendations,
    start=1
):

    print(
        f"\n{i}. "
        f"[{recommendation['priority']}] "
        f"{recommendation['category']}"
    )

    print(
        recommendation["message"]
    )