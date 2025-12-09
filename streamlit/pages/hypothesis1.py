"""
Hypothesis 1: Seasonal Patterns in PM2.5
This page analyzes the seasonal variation in PM2.5 levels in Beijing.
"""

import streamlit as st
from utils.load_data import load_cleaned
from utils.charts import seasonal_boxplot, monthly_trend

col1, col2 = st.columns([1, 3])
with col1:
    st.title("❄️ Hypothesis 1")

    df = load_cleaned()

    st.write("""
    **PM2.5 levels show a strong seasonal pattern.**

    This hypothesis evaluates whether pollution systematically increases or
            decreases across the
    four meteorological seasons in Beijing.
    """)

    st.success("✔ **Conclusion:** H1 is supported — PM2.5 levels  \
    vary strongly by season.")

    st.caption("Source: Notebook 05 — Seasonal Analysis •  \
    Dataset © Song Chen (CC BY 4.0)")
    with col2:
        tab1, tab2, tab3 = st.tabs(["Seasonal Boxplot",
                                    "Monthly Trend",
                                    "Observations & Justification"])
        with tab1:
            st.subheader("📊 Seasonal PM2.5 Distribution")
            st.plotly_chart(seasonal_boxplot(df), use_container_width=True)
        with tab2:
            st.subheader("📈 Monthly PM2.5 Trend")
            st.plotly_chart(monthly_trend(df), use_container_width=True)
        with tab3:
            # ------------------------- Observations -------------------------
            st.markdown("### 📝 Observations")
            st.markdown("""
            - Winter (Dec–Feb) shows the **highest PM2.5 concentrations** with
                        frequent extreme values.
            - Summer (Jun–Aug) has the **lowest pollution**, reflecting strong
                        atmospheric dispersion.
            - Transitional seasons (spring/autumn) sit between these extremes.
            - Monthly trend shows a clear U-shaped cycle across the year.
            """)

            # ------------------------- Justification -------------------------
            st.markdown("### 🎯 Justification")
            st.markdown("""
                        These visual patterns indicate substantial seasonal
                        variation in air quality, driven bytemperature
                        inversions, coal heating, wind strength, and
                        atmospheric mixing conditions. The statistical
                        ANOVA test performed in the notebook showed
                        **significant differences between seasons
                        (p < 0.001)**.
            """)
