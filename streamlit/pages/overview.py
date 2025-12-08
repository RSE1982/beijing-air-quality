import streamlit as st
import plotly.express as px
from utils.load_data import load_cleaned

st.header("🏠 Overview – Beijing Clean Air Dashboard")

df = load_cleaned()

st.subheader("📌 Project Summary")
st.write("""
This dashboard presents a full analysis of Beijing air quality (PM2.5) 
using statistical testing, machine learning, clustering, and forecasting.
""")

st.subheader("📊 PM2.5 Distribution")
fig = px.histogram(df, x="pm25", nbins=60, title="PM2.5 Distribution")
st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
col1.metric("Mean PM2.5", f"{df.pm25.mean():.1f}")
col2.metric("Median PM2.5", f"{df.pm25.median():.1f}")
col3.metric("Max PM2.5", f"{df.pm25.max():.1f}")

st.info("Use the left navigation to explore each hypothesis and model.")