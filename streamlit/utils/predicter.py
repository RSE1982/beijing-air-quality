"""
Utility functions for making predictions using pre-trained models.
"""


import pandas as pd
import numpy as np
from src.feature_engineering import apply_forecasting_features


def forecast_next_24h(df: pd.DataFrame, model, seasons_dtype) -> pd.DataFrame:
    """
    Forecast the next 24 hours of PM2.5 using the provided model.
    Args:
        df (pd.DataFrame): Input DataFrame containing historical data.
        model: Pre-trained model for forecasting.
    Returns:
        pd.DataFrame: DataFrame with datetime and predicted PM2.5 for the next
        24 hours.
    """

    # Apply feature engineering to the initial fake day
    history = apply_forecasting_features(df).reset_index(drop=True)

    preds = []

    for _ in range(24):

        last = history.iloc[-1].copy()
        next_time = last["datetime"] + pd.Timedelta(hours=1)

        # Start next row
        fr = pd.Series(dtype='float64')
        fr["datetime"] = next_time
        fr["year"] = next_time.year
        fr["month"] = next_time.month
        fr["day"] = next_time.day
        fr["hour"] = next_time.hour
        fr["day_of_week"] = next_time.dayofweek

        # Carry forward weather (no change in scenario mode)
        for col in ["temperature",
                    "dew_point",
                    "pressure",
                    "rain",
                    "wind_speed"]:
            fr[col] = last[col]

        # Categorical encodings
        def month_to_season(m):
            if m in [12, 1, 2]:
                return "winter"
            if m in [3, 4, 5]:
                return "spring"
            if m in [6, 7, 8]:
                return "summer"
            return "autumn"

        season_name = month_to_season(fr["month"])
        season_code = seasons_dtype.categories.get_loc(season_name)

        # MUST match model expectation:
        fr["season"] = season_code

# numeric column expected by the model

        fr["area_type"] = last["area_type"]
        fr["area_type_code"] = last["area_type_code"]

        # Cyclical encodings
        fr["hour_sin"] = np.sin(2 * np.pi * fr["hour"] / 24)
        fr["hour_cos"] = np.cos(2 * np.pi * fr["hour"] / 24)
        fr["month_sin"] = np.sin(2 * np.pi * fr["month"] / 12)
        fr["month_cos"] = np.cos(2 * np.pi * fr["month"] / 12)

        # Interaction terms
        fr["dew_point_spread"] = fr["temperature"] - fr["dew_point"]
        fr["temp_pres_interaction"] = fr["temperature"] * fr["pressure"]
        fr["rain_binary"] = fr["rain"] > 0

        # PM2.5 history for rolling + lag features
        pm25_history = history["pm25"].tolist()

        # Rolling windows
        for w in [3, 6, 12, 18]:
            fr[f"pm25_roll_{w}h_mean"] = (
                np.mean(pm25_history[-w:]) if len(pm25_history) >= w
                else np.mean(pm25_history)
            )

        # Lag features
        for lag in [1, 3, 6, 12, 18]:
            fr[f"pm25_lag_{lag}h"] = (
                pm25_history[-lag] if len(pm25_history) >= lag
                else pm25_history[0]
            )

        # Predict next PM2.5
        x_pred = fr[model.feature_names_in_].values.reshape(1, -1)
        pm25_pred = model.predict(x_pred)[0]

        preds.append({"datetime": next_time, "pm25_pred": pm25_pred})

        # Add predicted pm25 to fr and append to history
        fr["pm25"] = pm25_pred
        history = pd.concat([history, fr.to_frame().T], ignore_index=True)

    return pd.DataFrame(preds)
