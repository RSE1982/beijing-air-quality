"""
Utility functions to load data for Streamlit app.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent.parent.parent
DATA_PATH = ROOT / "data"


@st.cache_data
def load_cleaned() -> pd.DataFrame:
    """
    Load cleaned Beijing air quality data.

    Returns:
        pd.DataFrame: Cleaned Beijing air quality data.
    """
    return pd.read_csv(DATA_PATH / "cleaned" / "beijing_cleaned.csv")


@st.cache_data
def load_engineered() -> pd.DataFrame:
    """
    Load feature engineered Beijing air quality data.

    Returns:
        pd.DataFrame: Feature engineered Beijing air quality data.
    """
    return pd.read_csv(DATA_PATH / "engineered" /
                       "beijing_feature_engineered.csv")


@st.cache_data
def load_station_meta() -> pd.DataFrame:
    """
    Load station metadata.

    Returns:
        pd.DataFrame: Station metadata.
    """
    return pd.read_csv(DATA_PATH / "metadata" / "station_metadata.csv")
