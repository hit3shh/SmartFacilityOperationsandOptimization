from src.data_loader import DataLoader
from src.forecasting import EnergyForecaster


DATA_PATH = (
    "data/processed/"
    "energy_agent_dataset.csv"
)


# Load data
loader = DataLoader(
    DATA_PATH
)

df = loader.load_data()


# Create forecaster
forecaster = EnergyForecaster()


# Train model
print("\nTraining Energy Forecasting Model...")

forecaster.train(df)

print("Model training completed!")


# Forecast next 24 hours
forecast_df = forecaster.forecast(
    df,
    periods=24
)


print(
    "\n--- NEXT 24 HOURS "
    "ENERGY FORECAST ---"
)

print(
    forecast_df
)