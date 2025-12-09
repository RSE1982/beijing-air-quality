"""
Hypothesis 3: Meteorological Drivers of PM2.5
This page analyzes the relationship between PM2.5 levels and meteorological
variables like temperature, dew point, and wind speed using Spearman
correlation.
"""

import streamlit as st
from utils.load_data import load_cleaned
from utils.charts import corr_heatmap

st.title("🌦️ Hypothesis 3 — Meteorological Correlations")

df = load_cleaned()

st.write("""
### 📌 Hypothesis H3
**Meteorological variables strongly correlate with PM2.5.**

This hypothesis tests relationships using:
- temperature
- dew point
- pressure
- rainfall
- engineered interactions (temp × pres, dewpoint spread)
""")

# ------------------------- Correlation Heatmap -------------------------
st.subheader("📊 Correlation Matrix")
st.plotly_chart(corr_heatmap(df), use_container_width=True)

# ------------------------- Observations -------------------------
st.markdown("### 📝 Observations")
st.markdown("""
- Temperature and pressure both show **negative correlations** with PM2.5 —
            stable, cold conditions trap pollutants.
- Dew point and dewpoint spread show **moderate positive relationships**.
- Rainfall is negatively associated with PM2.5 due to washout effects.
- The engineered feature **temp × pressure** strengthens explanatory power.
""")

# ------------------------- Justification -------------------------
st.markdown("### 🎯 Justification")
st.markdown("""
The correlation structure aligns with physical meteorology:
cold, high-pressure systems with low wind speed favour pollution accumulation.
In Notebook 07, regression tests showed **significant contributions from
             meteorological variables**,
confirming their explanatory value.
""")

st.success("✔ **Conclusion:** H3 is supported — weather conditions\
            meaningfully influence PM2.5.")

st.caption("Source: Notebook 07 — Meteorological Analysis •\
            Dataset © Song Chen (CC BY 4.0)")
