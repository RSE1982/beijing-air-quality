import streamlit as st
import plotly.express as px
from utils.model_loader import load_best_model, load_metadata
from utils.data_loader import (load_feature_importance,
                               load_hyperparameter_results)
from utils.img_load import load_img

st.title("📈 Regression Modelling & Hyperparameter Search")

# load models and data
model = load_best_model()
metadata = load_metadata()
feature_imp = load_feature_importance()
grid_results = load_hyperparameter_results()


# ---------------------------------------------------------
# Summary Section
# ---------------------------------------------------------
st.header("🧠 Best Model Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Best Model", metadata["best_model"])
with col2:
    st.metric("RMSE", round(metadata.get("rmse",
                                         grid_results['RMSE'].min()), 3))
with col3:
    st.metric("R² Score", round(metadata.get("r2",
                                             grid_results['R2'].max()), 3))


st.subheader("Selected Hyperparameters")
st.json(metadata["best_params"])


st.divider()

# ---------------------------------------------------------
# Model Performance Visuals
# ---------------------------------------------------------
st.header("📊 Performance Visualisation")

tabs = st.tabs(["Model Comparison",
                "RMSE Ranking",
                "Predicted vs Actual",
                "Residuals",
                "Residuals vs Predicted"])

with tabs[0]:
    st.image(load_img("modelling/model_performance_comparison.png"))

with tabs[1]:
    st.image(load_img("modelling/rmse_ranked_models.png"))

with tabs[2]:
    st.image(load_img("modelling/predicted_vs_actual_best_model.png"))

with tabs[3]:
    st.image(load_img("modelling/residual_distribution.png"))

with tabs[4]:
    st.image(load_img("modelling/residuals_vs_predicted.png"))


st.divider()

# ---------------------------------------------------------
# Feature Importance (Tree Models)
# ---------------------------------------------------------
st.header("⭐ Feature Importance")

if "importance" in feature_imp.columns:
    fig = px.bar(
        feature_imp.sort_values("importance", ascending=False).head(15),
        x="importance",
        y="feature",
        orientation="h",
        title="Top 15 Feature Importances"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Feature importances are not available for this model type.")

st.divider()

# ---------------------------------------------------------
# Hyperparameter Search Results
# ---------------------------------------------------------
st.header("🔍 Hyperparameter Search Results (GridSearchCV)")

st.dataframe(grid_results, use_container_width=True)
st.divider()
