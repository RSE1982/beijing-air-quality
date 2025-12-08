import pandas as pd
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parent.parent.parent
DATA_PATH = ROOT / "data"

@st.cache_data
def load_cleaned() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "cleaned" / "beijing_cleaned.csv")

@st.cache_data
def load_engineered():
    return pd.read_csv(DATA_PATH / "engineered" / "beijing_feature_engineered.csv")

@st.cache_data
def load_station_meta() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH / "metadata" / "station_metadata.csv")

