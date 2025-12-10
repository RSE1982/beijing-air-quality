"""
Hypothesis 4: Temporal Structure in PM2.5
This page examines the temporal dependence in PM2.5 levels in Beijing.
"""

import streamlit as st
from utils.data_loader import load_engineered
import plotly.express as px


df = load_engineered()

col1, col2 = st.columns([1, 3])
with col1:
    st.title("⏳ Hypothesis 4")
    st.write("""
    ### 📌 Hypothesis H4
    **Temporal structure (hour-of-day, day-of-week, month) explains variation
            in PM2.5.**

    This uses engineered cyclical encodings:
    - hour_sin, hour_cos
    - month_sin, month_cos
    - day_of_week
    """)

    st.success("✔ **Conclusion:** H4 is supported — temporal structure\
                strongly explains PM2.5 variation.")

    st.caption("Source: Notebook 08 — Temporal Analysis \
            • Dataset © Song Chen (CC BY 4.0)")
with col2:
    tab1, tab2, tab3 = st.tabs(["Temporal Trends",
                                "Day of Week Trends",
                                "Observations & Justification"])
    with tab1:
        st.markdown("### 📈 Temporal Trends in PM2.5")
        hourly = df.groupby("hour")["pm25"].mean().reset_index()
        fig_hour = px.line(hourly, x="hour", y="pm25", markers=True,
                           title="Average PM2.5 by Hour of Day")
        st.plotly_chart(fig_hour, use_container_width=True)
    with tab2:
        st.markdown("### 📊 Day-of-Week Trends in PM2.5")
        dow = df.groupby("day_of_week")["pm25"].mean().reset_index()
        fig_dow = px.bar(dow, x="day_of_week", y="pm25",
                         title="Average PM2.5 by Day of Week")
        st.plotly_chart(fig_dow, use_container_width=True)
    with tab3:
        st.markdown("### 📝 Observations")
        st.markdown("""
        - PM2.5 rises sharply during **morning and evening peaks**, consistent
                    with traffic and atmospheric stability cycles.
        - Weekends often show **lower pollution**, indicating weekday human
                    activity as a contributor.
        - Monthly cyclical encoding reinforces seasonal behaviour observed in
                    H1.
        """)
        st.markdown("### 🎯 Justification")
        st.markdown("""
        Autocorrelation and cyclical feature tests in the notebook revealed
        predictable temporal dependencies.
        Temporal encodings improve model accuracy by capturing repeating
                    daily/monthly structure.
        """)
