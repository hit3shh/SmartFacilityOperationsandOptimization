from src.data_loader import DataLoader
from src.analytics import EnergyAnalytics


DATA_PATH = "data/processed/energy_agent_dataset.csv"


# Load data
loader = DataLoader(DATA_PATH)

df = loader.load_data()


# Initialize analytics
analytics = EnergyAnalytics()


# Summary
summary = analytics.calculate_summary(df)

print("\n--- ENERGY SUMMARY ---")

for key, value in summary.items():
    print(f"{key}: {value}")


# Hourly Consumption
hourly_data = analytics.hourly_consumption(df)

print("\n--- HOURLY CONSUMPTION ---")

print(hourly_data)


# Daily Consumption
daily_data = analytics.daily_consumption(df)

print("\n--- DAILY CONSUMPTION ---")

print(daily_data.head())


# Building Consumption
building_data = analytics.building_consumption(df)

print("\n--- BUILDING CONSUMPTION ---")

print(building_data)


# Peak Usage Period
peak_usage = analytics.peak_usage_period(df)

print("\n--- PEAK USAGE PERIOD ---")

print(peak_usage)