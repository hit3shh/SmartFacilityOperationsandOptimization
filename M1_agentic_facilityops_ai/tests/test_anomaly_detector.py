from src.data_loader import DataLoader
from src.anomaly_detector import AnomalyDetector


DATA_PATH = "data/processed/energy_agent_dataset.csv"


# Load data
loader = DataLoader(DATA_PATH)

df = loader.load_data()


# Create detector
detector = AnomalyDetector(
    contamination=0.02
)


# Detect anomalies
result_df = detector.detect(df)


# Count anomalies
anomaly_count = (
    result_df["is_anomaly"]
    .sum()
)


print("\n--- ANOMALY DETECTION RESULTS ---")

print(
    f"Total Records: {len(result_df)}"
)

print(
    f"Anomalies Detected: {anomaly_count}"
)


print("\n--- SAMPLE ANOMALIES ---")

print(
    result_df[
        result_df["is_anomaly"]
    ][
        [
            "building_id",
            "timestamp",
            "meter_reading",
            "air_temperature",
            "is_anomaly"
        ]
    ].head(20)
)