"""
Hypothesis 2: Spatial Variation in PM2.5
This page examines the spatial distribution of PM2.5 across monitoring
stations in Beijing using average PM2.5 levels and a map visualization.
"""

import streamlit as st
from utils.data_loader import load_cleaned, load_station_meta
from utils.charts import spatial_boxplot
import plotly.express as px

df = load_cleaned()
meta = load_station_meta()

col1, col2 = st.columns([1, 3])
with col1:
    st.title("📍Hypothesis 2")
    st.write("""
    **PM2.5 levels vary significantly across spatial regions of Beijing.**

    This is tested using:
    - station-level averages
    - boxplots
    - area type labels (urban / suburban / rural)
    - geographic coordinates
    """)
    st.success("✔ **Conclusion:** H2 is supported — PM2.5 varies\
            significantly across Beijing.")

    st.caption("Source: Notebook 06 — Spatial Analysis • \
                Dataset © Song Chen (CC BY 4.0)")
with col2:
    tab1, tab2, tab3 = st.tabs(["Boxplot", "Map", "Observations & Justification"])
    with tab1:
        # ------------------------- Charts -------------------------
        st.subheader("📊 PM2.5 Variation Across 12 Stations")
        st.plotly_chart(spatial_boxplot(df), use_container_width=True)
    with tab2:
        # Compute station averages
        station_means = df.groupby("station")["pm25"].mean().reset_index()

        st.subheader("🗺️ PM2.5 by Station (Mapped)")
        fig = px.scatter_mapbox(
            meta.merge(station_means, on="station"),
            lat="latitude",
            lon="longitude",
            color="pm25",
            size="pm25",
            hover_name="station",
            zoom=9,
            height=500,
            mapbox_style="open-street-map",
            title="Average PM2.5 by Station"
        )
        st.plotly_chart(fig, use_container_width=True)
    with tab3:
        # ------------------------- Observations -------------------------
        st.markdown("### 📝 Observations")
        st.markdown("""
        - Urban stations generally show **higher PM2.5 averages** than suburban
                    or rural stations.
        - Some stations display wider variability, indicating mixed microclimates.
        - Geographic map highlights distinct hotspots located around central districts.
        """)

        # ------------------------- Justification -------------------------
        st.markdown("### 🎯 Justification")
        st.markdown("""
        Spatial inequality is clearly expressed in both boxplots and the geospatial
                    map.
        The ANOVA performed in the notebook confirmed **significant between-station
                    differences (p < 0.001)**.
        Station-level meteorological differences explain part of this variation.
        """)


