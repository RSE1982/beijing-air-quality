"""
Module for feature engineering functions.
Includes functions to create lag and rolling features for time series
forecasting.
"""

import pandas as pd


def apply_forecasting_features(df: pd.DataFrame,
                               add_lags=True,
                               add_rollings=True):
    """
    Apply lag and rolling features safely AFTER splitting train/test.
    This prevents data leakage from future data points.
    Args:
        df (pd.DataFrame): Input dataframe with time series data.
        add_lags (bool): Whether to add lag features.
        add_rollings (bool): Whether to add rolling mean features.
    Returns:
        pd.DataFrame: DataFrame with added features.
    """

    # Create a copy to avoid modifying the original dataframe
    df = df.copy()

    # Add lag features
    if add_lags:
        for lag in [1, 3, 6, 12, 18]:
            df[f"pm25_lag_{lag}h"] = (
                df.groupby("station", observed=False)["pm25"].shift(lag)
            )

    # Add rolling mean features
    if add_rollings:
        for w in [3, 6, 12, 18]:
            df[f"pm25_roll_{w}h_mean"] = (
                df.groupby("station", observed=False)["pm25"]
                  .shift(1)
                  .rolling(w)
                  .mean()
                  .reset_index(level=0, drop=True)
            )

    return df
