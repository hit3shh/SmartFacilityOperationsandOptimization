from src.maintenance_data_loader import MaintenanceDataLoader
from src.maintenance_analytics import MaintenanceAnalytics


# Load dataset
loader = MaintenanceDataLoader(
    "data/raw/ai4i2020.csv"
)

df = loader.load_data()


# Initialize analytics
analytics = MaintenanceAnalytics()


# Overall summary
print("\n========== MAINTENANCE SUMMARY ==========")

summary = analytics.get_summary(df)

for key, value in summary.items():

    print(
        f"{key}: {value}"
    )


# Machine type analysis
print(
    "\n========== MACHINE TYPE ANALYSIS =========="
)

machine_type_analysis = (
    analytics.get_machine_type_analysis(df)
)

print(
    machine_type_analysis
)


# Failure type analysis
print(
    "\n========== FAILURE TYPE ANALYSIS =========="
)

failure_type_analysis = (
    analytics.get_failure_type_analysis(df)
)

print(
    failure_type_analysis
)