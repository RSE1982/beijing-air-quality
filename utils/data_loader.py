"""
Utility functions to load data for Streamlit app.
"""

from pathlib import Path
import pandas as pd
import streamlit as st
import yaml
import numpy as np
from utils.load_csv import load_csv

# Define the root data path
ROOT = Path(__file__).parent.parent

# Define the data directory
DATA_PATH = ROOT / "data"
MODEL_OUTPUT = ROOT / "model_outputs"

@st.cache_data
def load_engineered() -> pd.DataFrame:
    """
    Load feature engineered Beijing air quality data.

    Returns:
        pd.DataFrame: Feature engineered Beijing air quality data.
    """

    return load_csv(DATA_PATH / "engineered" / "beijing_engineered.csv")


@st.cache_data
def load_station_meta() -> pd.DataFrame:
    """
    Load station metadata.

    Returns:
        pd.DataFrame: Station metadata.
    """

    return load_csv(DATA_PATH / "metadata" / "station_metadata.csv")


@st.cache_data
def load_clustered() -> pd.DataFrame:
    """
    Load clustered Beijing air quality data.

    Returns:
        pd.DataFrame: Clustered Beijing air quality data.
    """

    return load_csv(MODEL_OUTPUT / "clustering" / "beijing_clustered.csv")


@st.cache_data
def load_pca_coords() -> pd.DataFrame:
    """
    Load PCA coordinates data.

    Returns:
        pd.DataFrame: PCA coordinates data.
    """

    return load_csv(MODEL_OUTPUT / "clustering" / "pca_coords.csv")


@st.cache_data
def load_silhouette_values() -> pd.DataFrame:
    """
    Load silhouette values for clusters.

    Returns:
        pd.DataFrame: Silhouette values data.
    """
    return load_csv(MODEL_OUTPUT / "clustering" / "silhouette_values.csv")


@st.cache_data
def load_cluster_profiles() -> dict:
    """
    Load cluster profiles from a YAML file.

    Args:
        path (Path): Path to the YAML file containing cluster profiles.
    Returns:
        dict: Cluster profiles with normalized keys.
    """

    CLUSTER_PROFILES = ROOT / "streamlit" / "cluster_profiles.yml"

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


@st.cache_data
def load_feature_importance(model: str) -> pd.DataFrame:
    """
    Load feature importance data.
    args:
        model (str): Model name.
    Returns:
        pd.DataFrame: Feature importance data.
    """

    return load_csv(MODEL_OUTPUT / model / "feature_importances.csv")


@st.cache_data
def load_hyperparameter_results() -> pd.DataFrame:
    """
    Load hyperparameter tuning results.

    Returns:
        pd.DataFrame: Hyperparameter tuning results.
    """
    return load_csv(MODEL_OUTPUT / "regression" /
                    "hyperparameter_results.csv")


@st.cache_resource
def load_model_predictions(model: str) -> pd.DataFrame:
    """
    Load model predictions data.
    args:
        model (str): Model name.
    Returns:
        pd.DataFrame: Model predictions data.
    """
    return np.load(MODEL_OUTPUT / model / "predictions.npz")
