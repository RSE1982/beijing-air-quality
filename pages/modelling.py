import pandas as pd
import streamlit as st
from utils.model_loader import load_best_model, load_metadata
from utils.data_loader import (load_feature_importance,
                               load_hyperparameter_results,
                               load_best_model_predictions)
from utils.modelling_charts import (bar_chart,
                                    prediction_vs_actual_chart,
                                    residuals_distribution_chart,
                                    residuals_vs_predicted_chart,
                                    feature_importance_chart)

# load models and data
model = load_best_model()
metadata = load_metadata()
feature_imp = load_feature_importance()
grid_results = load_hyperparameter_results()
predictions = load_best_model_predictions()

best_preds = predictions["normal_preds"]
y_true = predictions["y_true"]
residuals = y_true - best_preds

st.title("📈 Regression Modelling & Hyperparameter Search")

col1, col2 = st.columns([1, 3])
with col1:
    tab1, tab2, tab3 = st.tabs(["📄 Overview",
                                "❓ Best Model",
                                "📈 Hyperparameters"])
    with tab1:
        st.subheader("Modelling Overview")
        st.markdown(
            """
            In this section, we explore various regression models developed to
            predict PM2.5 concentrations in Beijing. The models were trained
            using historical air quality and meteorological data, with a focus
            on optimizing predictive accuracy through hyperparameter tuning.
            """
        )
    with tab2:
        st.subheader("Best Model Summary")
        st.metric("Best Model", metadata["best_model"])
        st.metric("RMSE", round(metadata.get("rmse",
                                             grid_results['RMSE'].min()), 3))
        st.metric("R² Score", round(metadata.get("r2",
                                                 grid_results['R2'].max()), 3))
    with tab3:
        st.subheader("Selected Hyperparameters")
        params = metadata["best_params"]
        params_df = (
            pd.DataFrame.from_dict(params, orient="index", columns=["value"])
            .dropna()
        )
        st.dataframe(params_df, use_container_width=True)
with col2:
    st.header("📊 Performance Visualisation")

    tabs = st.tabs(["RMSE Ranking",
                    "MAE Ranking",
                    "R² Ranking",
                    "Prediction vs Actual",
                    "Residuals",
                    "Residuals vs Predicted",
                    "Feature Importance",
                    "Hyperparameter Search Results"])
    with tabs[0]:
        st.subheader("RMSE Ranking")
        grid, info = st.columns([3, 2])
        with grid:
            st.plotly_chart(bar_chart(grid_results.sort_values("RMSE"),
                                      "RMSE"), use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This bar chart ranks all tested models by RMSE, where lower values
            indicate better predictive performance.

            **Why it matters:**
            - RMSE penalises large errors heavily.
            - Useful for assessing overall accuracy and how well the model
              captures extreme pollution events.
            - Helps identify which model generalises best on unseen data.

            **How to interpret:**
            - The model at the top (lowest RMSE) performed best.
            - Large gaps between bars indicate meaningful performance
              differences.
            """)
    with tabs[1]:
        st.subheader("MAE Ranking")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(bar_chart(grid_results.sort_values("MAE"),
                                      "MAE"), use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This bar chart ranks all tested models by MAE, where lower values
            indicate better predictive performance.

            **Why it matters:**
            - MAE provides a straightforward measure of average error.
            - Less sensitive to outliers compared to RMSE.
            - Useful for understanding typical prediction accuracy.

            **How to interpret:**
            - The model at the top (lowest MAE) performed best.
            - Smaller differences between bars suggest similar performance
              among models.
            """)
    with tabs[2]:
        st.subheader("R² Ranking")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(bar_chart(
                grid_results.sort_values("R2", ascending=False), "R2"),
                use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This bar chart ranks all tested models by R² score, where higher
            values indicate better predictive performance.

            **Why it matters:**
            - R² indicates the proportion of variance explained by the model.
            - Helps assess how well the model captures underlying patterns.
            - Useful for comparing models on their explanatory power.

            **How to interpret:**
            - The model at the top (highest R²) performed best.
            - Values closer to 1 indicate a better fit to the data.
            """)
    with tabs[3]:
        st.subheader("Prediction vs Actual Values")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(prediction_vs_actual_chart(y_true, best_preds),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This scatter plot compares the model's predicted PM2.5 values
            against the actual observed values.

            **Why it matters:**
            - Visualises how closely predictions align with reality.
            - The trendline indicates overall prediction accuracy.
            - Helps identify systematic biases in predictions.

            **How to interpret:**
            - Points close to the diagonal line indicate accurate predictions.
            - Deviations from the line highlight prediction errors.
            - The slope of the trendline reflects prediction bias.
            """)
    with tabs[4]:
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(residuals_distribution_chart(residuals),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This distribution plot visualises the residuals (errors) from the
            model's predictions.

            **Why it matters:**
            - Helps assess if residuals are normally distributed.
            - Identifies potential biases or patterns in prediction errors.
            - Aids in diagnosing model performance issues.

            **How to interpret:**
            - A symmetric, bell-shaped distribution indicates good model fit.
            - Skewness or multiple peaks suggest systematic errors.
            - Wider distributions indicate larger prediction errors.
            """)
    with tabs[5]:
        st.subheader("Residuals vs Predicted Values")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(
                residuals_vs_predicted_chart(residuals, best_preds),
                use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This scatter plot visualises the relationship between residuals
            and predicted PM2.5 values.

            **Why it matters:**
            - Helps identify patterns or biases in prediction errors.
            - Aids in diagnosing heteroscedasticity (changing variance).
            - Useful for assessing model assumptions.

            **How to interpret:**
            - A random scatter around zero indicates good model fit.
            - Patterns or funnels suggest systematic errors or
                        heteroscedasticity.
            - Large residuals at certain predicted values highlight weaknesses
              in the model.
            """)
    with tabs[6]:
        st.subheader("Feature Importance")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(feature_importance_chart(feature_imp),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This bar chart displays the importance of each feature used in the
            best-performing model.

            **Why it matters:**
            - Identifies which features have the most influence on predictions.
            - Helps understand the model's decision-making process.
            - Guides feature selection for future modelling efforts.

            **How to interpret:**
            - Taller bars indicate more important features.
            - Features with low importance may be candidates for removal.
            - Understanding feature importance can inform domain insights.
            """)
    with tabs[7]:
        st.subheader("🔍 Hyperparameter Search Results (GridSearchCV)")
        graph, info = st.columns([3, 2])
        with graph:
            st.dataframe(grid_results, use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            This table presents the results of the hyperparameter search using
            GridSearchCV for all tested models.

            **Why it matters:**
            - Provides insights into how different hyperparameter settings
              impact model performance.
            - Helps identify optimal configurations for future modelling.
            - Aids in understanding the sensitivity of models to hyperparameter
              changes.
            """)
