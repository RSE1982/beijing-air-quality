# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# 📘 Beijing Air Quality Analysis & Forecasting
## A Code Institute Data Analytics with AI Capstone Project
**Author:** Robert Steven Elliott

**Objective:** Analyse Beijing’s multi-station air quality data, identify temporal + spatial pollution patterns, and build machine learning models (baseline + lag-based) to forecast PM2.5 concentrations.

![Beijing Air Quality Banner](images/beijing_air_quality_banner.png)

---

## Dataset Content

This project uses the Beijing Multi-Site Air Quality Dataset, originally published by Song Chen (2017) and hosted on the UCI Machine Learning Repository (with a Kaggle mirror).

It contains hourly pollution and meteorological observations from 12 monitoring stations across Beijing, including:

- PM2.5
- Temperature, dew point, pressure, and rainfall
- Wind direction and speed
- Station identifiers and timestamps

The cleaned and engineered datasets have been optimised for GitHub storage using the Parquet format due to GitHub’s 100 MB file limit.

## Business Requirements

This project aims to:

1. Analyse Beijing’s air quality trends
    - Identify temporal (hourly, daily, monthly, seasonal) variation
    - Compare pollution across different monitoring stations
    - Detect relationships between weather and PM2.5 concentration
2. Forecast PM2.5 levels using machine learning
    - Build baseline models (no lag features)
    - Build lag-based models for improved forecasting accuracy
    - Compare performance between modelling approaches
3. Deliver insights through an interactive dashboard
    - Allow users to explore spatial, temporal, and predictive insights
    - Communicate findings clearly to both technical and non-technical users
