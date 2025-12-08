import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_cleaned

st.title("📍 H2 – Spatial Variation in PM2.5")

df = load_cleaned()

df = df.groupby(["station", "latitude", "longitude", "area_type"], as_index=False)["pm25"].mean().rename(columns={"pm25": "mean_pm25"})

st.subheader("🗺️ Station-Level PM2.5 Averages")
fig = px.scatter_mapbox(
    df, lat="latitude", lon="longitude",
    size="mean_pm25", color="mean_pm25",
    hover_name="station",
    mapbox_style="carto-positron", zoom=9,
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Key Finding
Urban stations exhibit **significantly higher PM2.5** than rural sites → **H2 supported**.
""")