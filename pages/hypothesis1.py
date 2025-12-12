"""
Hypothesis 1: Seasonal Patterns in PM2.5
This page analyzes the seasonal variation in PM2.5 levels in Beijing.
"""

import streamlit as st
from utils.data_loader import load_engineered
from utils.charts import (monthly_violin,
                          seasonal_boxplot,
                          monthly_trend,
                          yearly_trend)
import pingouin as pg

df = load_engineered()

st.title(":material/ac_unit: Hypothesis 1")
st.latex(r"""
         \begin{aligned}
         H_0 &: \text{There is no significant difference in mean PM2.5 levels
          between seasons.} \\
         H_1 &: \text{Mean PM2.5 levels differ significantly between seasons.}
         \end{aligned}
         """)

col1, col2 = st.columns([1, 2])
with col1:

    # -----------------------------------------------------
    # Summary Metrics
    # -----------------------------------------------------
    st.subheader(":material/thermostat: Season Averages")
    seasonal_avg = df.groupby("season")["pm25"].mean().round(1)
    colA, colB = st.columns(2)
    colA.metric("Winter avg PM2.5", f"{seasonal_avg['winter']}")
    colB.metric("Spring avg PM2.5", f"{seasonal_avg['spring']}")
    colA, colB = st.columns(2)
    colA.metric("Summer avg PM2.5", f"{seasonal_avg['summer']}")
    colB.metric("Autumn avg PM2.5", f"{seasonal_avg['autumn']}")

    # -----------------------------------------------------
    # Conclusion
    # -----------------------------------------------------
    st.success("""
        **Conclusion:**
        Hypothesis 1 is supported — PM2.5 levels vary strongly by season.
    """)

    with col2:
        tab = st.tabs([":material/partly_cloudy_day: Seasonal Boxplot",
                       ":material/calendar_month: Monthly Distribution",
                       ":material/calendar_month: Monthly Trend",
                       ":material/calendar_today: Yearly Trend",
                       ":material/assessment: ANOVA Test",])
        with tab[0]:
            st.subheader(":material/partly_cloudy_day:\
                         Seasonal PM2.5 Distribution")
            graph, info = st.columns([3, 2])
            with graph:
                st.plotly_chart(seasonal_boxplot(df), use_container_width=True)
            with info:
                st.markdown("""
                    **What this shows:**
                    This boxplot compares the distribution of PM2.5 values
                    across the four seasons.
                    Winter has the highest median and the largest spread,
                    including more extreme pollution spikes.
                    Summer displays the lowest concentrations with a much
                    narrower distribution.

                    **Why it matters:**
                    A clear ordering emerges (Winter > Autumn ≈
                    Spring > Summer), demonstrating that PM2.5 levels vary
                    strongly by season.

                    **Key takeaway:**
                    Season is a major driver of pollution levels, with winter
                    pollution being consistently and significantly higher.
                    """)
        with tab[1]:
            st.subheader(":material/calendar_month:\
                         Monthly PM2.5 Distribution")
            graph, info = st.columns([3, 2])
            with graph:
                st.plotly_chart(monthly_violin(df), use_container_width=True)
            with info:
                st.markdown("""
                    **What this shows:**
                    The violin plot visualises the full distribution of PM2.5
                    for each month.
                    It reveals a **smooth seasonal cycle**, with peaks around
                    December-January and troughs around July-August.

                    **Why it matters:**
                    Monthly patterns follow the same seasonal structure seen
                    in the boxplot, strengthening the evidence that pollution
                    varies systematically through the year.

                    **Key takeaway:**
                    Monthly patterns show a clear U-shaped seasonal cycle,
                    confirming strong periodic behaviour in PM2.5.
                    """)
        with tab[2]:
            st.subheader(":material/calendar_month: Monthly PM2.5 Trend")
            graph, info = st.columns([3, 2])
            with graph:
                st.plotly_chart(monthly_trend(df), use_container_width=True)
            with info:
                st.markdown("""
                    **What this shows:**
                    This trend line aggregates PM2.5 by month across all years
                    and highlights the overall monthly pattern.
                    Pollution gradually rises through autumn, peaks sharply in
                    winter, then falls through spring into summer.

                    **Why it matters:**
                    The smoothness of the curve confirms that the seasonal
                    effect is not random noise but a stable, repeating pattern
                    over multiple years.

                    **Key takeaway:**
                    PM2.5 follows a predictable seasonal rhythm, with winter
                    peaks and summer lows.
                    """)
        with tab[3]:
            st.subheader(":material/calendar_today: Yearly PM2.5 Trend")
            graph, info = st.columns([3, 2])
            with graph:
                st.plotly_chart(yearly_trend(df), use_container_width=True)
            with info:
                st.markdown("""
                    **What this shows:**
                    The yearly trend chart displays long-term changes in
                    average PM2.5 from 2013-2016.
                    The seasonal cycle repeats each year, but the year-to-year
                    trend shows a gradual downward shift in overall levels.

                    **Why it matters:**
                    This confirms that seasonal differences persist even when
                    accounting for longer-term improvements in Beijing air
                    quality policies.

                    **Key takeaway:**
                    Seasonal variation is consistent across years,
                    demonstrating that the effect is structural rather than
                    temporary.
                    """)
        with tab[4]:
            st.subheader(":material/assessment: ANOVA Test Results")
            anova_results = pg.anova(dv="pm25",
                                     between="season",
                                     data=df,
                                     detailed=True)
            st.dataframe(anova_results, hide_index=True,
                         use_container_width=True)
            st.markdown("""
            **What this shows:**
            A one-way ANOVA tests whether mean PM2.5 differs significantly
            between seasons.

            **Why it matters:**
            The test evaluates whether the visual differences seen in the
            plots reflect a real statistical effect.

            **Key takeaway:**
            """)
            p_value = anova_results["p-unc"][0]
            if p_value < 0.05:
                st.markdown(f"The p-value is {p_value:.4f}, which is less than\
                             0.05. We reject the null hypothesis and conclude\
                             that there are significant differences in mean\
                             PM2.5 levels between seasons.")
            else:
                st.markdown(f"The p-value is {p_value:.4f}, which is greater\
                              than 0.05. We fail to reject the null hypothesis\
                              and conclude that there are no significant\
                              differences in mean PM2.5 levels between\
                              seasons.")
