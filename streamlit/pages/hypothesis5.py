import streamlit as st
from utils.load_data import load_engineered
import plotly.graph_objects as go

st.title("🤖 Hypothesis 5 — Lag Features Improve Model Performance")

df = load_engineered()

st.write("""
### 📌 Hypothesis H5
**Lag features improve PM2.5 forecasting performance compared to baseline
          models.**

Models compared:
- Baseline: weather + time features only
- Lag-based: pm25_lag_1h, 3h, 6h, 12h, 18h + rolling means
""")

# ------------------------- Performance Comparison -------------------------
st.subheader("📊 Model Performance Comparison")

# Replace these with values from your notebook
baseline_mae = 37.613408
baseline_rmse = 52.778598
baseline_r2 = 0.450872
lag_mae = 10.001359
lag_rmse = 16.223324
lag_r2 = 0.941921

fig = go.Figure(data=[
    go.Bar(name="Baseline Model",
           x=["MAE", "RMSE"],
           y=[baseline_mae, baseline_rmse]),
    go.Bar(name="Lag-Based Model",
           x=["MAE", "RMSE"],
           y=[lag_mae, lag_rmse])
])
fig.update_layout(
    title="MAE & RMSE Comparison: Baseline vs Lag-Based Model",
    yaxis_title="Error (µg/m³)",
    barmode="group"
)
st.plotly_chart(fig, use_container_width=True)


fig = go.Figure(data=[
    go.Bar(name="Baseline Model",
           x=["R2"],
           y=[baseline_r2]),
    go.Bar(name="Lag-Based Model",
           x=["R2"],
           y=[lag_r2])
])
fig.update_layout(
    title="R2 Comparison: Baseline vs Lag-Based Model",
    yaxis_title="R2",
    barmode="group"
)
st.plotly_chart(fig, use_container_width=True)


# ------------------------- Observations -------------------------
st.markdown("### 📝 Observations")
st.markdown("""
- Lag-based model reduces error by **40–50%**, a substantial improvement.
- Rolling mean features help smooth volatility and capture pollutant momentum.
- Feature importance plots showed lag features dominating predictive power.
""")

# ------------------------- Justification -------------------------
st.markdown("### 🎯 Justification")
st.markdown("""
Lag features encode pollutant persistence and short-term autocorrelation,
             which are
critical for air-quality forecasting.
Notebook 09 confirmed that lag-based XGBoost achieved the
            **best RMSE and MAE scores**.
""")

st.success("✔ **Conclusion:** H5 is supported —  \
            lag features significantly improve forecasting accuracy.")

st.caption("Source: Notebook 09 — Forecasting Analysis \
           • Dataset © Song Chen (CC BY 4.0)")
