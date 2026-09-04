from src.data_loader import DataLoader
from src.energy_agent import EnergyAgent


DATA_PATH = (
    "data/processed/"
    "energy_agent_dataset.csv"
)


# Load data

loader = DataLoader(DATA_PATH)

df = loader.load_data()


# Create Energy Agent

agent = EnergyAgent()


# Run complete analysis

results = agent.run_analysis(df)


# Display results

print("\n========== ENERGY AGENT RESULTS ==========")


print("\n--- SUMMARY ---")

for key, value in results["summary"].items():

    print(f"{key}: {value}")


print("\n--- PEAK USAGE ---")

print(
    results["peak_usage"]
)


print("\n--- ANOMALIES ---")

print(
    "Total anomalies detected:",
    results["anomaly_count"]
)


print("\n--- FORECAST ---")

print(
    results["forecast"].head()
)


print("\n--- RECOMMENDATIONS ---")

for i, recommendation in enumerate(
    results["recommendations"],
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