"""
Hypothesis 4: Temporal Structure in PM2.5
This page examines the temporal dependence in PM2.5 levels in Beijing.
"""

import streamlit as st
from utils.data_loader import load_engineered
from scipy.stats import spearmanr
import pandas as pd
from utils.charts import temperal_variation

df = load_engineered()

st.title("⏳ Hypothesis 4")

st.latex(r"""
    \begin{aligned}
H_0 &: \text{PM2.5 levels do not exhibit temporal structure.} \\
H_1 &: \text{PM2.5 levels show significant temporal patterns such as daily, monthly, or seasonal cycles.}
\end{aligned}
""")

col1, col2 = st.columns([1, 3])
with col1:
    time_vars = ["hour", "day_of_week", "month", "year"]

    results = {}
    sig_count = 0

    for var in time_vars:
        coef, p = spearmanr(df["pm25"], df[var])
        results[var] = {"coef": coef, "p": p}
        if p < 0.05:
            sig_count += 1

    # strongest + weakest correlations
    strongest_var = max(results.keys(), key=lambda v: abs(results[v]["coef"]))
    weakest_var = min(results.keys(), key=lambda v: abs(results[v]["coef"]))

    corr_range = abs(results[strongest_var]["coef"]) - abs(results[weakest_var]["coef"])

    st.metric(
        "Strongest Temporal Correlation",
        f"{results[strongest_var]['coef']:.2f}",
        strongest_var.replace("_", " ").title()
    )

    st.metric(
        "Weakest Temporal Correlation",
        f"{results[weakest_var]['coef']:.2f}",
        weakest_var.replace("_", " ").title()
    )

    st.metric(
        "Significant Temporal Patterns (p < 0.05)",
        f"{sig_count} / {len(time_vars)}"
    )

    st.metric(
        "Temporal Correlation Range",
        f"{corr_range:.2f}"
    )
with col2:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Hourly Variation",
                                            "Day of Week Variation",
                                            "Monthly Variation",
                                            "Yearly Variation",
                                            "Spearman Correlation"])
    with tab1:
        colA, colB = st.columns([3, 2])
        with colA:
            st.markdown("### 📈 Hourly Trends in PM2.5")
            st.plotly_chart(temperal_variation(df, "hour"), 
                            use_container_width=True)
        with colB:
            st.markdown("""
            **What this shows:**
            How PM2.5 levels change throughout a 24-hour period, 
            revealing typical daily pollution cycles.
            
            **Why it matters:**
            Hourly trends highlight human activity patterns (traffic peaks,
            heating use) and atmospheric behaviours like nighttime stagnation
            or daytime mixing.

            **Key takeaway:**
            PM2.5 often follows a predictable daily rhythm, with identifiable
            high- and low-pollution hours linked to routine human and
            atmospheric cycles.
        """)
    with tab2:
        colA, colB = st.columns([3, 2])
        with colA:
            st.markdown("### 📊 Day-of-Week Trends in PM2.5")
            st.plotly_chart(temperal_variation(df, "day_of_week"),
                            use_container_width=True)
        with colB:
            st.markdown("""
            **What this shows:**
            A comparison of PM2.5 levels across different days of the week.

            **Why it matters:**
            Day-of-week patterns can reveal the influence of work schedules,
            industrial activity, and weekend behavioural changes on air quality.

            **Key takeaway:**
            Understanding day-of-week trends helps identify periods of 
            elevated pollution linked to human routines, guiding targeted 
            mitigation efforts.
        """)
    with tab3:
        colA, colB = st.columns([3, 2])
        with colA:
            st.markdown("### 📉 Monthly Trends in PM2.5")
            st.plotly_chart(temperal_variation(df, "month"), 
                            use_container_width=True)
        with colB:
            st.markdown("""
            **What this shows:**
            How PM2.5 levels change throughout the months of the year, 
            reflecting seasonal patterns.

            **Why it matters:**
            Seasonal variations can indicate the influence of weather, 
            heating, and agricultural activities on air quality.

            **Key takeaway:**
            Recognizing monthly trends helps anticipate periods of 
            higher pollution and plan seasonal interventions.
        """)
    with tab4:
        colA, colB = st.columns([3, 2])
        with colA:
            st.markdown("### 📆 Yearly Trends in PM2.5")
            st.plotly_chart(temperal_variation(df, "year"), 
                            use_container_width=True)
        with colB:
            st.markdown("""
            **What this shows:**
            How PM2.5 levels change across different years, 
            indicating long-term trends.

            **Why it matters:**
            Yearly variations can reflect the impact of policy changes, 
            economic shifts, and long-term environmental factors.

            **Key takeaway:**
            Understanding yearly trends helps evaluate the effectiveness 
            of air quality interventions and identify persistent challenges.
        """)
    with tab5:
        colA, colB = st.columns([3, 2])
        with colA:
            time_vars = ["hour", "month", "day_of_week", "year"]

            results = []

            for var in time_vars:
                coef, p = spearmanr(df["pm25"], df[var])
                results.append({"Variable": var, "Spearman ρ": coef, "p-value": p})

            spearman_time_df = pd.DataFrame(results)

            st.dataframe(spearman_time_df.style.format({"Spearman ρ": "{:.3f}", 
                                                        "p-value": "{:.3f}"}),
                        use_container_width=True)
        with colB:
            st.markdown("""
            **What this shows:**
            A table of Spearman rank correlations between PM2.5 and each
            temporal variable (hour, day, month, year).
                        
            **Why it matters:**
            Spearman correlation measures how strongly PM2.5 follows monotonic
            trends across time-related cycles. It provides statistical confirmation
            of visible patterns.
                        
            **Key takeaway:**
            The correlation values quantify how PM2.5 varies across hourly, 
            weekly, monthly, and yearly patterns, supporting the evidence
            for temporal structure in the dataset.
        """)
