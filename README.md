# 📘 Beijing Air Quality Analysis & Forecasting

## A Code Institute Data Analytics with AI Capstone Project

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

**Author:** Robert Steven Elliott

**Objective:** Analyse Beijing’s multi-station air quality data, identify temporal + spatial pollution patterns, and build machine learning models (baseline + lag-based) to forecast PM2.5 concentrations.

![Beijing Air Quality Banner](images/beijing_air_quality_banner.png)

---

## 🧭 CRISP-DM Overview

This project follows the CRISP-DM analytical lifecycle:

1. Business Understanding:\
  Explore air quality behaviour to support public health insights.
2. Data Understanding:\
  Examine pollutants, meteorological drivers, and spatial variation across Beijing.
3. Data Preparation:\
  Clean, merge, and engineer features (rolling windows, lags, cyclical encodings).
4. Modelling:
    - Baseline forecasting using cleaned data
    - Lag-based forecasting using engineered features
    - Clustering for spatial pattern discovery
5. Evaluation:
    - Hypothesis testing
    - Silhouette analysis for clustering
    - Model metrics (MAE, RMSE, R²)
6. Deployment:\
  Multi-page Streamlit dashboard communicating findings interactively.

## 📊 Dataset Content

This project uses the Beijing Multi-Site Air Quality Dataset, originally published by Chen et al. (2017) on the UCI Machine Learning Repository with a verified Kaggle mirror.

The dataset contains hourly pollutant and meteorological observations from 12 monitoring stations across Beijing.

### Variables include:

- PM2.5 concentration
- Temperature, dew point, pressure, rainfall
- Wind speed and wind direction
- Station ID and precise timestamps

### Time Coverage

- Full years 2013–2016 are used.
- Early 2017 data was removed because it is incomplete and would distort seasonal analysis.

## 🔐 Data Licensing (CC BY 4.0)

This dataset is licensed under the Creative Commons Attribution 4.0 International Licence.

Required Attribution:

Chen, Song (2017). Beijing Multi-Site Air Quality.
UCI Machine Learning Repository.
DOI: [https://doi.org/10.24432/C5RK5G](https://doi.org/10.24432/C5RK5G)

Mirrored on Kaggle by Manu Siddhartha.
Licensed under CC BY 4.0.

Full licence text: [https://creativecommons.org/licenses/by/4.0/](https://creativecommons.org/licenses/by/4.0/)


## 🧹 Data Collection, Cleaning & Storage

Following extensive testing, all final datasets are stored exclusively in CSV format because:

- Streamlit Cloud has inconsistent support for Parquet
- CSV files guarantee compatibility across environments
- They are transparent and easy for assessors to inspect
- They avoid dependency issues in the dashboard

### Workflow Summary

- Raw data loaded from 12 station CSVs
- Cleaned with robust missing value and outlier handling
- Engineered features added:
  - Lag features (1h, 6h, 12h, 24h)
  - Rolling windows (3h, 12h, 24h)
  - Cyclical encodings
  - Relative Humidity, Dewpoint spread, interaction terms
- Metadata generated at each stage

## 🧪 Methodology Summary

This project uses observational environmental data and a complete analytical workflow:

### 🟥 Descriptive Analytics

- Distributions
- Seasonal averages
- Temporal patterns

### 🟧 Inferential Analytics

- ANOVA
- t-tests
- Correlation analysis

### 🟨 Predictive Analytics

- Linear Regression
- Random Forest
- XGBoost
- Model comparison (MAE, RMSE, R²)

### 🟩 Unsupervised Learning

- KMeans clustering
- PCA for dimensionality reduction
- Silhouette analysis

### 🟦 Feature Engineering

- Lags, rolling windows
- Cyclical time features
- Derived meteorological interactions
- Spatial metadata

### 🟪 Interactive Storytelling

- Multi-page Streamlit dashboard
- Tooltips, explanations, statistical summaries

## 🎯 Business Requirements

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

## 🔍 Hypotheses & Validation Methods

### H1 — There is a strong seasonal pattern in PM2.5 levels.

- Monthly and seasonal plots
- Weather-driven analysis

### H2 — PM2.5 varies significantly between stations.

- Station boxplots
- Spatial metadata

### H3 — Meteorological variables correlate with PM2.5.

- Correlation matrix
- Scatterplots + regression lines

### H4 — Short-term temporal structure explains PM2.5 variability.

- Hourly/daily profiles
- Rolling window analysis

### H5 — Lag features improve model accuracy.

- Compare baseline vs lag-enhanced models
- Evaluate MAE, RMSE, R²

## 🗺 Mapping Business Requirements to Visualisations

The dashboard and supporting notebooks were designed so that **each business requirement** is clearly addressed by one or more specific visualisations. This ensures that insights are not only computed, but also communicated in a way that is accessible to both technical and non-technical users.

| Business Requirement | Data Visualisation(s) | Rationale |
|----------------------|-----------------------|-----------|
| **BR1 – Understand temporal behaviour and seasonality of PM2.5 in Beijing** | Line charts of daily and monthly PM2.5 averages, bar charts of average PM2.5 by month/season, hourly profile plots, rolling mean plots (Initial EDA + “Temporal Trends” dashboard page) | Time-series line and bar charts make it easy to see when pollution peaks occur (winter vs summer, weekday vs weekend, night vs day). Rolling means help smooth short-term noise so seasonal and diurnal patterns are visible at a glance. These visualisations directly support hypothesis testing around temporal patterns (H1, H4). |
| **BR2 – Compare air quality between monitoring stations and area types** | Station-level bar charts of mean PM2.5, boxplots by station, grouped plots by area_type (urban/suburban/residential) on the “Station Analysis” page | Bar charts show which stations have higher average pollution, while boxplots reveal variability and extreme events. Grouping by area_type helps non-technical audiences understand spatial differences (e.g. “urban stations are generally worse than suburban ones”) without needing to read tables. This supports spatial hypotheses (H2). |
| **BR3 – Understand how weather conditions relate to PM2.5 levels** | Correlation heatmap, pairplot of PM2.5 vs TEMP/DEWP/PRES/RAIN, scatterplots with trendlines on the “Correlation & Relationships” page | The correlation heatmap provides a high-level summary of linear relationships, while pairplots and scatterplots allow more detailed inspection of individual variable pairs. This combination helps explain how temperature, pressure and rainfall influence PM2.5, grounding H3 in clear visuals that are easy to interpret. |
| **BR4 – Evaluate and compare forecasting models (baseline vs lag-based)** | Metric summary cards (MAE, RMSE, R²), side-by-side bar charts of model performance, line plots of actual vs predicted PM2.5 on the “Model Comparison” page | Metric cards provide an at-a-glance summary for decision-makers, while bar charts allow direct comparison between baseline and lag-enhanced models. Actual vs predicted line plots show how well the model tracks episodes and peaks. Together, these visuals make the outcome of H5 (whether lag features improve performance) transparent and understandable. |
| **BR5 – Provide short-term PM2.5 forecasts for selected stations** | Forecast line charts showing future PM2.5, with historical context, on the “Forecasting” page; station selector widget | Overlaying recent history with model forecast allows users to see both where the model is coming from and where it predicts levels are heading. Station filters allow localised insights. This addresses the practical decision-support side of the project by turning model outputs into actionable, station-specific information. |
| **BR6 – Communicate data quality, coverage and limitations** | Summary tables/figures on record counts, missing data patterns (in notebooks), brief data quality notes on the “Home” or “About” dashboard section | Simple tables and high-level charts summarising data availability, along with short narrative notes, help users understand where the data is strong and where it is limited. This supports honest communication of uncertainty and reinforces the ethical considerations of the project. |

## 🧰 Analysis Techniques Used

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

### 🧠 Use of Generative AI Tools

AI-assisted tools were used for:

- Code suggestions (GitHub Copilot)
- Summarising exploratory insights (ChatGPT)
- Grammar and readability improvements (Grammarly)
- Generating station metadata (ChatGPT)
- Drafting documentation sections (ChatGPT)

All analytical decisions and implementation remain human-led.

## ⚖️ Ethical, Legal & Social Considerations

This project considers several ethical and social factors:

### Legal

- Dataset is openly licensed under CC BY 4.0 — attribution fully maintained
- No personal data, IDs, or sensitive attributes appear, making project GDPR compliant

### Ethical

- Forecasts are used only for academic and informational purposes
- Care is taken not to present predictions as official air-quality warnings
- Dashboard avoids sensational language or claims

### Social Implications

- Air pollution disproportionately affects vulnerable groups
- High pollution alerts must be communicated responsibly
- Insights are framed to inform, not to alarm, the public
- Spatial clustering highlights neighbourhood-level disparities that may inform policy discussions

## 🖥 Dashboard Design


## 🐞 Unfixed Bugs

- Some mobile plots may overflow the screen
- Large datasets may cause slow initial load

## 🚀 Deployment

### Streamlit Cloud

The app is deployed via Streamlit Cloud.

**Steps:**

1. Push repository to GitHub
2. Connect GitHub repo to Streamlit Cloud
3. Add required secrets (if any)
4. Deploy and test

App Link: [rse1982-beijing-air-quality.streamlit.app](https://rse1982-beijing-air-quality.streamlit.app/)

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

## 🔚 Conclusion
This project demonstrates that Beijing’s PM2.5 levels show:

- Strong and consistent seasonal patterns, with winter pollution significantly higher

- Clear spatial variation, reflecting urban density and geography

- Meaningful relationships with meteorological variables, such as temperature inversions and low wind conditions

- Predictability through machine learning, where lag-based models outperform baseline models

- The dashboard transforms complex analysis into clear, interactive insights suitable for both technical and non-technical audiences.

## 🔮 Future Work & Learning Roadmap

- Incorporate deep learning models (LSTM, TFT)
- Build automated retraining pipelines
- Add real-time data ingestion
- Evaluate SHAP values for model interpretability
- Extend dashboard to include forecasting alerts
- Deploy models using FastAPI or AWS Lambda

## 🙏 Credits & Acknowledgements

### Content

- Dataset: Chen, Song (2017). Beijing Multi-Site Air Quality. \
UCI Machine Learning Repository — Licensed under CC BY 4.0.\
DOI: https://doi.org/10.24432/C5RK5G\
Kaggle mirror by Manu Siddhartha.
- Research context from UCI and Kaggle dataset pages

#### Media

- Icons from FontAwesome / Streamlit icon set
- Images from Unsplash or user-created

## Acknowledgements

- Code Institute facilitators
- Cohort peers for feedback
- ChatGPT for documentation and code optimisation support
