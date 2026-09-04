import os
import pandas as pd


# -------------------------------
# FILE PATHS
# -------------------------------

ENERGY_PATH = "data/raw/train.csv"

METADATA_PATH = "data/raw/building_metadata.csv"

WEATHER_PATH = "data/raw/weather_train.csv"

OUTPUT_PATH = (
    "data/processed/"
    "processed_energy_data.csv"
)


# -------------------------------
# LOAD DATA
# -------------------------------

print("Loading datasets...")

energy_df = pd.read_csv(
    ENERGY_PATH
)

metadata_df = pd.read_csv(
    METADATA_PATH
)

weather_df = pd.read_csv(
    WEATHER_PATH
)


# -------------------------------
# CONVERT TIMESTAMPS
# -------------------------------

print("Converting timestamps...")

energy_df["timestamp"] = pd.to_datetime(
    energy_df["timestamp"]
)

weather_df["timestamp"] = pd.to_datetime(
    weather_df["timestamp"]
)


# -------------------------------
# FILTER ELECTRICITY DATA
# -------------------------------

print("Filtering electricity meter data...")

energy_df = energy_df[
    energy_df["meter"] == 0
].copy()


# -------------------------------
# REMOVE INVALID READINGS
# -------------------------------

energy_df = energy_df[
    energy_df["meter_reading"] >= 0
].copy()


# -------------------------------
# MERGE BUILDING METADATA
# -------------------------------

print("Merging building metadata...")

df = energy_df.merge(
    metadata_df,
    on="building_id",
    how="left"
)


# -------------------------------
# MERGE WEATHER DATA
# -------------------------------

print("Merging weather data...")

df = df.merge(
    weather_df,
    on=[
        "site_id",
        "timestamp"
    ],
    how="left"
)


# -------------------------------
# HANDLE MISSING VALUES
# -------------------------------

print("Handling missing values...")

df = df.sort_values(
    ["building_id", "timestamp"]
)

df = df.fillna(
    df.median(
        numeric_only=True
    )
)


# -------------------------------
# CREATE TIME FEATURES
# -------------------------------

print("Creating time features...")

df["hour"] = (
    df["timestamp"].dt.hour
)

df["day_of_week"] = (
    df["timestamp"].dt.dayofweek
)

df["month"] = (
    df["timestamp"].dt.month
)

df["date"] = (
    df["timestamp"].dt.date
)


# -------------------------------
# CREATE OUTPUT FOLDER
# -------------------------------

os.makedirs(
    "data/processed",
    exist_ok=True
)


# -------------------------------
# SAVE PROCESSED DATA
# -------------------------------

print("Saving processed dataset...")

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nData preparation completed!")

print(
    f"Processed dataset saved to: "
    f"{OUTPUT_PATH}"
)

print(
    f"Dataset shape: {df.shape}"
)