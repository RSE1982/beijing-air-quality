import streamlit as st

st.set_page_config(page_title="Home — Beijing Clean Air Dashboard", page_icon="🏠")

st.title("🏠 Beijing Clean Air Dashboard")

st.markdown("""
Welcome to the **Beijing Clean Air Dashboard**, an interactive data analysis and forecasting tool 
developed as part of a Code Institute Data Analytics with AI Capstone Project.

This dashboard allows you to:

- Explore **seasonal**, **spatial**, **meteorological**, and **temporal** patterns in PM2.5  
- Evaluate five structured **hypotheses** using statistical evidence  
- Examine **station clustering** and spatial behaviour  
- Compare machine learning models for PM2.5 forecasting  
- Generate **short-term forecasts** for individual stations  

Use the left navigation menu to explore each section.
""")

st.divider()

st.subheader("📌 Quick Links")
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/overview.py", label="Overview", icon="📘")

with col2:
    st.page_link("pages/hypothesis1.py", label="Hypothesis 1", icon="❄️")

with col3:
    st.page_link("pages/forecasting.py", label="Forecasting", icon="📈")

