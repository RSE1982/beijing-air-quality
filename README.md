# 📘 Beijing Air Quality Analysis & Forecasting

## A Code Institute Data Analytics with AI Capstone Project

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

**Author:** Robert Steven Elliott

**Objective:** Analyse Beijing’s multi-station air quality data, identify temporal + spatial pollution patterns, and build machine learning models (baseline + lag-based) to forecast PM2.5 concentrations.

🚀 **Live Dashboard:**  
[rse1982-beijing-air-quality.streamlit.app](https://rse1982-beijing-air-quality.streamlit.app/)

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

## 🧪 Research Methodology Rationale

The Beijing dataset is observational and non-experimental, making it suitable for an exploratory and hypothesis-driven research approach.
Time-series methods were chosen because air quality exhibits:

- Autocorrelation (recent values influence near-future values)
- Seasonality
- Hourly and daily cycles

KMeans clustering was selected because:

- It is effective for grouping stations based on continuous pollution metrics
- PCA allows reduction of multicollinearity in meteorological features
- It supports spatial interpretation without requiring labelled outcomes

Machine learning models such as Random Forest and XGBoost were chosen due to:

- Their robustness to nonlinear relationships
- Strong performance on environmental data
- Ability to incorporate engineered temporal features

This methodological framework was selected to align with environmental modelling best practices and the project’s forecasting goals.

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

## 🌍 Application of Data Analytics in Air Quality Management

Air quality analytics plays a critical role in environmental health, enabling:

- Identification of pollution hotspots
- Understanding diurnal and seasonal pollution cycles
- Evaluating policy impacts (e.g., vehicle restrictions, heating controls)
- Supporting public health advisories (especially for vulnerable groups)
- Building medium- and short-term pollution forecasts

Machine learning and AI address real-world challenges such as:

- Predicting harmful PM2.5 peaks ahead of time
- Detecting station behaviour patterns that may indicate local emission sources
- Automating anomaly detection in sensor networks

These applications demonstrate the value of analytical and AI-driven approaches in environmental decision-making and policy planning.

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

### 🔍 Additional Limitations & Alternative Approaches

Beyond the challenges mentioned, this project also faced:

#### Data Gaps & Station Variability

Several stations contain long gaps or unexpectedly flat periods in early years.
Alternative: imputation via Kalman filters or hierarchical models.

#### Temporal Leakage Risk

Forecast models required careful handling of lags and rolling windows to avoid leaking future information.
Alternative: using window generators from TensorFlow/Keras.

#### Model Interpretability

Tree-based models outperform linear models but are harder to explain.
Alternative: SHAP or LIME could provide clearer reasoning for predictions.

#### Clustering Sensitivity

KMeans assumes spherical clusters, which may oversimplify spatial behaviour.
Alternative: DBSCAN or HDBSCAN can detect arbitrary shapes and noise points.

Reflecting on these limitations shaped the design of the final modelling and dashboard choices.

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

## 📝 Dashboard Narrative & Communication Strategy

The dashboard is structured to communicate insights clearly to both technical and non-technical audiences. 

Each page includes:

- A short explanation of what each visualisation shows
- Tooltips and labels to guide interpretation
- A narrative linking visual patterns to the project’s hypotheses
- Colour schemes and layouts designed for clarity and accessibility

Pages are arranged to follow a logical analytical journey:

- Overview – high-level insights
- Hypotheses (1–5) – statistical evidence presented visually
- Clustering – spatial behaviour patterns
- Modelling – baseline vs lag-based performance
- Forecasting – short-term predictions with context
- About – dashboard narrative, instructions, ethics, methodology, and guidance

This ensures the dashboard supports data storytelling and helps users interpret air-quality patterns responsibly.

### 🧭 How to Navigate the Dashboard

- Use the **Overview** page for high-level trends and context
- Hypotheses pages (H1–H5) present statistical evidence visually
- The **Clustering** page explores spatial station behaviour
- The **Modelling** page compares baseline and lag-based models
- The **Forecasting** page shows short-term PM2.5 predictions by station
- The **About** page explains methodology, ethics, and limitations

## 🐞 Unfixed Bugs

- Some mobile plots may overflow the screen
- On the clustering page, only the radar plot filters correctly for the selected cluster
- Large datasets may cause slow initial load

## 🔧 Code Evaluation & Performance Improvements

Throughout development, several iterations were required to enhance performance, reliability, and maintainability. Key improvements include:

- Vectorised pandas operations replaced earlier slower loops, significantly reducing execution time when handling millions of rows.
- Feature engineering code was consolidated into modular functions, improving reproducibility and enabling consistent transformations across notebooks and the Streamlit app.
- The forecasting pipeline underwent optimisation by removing unused lag features, reducing RAM usage and model training time.
- Errors relating to missing categories and inconsistent encodings were resolved by enforcing deterministic dtype mappings and explicitly saving/loading categorical state.
- XGBoost integration was improved by upgrading to a modern version, resolving feature-mismatch errors and enabling faster prediction times.

These refinements demonstrate an iterative, evidence-based approach to writing efficient and maintainable Python code.

## 🚀 Deployment

### Local Installation & Deployment (Optional)

This project can be run locally for development or exploration.

#### Requirements

- Python 3.12+
- Git

#### Setup Steps
```bash
git clone https://github.com/RSE1982/beijing-air-quality.git
cd beijing-air-quality
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit/app.py
```

### Streamlit Cloud

The app is deployed via Streamlit Cloud following the steps below:

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

## 🛠 Project Maintenance & Update Plan

To ensure the long-term value of this project, future maintenance will include periodic model retraining when new data becomes available, extending the forecasting horizon, and monitoring prediction drift over time.

The dashboard can be updated with live data ingestion, versioned model deployments, and improved performance using more efficient caching or incremental loading.

A structured update cycle—data ingestion → cleaning → engineering → retraining → evaluation → dashboard release—ensures sustainable long-term operation.

## 🔚 Conclusion

This project demonstrates that Beijing’s PM2.5 levels show:

- Strong and consistent seasonal patterns, with winter pollution significantly higher
- Clear spatial variation, reflecting urban density and geography
- Meaningful relationships with meteorological variables, such as temperature inversions and low wind conditions
- Predictability through machine learning, where lag-based models outperform baseline models
- The dashboard transforms complex analysis into clear, interactive insights suitable for both technical and non-technical audiences.

### Hypothesis summary table

| Hypothesis | Test             | Result            | Conclusion          |
| ---------- | ---------------- | ----------------- | ------------------- |
| H1         | ANOVA            | p < 0.001         | Supported           |
| H2         | ANOVA            | p < 0.001         | Supported           |
| H3         | Correlation      | Mixed             | Partially supported |
| H4         | Time-series      | Clear structure   | Supported           |
| H5         | Model comparison | Lag models better | Supported           |


## 🔮 Future Work & Learning Roadmap

- Incorporate deep learning models (LSTM, TFT)
- Build automated retraining pipelines
- Add real-time data ingestion
- Evaluate SHAP values for model interpretability
- Extend dashboard to include forecasting alerts
- Deploy models using FastAPI or AWS Lambda

## 🤖 Use of AI Tools in This Project

Generative AI (ChatGPT) was used during this project to assist with:

- Ideation of dashboard layout and user experience
- Debugging code errors, particularly mismatches in XGBoost feature naming
- Designing EDA narrative structure
- Producing documentation templates (e.g., metadata YAML)
- Generating explanatory text for statistical concepts and insights
- Creating design variations for clustering visualisations and station profiling

AI tools supported the workflow, but all data analysis, modelling decisions, and code execution were performed by the learner.
This hybrid human–AI workflow improved productivity while maintaining academic integrity.

## 📚 Learning Reflection

This project strengthened my skills in managing large environmental datasets, engineering time-series features, and applying both classical statistical methods and machine learning models.

Debugging forecasting pipelines, handling inconsistent station data, and optimising XGBoost workflows deepened my understanding of real-world data challenges.

Building a Streamlit dashboard improved my ability to communicate complex insights to technical and non-technical audiences, and integrating AI tools taught me how to use generative assistance responsibly and effectively.

The project prepared me for continuous learning in areas such as advanced time-series modelling, cloud deployment, and applied environmental analytics.


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
