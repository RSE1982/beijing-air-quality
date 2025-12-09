import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.load_data import load_clustered, load_pca_coords
from utils.load_data import load_silhouette_values, load_cluster_profiles


df_clusters = load_clustered()
df_pca = load_pca_coords()
df_sil = load_silhouette_values()
cluster_profiles = load_cluster_profiles()


# Identify some numeric features for radar plots
NUMERIC_FEATURE_CANDIDATES = [
    "pm25",
    "temperature",
    "pressure",
    "dew_point",
    "wind_speed",
    "dew_point_spread",
    "temp_pres_interaction",
]

numeric_features = [
    col for col in NUMERIC_FEATURE_CANDIDATES
    if col in df_clusters.select_dtypes(include=["int64", "float64"]).columns
]


# ==============================
# Helper: Radar chart
# ==============================
def make_cluster_radar(df: pd.DataFrame, cluster_id: int,
                       features: list[str]) -> go.Figure:
    """
    Creates a normalised radar chart for a given cluster.
    Normalisation is done over cluster-level means for each feature.
    """
    if not features:
        return go.Figure()

    cluster_means_all = df.groupby("cluster")[features].mean()
    feature_min = cluster_means_all.min()
    feature_max = cluster_means_all.max()

    # avoid division by zero
    denom = (feature_max - feature_min).replace(0, 1e-9)

    this_cluster_mean = cluster_means_all.loc[cluster_id]
    scaled = (this_cluster_mean - feature_min) / denom

    theta = list(features) + [features[0]]
    r = scaled.tolist() + [scaled.tolist()[0]]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=r,
            theta=theta,
            fill="toself",
            name=f"Cluster {cluster_id}",
        )
    )

    fig.update_layout(
        title=f"Cluster {cluster_id} — Normalised Feature Profile",
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
    )
    return fig


# ==============================
# Sidebar — Cluster Profile Explorer
# ==============================
with st.sidebar:
    st.header("🧭 Cluster Profile Explorer")

    cluster_ids = sorted(df_clusters["cluster"].unique())
    default_cluster = cluster_ids[0] if cluster_ids else None

    selected_cluster = st.selectbox(
        "Select a cluster:",
        options=cluster_ids,
        index=0,
        format_func=lambda c: f"Cluster {c} — {cluster_profiles.get(c, {})
                                               .get('name', 'Unlabelled')}",
    )

    profile = cluster_profiles.get(selected_cluster, {})

    st.subheader(profile.get("name", f"Cluster {selected_cluster}"))
    st.write(profile.get("summary", "No profile description available."))

    notes = profile.get("notes", [])
    if notes:
        st.markdown("**Key characteristics:**")
        for item in notes:
            st.markdown(f"- {item}")

    st.markdown("---")
    st.caption(
        "Profiles are derived from cluster-level means of PM2.5 and key\
              meteorological features."
    )


# ==============================
# Main Page Title & Overview
# ==============================
st.title("🧩 Clustering Analysis")

st.markdown(
    """
This page summarises the clustering performed in **Notebook 10**:

- Visualising clusters in **PCA space**
- Understanding **cluster sizes** & **quality** (silhouette scores)
- Exploring **cluster-specific feature profiles**
- Providing **human-readable profiles** loaded from YAML
"""
)

# ==============================
# Section 1 — Cluster Overview
# ==============================
st.header("📌 Cluster Overview")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Observations", len(df_clusters))
with col2:
    st.metric("Number of Clusters", df_clusters["cluster"].nunique())
with col3:
    st.metric("Average Silhouette Score", f"{df_sil['silhouette'].mean():.3f}")

st.dataframe(df_clusters.head())


# ==============================
# Section 2 — PCA Visualisation
# ==============================
st.header("🌀 PCA Cluster Visualisation")

pca_clusters = st.multiselect(
    "Filter clusters:",
    options=sorted(df_pca["cluster"].unique()),
    default=sorted(df_pca["cluster"].unique()),
)

df_pca_filtered = df_pca[df_pca["cluster"].isin(pca_clusters)]

fig_pca = px.scatter(
    df_pca_filtered,
    x="pc1",
    y="pc2",
    color="cluster",
    hover_data=["cluster"],
    opacity=0.75,
    title="PCA Scatter Plot of Clusters",
)
fig_pca.update_traces(
    unselected=dict(marker=dict(opacity=0.15)),
    selected=dict(marker=dict(size=10, opacity=1)),
)
fig_pca.update_layout(
    hovermode="closest",
    clickmode="event+select",
)

st.plotly_chart(fig_pca, use_container_width=True)


# ==============================
# Section 3 — Cluster Size Distribution
# ==============================
st.header("📊 Cluster Size & Silhouette")

cluster_counts = df_clusters["cluster"].value_counts().sort_index()
fig_counts = px.bar(
    cluster_counts,
    title="Cluster Sizes",
    labels={"index": "Cluster", "value": "Count"},
)
st.plotly_chart(fig_counts, use_container_width=True)

fig_sil = px.box(
    df_sil,
    x="cluster",
    y="silhouette",
    title="Silhouette Values per Cluster",
    labels={"silhouette": "Silhouette Score"},
)
st.plotly_chart(fig_sil, use_container_width=True)


# ==============================
# Section 4 — Cluster Feature Profiles (Radar)
# ==============================
st.header("📡 Cluster Feature Profiles")

if not numeric_features:
    st.warning("No suitable numeric features found for radar charts.")
else:
    st.caption(
        "Features are normalised across cluster-level means to allow\
              comparison on a common 0–1 scale."
    )

    radar_features = st.multiselect(
        "Select features for radar chart:",
        options=numeric_features,
        default=numeric_features,
    )

    if radar_features:
        radar_fig = make_cluster_radar(df_clusters, selected_cluster,
                                       radar_features)
        st.plotly_chart(radar_fig, use_container_width=True)
    else:
        st.info("Select at least one feature to display the radar chart.")


# ==============================
# Section 5 — Cluster-wise Feature Distribution
# ==============================
st.header("🔍 Cluster Feature Exploration")

if numeric_features:
    feature_for_box = st.selectbox(
        "Select a feature to compare across clusters:",
        numeric_features,
    )

    fig_box = px.box(
        df_clusters,
        x="cluster",
        y=feature_for_box,
        points="all",
        title=f"{feature_for_box} Distribution Across Clusters",
    )
    st.plotly_chart(fig_box, use_container_width=True)
else:
    st.info("No numeric features available for distribution plots.")

st.header("📊 Cluster Size & Silhouette")

# ============================================================
# SECTION — Silhouette Plot (Classic Style)
# ============================================================

st.header("📈 Silhouette Plot (Cluster Quality)")

df_sil_sorted = df_sil.sort_values(["cluster", "silhouette"])
clusters = sorted(df_sil["cluster"].unique())

fig_silhouette = go.Figure()

y_offset = 0
yticks = []
ytick_labels = []

for cluster in clusters:
    cluster_values = df_sil_sorted[df_sil_sorted["cluster"]
                                   == cluster]["silhouette"]
    n_points = len(cluster_values)

    # Highlight if selected in sidebar
    if cluster == selected_cluster:
        opacity = 0.9
        line_width = 1.5
        bar_color = px.colors.qualitative.Set1[cluster % 9]
    else:
        opacity = 0.15
        line_width = 0.3
        bar_color = px.colors.qualitative.Set1[cluster % 9]

    fig_silhouette.add_trace(
        go.Bar(
            x=cluster_values,
            y=list(range(y_offset, y_offset + n_points)),
            orientation="h",
            marker=dict(color=cluster),
            showlegend=False,
        )
    )

    # Save centre position for y-axis tick
    yticks.append(y_offset + n_points / 2)
    ytick_labels.append(f"Cluster {cluster}")

    y_offset += n_points


# Add average silhouette score line
avg_sil = df_sil["silhouette"].mean()

fig_silhouette.add_vline(
    x=avg_sil,
    line_dash="dash",
    line_color="black",
    annotation_text=f"Avg Silhouette = {avg_sil:.3f}",
    annotation_position="top right",
)


fig_silhouette.update_layout(
    title="Silhouette Plot",
    xaxis_title="Silhouette score",
    yaxis=dict(
        tickmode="array",
        tickvals=yticks,
        ticktext=ytick_labels,
        showgrid=False,
    ),
    height=600,
)

st.plotly_chart(fig_silhouette, use_container_width=True)


st.success("Clustering analysis page loaded successfully.")

st.caption("""
© 2025 Robert Steven Elliott — Beijing Air Quality Capstone
Dataset © Song Chen (2017), licensed under CC BY 4.0
""")
