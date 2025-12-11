"""
Module for forecasting PM2.5 levels for the next 24 hours using a trained model.
"""

import pandas as pd
import numpy as np


def forecast_next_24h(df_station: pd.DataFrame, model: object, features: list) -> pd.DataFrame:
    """
    Forecast PM2.5 levels for the next 24 hours for a given station.
    Parameters:
    df_station (pd.DataFrame): DataFrame containing historical
    data for the station.
    model: Trained machine learning model for prediction.
    features (list): List of feature column names used for prediction.
    Returns:
    pd.DataFrame: DataFrame containing datetime and predicted PM2.5 levels for
    the next 24 hours.
    """

    df_station = df_station.sort_values("datetime")
    last = df_station.iloc[-1][features].copy()
    forecasts = []

    for step in range(24):
        new_time = df_station["datetime"].max() + pd.Timedelta(hours=step + 1)

        # Update calendar features in-place if present in features
        for col, value in {
            "hour": new_time.hour,
            "month": new_time.month,
            "day_of_week": new_time.dayofweek,
            "year": new_time.year,
            "hour_sin": np.sin(2*np.pi*new_time.hour/24),
            "hour_cos": np.cos(2*np.pi*new_time.hour/24),
            "month_sin": np.sin(2*np.pi*new_time.month/12),
            "month_cos": np.cos(2*np.pi*new_time.month/12)
        }.items():
            if col in features:
                last[col] = value

        # Update lag features
        lag_cols = ["pm25_lag_18h","pm25_lag_12h","pm25_lag_6h","pm25_lag_3h","pm25_lag_1h"]
        if all(col in features for col in lag_cols):
            last["pm25_lag_18h"] = last["pm25_lag_12h"]
            last["pm25_lag_12h"] = last["pm25_lag_6h"]
            last["pm25_lag_6h"] = last["pm25_lag_3h"]
            last["pm25_lag_3h"] = last["pm25_lag_1h"]

        # Predict
        X = last[features].astype("float32").to_numpy().reshape(1, -1)
        pred = model.predict(X)[0]

        # Update lag_1h
        if "pm25_lag_1h" in features:
            last["pm25_lag_1h"] = pred

        # Update rolling means
        rolling_map = {
            "pm25_roll_3h_mean": ["pm25_lag_1h","pm25_lag_3h"],
            "pm25_roll_6h_mean": ["pm25_lag_1h","pm25_lag_3h","pm25_lag_6h"],
            "pm25_roll_12h_mean": ["pm25_lag_1h","pm25_lag_3h","pm25_lag_6h","pm25_lag_12h"],
            "pm25_roll_18h_mean": ["pm25_lag_1h","pm25_lag_3h","pm25_lag_6h","pm25_lag_12h","pm25_lag_18h"]
        }
        for roll_col, lag_list in rolling_map.items():
            if roll_col in features:
                last[roll_col] = np.mean([last[c] for c in lag_list])

        forecasts.append({"datetime": new_time, "pm25_predicted": pred})

    return pd.DataFrame(forecasts)