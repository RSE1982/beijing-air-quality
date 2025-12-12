import streamlit as st
import pandas as pd
from utils.model_loader import load_best_model, load_encoders
from utils.data_loader import load_engineered
from utils.feature_engineering import apply_forecasting_features
from utils.forcast import forecast_horizon
from utils.modelling_charts import forecast_line_chart


st.header(":material/online_prediction: PM2.5 Forecast — All Stations")

model = load_best_model()
features = model.feature_names_in_.tolist()
season_dtype, area_dtype, station_dtype = load_encoders()


# Helper — Apply SAME categorical encoding used during training
def apply_model_dtypes(df):
    df = df.copy()
    df["season"] = df["season"]\
        .astype(season_dtype).cat.codes.astype("int16")
    df["area_type"] = df["area_type"]\
        .astype(area_dtype).cat.codes.astype("int16")
    df["station"] = df["station"]\
        .astype(station_dtype).cat.codes.astype("int16")
    return df


df = load_engineered()  # Load engineered data

# Keep only model features + datetime + pm25 (needed for lags)
required_cols = set(features) | {"datetime", "pm25"}

# Keep only required columns
df = df[[col for col in df.columns if col in required_cols]]

# Apply forecasting features per station, forward-fill missing values
df_list = []
for st_name in df["station"].unique():
    d = df[df["station"] == st_name].copy()
    d = apply_forecasting_features(d).fillna(method="ffill")
    if not d.empty:
        df_list.append(d)

df = pd.concat(df_list, ignore_index=True)

# Drop pm25 if not used in features
if "pm25" in df.columns and "pm25" not in features:
    df.drop(columns=["pm25"], inplace=True)

# Horizon mapping
horizon_map = {"3 Hours": 3,
               "6 Hours": 6,
               "12 Hours": 12,
               "18 Hours": 18,
               "24 Hours": 24,
               "48 Hours": 48}

# Select forecast horizon
horizon = horizon_map.get(st.session_state.get("horizon_label", "3 Hours"), 3)

# Forecast all stations
forcast_list = []

# Generate forecasts for each station
for st_name in df["station"].unique():
    # Filter data for the station
    df_station = df[df["station"] == st_name].copy()

    # Apply categorical dtypes
    df_station = apply_model_dtypes(df_station)

    # keep only model features + datetime
    df_station = df_station[features + ["datetime"]]
    forecast_df = forecast_horizon(df_station,
                                   model,
                                   features,
                                   horizon)  # Generate forecast
    forecast_df["station_name"] = st_name  # Add station name
    forcast_list.append(forecast_df)  # Collect forecast

# Combine all forecasts
all_forecasts = pd.concat(forcast_list, ignore_index=True)  # Combi


# display forecasts
if forcast_list:
    col1, col2 = st.columns([3, 2])
    # Plotting
    with col1:
        st.subheader(f":material/trending_up:\
                      PM2.5 Forecast for Next {horizon} Hours")
        st.plotly_chart(forecast_line_chart(all_forecasts, horizon),
                        use_container_width=True)
    with col2:
        # Data display
        st.subheader(":material/assignment: Forecast Data")
        st.write("Forecast table for selected stations:")
        st.dataframe(all_forecasts)
