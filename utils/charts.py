"""Chart utility functions for visualizing PM2.5 data in Beijing."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def seasonal_boxplot(df: pd.DataFrame) -> px.box:
    """
    Create a box plot of PM2.5 levels by season.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'season' and 'pm25' columns
    Returns:
        px.box: Plotly box plot figure
    """
    return px.box(
        df, x="season", y="pm25", color="season",
        title="PM2.5 Distribution by Season",
    )


def monthly_trend(df: pd.DataFrame) -> px.line:
    """
    Create a line plot showing the monthly trend of PM2.5 levels.
    Parameters:
        df (pd.DataFrame): DataFrame containing 'month' and 'pm25' columns
    Returns:
        px.line: Plotly line plot figure
    """
    monthly = df.groupby("month")["pm25"].mean().reset_index()
    return px.line(monthly, x="month", y="pm25",
                   title="Monthly PM2.5 Trend", markers=True)


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


def corr_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create a heatmap of the correlation matrix for the DataFrame.
    Parameters:
        df (pd.DataFrame): DataFrame with numerical columns to correlate
    Returns:
        go.Figure: Plotly heatmap figure
    """
    corr = df.corr(numeric_only=True)
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="RdBu",
        reversescale=True
    ))
    fig.update_layout(title="Correlation Heatmap")
    return fig
