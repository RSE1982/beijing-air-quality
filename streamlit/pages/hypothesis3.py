import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_cleaned

st.title("🌦️ H3 – Meteorological Drivers of PM2.5")


df = load_cleaned()

df = df[["pm25", "temperature", "dew_point", "wind_speed"]].corr(method="spearman")["pm25"].reset_index()
df.columns = ["variable", "spearman_rho"]
df = df[df["variable"] != "pm25"]

st.subheader("🔗 Spearman Correlations")
st.dataframe(df)

fig = px.bar(df, x="variable", y="spearman_rho", title="Spearman Correlation with PM2.5")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Interpretation
- Dew Point has the strongest monotonic correlation with PM2.5.
- Temperature and Wind Speed are negatively correlated.
- Supports **H3: Meteorology is strongly linked to PM2.5**.
""")