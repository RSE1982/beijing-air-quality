"""
Utility functions to load data for Streamlit app.
"""

from pathlib import Path
import pandas as pd
import streamlit as st
import yaml

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
                       "beijing_engineered.csv")


@st.cache_data
def load_station_meta() -> pd.DataFrame:
    """
    Load station metadata.

    Returns:
        pd.DataFrame: Station metadata.
    """
    return pd.read_csv(DATA_PATH / "metadata" / "station_metadata.csv")


@st.cache_data
def load_clustered() -> pd.DataFrame:
    """
    Load clustered Beijing air quality data.

    Returns:
        pd.DataFrame: Clustered Beijing air quality data.
    """
    return pd.read_csv(DATA_PATH / "derived" / "beijing_clustered.csv")

@st.cache_data
def load_pca_coords() -> pd.DataFrame:
    """
    Load PCA coordinates data.

    Returns:
        pd.DataFrame: PCA coordinates data.
    """
    return pd.read_csv(DATA_PATH / "derived" / "pca_coords.csv")


@st.cache_data
def load_silhouette_values() -> pd.DataFrame:
    """
    Load silhouette values for clusters.

    Returns:
        pd.DataFrame: Silhouette values data.
    """
    return pd.read_csv(DATA_PATH / "derived" / "silhouette_values.csv")


@st.cache_data
def load_cluster_profiles() -> dict:
    """
    Load cluster profiles from a YAML file.

    Args:
        path (Path): Path to the YAML file containing cluster profiles.
    Returns:
        dict: Cluster profiles with normalized keys.
    """

    CLUSTER_PROFILES = DATA_PATH / "derived" / "cluster_profiles.yml"

    with open(CLUSTER_PROFILES, "r", encoding="utf-8") as f:
        profiles = yaml.safe_load(f) or {}
    # normalise keys to int where possible
    normalised = {}
    for k, v in profiles.items():
        try:
            normalised[int(k)] = v
        except (ValueError, TypeError):
            normalised[k] = v
    return normalised
