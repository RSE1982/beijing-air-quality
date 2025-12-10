import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.model_loader import load_best_model, load_encoders, load_feature_names
from utils.data_loader import load_engineered
from utils.feature_engineering import apply_forecasting_features

# ==============================================================
# Title
# ==============================================================
st.title("🌆 PM2.5 Forecast — All Stations")

# ==============================================================
# Load Model + Features + Encoders
# ==============================================================
model = load_best_model()
features = model.feature_names_in_.tolist()
season_dtype, area_dtype, station_dtype = load_encoders()

# ==============================================================
# Helper — Apply SAME categorical encoding used during training
# ==============================================================
def apply_model_dtypes(df):
    df = df.copy()
    df["season"] = df["season"].astype(season_dtype).cat.codes.astype("int16")
    df["area_type"] = df["area_type"].astype(area_dtype).cat.codes.astype("int16")
    df["station"] = df["station"].astype(station_dtype).cat.codes.astype("int16")
    return df

# ==============================================================
# Load engineered dataset
# ==============================================================
df = load_engineered()

# Keep only model features + datetime + pm25 (needed for lags)
required_cols = set(features) | {"datetime", "pm25"}
drop_cols = set(df.columns) - required_cols
df.drop(columns=list(drop_cols), inplace=True)

# Apply forecasting features per station, forward-fill missing values
df_list = []
for st_name in df["station"].unique():
    d = df[df["station"] == st_name].copy()
    d = apply_forecasting_features(d)
    d = d.fillna(method="ffill")  # forward-fill missing lags/rollings
    if d.empty:
        st.warning(f"No usable data for station: {st_name}")
        continue
    df_list.append(d)

df = pd.concat(df_list, ignore_index=True)

# Drop pm25 if not used in features
if "pm25" in df.columns and "pm25" not in features:
    df.drop(columns=["pm25"], inplace=True)

# ==============================================================
# Recursive 24h Forecast
# ==============================================================
def forecast_next_24h(df_station, model, features):
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

# ==============================================================
# Multi-select stations
# ==============================================================
st.sidebar.header("Select stations to display")
valid_stations = df["station"].unique()
selected_stations = st.sidebar.multiselect(
    "Stations", options=valid_stations, default=list(valid_stations)
)

# ==============================================================
# Forecast all selected stations
# ==============================================================
forecast_list = []
for st_name in selected_stations:
    df_station = df[df["station"] == st_name].copy()
    df_station = apply_model_dtypes(df_station)
    df_station = df_station[features + ["datetime"]]

    if df_station.empty:
        st.warning(f"No usable data for station: {st_name}")
        continue

    forecast_df = forecast_next_24h(df_station, model, features)
    forecast_df["station_name"] = st_name
    forecast_list.append(forecast_df)

if forecast_list:
    all_forecasts = pd.concat(forecast_list, ignore_index=True)

    # ==============================================================
    # Plot
    # ==============================================================
    st.subheader("📈 PM2.5 Forecast — Next 24 Hours")
    fig = px.line(
        all_forecasts,
        x="datetime",
        y="pm25_predicted",
        color="station_name",
        labels={"station_name": "Station", "pm25_predicted": "PM2.5 (µg/m³)"},
        title="Next 24h PM2.5 Forecast for Selected Stations"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("Forecast table for selected stations:")
    st.dataframe(all_forecasts)
else:
    st.warning("No forecastable stations selected or available.")
