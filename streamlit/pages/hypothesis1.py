import streamlit as st
import plotly.express as px
from utils.load_data import load_cleaned

st.title("❄️ H1 – Seasonal Patterns in PM2.5")

df = load_cleaned()

st.subheader("📈 Seasonal PM2.5 Distribution")
fig = px.box(df, x="season", y="pm25", color="season", title="PM2.5 by Season")
st.plotly_chart(fig, use_container_width=True)

st.subheader("🔍 Interpretation")
st.markdown("""
- Winter shows the highest PM2.5 concentrations and greatest variability.
- Summer has consistently low PM2.5.
- This supports **H1: PM2.5 displays a strong seasonal pattern**.
""")