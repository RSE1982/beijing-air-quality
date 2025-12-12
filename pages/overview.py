"""Overview page for the Beijing Clean Air Dashboard."""

import streamlit as st
import pandas as pd
from utils.data_loader import load_engineered, load_station_meta
from utils.charts import seasonal_boxplot, monthly_trend, spatial_boxplot
import plotly.express as px

# ------------------------- Page Header -------------------------
st.title(":material/home: Overview")

# ------------------------- Load Data -------------------------
df = load_engineered()
meta = load_station_meta()


col1, col2 = st.columns([1, 2])
with col1:
    tab = st.tabs([
        ":material/trending_up: Snapshot",
        ":material/access_time: Time Summary",
        ":material/info: PM2.5 Summary"])
    with tab[0]:
        # ------------------------- Dataset KPIs -------------------------
        st.subheader(":material/dataset: Dataset Snapshot")
        # two rows of two columns
        k1, k2 = st.columns(2)  # first row
        k3, k4 = st.columns(2)  # second row

        # metrics showing no records, unique stations, year range, no features
        k1.metric("Rows", f"{len(df):,}")
        k2.metric("Stations", df["station"].nunique())
        k3.metric("Years Covered", f"{df['year'].min()}-{df['year'].max()}")
        k4.metric("Features", df.shape[1])
    with tab[1]:
        # ------------------------- Time Coverage -------------------------
        st.subheader(":material/access_time: Time Coverage")
        first_date = df['datetime'].min().date()
        last_date = df['datetime'].max().date()
        date_range = last_date - first_date
        st.metric("First Date", str(first_date))
        st.metric("Last Date", str(last_date))
        st.metric("Days Covered", f"{date_range.days:,}")
    with tab[2]:
        # ------------------------- PM2.5 Summary -------------------------
        st.subheader(":material/air: PM2.5 Summary")

        # compute statistics
        mean_pm25 = df["pm25"].mean()
        max_pm25 = df["pm25"].max()
        min_pm25 = df["pm25"].min()

        station_means = df.groupby("station")["pm25"].mean()
        worst_station = station_means.idxmax()
        best_station = station_means.idxmin()

        pm1, pm2 = st.columns(2)
        pm3, pm4 = st.columns(2)

        pm1.metric("Mean PM2.5", f"{mean_pm25:.1f} µg/m³")
        pm2.metric("Max PM2.5", f"{max_pm25:.0f} µg/m³")
        pm3.metric("Worst Station", f"{worst_station}")
        pm4.metric("Best Station", f"{best_station}")

        who_limit = 25
        exceed_hours = (df["pm25"] > who_limit).sum()
        pct_exceed = exceed_hours / len(df) * 100

        pm5, pm6 = st.columns(2)
        pm5.metric("Hours Above WHO Guideline", f"{exceed_hours:,}")
        pm6.metric("Percent Exceedance", f"{pct_exceed:.1f}%")

with col2:
    # ------------------------- Tabs -------------------------
    tab = st.tabs([
        ":material/partly_cloudy_day: Seasonal Trends",
        ":material/calendar_month: Monthly Trends",
        ":material/location_on: Spatial Variation",
        ":material/map: Station Map",
        ":material/assessment: Hypothesis Results"
    ])

    with tab[0]:
        st.subheader(":material/partly_cloudy_day: Seasonal & Monthly Trends")
        st.plotly_chart(seasonal_boxplot(df), use_container_width=True)
    with tab[1]:
        st.subheader(":material/calendar_month: Monthly PM2.5 Trends")
        st.plotly_chart(monthly_trend(df), use_container_width=True)
    with tab[2]:
        st.subheader(":material/location_on:\
                     Spatial Variation Across Stations")
        st.plotly_chart(spatial_boxplot(df), use_container_width=True)
    with tab[3]:
        st.subheader(":material/map: Interactive Station Map")
        station_means = df.groupby("station")["pm25"].mean().reset_index()
        meta_map = meta.merge(station_means, on="station")

        # More mobile-friendly + no Mapbox token needed
        fig_map = px.scatter_mapbox(
            meta_map,
            lat="latitude",
            lon="longitude",
            color="pm25",
            size="pm25",
            hover_name="station",
            mapbox_style="carto-positron",
            center={"lat": meta_map.latitude.mean(),
                    "lon": meta_map.longitude.mean()},
            zoom=8,
            height=500,
        )

        fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))

        st.plotly_chart(fig_map, use_container_width=True)
    with tab[4]:
        st.subheader("📊 Hypothesis Results Summary")

        results = [
            ["H1",
             "Seasonal PM2.5 patterns exist",
             "ANOVA", "Supported",
             "Winter levels significantly higher than summer."],
            ["H2",
             "PM2.5 varies between stations",
             "ANOVA",
             "Supported",
             "Urban stations show consistently higher pollution."],
            ["H3", "Weather variables correlate with PM2.5",
             "Correlation tests",
             "Partially Supported",
             "Temperature & dew point correlate strongly; rainfall weak."],
            ["H4",
             "Short-term temporal structure explains PM2.5",
             "Rolling analysis", "Supported",
             "Strong hourly & daily autocorrelation detected."],
            ["H5",
             "Lag features improve modelling",
             "Model comparison", "Supported",
             "Lag-based XGBoost outperforms baseline model."]]

        df_results = pd.DataFrame(results,
                                  columns=["Hypothesis",
                                           "Statement",
                                           "Method",
                                           "Result",
                                           "Interpretation"])

        st.dataframe(df_results.reset_index(drop=True),
                     hide_index=True,
                     use_container_width=True)
