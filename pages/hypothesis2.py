"""
Hypothesis 2: Spatial Variation in PM2.5
This page examines the spatial distribution of PM2.5 across monitoring
stations in Beijing using average PM2.5 levels and a map visualization.
"""

import streamlit as st
from utils.data_loader import load_engineered, load_station_meta
from scipy import stats
import numpy as np
import pandas as pd
from utils.charts import (spatial_boxplot,
                          map_pm25_by_station,
                          violin_by_station,
                          area_boxplot,
                          violin_by_area_type)
from utils.eta_squared import eta_squared_anova


# Load data
df = load_engineered()
meta = load_station_meta()

# Prepare data for ANOVA
station_means = df.groupby("station")["pm25"].mean().reset_index()

# ANOVA for stations and area types
station_groups = [group["pm25"].dropna().values
                  for _, group in df.groupby("station", observed=False)
                  if group["pm25"].notna().sum() > 0]
area_groups = [
    group["pm25"].dropna().values
    for _, group in df.groupby("area_type", observed=False)
    if group["pm25"].notna().sum() > 0
    ]

# Perform ANOVA
f_stat_station, p_value_station = stats.f_oneway(*station_groups)
f_stat_area, p_value_area = stats.f_oneway(*area_groups)

# Calculate eta-squared effect sizes
eta_station = np.nan
eta_area = np.nan
eta_station = eta_squared_anova(station_groups)
eta_area = eta_squared_anova(area_groups)

# Compute station statistics
station_stats = df.groupby("station")["pm25"].agg(
            Mean="mean",
            Median="median",
            Std_Dev="std",
            Max="max",
            Min="min"
        ).reset_index()
# Prepare ANOVA results for display
anova_results = {
            "Stations": {
                "type": "Stations",
                "F-statistic": f_stat_station,
                "p-value": p_value_station,
                "eta-squared": eta_station
            },
            "Area Types": {
                "type": "Area Types",
                "F-statistic": f_stat_area,
                "p-value": p_value_area,
                "eta-squared": eta_area
            }
        }

# Compute area-type means
area_means = df.groupby("area_type")["pm25"].mean()
urban_mean = area_means.get("urban", float("nan"))
suburban_mean = area_means.get("suburban", float("nan"))
residential_mean = area_means.get("residential", float("nan"))

# Compute differences
urban_suburban_delta = urban_mean - suburban_mean
urban_residential_delta = urban_mean - residential_mean
suburban_residential_delta = suburban_mean - residential_mean

# Highest and lowest area-type averages
highest_area = area_means.idxmax()
lowest_area = area_means.idxmin()
highest_area_value = area_means.max()
lowest_area_value = area_means.min()


st.title(":material/cell_tower: Hypothesis 2")
st.latex(r"""

        \begin{aligned}
        H_0 &: \text{There is no significant difference in mean PM2.5 levels
            between monitoring stations or spatial categories.} \\
        H_1 &: \text{Mean PM2.5 levels differ significantly across monitoring
            stations and/or spatial categories.}
        \end{aligned}

        """)

col1, col2 = st.columns([1, 3])
with col1:
    st.subheader(":material/key: Key Metrics")
    colA, colB = st.columns(2)
    colA.metric("Highest Avg PM2.5 (Station)",
                f"{station_means['pm25'].max():.1f} µg/m³",
                station_means.loc[station_means['pm25'].idxmax(),
                                  'station'])

    colB.metric("Lowest Avg PM2.5 (Station)",
                f"{station_means['pm25'].min():.1f} µg/m³",
                station_means.loc[station_means['pm25'].idxmin(),
                                  'station'])
    colA, colB = st.columns(2)
    colA.metric("Highest Area-Type Mean",
                f"{highest_area_value:.1f} µg/m³",
                highest_area)

    colB.metric("Lowest Area-Type Mean",
                f"{lowest_area_value:.1f} µg/m³",
                lowest_area)

    st.success("""
        **Conclusion:**
        Hypothesis 2 is supported — PM2.5 levels differ significantly across
        monitoring stations and spatial area types, although the statistical
        effect size indicates that spatial location explains only a small
        portion of overall PM2.5 variability.
    """)
with col2:
    tab = st.tabs([":material/bar_chart_4_bars: Station Statistics",
                   ":material/bar_chart: Plot Station Boxplot",
                   ":material/bar_chart: Station Violin Plot",
                   ":material/map: Station Map",
                   ":material/bar_chart: Plot Area Boxplot",
                   ":material/bar_chart: Area Violin Plot",
                   ":material/analytics: ANOVA & Eta Squared"])
    with tab[0]:
        st.subheader(":material/bar_chart_4_bars:\
                      Station-wise PM2.5 Statistics")
        graph, info = st.columns([3, 2])
        with graph:
            st.dataframe(station_stats.style.format({
                "Mean": "{:.2f} µg/m³",
                "Median": "{:.2f} µg/m³",
                "Std_Dev": "{:.2f} µg/m³",
                "Max": "{:.2f} µg/m³",
                "Min": "{:.2f} µg/m³"
            }), use_container_width=True, hide_index=True)
        with info:
            st.markdown("""
                **What this shows:**
                This table summarises the mean, median, standard
                deviation, and range of PM2.5 for each of Beijing's
                12 monitoring stations. It highlights both central tendency
                and variability, making it easy to compare pollution levels
                between stations.

                **Why it matters:**
                Understanding basic descriptive statistics reveals which
                stations consistently experience higher or lower pollution
                and whether certain locations show more extreme PM2.5 spikes.
                This evidence directly supports assessing spatial variation.

                **Key takeaway:**
                Stations differ noticeably in both average PM2.5 and
                variability, suggesting that spatial location plays a
                meaningful role in pollution exposure.
                """)
    with tab[1]:
        # ------------------------- Charts -------------------------
        st.subheader(":material/bar_chart:\
                     Plot PM2.5 Variation Across 12 Stations")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(spatial_boxplot(df), use_container_width=True)
        with info:
            st.markdown("""
                **What this shows:**
                This boxplot visualises the distribution of PM2.5 levels for
                each station, showing medians, quartiles, and outliers. It
                reveals which stations experience more variability or more
                extreme pollution events.

                **Why it matters:**
                Boxplots are ideal for comparing multiple groups. They quickly
                show whether some stations have systematically higher typical
                PM2.5 or wider ranges, supporting the hypothesis of spatial
                differences.

                **Key takeaway:**
                Some stations — particularly urban ones — consistently show
                higher typical PM2.5 and a wider spread, reinforcing that
                spatial location impacts pollution intensity.
                """)
    with tab[2]:
        st.subheader(":material/bar_chart: PM2.5 Distribution by Station")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(violin_by_station(df), use_container_width=True)
        with info:
            st.markdown("""
                **What this shows:**
                This violin plot shows the full distribution density of PM2.5
                for each monitoring station. It highlights the shape of each
                station’s pollution distribution, including multimodal
                patterns.

                **Why it matters:**
                Density insights provide additional nuance beyond quartiles —
                for example, whether a station often experiences very high
                PM2.5 or if most values cluster at certain levels.

                **Key takeaway:**
                The distribution shapes differ notably between stations,
                indicating that pollution behaviour varies spatially, not
                just in averages but also in overall distribution patterns.
                """)
    with tab[3]:
        # Compute station averages
        st.subheader(":material/map: Average PM2.5 by Station on Map")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(map_pm25_by_station(station_means, meta),
                            use_container_width=True)
        with info:
            st.markdown("""
                        **What this shows:**
                        This map plots each monitoring station geographically
                        and colours/sizes them based on average PM2.5 levels.
                        It visualises spatial pollution patterns directly on
                        Beijing’s map.

                        **Why it matters:**
                        Mapping makes spatial variation immediately
                        interpretable — users can see whether high-pollution
                        stations cluster in certain city regions (e.g., urban
                        core vs. suburban outskirts).

                        **Key takeaway:**
                        High-PM2.5 stations tend to cluster in more urbanised
                        zones, supporting the hypothesis that geography
                        influences pollution levels.""")
    with tab[4]:
        st.subheader(":material/bar_chart: PM2.5 Variation Across Areas")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(area_boxplot(df), use_container_width=True)
        with info:
            st.markdown("""
                **What this shows:**
                This boxplot compares PM2.5 across Beijing’s area types
                (e.g., urban vs suburban vs other categories). It shows
                typical values and variability for each spatial classification.

                **Why it matters:**
                Area type generalises station-level insights and reveals
                structural spatial differences across the city. Urban areas
                often correlate with traffic density and local emissions.

                **Key takeaway:**
                Urban area types show higher median PM2.5 and more extreme
                values, confirming that broader spatial characteristics
                influence pollution levels.
                """)
    with tab[5]:
        st.subheader(":material/bar_chart: PM2.5 Distribution by Area")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(violin_by_area_type(df), use_container_width=True)
        with info:
            st.markdown("""
                **What this shows:**
                This violin plot shows the distribution density of PM2.5 for
                each area type, highlighting how pollution patterns differ
                between urban, suburban, and other categories.

                **Why it matters:**
                It reveals not just median differences but also distribution
                shapes — useful for understanding how often each area type
                experiences very high PM2.5.

                **Key takeaway:**
                Urban areas have a denser concentration of high-PM2.5 values,
                strengthening evidence that spatial characteristics are a
                major factor in pollution exposure.""")
    with tab[6]:
        st.subheader(":material/analytics: ANOVA & Effect Size")
        st.dataframe(pd.DataFrame(anova_results).T.style.format({
            "type": "{}",
            "F-statistic": "{:.4f}",
            "p-value": "{:.4e}",
            "eta-squared": "{:.4f}"
        }), use_container_width=True, hide_index=True)

        st.markdown("""
                    **What this shows:**
                    The table presents results from ANOVA tests comparing
                    PM2.5 across stations and area types, along with
                    eta-squared effect sizes indicating how much variance
                    each factor explains.

                    **Why it matters:**
                    ANOVA provides formal statistical evidence to confirm or
                    reject the hypothesis. Eta-squared quantifies how
                    meaningful the spatial differences are in practical terms.

                    **Key takeaway:**
                    Both ANOVA tests return statistically significant
                    differences, but the eta-squared values indicate a small
                    practical effect, meaning spatial patterns exist but other
                    factors (season, weather, temporal dynamics) explain much
                    more variance.""")
