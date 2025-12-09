"""
Utility functions to load machine learning models with caching.
"""

from pathlib import Path
import joblib
import streamlit as st
import json


ROOT = Path(__file__).parent.parent.parent
MODEL_PATH = ROOT / "models"


@st.cache_resource
def load_best_model():
    """Load the XGBoost regression model used in the analysis."""
    with open(MODEL_PATH / "best_regression_model.joblib", "rb") as f:
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
    metadata_path = MODEL_PATH / "regression_metadata.json"
    with open(metadata_path, "r") as f:
        return json.load(f)


@st.cache_resource
def load_encoders():
    """Load categorical encoders used in the models."""
    season_dtype = joblib.load(MODEL_PATH / "season_dtype.joblib")
    area_dtype = joblib.load(MODEL_PATH / "area_dtype.joblib")
    station_dtype = joblib.load(MODEL_PATH / "station_dtype.joblib")
    return season_dtype, area_dtype, station_dtype

@st.cache_resource
def load_feature_names():
    """Load feature names used in the models."""
    features = joblib.load(MODEL_PATH / "forecasting_feature_names.joblib")
    return features
