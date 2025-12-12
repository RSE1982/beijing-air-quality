"""
Hypothesis 3: Meteorological Drivers of PM2.5
This page analyzes the relationship between PM2.5 levels and meteorological
variables like temperature, dew point, and wind speed using Spearman
correlation.
"""

import streamlit as st
from utils.data_loader import load_engineered
from utils.charts import weather_distribution, weather_boxplot, corr_heatmap
import numpy as np
from scipy import stats
import json
from pathlib import Path

df = load_engineered()
EXPLANATION_PATH = Path("streamlit/weather_explanations.json")


with open(EXPLANATION_PATH, "r") as f:
    WEATHER_EXPLANATIONS = json.load(f)


def get_weather_explanation(weather_var: str) -> dict:
    """
    Return the explanation dict for the selected weather variable.
    Args:
        weather_var (str): The weather variable name.
    Returns:
        dict: Explanation dictionary with 'what', 'why', and 'takeaway' keys.
    """
    return WEATHER_EXPLANATIONS.get(weather_var, None)


weather_var = st.session_state.get("weather_filter", "temperature")
weather_vars = [
    "temperature",
    "dew_point",
    "pressure",
    "rain",
    "wind_speed",
    "relative_humidity",
]

# Compute simple Pearson correlations against pm25
corrs = {}
pvals = {}

for var in weather_vars:
    valid = df[[var, "pm25"]].dropna()
    r, p = stats.pearsonr(valid[var], valid["pm25"])
    corrs[var] = r
    pvals[var] = p

# Strongest positive and negative
strongest_pos = max(corrs, key=lambda v: corrs[v])
strongest_neg = min(corrs, key=lambda v: corrs[v])

# Count significant variables
sig_vars = [v for v in weather_vars if pvals[v] < 0.05]
n_sig = len(sig_vars)

avg_abs_corr = np.mean([abs(corrs[v]) for v in weather_vars])


st.title(":material/weather_mix: Hypothesis 3")
st.latex(r"""
    \begin{aligned}
H_0 &: \text{There is no statistically significant relationship between
         meteorological variables and PM2.5 levels.} \\
H_1 &: \text{Meteorological variables show statistically significant linear or
         monotonic relationships with PM2.5 levels.}
\end{aligned}
""")
col1, col2 = st.columns([1, 3])
with col1:
    st.subheader(":material/key: Key Metrics")
    cola, colb = st.columns(2)
    with cola:
        st.metric("Strongest + corr with PM2.5",
                  f"{corrs[strongest_pos]:.2f}",
                  strongest_pos.replace("_", " ").title())
    with colb:
        st.metric("Strongest − corr with PM2.5",
                  f"{corrs[strongest_neg]:.2f}",
                  strongest_neg.replace("_", " ").title())
    cola, colb = st.columns(2)
    with cola:
        st.metric("Significant weather vars (p < 0.05)",
                  f"{n_sig} / {len(weather_vars)}")
    with colb:
        st.metric("Mean |corr| with PM2.5",
                  f"{avg_abs_corr:.2f}")
    st.info("""
        **Conclusion:**
        Hypothesis 3 is partially supported. Several meteorological variables
        show statistically significant correlations with PM2.5 levels,
        indicating that certain weather conditions influence air pollution,
        though not all variables exhibit strong or consistent effects.
    """)
with col2:
    tab1, tab2 = st.tabs([":material/finance_mode: Weather Variable Analysis",
                         ":material/scatter_plot: Correlation Matrix"])
    with tab1:
        st.subheader(":material/weather_mix: Weather Variable Analysis")
        col1, col2 = st.columns([3, 2])
        with col1:
            tabA, tabB = st.tabs([":material/bar_chart: Distribution Plot",
                                  ":material/bar_chart: Box Plot"])
            with tabA:
                st.plotly_chart(weather_distribution(df, weather_var),
                                use_container_width=True)
            with tabB:
                st.plotly_chart(weather_boxplot(df, weather_var),
                                use_container_width=True)
        with col2:
            explanation = get_weather_explanation(weather_var)
            if explanation:
                st.markdown(f"""
                **What this shows:** {explanation["what"]}

                **Why it matters:** {explanation["why"]}

                **Key takeaway:** {explanation["takeaway"]}
                """)
    with tab2:
        # ------------------------- Correlation Heatmap ------------------
        st.subheader(":material/scatter_plot: Correlation Matrix")
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
