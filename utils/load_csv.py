"""
Utility functions for loading CSV files.
"""

import pandas as pd
from pathlib import Path


def load_csv(path: Path) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    Args:
        path (Path): Path to the CSV file.
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    df = pd.read_csv(path)  # Read CSV file into DataFrame

    # Convert 'datetime' column to datetime dtype if it exists
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])

    # Convert all object dtype columns (except 'datetime') to category dtype
    for col in df.select_dtypes(include="object").columns:
        if col != "datetime":
            df[col] = df[col].astype("category")

    return df
