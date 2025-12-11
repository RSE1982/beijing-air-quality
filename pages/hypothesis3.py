"""
Hypothesis 3: Meteorological Drivers of PM2.5
This page analyzes the relationship between PM2.5 levels and meteorological
variables like temperature, dew point, and wind speed using Spearman
correlation.
"""

import streamlit as st
from utils.data_loader import load_engineered
from utils.charts import weather_distribution, weather_boxplot, corr_heatmap
import json
from pathlib import Path

df = load_engineered()
EXPLANATION_PATH = Path("streamlit/weather_explanations.json")

with open(EXPLANATION_PATH, "r") as f:
    WEATHER_EXPLANATIONS = json.load(f)

def get_weather_explanation(weather_var: str):
    """Return the explanation dict for the selected weather variable."""
    return WEATHER_EXPLANATIONS.get(weather_var, None)

weather_var = st.session_state.get("weather_filter", "temperature")

col1, col2 = st.columns([1, 3])
with col1:
    st.title("🌦️ Hypothesis 3")
    st.write("""
             **Meteorological variables strongly correlate with PM2.5.**
             This hypothesis tests relationships using:
             - temperature
             - dew point
             - pressure
             - rainfall
             - engineered interactions (temp × pres, dewpoint spread)
             """)
    st.info("✔ **Conclusion:** H3 is partially supported — some weather\
             variables correlate with PM2.5, but the effects vary in strength.")

    st.caption("Source: Notebook 07 — Meteorological Analysis •\
            Dataset © Song Chen (CC BY 4.0)")
with col2:
    tab1, tab2= st.tabs(["📈 Distributions",
                                "📊 Correlation Matrix"])
    with tab1:
        st.subheader("🔍 Weather Variable Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"📈 {weather_var.replace('_', ' ').title()} KDE plot")
            st.plotly_chart(weather_distribution(df, weather_var),
                        use_container_width=True)
        with col2:
            st.subheader(f"📊 {weather_var.replace('_', ' ').title()} Box Plot")
            st.plotly_chart(weather_boxplot(df, weather_var),
                        use_container_width=True)
        
        explanation = get_weather_explanation(weather_var)
        if explanation:
            st.markdown(f"""
            **What this shows:** {explanation["what"]}

            **Why it matters:** {explanation["why"]}

            **Key takeaway:** {explanation["takeaway"]}
            """)
    with tab2:
        # ------------------------- Correlation Heatmap ------------------
        st.subheader("📊 Correlation Matrix")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.plotly_chart(corr_heatmap(df), use_container_width=True)
        with col2:
            st.markdown("""
                        **What this shows:**
                        The correlation heatmap displays the strength and
                        direction of linear relationships between PM2.5 and a
                        range of meteorological variables. Each cell represents
                        a correlation coefficient, where values closer to +1
                        indicate strong positive relationships, values near -1
                        indicate strong negative relationships, and values
                        around 0 suggest little or no linear relationship.

                        **Why it matters:**
                        Understanding how weather variables correlate with
                        PM2.5 helps identify which atmospheric conditions have
                        the strongest influence on pollution levels. This
                        guides both the hypothesis evaluation and supports
                        feature selection for machine learning models. It also
                        helps distinguish meaningful drivers of PM2.5 from
                        variables that have little predictive value.
                        
                        **Key takeaway:**
                        The correlation heatmap provides a clear overview of
                        which meteorological factors are most closely
                        associated with PM2.5. Strong correlations suggest
                        potential causal links or conditions that consistently
                        accompany pollution events, while weak correlations
                        indicate limited influence on PM2.5 levels.
""")