"""
Occupancy Forecasting Module

Loads the trained Random Forest model and performs
next-step occupancy forecasting using the same feature
engineering pipeline developed in the occupancy analysis notebook.
"""

import json
import os

import joblib
import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OCCUPANCY_SYSTEM_DIR = os.path.dirname(CURRENT_DIR)

MODEL_PATH = os.path.join(
    OCCUPANCY_SYSTEM_DIR,
    "models",
    "occupancy_random_forest.joblib"
)

FEATURE_INFO_PATH = os.path.join(
    OCCUPANCY_SYSTEM_DIR,
    "models",
    "occupancy_model_features.json"
)


# -------------------------------------------------------------------
# Sensor features
# -------------------------------------------------------------------

SENSOR_COLUMNS = [
    "S1_Temp",
    "S2_Temp",
    "S3_Temp",
    "S4_Temp",
    "S1_Light",
    "S2_Light",
    "S3_Light",
    "S4_Light",
    "S1_Sound",
    "S2_Sound",
    "S3_Sound",
    "S4_Sound",
    "S5_CO2",
    "S5_CO2_Slope",
    "S6_PIR",
    "S7_PIR",
]


# -------------------------------------------------------------------
# Forecasting features
# -------------------------------------------------------------------

FORECAST_FEATURES = [
    "Hour",
    "Minute",
    "DayOfWeek",
    "Hour_sin",
    "Hour_cos",
    "Day_sin",
    "Day_cos",
    "Occupancy_Lag_1",
    "Occupancy_Lag_2",
    "Occupancy_Lag_5",
    "Occupancy_Lag_10",
    "Occupancy_Rolling_Mean_5",
    "Occupancy_Rolling_Mean_10",
]

FORECAST_FEATURES.extend(SENSOR_COLUMNS)


# -------------------------------------------------------------------
# Model loading
# -------------------------------------------------------------------

def load_model():
    """
    Load the trained Random Forest occupancy forecasting model.
    """

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Occupancy model not found at: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def load_feature_info():
    """
    Load the saved model feature metadata.
    """

    if not os.path.exists(FEATURE_INFO_PATH):
        raise FileNotFoundError(
            f"Feature information not found at: "
            f"{FEATURE_INFO_PATH}"
        )

    with open(FEATURE_INFO_PATH, "r") as file:
        return json.load(file)


# -------------------------------------------------------------------
# Feature engineering
# -------------------------------------------------------------------

def prepare_forecasting_features(dataframe):
    """
    Prepare forecasting features using the same feature engineering
    process used in the occupancy analysis notebook.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Occupancy sensor dataframe containing:
        Date, Time, sensor columns, and Room_Occupancy_Count.

    Returns
    -------
    pandas.DataFrame
        Dataframe containing the model forecasting features.
    """

    df = dataframe.copy()

    required_columns = [
        "Date",
        "Time",
        "Room_Occupancy_Count",
    ] + SENSOR_COLUMNS

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # Create timestamp
    df["Timestamp"] = pd.to_datetime(
        df["Date"].astype(str)
        + " "
        + df["Time"].astype(str),
        errors="coerce"
    )

    if df["Timestamp"].isna().any():
        raise ValueError(
            "Invalid Date/Time values found in the input data."
        )

    # Sort chronologically
    df = df.sort_values("Timestamp").reset_index(drop=True)

    # Time features
    df["Hour"] = df["Timestamp"].dt.hour
    df["Minute"] = df["Timestamp"].dt.minute
    df["DayOfWeek"] = df["Timestamp"].dt.dayofweek

    # Cyclic time features
    df["Hour_sin"] = np.sin(
        2 * np.pi * df["Hour"] / 24
    )

    df["Hour_cos"] = np.cos(
        2 * np.pi * df["Hour"] / 24
    )

    df["Day_sin"] = np.sin(
        2 * np.pi * df["DayOfWeek"] / 7
    )

    df["Day_cos"] = np.cos(
        2 * np.pi * df["DayOfWeek"] / 7
    )

    # Occupancy lag features
    df["Occupancy_Lag_1"] = (
        df["Room_Occupancy_Count"].shift(1)
    )

    df["Occupancy_Lag_2"] = (
        df["Room_Occupancy_Count"].shift(2)
    )

    df["Occupancy_Lag_5"] = (
        df["Room_Occupancy_Count"].shift(5)
    )

    df["Occupancy_Lag_10"] = (
        df["Room_Occupancy_Count"].shift(10)
    )

    # Rolling occupancy features
    df["Occupancy_Rolling_Mean_5"] = (
        df["Room_Occupancy_Count"]
        .shift(1)
        .rolling(window=5)
        .mean()
    )

    df["Occupancy_Rolling_Mean_10"] = (
        df["Room_Occupancy_Count"]
        .shift(1)
        .rolling(window=10)
        .mean()
    )

    return df


# -------------------------------------------------------------------
# Prediction
# -------------------------------------------------------------------

def predict_next_occupancy(dataframe):
    """
    Predict the next occupancy value using the trained
    Random Forest model.

    The final row of the supplied dataframe is used to
    generate the next-step prediction.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Historical occupancy and sensor data.

    Returns
    -------
    int
        Predicted occupancy count for the next time step.
    """

    prepared_df = prepare_forecasting_features(dataframe)

    # Remove rows where lag/rolling features are unavailable
    prepared_df = prepared_df.dropna(
        subset=[
            "Occupancy_Lag_1",
            "Occupancy_Lag_2",
            "Occupancy_Lag_5",
            "Occupancy_Lag_10",
            "Occupancy_Rolling_Mean_5",
            "Occupancy_Rolling_Mean_10",
        ]
    )

    if prepared_df.empty:
        raise ValueError(
            "Not enough historical occupancy data "
            "to generate forecasting features."
        )

    # Use the latest available observation
    latest_row = prepared_df.iloc[[-1]]

    X_latest = latest_row[FORECAST_FEATURES]

    # Load model
    model = load_model()

    # Generate prediction
    prediction = model.predict(X_latest)[0]

    # Occupancy is a discrete count
    prediction = int(np.rint(prediction))

    # Prevent impossible negative occupancy
    prediction = max(0, prediction)

    return prediction


# -------------------------------------------------------------------
# Convenience function
# -------------------------------------------------------------------

def forecast_with_details(dataframe):
    """
    Generate a next-step occupancy forecast together with
    useful operational information.
    """

    prepared_df = prepare_forecasting_features(dataframe)

    prepared_df = prepared_df.dropna(
        subset=[
            "Occupancy_Lag_1",
            "Occupancy_Lag_2",
            "Occupancy_Lag_5",
            "Occupancy_Lag_10",
            "Occupancy_Rolling_Mean_5",
            "Occupancy_Rolling_Mean_10",
        ]
    )

    if prepared_df.empty:
        raise ValueError(
            "Not enough historical occupancy data "
            "to generate a forecast."
        )

    latest_row = prepared_df.iloc[-1]

    model = load_model()

    X_latest = latest_row[FORECAST_FEATURES]

    raw_prediction = model.predict(
        X_latest.to_frame().T
    )[0]

    predicted_occupancy = int(
        np.rint(raw_prediction)
    )

    predicted_occupancy = max(
        0,
        predicted_occupancy
    )

    current_occupancy = int(
        latest_row["Room_Occupancy_Count"]
    )

    return {
        "timestamp": str(latest_row["Timestamp"]),
        "current_occupancy": current_occupancy,
        "predicted_next_occupancy": predicted_occupancy,
        "forecast_horizon": "30 seconds",
    }
