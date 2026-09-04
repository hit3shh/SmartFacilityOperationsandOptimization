from src.maintenance_data_loader import MaintenanceDataLoader
from src.maintenance_agent import MaintenanceAgent


# ==========================================
# LOAD DATA
# ==========================================

loader = MaintenanceDataLoader(
    "data/raw/ai4i2020.csv"
)

df = loader.load_data()


# ==========================================
# INITIALIZE MAINTENANCE AGENT
# ==========================================

agent = MaintenanceAgent(
    "models/maintenance_failure_model.pkl"
)

print("\nMaintenance Agent started...")


# ==========================================
# DATASET ANALYSIS
# ==========================================

print("\n========== DATASET SUMMARY ==========")

summary = agent.get_dataset_summary(
    df
)

for key, value in summary.items():

    print(
        f"{key}: {value}"
    )


# ==========================================
# MACHINE ANALYSIS
# ==========================================

print(
    "\n========== MACHINE ANALYSIS =========="
)

# Select a sample of machines
sample_records = df.sample(
    5,
    random_state=42
)


for index, row in sample_records.iterrows():

    result = agent.analyze_machine(
        row
    )

    print("\n--------------------------------")

    print(
        f"Product ID: {result['product_id']}"
    )

    print(
        f"Machine Type: {result['machine_type']}"
    )

    print(
        f"Health Score: "
        f"{result['health_score']}/100"
    )

    print(
        f"Health Status: "
        f"{result['health_status']}"
    )

    print(
        f"Failure Prediction: "
        f"{result['failure_prediction']}"
    )

    print(
        f"Failure Probability: "
        f"{result['failure_probability']}%"
    )

    print(
        f"Risk Level: "
        f"{result['risk_level']}"
    )

    print(
        f"Message: "
        f"{result['message']}"
    )

    print(
        f"Recommendation: "
        f"{result['recommendation']}"
    )


print(
    "\nMaintenance Agent analysis completed."
)