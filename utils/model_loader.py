"""
Utility functions to load machine learning models with caching.
"""

from pathlib import Path
import joblib
import streamlit as st
import json

# Define the root directory and model path
ROOT = Path(__file__).parent.parent
MODEL_PATH = ROOT / "models"
MODEL_OUTPUT = ROOT / "model_outputs"


@st.cache_resource
def load_best_model():
    """Load the XGBoost regression model used in the analysis."""
    with open(MODEL_PATH / "regression" / "best_regression_model.joblib", "rb") as f:
        return joblib.load(f)


@st.cache_resource
def load_cluster_model():
    """Load the clustering model used in the analysis."""
    with open(MODEL_PATH / "kmeans_cluster_model.pkl", "rb") as f:
        return joblib.load(f)


@st.cache_resource
def load_scaler():
    """If you used StandardScaler or MinMaxScaler in clustering."""
    with open(MODEL_PATH / "scaler_cluster.joblib", "rb") as f:
        return joblib.load(f)


@st.cache_resource
def load_baseline_model():
    """Load a baseline model for comparison."""
    with open(MODEL_PATH / "rf_baseline_model.joblib", "rb") as f:
        return joblib.load(f)


@st.cache_resource
def load_lag_model():
    """Load a lag-based model for time series forecasting."""
    with open(MODEL_PATH / "rf_lag_model.joblib", "rb") as f:
        return joblib.load(f)


@st.cache_resource
def load_metadata():
    """Load regression metadata."""
    metadata_path = MODEL_OUTPUT / "regression" / "regression_metadata.json"
    with open(metadata_path, "r") as f:
        return json.load(f)


@st.cache_resource
def load_encoders():
    """Load categorical encoders used in the models."""
    ENCODERS_PATH = MODEL_OUTPUT / "regression"

    season_dtype = joblib.load(ENCODERS_PATH / "season_dtype.joblib")
    area_dtype = joblib.load(ENCODERS_PATH / "area_dtype.joblib")
    station_dtype = joblib.load(ENCODERS_PATH / "station_dtype.joblib")
    return season_dtype, area_dtype, station_dtype
