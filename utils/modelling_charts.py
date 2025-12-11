"""
Utility functions for creating modelling-related charts using Plotly.
"""

import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from utils.charts import MARGINS


def bar_chart(df, metric: str = "RMSE") -> px.bar:
    """
    Creates a horizontal bar chart ranking models based on a specified metric.
    Args:
        df (pd.DataFrame): DataFrame containing model names and their metrics.
        metric (str): The metric to rank models by (default is "RMSE").
    Returns:
        px.bar: A Plotly bar chart figure.
    """
    fig = px.bar(
            df,
            x=metric,
            y="Model",
            orientation="h",
            title=f"Model {metric} Ranking",
            labels={metric: f"{metric}", "Model": "Model"},
            color="Model",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    fig.update_layout(margin=MARGINS, height=400)
    return fig


def prediction_vs_actual_chart(actual: list, predicted: list) -> px.scatter:
    """
    Creates a scatter plot comparing predicted values against actual values.
    Args:
        actual (array-like): Actual target values.
        predicted (array-like): Predicted target values from the model.
    Returns:
        px.scatter: A Plotly scatter plot figure.
    """
    fig = px.scatter(
        x=actual[:300],
        y=predicted[:300],
        title="Prediction vs Actual",
        labels={"Actual": "Actual Values", "Predicted": "Predicted Values"},
        trendline="ols",
    )  # define parameters of the scatter plot

    # Customize trendline appearance
    for trace in fig.data:
        if trace.mode == "lines":
            trace.line.color = "red"
            trace.line.width = 3

    fig.update_layout(margin=MARGINS,
                      height=500)  # set layout properties
    return fig  # return the figure


def residuals_distribution_chart(residuals: list) -> px.histogram:
    """
    Creates a distribution plot of residuals.
    Args:
        residuals (array-like): Residuals from the model predictions.
    Returns:
        px.histogram: A Plotly histogram figure.
    """
    binsize = residuals.std() / 5
    fig = ff.create_distplot(
        [residuals],
        group_labels=["Residuals"],
        bin_size=binsize,
        show_hist=True,
        show_rug=False
    )
    fig.update_layout(
        title="Residuals Distribution",
        xaxis_title="Residuals",
        margin=MARGINS,
        height=500,
        showlegend=False
    )
    return fig


def residuals_vs_predicted_chart(residuals: list,
                                 predicted: list) -> px.scatter:
    """
    Creates a scatter plot of residuals versus predicted values.
    Args:
        residuals (array-like): Residuals from the model predictions.
        predicted (array-like): Predicted target values from the model.
    Returns:
        px.scatter: A Plotly scatter plot figure.
    """
    fig = px.scatter(
        x=predicted,
        y=residuals,
        title="Residuals vs Predicted",
        labels={"x": "Predicted Values", "y": "Residuals"},
        trendline="ols",
    )
    for trace in fig.data:
        if trace.mode == "lines":
            trace.line.color = "red"
            trace.line.width = 3
    fig.update_layout(margin=MARGINS, height=500)
    return fig


def feature_importance_chart(feature_imp: pd.DataFrame) -> px.bar:
    """
    Creates a horizontal bar chart of the top 10 feature importances.
    Args:
        feature_imp (pd.DataFrame): DataFrame containing features and their
        importance scores.
    Returns:
        px.bar: A Plotly bar chart figure.
    """
    fi = feature_imp.sort_values("importance", ascending=False).head(10)
    fi = fi.sort_values("importance")  # for better visualization
    fig = px.bar(
        fi,
        x="importance",
        y="feature",
        orientation="h",
        title="Top 10 Feature Importance",
        labels={"importance": "Importance", "feature": "Feature"},
    )
    fig.update_layout(margin=MARGINS,
                      height=400)
    return fig
