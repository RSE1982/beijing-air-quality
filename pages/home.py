import streamlit as st

# Introduction Section
st.markdown("""
Welcome to the **Beijing Clean Air Dashboard**, an interactive data analysis
            and forecasting tool
developed as part of a Code Institute Data Analytics with AI Capstone Project.

This dashboard allows you to:

- Explore **seasonal**, **spatial**, **meteorological**, and **temporal**
            patterns in PM2.5
- Evaluate five structured **hypotheses** using statistical evidence
- Examine **station clustering** and spatial behaviour
- Compare machine learning models for PM2.5 forecasting
- Generate **short-term forecasts** for individual stations

Use the left navigation menu to explore each section.
""")

st.divider()

# Quick Links Section
st.subheader(":material/keep: Quick Links")
col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/overview.py", label="Overview", icon=":material/book:")
with col2:
    st.page_link("pages/hypothesis1.py", label="Hypothesis 1",
                 icon=":material/ac_unit:")

with col3:
    st.page_link("pages/forecasting.py", label="Forecasting",
                 icon=":material/trending_up:")
