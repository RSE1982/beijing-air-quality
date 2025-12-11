import streamlit as st
import pandas as pd
import plotly.express as px

from utils.model_loader import load_best_model, load_encoders
from utils.data_loader import load_engineered
from utils.feature_engineering import apply_forecasting_features
from utils.forcast import forecast_horizon 
from utils.charts import MARGINS    


st.title("🌆 PM2.5 Forecast — All Stations")

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


df = load_engineered()  # Load engineered data

# Keep only model features + datetime + pm25 (needed for lags)
required_cols = set(features) | {"datetime", "pm25"} 
df = df[[col for col in df.columns if col in required_cols]]  # Keep only required columns

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

horizon_map = {"3 Hours": 3,
               "6 Hours": 6,
               "12 Hours": 12,
               "18 Hours": 18,
               "24 Hours": 24,
               "48 Hours": 48}

horizon = horizon_map.get(st.session_state.get("horizon_label", "3 Hours"), 3)


# ==============================================================
# Forecast all selected stations
# ==============================================================
forcast_list = []

for st_name in df["station"].unique():
    df_station = df[df["station"] == st_name].copy()
    df_station = apply_model_dtypes(df_station)
    df_station = df_station[features + ["datetime"]]

    if df_station.empty:
        st.warning(f"No usable data for station: {st_name}")
        continue

    forecast_df = forecast_horizon(df_station,
                                   model,
                                   features,
                                   horizon)
    forecast_df["station_name"] = st_name
    forcast_list.append(forecast_df)

if forcast_list:
    all_forecasts = pd.concat(forcast_list, ignore_index=True)
    col1, col2 = st.columns([3, 2])
    # ==============================================================
    # Plot
    # ==============================================================
    with col1:
        st.subheader(f"📈 PM2.5 Forecast for Next {horizon} Hours")

        fig = px.line(
            all_forecasts,
            x="datetime",
            y="pm25_predicted",
            color="station_name",
            labels={"station_name": "Station", "pm25_predicted": "PM2.5 (µg/m³)"},
            title=f"Next {horizon} Hours PM2.5 Forecast for All Stations"
        )
        fig.update_layout(legend_title_text="Stations",
                          hovermode="closest",
                          margin=MARGINS)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write("Forecast table for selected stations:")
        st.dataframe(all_forecasts)
