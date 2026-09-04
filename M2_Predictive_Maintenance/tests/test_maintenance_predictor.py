from src.maintenance_data_loader import MaintenanceDataLoader
from src.maintenance_predictor import MaintenancePredictor


# Load dataset
loader = MaintenanceDataLoader(
    "data/raw/ai4i2020.csv"
)

df = loader.load_data()


# Load trained model
predictor = MaintenancePredictor(
    "models/maintenance_failure_model.pkl"
)


print("\n========== MAINTENANCE PREDICTION RESULTS ==========")


# Test a few records
sample_records = df.sample(
    10,
    random_state=42
)


for index, row in sample_records.iterrows():

    result = predictor.predict_failure(
        row
    )

    print(
        f"\nProduct ID: {row['Product ID']}"
    )

    print(
        f"Machine Type: {row['Type']}"
    )

    print(
        f"Actual Failure: {row['Machine failure']}"
    )

    print(
        f"Predicted Failure: "
        f"{result['failure_prediction']}"
    )

    print(
        f"Failure Probability: "
        f"{result['failure_probability']}%"
    )