"""
Hypothesis 5 page: Lag Features Improve Model Performance
This page evaluates whether including lag features in the model
improves PM2.5 forecasting accuracy.
"""

import streamlit as st
from utils.data_loader import (load_engineered,
                               load_model_predictions,
                               load_lag_feature_importance)
from utils.charts import (plot_actual_vs_pred,
                          befere_vs_after,
                          plot_lag_feature_importances)

st.title(":material/smart_toy: Hypothesis 5 —\
         Lag Features Improve Model Performance")
st.latex(r"""
         \begin{aligned}
         H_0 &: \text{Lag features do not improve PM2.5 forecasting
         performance.} \\
         H_1 &: \text{Lag features significantly improve PM2.5 forecasting
         performance.​}
         \end{aligned}
""")

# Load data and model predictions
df = load_engineered()
predictions = load_model_predictions()
y_true = predictions["y_true"]
baseline_pred = predictions["baseline_pred"]
lag_pred = predictions["l_pred"]
feature_importance = load_lag_feature_importance()

# Model performance metrics from notebook evaluation
baseline_mae = 42.163872063135194  # obtained from notebook
baseline_rmse = 56.09295025109381  # obtained from notebook
baseline_r2 = 0.37973956724526914  # obtained from notebook
lag_mae = 10.227534681736866  # obtained from notebook
lag_rmse = 16.55474291376961  # obtained from notebook
lag_r2 = 0.9395242494495807  # obtained from notebook

col1, col2 = st.columns([1, 3])
with col1:
    st.subheader(":material/key: Key Metrics")
    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Baseline Model**")
        st.metric(label="MAE", value=f"{baseline_mae:.2f}")
        st.metric(label="RMSE", value=f"{baseline_rmse:.2f}")
        st.metric(label="R2", value=f"{baseline_r2:.4f}")
    with colB:
        st.markdown("**Lag-Based Model**")
        st.metric(label="MAE", value=f"{lag_mae:.2f}")
        st.metric(label="RMSE", value=f"{lag_rmse:.2f}")
        st.metric(label="R2", value=f"{lag_r2:.4f}")

    st.success("✔ **Conclusion:** H5 is supported —  \
                    lag features significantly improve forecasting accuracy.")
with col2:
    tab1, tab2, tab3 = st.tabs([":material/trending_up:\
                                 Actual vs Lag-Based Predictions",
                                ":material/bar_chart:\
                                 Model Performance Comparison",
                                ":material/insights:\
                                 Feature Importance Analysis"])
    with tab1:
        graph, info = st.columns([3, 2])
        with graph:
            st.subheader(":material/trending_up:\
                          Actual vs Lag-Based Model Predictions")
            st.plotly_chart(plot_actual_vs_pred(y_true,
                                                baseline_pred,
                                                lag_pred),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            A side-by-side comparison of real PM2.5 values and the lag-based
            model's predictions over time. The closer the prediction line
            follows the actual values, the better the model performance.

            **Why it matters:**
            This visual directly demonstrates how well the model captures
            PM2.5 behaviour, especially rapid rises, peaks, and drops. It
            provides intuitive, real-world evidence of forecasting accuracy
            that numerical metrics alone cannot show.

            **Key takeaway:**
            The lag-based model closely tracks the actual PM2.5 pattern,
            capturing both trends and turning points, confirming strong
            predictive capability.""")
    with tab2:
        graph, info = st.columns([3, 2])
        with graph:
            st.subheader(":material/bar_chart: Model Performance Comparison")
            st.plotly_chart(befere_vs_after(baseline_mae,
                                            baseline_rmse,
                                            baseline_r2,
                                            lag_mae,
                                            lag_rmse,
                                            lag_r2),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            A grouped bar chart comparing MAE, RMSE, and R² for the baseline
            and lag-based models. Lower MAE/RMSE and higher R² indicate better
            forecasting performance.

            **Why it matters:**
            This visual makes it easy to see the magnitude of improvement
            delivered by lag features. The large gap between baseline and
            lag-based errors highlights how much more accurate the enhanced
            model is.

            **Key takeaway:**
            The lag-based model dramatically outperforms the baseline model,
            reducing error by over 70% and achieving far higher explanatory
            power.""")
    with tab3:
        graph, info = st.columns([3, 2])
        with graph:
            st.subheader(":material/insights:\
                          Lag-Based Model Feature Importance")
            st.plotly_chart(plot_lag_feature_importances(feature_importance),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            A ranked feature importance chart from the lag-based model,
            showing which predictors contribute most strongly to PM2.5
            forecasting.

            **Why it matters:**
            If lag features truly improve forecasting, they should appear as
            the most influential predictors. This confirms whether the model
            relies on recent PM2.5 history as expected.

            **Key takeaway:**
            Lag features dominate the model’s decision-making process,
            demonstrating that short-term pollutant persistence is the
            key driver of PM2.5 forecasting accuracy.""")
