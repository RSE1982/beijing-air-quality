"""Chart utility functions for visualizing PM2.5 data in Beijing."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np


# Hypothesis 1 Charts #
def seasonal_boxplot(df: pd.DataFrame) -> px.box:
    """
    Create a box plot of PM2.5 levels by season.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'season' and 'pm25' columns
    Returns:
        px.box: Plotly box plot figure
    """
    fig = px.box(
        df, x="season", y="pm25", color="season",
        labels={"season": "Season", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Season"
    )
    fig.update_layout(showlegend=False)
    return fig


def monthly_violin(df: pd.DataFrame) -> px.violin:
    """
    Create a violin plot of PM2.5 levels by month.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'month' and 'pm25' columns
    Returns:
        px.violin: Plotly violin plot figure
    """

    df["month_name"] = df["datetime"].dt.strftime("%B")

    fig = px.violin(
        df.sort_values("month"), x="month_name", y="pm25", color="month_name",
        labels={"month_name": "Month", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Month"
    )
    fig.update_layout(showlegend=False)
    return fig

def monthly_trend(df: pd.DataFrame) -> px.line:
    """
    Create a line plot showing the monthly trend of PM2.5 levels.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'month' and 'pm25' columns
    Returns:
        px.line: Plotly line plot figure
    """
    df["month_name"] = df["datetime"].dt.strftime("%B")
    monthly_trend = df.groupby(["year", "month", "month_name"],
                               as_index=False)["pm25"].mean()
    fig = px.line(monthly_trend,
                  x="month_name",
                  y="pm25",
                  color="year",
                  markers=True,
                  title="Monthly PM2.5 Trends by Year",
                  labels={
                      "month_name": "Month",
                      "pm25": "PM2.5 Levels (µg/m³)",
                      "year": "Year"
                      },
                  category_orders={
                      "month_name": [
                          "January", "February", "March",
                          "April", "May", "June",
                          "July", "August", "September",
                          "October", "November", "December"
                          ]})

    fig.update_layout(
        width=800,
        height=350,
        legend_title_text="Year"
    )
    return fig


def yearly_trend(df: pd.DataFrame) -> px.line:
    """
    Create a line plot showing the yearly trend of PM2.5 levels.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'year' and 'pm25' columns
    Returns:
        px.line: Plotly line plot figure
    """
    yearly_trend = df.groupby(['year', 'season'],
                              as_index=False)['pm25'].mean()
    fig = px.line(
        yearly_trend,
        x="season",
        y="pm25",
        markers=True,
        title="Yearly PM2.5 Trend",
        color="year",
        labels={
            "year": "Year",
            "pm25": "PM2.5 Levels (µg/m³)"
        }
    )

    fig.update_layout(
        width=800,
        height=400
    )
    return fig


# Hypothesis 2 Charts #
def spatial_boxplot(df: pd.DataFrame) -> px.box:
    """
    Create a box plot of PM2.5 levels across different stations.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'station' and 'pm25' columns
    Returns:
        px.box: Plotly box plot figure
    """
    return px.box(df, x="station", y="pm25",
                  title="PM2.5 Variation Across Stations")

def violin_by_station(df: pd.DataFrame) -> px.violin:
    """
    Create a violin plot of PM2.5 levels across different stations.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'station' and 'pm25' columns
    Returns:
        px.violin: Plotly violin plot figure
    """
    fig = px.violin(
        df, x="station", y="pm25", color="station",
        labels={"station": "Station", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Station"
    )
    fig.update_layout(showlegend=False)
    return fig

def map_pm25_by_station(df: pd.DataFrame, meta: pd.DataFrame) -> px.scatter_mapbox:
    """
    Create a map showing average PM2.5 levels by station.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'station' and 'pm25' columns
        meta (pd.DataFrame): DataFrame containing station metadata with
                             'station', 'latitude', and 'longitude' columns
    Returns:
        px.scatter_mapbox: Plotly scatter mapbox figure
    """
    fig = px.scatter_mapbox(
        meta.merge(df, on="station"),
        lat="latitude",
        lon="longitude",
        color="pm25",
        size="pm25",
        hover_name="station",
        zoom=8,
        height=500,
        range_color=[df["pm25"].min(), df["pm25"].max()],
        color_continuous_midpoint=df["pm25"].mean(),
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={"pm25": "Avg PM2.5 (µg/m³)"},
        mapbox_style="carto-positron",
        title="Average PM2.5 by Station"
    )
    fig.update_layout(margin={"r": 0,
                              "t": 30,
                              "l": 0,
                              "b": 0},
                      height=400,
                      width=1000)
    return fig


def area_boxplot(df: pd.DataFrame) -> px.box:
    """
    Create a box plot of PM2.5 levels across different area types.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'area_type' and 'pm25' columns
    Returns:
        px.box: Plotly box plot figure
    """
    fig = px.box(
        df, x="area_type", y="pm25",
        labels={"area_type": "Area Type", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Variation Across Area Types"
    )
    fig.update_layout(showlegend=False)
    return fig

def violin_by_area_type(df: pd.DataFrame) -> px.violin:
    """
    Create a violin plot of PM2.5 levels across different area types.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'area_type' and 'pm25' columns
    Returns:
        px.violin: Plotly violin plot figure
    """
    fig = px.violin(
        df, x="area_type", y="pm25", color="area_type",
        labels={"area_type": "Area Type", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Area Type"
    )
    fig.update_layout(showlegend=False)
    return fig


# Hypothesis 3 Charts #
def weather_distribution(df: pd.DataFrame, weather_var: str) -> px.histogram:
    """
    Create a histogram showing the distribution of a meteorological variable.
    Parameters:
        df (pd.DataFrame): DataFrame containing the weather variable column
        weather_var (str): The meteorological variable to plot
    Returns:
        px.histogram: Plotly histogram figure
    """
    data = df[weather_var].dropna().values.tolist()
    label = weather_var.replace("_", " ").title()

    data_min, data_max = np.min(data), np.max(data)
    bin_size = (data_max - data_min) / 30

    fig = ff.create_distplot(
        [data],
        [label],
        bin_size=bin_size,
        show_rug=False,
    )

    fig.update_layout(
        width=700,
        height=400,
        title=f"Distribution of {label}",
        showlegend=False,
        margin={"r": 0,
                "t": 30,
                "l": 0,
                "b": 0}
    )

    return fig

def weather_boxplot(df: pd.DataFrame, weather_var: str) -> px.box:
    """
    Create a single boxplot showing the distribution of one weather variable.
    """
    label = weather_var.replace("_", " ").title()

    fig = px.box(
        df,
        y=weather_var,
        labels={"y": label},
        title=f"Distribution of {label}",
        points="outliers"  # optional: shows outlier points
    )

    fig.update_layout(
        width=700,
        height=400,
        xaxis_visible=False,     # hides empty x-axis
        xaxis_showticklabels=False,
        showlegend=False,
        margin={"r": 0,
                "t": 30,
                "l": 0,
                "b": 0}
    )

    return fig


def corr_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create a heatmap of the correlation matrix for the DataFrame.
    Parameters:
        df (pd.DataFrame): DataFrame with numerical columns to correlate
    Returns:
        go.Figure: Plotly heatmap figure
    """
    vars = ["pm25",
            "temperature",
            "dew_point",
            "pressure",
            "rain",
            "wind_speed",
            "relative_humidity"]
    corr = df[vars].corr(numeric_only=True)
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu",
        reversescale=True
    ))
    fig.update_layout(title="Correlation Heatmap")
    return fig


# Hypothesis 4 Charts #


def temperal_variation(df: pd.DataFrame, value: str) -> px.line:
    """
    Create a line plot showing the hourly trend of PM2.5 levels.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'hour' and 'pm25' columns
    Returns:
        px.line: Plotly line plot figure
    """
    variation = df.groupby([value], as_index=False)['pm25'].mean().reset_index()
    fig = px.line(
        variation,
        x=value,
        y="pm25",
        markers=True,
        title=f"{value.capitalize()} PM2.5 Variation",
        labels={
            value: value.replace("_", " ").capitalize(),
            "pm25": "PM2.5 Levels (µg/m³)"
        }
    )

    fig.update_layout(
        width=800,
        height=400,
        margin={"r": 0,
                "t": 30,
                "l": 0,
                "b": 0}
    )

    return fig

### Hypothesis 5 Charts #

def plot_actual_vs_pred(y_true, baseline_pred, lag_pred, n=300):
    """Reproduce the Matplotlib actual vs predicted plot using Plotly."""
    
    fig = go.Figure()

    # Actual
    fig.add_trace(go.Scatter(
        y=y_true[:n],
        mode="lines",
        name="Actual",
        line=dict(color="green", width=2)
    ))

    # Baseline prediction
    fig.add_trace(go.Scatter(
        y=baseline_pred[:n],
        mode="lines",
        name="Baseline Prediction",
        line=dict(color="blue", width=2),
        opacity=0.8
    ))

    # Lag-based prediction
    fig.add_trace(go.Scatter(
        y=lag_pred[:n],
        mode="lines",
        name="Lag Model Prediction",
        line=dict(color="orange", width=2),
        opacity=0.8
    ))

    fig.update_layout(
        title="PM2.5: Actual vs Predicted",
        xaxis_title="Time Index (sample)",
        yaxis_title="PM2.5 (µg/m³)",
        legend=dict(x=0, y=1),
        height=400,
    )

    return fig


def befere_vs_after(baseline_mae, baseline_rmse, baseline_r2,
                    lag_mae, lag_rmse, lag_r2):
    """Bar charts comparing model performance metrics."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["MAE", "RMSE", "R²"],
        y=[baseline_mae, baseline_rmse, baseline_r2],
        name="Baseline",
        marker_color="indianred"
    ))

    fig.add_trace(go.Bar(
        x=["MAE", "RMSE", "R²"],
        y=[lag_mae, lag_rmse, lag_r2],
        name="Lag-Based",
        marker_color="seagreen"
    ))

    fig.update_layout(
        title="📉 Baseline vs Lag-Based Model Performance",
        barmode="group",
        yaxis_title="Error / Score",
    )

    return fig


def plot_lag_feature_importances(fi: pd.DataFrame):
    fig = px.bar(
        fi.sort_values("importance", ascending=True),
        x="importance",
        y="feature",
        orientation="h",
        title="Lag Model Feature Importances",
        labels={"importance": "Importance", "feature": "Feature"},
    )
    fig.update_layout(
        height=400,
        margin={"r": 0,
                "t": 30,
                "l": 0,
                "b": 0})
    return fig
