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

## The Rationale to Map the Business Requirements to the Data Visualisations

The dashboard and supporting notebooks were designed so that **each business requirement** is clearly addressed by one or more specific visualisations. This ensures that insights are not only computed, but also communicated in a way that is accessible to both technical and non-technical users.

| Business Requirement | Data Visualisation(s) | Rationale |
|----------------------|-----------------------|-----------|
| **BR1 – Understand temporal behaviour and seasonality of PM2.5 in Beijing** | Line charts of daily and monthly PM2.5 averages, bar charts of average PM2.5 by month/season, hourly profile plots, rolling mean plots (Initial EDA + “Temporal Trends” dashboard page) | Time-series line and bar charts make it easy to see when pollution peaks occur (winter vs summer, weekday vs weekend, night vs day). Rolling means help smooth short-term noise so seasonal and diurnal patterns are visible at a glance. These visualisations directly support hypothesis testing around temporal patterns (H1, H4). |
| **BR2 – Compare air quality between monitoring stations and area types** | Station-level bar charts of mean PM2.5, boxplots by station, grouped plots by area_type (urban/suburban/residential) on the “Station Analysis” page | Bar charts show which stations have higher average pollution, while boxplots reveal variability and extreme events. Grouping by area_type helps non-technical audiences understand spatial differences (e.g. “urban stations are generally worse than suburban ones”) without needing to read tables. This supports spatial hypotheses (H2). |
| **BR3 – Understand how weather conditions relate to PM2.5 levels** | Correlation heatmap, pairplot of PM2.5 vs TEMP/DEWP/PRES/RAIN, scatterplots with trendlines on the “Correlation & Relationships” page | The correlation heatmap provides a high-level summary of linear relationships, while pairplots and scatterplots allow more detailed inspection of individual variable pairs. This combination helps explain how temperature, pressure and rainfall influence PM2.5, grounding H3 in clear visuals that are easy to interpret. |
| **BR4 – Evaluate and compare forecasting models (baseline vs lag-based)** | Metric summary cards (MAE, RMSE, R²), side-by-side bar charts of model performance, line plots of actual vs predicted PM2.5 on the “Model Comparison” page | Metric cards provide an at-a-glance summary for decision-makers, while bar charts allow direct comparison between baseline and lag-enhanced models. Actual vs predicted line plots show how well the model tracks episodes and peaks. Together, these visuals make the outcome of H5 (whether lag features improve performance) transparent and understandable. |
| **BR5 – Provide short-term PM2.5 forecasts for selected stations** | Forecast line charts showing future PM2.5, with historical context, on the “Forecasting” page; station selector widget | Overlaying recent history with model forecast allows users to see both where the model is coming from and where it predicts levels are heading. Station filters allow localised insights. This addresses the practical decision-support side of the project by turning model outputs into actionable, station-specific information. |
| **BR6 – Communicate data quality, coverage and limitations** | Summary tables/figures on record counts, missing data patterns (in notebooks), brief data quality notes on the “Home” or “About” dashboard section | Simple tables and high-level charts summarising data availability, along with short narrative notes, help users understand where the data is strong and where it is limited. This supports honest communication of uncertainty and reinforces the ethical considerations of the project. |

## Analysis techniques used

### Exploratory Data Analysis (EDA)

- Histograms, boxplots, KDEs
- Temporal decomposition
- Spatial comparison
- Correlation heatmaps

### Feature Engineering

- Lagging
- Rolling windows
- Season classification
- Cyclical time encoding
- Interaction terms
- Spatial metadata

### Machine Learning

- Linear Regression
- Random Forest Regressor
- XGBoost Regressor
- Train/test split
- Evaluation via MAE, RMSE, R²

### Limitations and Alternatives

- Dataset lacks wind speed/direction for some stations → could limit modelling
- PM2.5 spikes are difficult to predict linearly → tree models perform better
- Seasonal effects not explicitly encoded in raw data → added manually

### Use of Generative AI Tools

- Ideation for feature engineering strategies
- Optimising notebook structure and explanations
- Assisting with Streamlit layout
- Auto-generating metadata templates and documentation

## Ethical considerations

- Dataset is licensed under CC BY 4.0; attribution maintained throughout
- No personal or sensitive data is included
- Weather and pollution readings pose no privacy risk
- Machine learning models used purely for environmental insight
- Dashboard avoids alarmist or misleading conclusions

## Dashboard Design

to be added

## Unfixed Bugs

to be added

## Deployment

### Streamlit Cloud

The app is deployed via Streamlit Cloud.

**Steps:**

1. Push repository to GitHub
2. Connect GitHub repo to Streamlit Cloud
3. Add required secrets (if any)
4. Deploy and test

App Link: \<To Be Added\>

## Main Data Analysis Libraries

| Library              | Purpose                        |
| -------------------- | ------------------------------ |
| Pandas               | Data cleaning and manipulation |
| NumPy                | Numerical operations           |
| Matplotlib / Seaborn | Data visualisation             |
| Plotly               | Interactive visualisation      |
| Scikit-learn         | Baseline ML models             |
| XGBoost              | Advanced regression modelling  |
| PyYAML               | Metadata generation            |
| Streamlit            | Dashboard application          |

## Credits

### Content

- Dataset: Chen, Song (2017). Beijing Multi-Site Air Quality
- Research context from UCI and Kaggle dataset pages

#### Media

- Icons from FontAwesome / Streamlit icon set
- Images from Unsplash or user-created
