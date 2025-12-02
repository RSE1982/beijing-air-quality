# 📘 Beijing Air Quality Analysis & Forecasting

## A Code Institute Data Analytics with AI Capstone Project

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

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

## Hypothesis and how to validate?

### H1: There is a strong seasonal pattern in PM2.5 levels

**Validation:**

- Monthly/seasonal EDA plots
- Year-on-year comparison
- Weather variable analysis

### H2: PM2.5 varies significantly between monitoring stations

**Validation:**

- Station-level boxplots
- Mean PM2.5 comparison
- Spatial metadata analysis (urban vs suburban vs residential)

### H3: Meteorological variables correlate with PM2.5

**Validation:**

- Correlation heatmap
- Pairplots
- Scatter + regression visualisation

### H4: Hourly and daily temporal patterns explain short-term PM2.5 variability

**Validation:**

- Hourly averages
- Daily rolling mean plots

### H5: Lag features improve predictive model accuracy

**Validation:**

- Train baseline models (no lag features)
- Train lag-based models (1h, 6h, 12h, 24h lags + rolling windows)
- Compare MAE/RMSE/R² metrics

## Project Plan

This project follows a structured data analytics workflow aligned with Code Institute’s Capstone standards. It includes extraction, cleaning, exploration, feature engineering, hypothesis testing, modelling, and dashboard development.

### 1. Data Extraction

- Load 12 raw station CSV files  
- Validate structure and column consistency  
- Standardise column names  
- Combine all stations into a unified dataset  
- Generate raw + combined metadata  

### 2. Data Cleaning

- Merge timestamp fields into a single datetime column  
- Correct datatypes  
- Remove duplicates  
- Handle missing values  
- Drop unused pollutant columns (PM10, SO₂, NO₂, CO, O₃)  
- Save cleaned dataset + metadata  

### 3. Initial Exploratory Data Analysis (EDA)

- Distribution analysis (PM2.5 + weather)  
- Temporal trends (hourly, daily, monthly, seasonal)  
- Spatial station comparisons  
- Correlation and relationship analysis  
- Identify candidate features for engineering  

EDA produces the insights that justify the engineered features used later.

### 4. Feature Engineering

Feature Engineering is performed **before hypothesis testing**, because several hypotheses require enhanced or transformed features.

Features engineered include:

#### Temporal Features

- Year, month, day, hour, day-of-week  
- Seasonal categories (winter/spring/summer/autumn)  
- Cyclical encodings (sin/cos for hour + month)

#### Lag & Rolling Features

- Lag features: 1h, 6h, 12h, 24h  
- Rolling statistics: 3h, 12h, 24h means

#### Derived Meteorological Features

- Dewpoint spread  
- Temperature-pressure interaction  
- Rainfall binary indicator  

#### Spatial Features

- Latitude, longitude  
- Area type (urban/suburban/residential/industrial)

#### Export

- Saved as **Parquet** due to GitHub’s 100 MB file limit  
- Metadata generated for the engineered dataset  

### 5. Hypothesis Testing (H1–H4)

Hypotheses are tested **after Feature Engineering**, because several require engineered variables (season, spatial metadata, cyclical encodings, derived weather features).

#### H1 — PM2.5 displays a strong seasonal pattern

- Validated using monthly, seasonal, and temperature-related engineered features.

#### H2 — PM2.5 varies significantly across spatial regions

- Validated using station averages, boxplots, and spatial metadata (area_type, latitude/longitude).

#### H3 — Meteorological variables strongly correlate with PM2.5

- Validated using engineered weather interactions (temp × pres, dewpoint spread).  

#### H4 — Temporal structure explains PM2.5 variation

- Uses engineered cyclical hour/month encodings and lag correlations.

### 6. Modelling

#### H5 — Lag features improve model performance

- Tested during modelling by comparing:  
  - Baseline models (no lag features)  
  - Lag-based models (with engineered temporal features)

##### Baseline Models (cleaned dataset)

- Linear Regression  
- Random Forest Regressor  
- XGBoost Regressor  
- Evaluated with MAE, RMSE, R²  

#### Lag-Based Models (feature-engineered dataset)

- NA rows removed (lag-related)  
- Same modelling families for fair comparison  
- Hyperparameter optimisation  
- Performance comparison against baseline  
- Feature importances ranked  

---

### 7. Dashboard Development

- Multi-page Streamlit dashboard  
- Pages:  
  - Home  
  - Station Analysis  
  - Temporal Trends  
  - Correlation  
  - Model Comparison  
  - Forecasting  
- Loads Parquet datasets + saved models  
- Designed for both technical and non-technical users  

### 8. Final Documentation

- Metadata for all dataset stages  
- Provenance diagram  
- Workflow diagram  
- Limitations + ethical considerations  
- Deployment instructions  
- Final README and dashboard guide
