import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_cleaned

st.title("⏳ H4 – Temporal Structure in PM2.5")

df = load_cleaned()



st.subheader("📊 Autocorrelation Plot")
fig = px.scatter(
    pd.DataFrame({
        "lag": [1, 3, 6, 12, 18],
        "autocorrelation": [df["pm25"].autocorr(lag=lag) for lag in [1, 3, 6, 12, 18]]
    }),
    x="lag",
    y="autocorrelation",
    title="Autocorrelation of PM2.5"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Key Insights
- Strong autocorrelation at short lags.
- Signifies PM2.5 depends strongly on recent values.
- Supports **H4: Temporal dependence exists**.
""")