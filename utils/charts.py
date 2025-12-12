"""Chart utility functions for visualizing PM2.5 data in Beijing."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np

MARGINS = {"r": 0,
           "t": 30,
           "l": 0,
           "b": 0}  # Common margin settings for all charts


# Hypothesis 1 Charts #
def seasonal_boxplot(df: pd.DataFrame) -> px.box:
    """
    Create a box plot of PM2.5 levels by season.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'season' and 'pm25' columns
    Returns:
        px.box: Plotly box plot figure
    """

    # Create box plot
    fig = px.box(
        df, x="season", y="pm25", color="season",
        labels={"season": "Season", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Season"
    )

    # Update layout
    fig.update_layout(showlegend=False,
                      margin=MARGINS)
    return fig


def monthly_violin(df: pd.DataFrame) -> px.violin:
    """
    Create a violin plot of PM2.5 levels by month.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'month' and 'pm25' columns
    Returns:
        px.violin: Plotly violin plot figure
    """

    # Convert month number to name
    df["month_name"] = df["datetime"].dt.strftime("%B")

    # Create violin plot
    fig = px.violin(
        df.sort_values("month"), x="month_name", y="pm25", color="month_name",
        labels={"month_name": "Month", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Month"
    )

    # Update layout
    fig.update_layout(showlegend=False,
                      margin=MARGINS)

    return fig


def monthly_trend(df: pd.DataFrame) -> px.line:
    """
    Create a line plot showing the monthly trend of PM2.5 levels.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'month' and 'pm25' columns
    Returns:
        px.line: Plotly line plot figure
    """

    # Convert month number to name
    df["month_name"] = df["datetime"].dt.strftime("%B")

    # Create monthly trend line plot
    monthly_trend = df.groupby(["year", "month", "month_name"],
                               as_index=False)["pm25"].mean()

    # Create line plot
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

    # Update layout
    fig.update_layout(
        width=800,
        height=350,
        legend_title_text="Year",
        margin=MARGINS
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

    # Create yearly trend line plot
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

    # Update layout
    fig.update_layout(
        width=800,
        height=400,
        margin=MARGINS,
        legend_title_text="Year"
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

    # Create box plot
    fig = px.box(df, x="station", y="pm25",
                 title="PM2.5 Variation Across Stations")

    # Update layout
    fig.update_layout(showlegend=False,
                      margin=MARGINS)

    return fig


def violin_by_station(df: pd.DataFrame) -> px.violin:
    """
    Create a violin plot of PM2.5 levels across different stations.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'station' and 'pm25' columns
    Returns:
        px.violin: Plotly violin plot figure
    """

    # Create violin plot
    fig = px.violin(
        df, x="station", y="pm25", color="station",
        labels={"station": "Station", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Station"
    )

    # Update layout
    fig.update_layout(showlegend=False,
                      margin=MARGINS)

    return fig


def map_pm25_by_station(df: pd.DataFrame,
                        meta: pd.DataFrame) -> px.scatter_mapbox:
    """
    Create a map showing average PM2.5 levels by station.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'station' and 'pm25' columns
        meta (pd.DataFrame): DataFrame containing station metadata with
                             'station', 'latitude', and 'longitude' columns
    Returns:
        px.scatter_mapbox: Plotly scatter mapbox figure
    """

    # Create map plot
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

    # Update layout
    fig.update_layout(margin=MARGINS,
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

    # Create box plot
    fig = px.box(
        df, x="area_type", y="pm25",
        labels={"area_type": "Area Type", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Variation Across Area Types"
    )

    # Update layout
    fig.update_layout(showlegend=False,
                      margin=MARGINS)
    return fig


def violin_by_area_type(df: pd.DataFrame) -> px.violin:
    """
    Create a violin plot of PM2.5 levels across different area types.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'area_type' and 'pm25' columns
    Returns:
        px.violin: Plotly violin plot figure
    """

    # Create violin plot
    fig = px.violin(
        df, x="area_type", y="pm25", color="area_type",
        labels={"area_type": "Area Type", "pm25": "PM2.5 Levels (µg/m³)"},
        title="PM2.5 Distribution by Area Type"
    )

    # Update layout
    fig.update_layout(showlegend=False,
                      margin=MARGINS)
    return fig


# Hypothesis 3 Charts #
def weather_distribution(df: pd.DataFrame,
                         weather_var: str) -> px.histogram:
    """
    Create a histogram showing the distribution of a meteorological variable.
    Parameters:
        df (pd.DataFrame): DataFrame containing the weather variable column
        weather_var (str): The meteorological variable to plot
    Returns:
        px.histogram: Plotly histogram figure
    """

    # Prepare data
    data = df[weather_var].dropna().values.tolist()

    # Create label
    label = weather_var.replace("_", " ").title()

    # calculate bin size using Freedman-Diaconis rule
    data_min, data_max = np.min(data), np.max(data)
    bin_size = (data_max - data_min) / 30

    # Create histogram
    fig = ff.create_distplot(
        [data],
        [label],
        bin_size=bin_size,
        show_rug=False,
    )

    # Update layout
    fig.update_layout(
        width=700,
        height=400,
        title=f"Distribution of {label}",
        showlegend=False,
        margin=MARGINS
    )

    return fig


def weather_boxplot(df: pd.DataFrame, weather_var: str) -> px.box:
    """
    Create a single boxplot showing the distribution of one weather variable.
    Parameters:
        df (pd.DataFrame): DataFrame containing the weather variable column
        weather_var (str): The meteorological variable to plot
    Returns:
        px.box: Plotly box plot figure
    """

    # Create label
    label = weather_var.replace("_", " ").title()

    # Create box plot
    fig = px.box(
        df,
        y=weather_var,
        labels={"y": label},
        title=f"Distribution of {label}",
        points="outliers"
    )

    # Update layout
    fig.update_layout(
        width=700,
        height=400,
        xaxis_visible=False,
        xaxis_showticklabels=False,
        showlegend=False,
        margin=MARGINS
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

    # Select relevant variables for correlation
    vars = ["pm25",
            "temperature",
            "dew_point",
            "pressure",
            "rain",
            "wind_speed",
            "relative_humidity"]
    corr = df[vars].corr(numeric_only=True)

    # Create heatmap
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu",
        reversescale=True
    ))

    # Update layout
    fig.update_layout(title="Correlation Heatmap",
                      width=800,
                      height=400,
                      margin=MARGINS)
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

    # calculate variation
    variation = df.groupby([value],
                           as_index=False)['pm25'].mean().reset_index()

    # Create line plot
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

    # Update layout
    fig.update_layout(
        width=800,
        height=400,
        margin=MARGINS
    )

    return fig


# Hypothesis 5 Charts #
def plot_actual_vs_pred(y_true: list,
                        baseline_pred: list,
                        lag_pred: list, n=300) -> go.Figure:
    """Reproduce the Matplotlib actual vs predicted plot using Plotly.
     Parameters:
        y_true (array-like): Actual PM2.5 values
        baseline_pred (array-like): Baseline model predictions
        lag_pred (array-like): Lag-based model predictions
        n (int): Number of samples to plot
    Returns:
        go.Figure: Plotly figure object
    """

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

    # Update layout
    fig.update_layout(
        title="PM2.5: Actual vs Predicted",
        xaxis_title="Time Index (sample)",
        yaxis_title="PM2.5 (µg/m³)",
        legend=dict(x=0, y=1),
        height=400,
        width=800,
        margin=MARGINS
    )

    return fig


def befere_vs_after(baseline_mae: float,
                    baseline_rmse: float,
                    baseline_r2: float,
                    lag_mae: float,
                    lag_rmse: float,
                    lag_r2: float) -> go.Figure:
    """
    Create a bar chart comparing baseline and lag-based model performance.
    Parameters:
        baseline_mae (float): Baseline model MAE
        baseline_rmse (float): Baseline model RMSE
        baseline_r2 (float): Baseline model R²
        lag_mae (float): Lag-based model MAE
        lag_rmse (float): Lag-based model RMSE
        lag_r2 (float): Lag-based model R²
    Returns:
        go.Figure: Plotly bar chart figure"""

    # Create bar chart
    fig = go.Figure()

    # Baseline bars
    fig.add_trace(go.Bar(
        x=["MAE", "RMSE", "R²"],
        y=[baseline_mae, baseline_rmse, baseline_r2],
        name="Baseline",
        marker_color="indianred"
    ))

    # Lag-based bars
    fig.add_trace(go.Bar(
        x=["MAE", "RMSE", "R²"],
        y=[lag_mae, lag_rmse, lag_r2],
        name="Lag-Based",
        marker_color="seagreen"
    ))

    # Update layout
    fig.update_layout(
        title="📉 Baseline vs Lag-Based Model Performance",
        barmode="group",
        yaxis_title="Error / Score",
        height=400,
        width=700,
        margin=MARGINS
    )

    return fig


def plot_lag_feature_importances(fi: pd.DataFrame) -> px.bar:
    """
    Create a horizontal bar chart of lag feature importances.
    Parameters:
        fi (pd.DataFrame): DataFrame containing
        'feature' and 'importance' columns
    Returns:
        px.bar: Plotly bar chart figure
    """

    # Create bar chart
    fig = px.bar(
        fi.sort_values("importance", ascending=True),
        x="importance",
        y="feature",
        orientation="h",
        title="Lag Model Feature Importances",
        labels={"importance": "Importance", "feature": "Feature"},
    )

    # Update layout
    fig.update_layout(
        height=400,
        margin=MARGINS)

    return fig
