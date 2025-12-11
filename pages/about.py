import streamlit as st

st.set_page_config(page_title="About — Beijing Clean Air Dashboard", page_icon="ℹ️")

st.title("ℹ️ About This Project")

st.markdown("""
The **Beijing Clean Air Dashboard** communicates insights from the 
**Beijing Multi-Site Air Quality Dataset**, using statistical analysis, feature engineering, machine learning, 
and interactive visualisations.

This dashboard was built as part of the **Code Institute Data Analytics with AI Diploma Capstone Project**.
""")

st.subheader("🎯 Project Objectives")
st.markdown("""
- Analyse air quality patterns across multiple stations in Beijing  
- Understand seasonal, spatial, and meteorological drivers of PM2.5  
- Apply statistical testing to validate five specific hypotheses  
- Train machine learning models to forecast PM2.5 using engineered features  
- Present insights interactively for both technical and non-technical audiences  
""")

st.subheader("📚 Dataset")
st.markdown("""
This project uses the **Beijing Multi-Site Air Quality Data (2013–2017)**  
from Chen & Song (2017), originally published on the **UCI Machine Learning Repository**, 
and mirrored on Kaggle.

- **12 monitoring stations**
- **Hourly pollution & meteorological data**
- **PM2.5, PM10, SO2, NO2, temperature, pressure, wind, rainfall**
- Coverage: **2013–2016** used in analysis  
""")

st.subheader("🔐 Licensing")
st.markdown("""
The dataset is licensed under **CC BY 4.0**.

Required attribution:

Chen, Song (2017). *Beijing Multi-Site Air Quality*.  
UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5RK5G  

Kaggle mirror by Manu Siddhartha (CC BY 4.0).
""")

st.subheader("🧠 Methodology Summary")
st.markdown("""
- **CRISP-DM** analytical workflow  
- ETL pipeline with staged data cleaning and feature engineering  
- Hypothesis-driven statistical testing  
- Forecasting using **XGBoost Regressor** with lag features  
- Spatial clustering using **KMeans + PCA**  
- Deployment via **Streamlit**  
""")

st.subheader("✨ Dashboard Structure")
st.markdown("""
**Dashboard**
- Home  
- Overview  
- About  

**Hypotheses**
1. Seasonal variation  
2. Spatial variation  
3. Meteorological drivers  
4. Temporal structure  
5. Lag-feature impact  

**Analysis**
- Clustering  
- Model comparison  

**Forecasting**
- Station-level predictions  
""")

st.subheader("👨‍💻 Author")
st.markdown("""
**Robert Steven Elliott**
""")
