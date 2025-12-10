"""Overview page for the Beijing Clean Air Dashboard."""

import streamlit as st
from utils.data_loader import load_engineered, load_station_meta
from utils.charts import seasonal_boxplot, monthly_trend, spatial_boxplot
import plotly.express as px

col1, col2 = st.columns([1, 3])
with col1:
    st.title("🏠 Overview")

    st.write("""
    Welcome to the **Beijing Clean Air Dashboard**, an interactive companion to the
    **Beijing Air Quality Analysis & Forecasting** Capstone project.

    This dashboard allows you to explore:
    - Seasonal, spatial, meteorological, and temporal pollution patterns
    - Statistical validation of five hypotheses
    - Forecasting using an XGBoost lag-based model
    - Station clustering patterns
    """)

    # ------------------------- Footer -------------------------
    st.caption("""
    © 2025 Robert Steven Elliott — Beijing Air Quality Capstone
    Dataset © Song Chen (2017), licensed under CC BY 4.0
    """)
with col2:
    # ------------------------- Load Data -------------------------
    df = load_engineered()
    meta = load_station_meta()

    # ------------------------- KPI Metrics -------------------------
    st.subheader("📊 Dataset Snapshot")

    col2_1, col2_2, col2_3, col2_4 = st.columns(4)
    col2_1.metric("Rows", f"{len(df):,}")
    col2_2.metric("Stations", df["station"].nunique())
    col2_3.metric("Years Covered", df["year"].nunique())
    col2_4.metric("Features", df.shape[1])

    tab1, tab2, tab3 = st.tabs(["Seasonal & Monthly Trends", "Spatial Variation", "Station Map"])

    with tab1:
        # ------------------------- Quick Visuals -------------------------
        st.subheader("🌤 Seasonal & Monthly Trends")

        colA, colB = st.columns(2)
        with colA:
            st.plotly_chart(seasonal_boxplot(df), use_container_width=True)

        with colB:
            st.plotly_chart(monthly_trend(df), use_container_width=True)

    with tab2:
        # ------------------------- Spatial Snapshot -------------------------
        st.subheader("📍 Spatial Variation Across Stations")
        st.plotly_chart(spatial_boxplot(df), use_container_width=True)
    with tab3:
        # ------------------------- Station Map -------------------------
        station_means = df.groupby("station")["pm25"].mean().reset_index()
        meta_map = meta.merge(station_means, on="station")

        fig_map = px.scatter_mapbox(
            meta_map,
            lat="latitude",
            lon="longitude",
            color="pm25",
            size="pm25",
            hover_name="station",
            mapbox_style="open-street-map",  # more mobile-friendly
            zoom=8,
            title="Average PM2.5 by Station",
            height=500,
        )
        st.plotly_chart(fig_map, use_container_width=True)
