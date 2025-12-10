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
