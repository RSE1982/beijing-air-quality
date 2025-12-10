"""Overview page for the Beijing Clean Air Dashboard."""

import streamlit as st
from utils.data_loader import load_engineered, load_station_meta
from utils.charts import seasonal_boxplot, monthly_trend, spatial_boxplot
import plotly.express as px

# ------------------------- Page Header -------------------------
st.title("🏠 Overview")

# ------------------------- Load Data -------------------------
df = load_engineered()
meta = load_station_meta()


col1, col2 = st.columns([1, 2])
with col1:
    col1_tab1, col1_tab2, col1_tab3, col1_tab4 = st.tabs(["About", "📈 Snapshot", "Time Summary", "ℹ️ PM2.5 Summary"])
    with col1_tab1:
        st.write("""
            Welcome to the **Beijing Clean Air Dashboard**, your interactive companion to the  
            **Beijing Air Quality Analysis & Forecasting** Capstone project.

            Use this dashboard to explore:
            - Seasonal, spatial, meteorological, and temporal pollution patterns  
            - Statistical validation of five hypotheses  
            - XGBoost-based PM2.5 forecasting  
            - Station-level clustering and PCA insights  
            """)
    with col1_tab2:
        # ------------------------- KPI Metrics -------------------------
        st.markdown("## 📊 Dataset Snapshot")

        k1, k2 = st.columns(2)
        k3, k4 = st.columns(2)
        
        k1.metric("Rows", f"{len(df):,}")
        k2.metric("Stations", df["station"].nunique())
        k3.metric("Years Covered", f"{df['year'].min()}–{df['year'].max()}")
        k4.metric("Features", df.shape[1])
    with col1_tab3:
        first_date = df['datetime'].min().date()
        last_date = df['datetime'].max().date()
        date_range = last_date - first_date

        st.metric("First Date", str(first_date))
        st.metric("Last Date", str(last_date))
        st.metric("Days Covered", f"{date_range.days:,}")
    with col1_tab4:
        # ------------------------- PM2.5 KPIs -------------------------
        st.markdown("## 🌫 PM2.5 Summary")

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
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌤 Seasonal Trends",
        "Monthly Trends",
        "📍 Spatial Variation",
        "🗺 Station Map",
    ])

    with tab1:
        st.subheader("Seasonal & Monthly Trends")
        st.plotly_chart(seasonal_boxplot(df), use_container_width=True)
    with tab2:
        st.subheader("Monthly PM2.5 Trends")
        st.plotly_chart(monthly_trend(df), use_container_width=True)
    with tab3:
        st.subheader("Spatial Variation Across Stations")
        st.plotly_chart(spatial_boxplot(df), use_container_width=True)
    with tab4:
        st.subheader("Interactive Station Map")
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
            mapbox_style="open-street-map",
            center={"lat": meta_map.latitude.mean(), "lon": meta_map.longitude.mean()},
            zoom=8,
            height=500,
        )

        fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))

        st.plotly_chart(fig_map, use_container_width=True)

# ------------------------- Footer -------------------------
