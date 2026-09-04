import os
import pandas as pd


INPUT_PATH = (
    "data/processed/"
    "processed_energy_data.csv"
)

OUTPUT_PATH = (
    "data/processed/"
    "energy_agent_dataset.csv"
)


print("Loading processed energy data...")


# Read only required columns
columns = [
    "building_id",
    "timestamp",
    "meter_reading",
    "site_id",
    "primary_use",
    "square_feet",
    "air_temperature",
    "dew_temperature",
    "wind_speed",
    "hour",
    "day_of_week",
    "month"
]


df = pd.read_csv(
    INPUT_PATH,
    usecols=columns
)


print(
    f"Original dataset shape: {df.shape}"
)


# --------------------------------
# SELECT BUILDINGS
# --------------------------------

print("Selecting representative buildings...")


selected_buildings = (
    df["building_id"]
    .drop_duplicates()
    .sample(
        n=25,
        random_state=42
    )
    .tolist()
)


df = df[
    df["building_id"]
    .isin(selected_buildings)
].copy()


# --------------------------------
# LIMIT TIME PERIOD
# --------------------------------

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)


df = df[
    df["timestamp"]
    < df["timestamp"].min()
    + pd.DateOffset(months=3)
]


# --------------------------------
# REMOVE EXTREME ZERO DATA
# --------------------------------

df = df[
    df["meter_reading"] >= 0
]


# --------------------------------
# SORT DATA
# --------------------------------

df = df.sort_values(
    ["building_id", "timestamp"]
)


# --------------------------------
# SAVE
# --------------------------------

os.makedirs(
    "data/processed",
    exist_ok=True
)


df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nEnergy Agent dataset created successfully!")

print(
    f"Final dataset shape: {df.shape}"
)

print(
    f"Saved to: {OUTPUT_PATH}"
)