from src.maintenance_data_loader import MaintenanceDataLoader
from src.health_scoring import HealthScoring


# Load dataset
loader = MaintenanceDataLoader(
    "data/raw/ai4i2020.csv"
)

df = loader.load_data()


# Initialize Health Scoring
health_scoring = HealthScoring()


print("\n========== HEALTH SCORING RESULTS ==========")


# Test a few records
sample_records = df.head(10)


for index, row in sample_records.iterrows():

    score = health_scoring.calculate_health_score(
        row
    )

    status = health_scoring.get_health_status(
        score
    )

    print(
        f"\nProduct ID: {row['Product ID']}"
    )

    print(
        f"Tool Wear: {row['Tool wear [min]']}"
    )

    print(
        f"Torque: {row['Torque [Nm]']}"
    )

    print(
        f"Process Temperature: "
        f"{row['Process temperature [K]']}"
    )

    print(
        f"Rotational Speed: "
        f"{row['Rotational speed [rpm]']}"
    )

    print(
        f"Health Score: {score}/100"
    )

    print(
        f"Status: {status}"
    )