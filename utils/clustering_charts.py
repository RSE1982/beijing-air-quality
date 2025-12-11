import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.charts import MARGINS

CLUSTER_COLORS_INT = {
    0: "#1f77b4",
    1: "#ff7f0e",
    2: "#2ca02c",
    3: "#d62728",
    4: "#9467bd",
    5: "#8c564b",
    6: "#e377c2",
    7: "#7f7f7f",
}

CLUSTER_COLORS_STR = {str(k): v for k, v in CLUSTER_COLORS_INT.items()}

def make_cluster_radar(df: pd.DataFrame, cluster_id: int,
                       features: list[str]) -> go.Figure:
    """
    Creates a normalised radar chart for a given cluster.
    Normalisation is done over cluster-level means for each feature.
    """
    color = CLUSTER_COLORS_INT[cluster_id]

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
            line=dict(color=color),
            marker=dict(color=color)
        )
    )

    fig.update_layout(
        title=f"Cluster {cluster_id} — Normalised Feature Profile",
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        margin=MARGINS,
        height=400,
        width=400
    )
    return fig

def pca_cluster_scatter(df: pd.DataFrame) -> go.Figure:
    """
    Creates a PCA scatter plot colored by cluster.
    """
    df["cluster"] = df["cluster"].astype(str)  # Ensure cluster is string for color mapping
    fig = px.scatter(
        df.sort_values("cluster"),
        x="pc1",
        y="pc2",
        color="cluster",
        color_discrete_map=CLUSTER_COLORS_STR,
        hover_data=["cluster"],
        opacity=0.8,
        title="PCA Scatter Plot of Clusters",
        labels={"pc1": "Principal Component 1", "pc2": "Principal Component 2"}
    )
    
    fig.update_layout(legend_title_text="Cluster",
                      margin=MARGINS,
                      height=400)

    return fig

def plot_cluster_size(df: pd.DataFrame) -> go.Figure:
    """
    Plots the size of each cluster as a bar chart.
    """
    cluster_counts = df["cluster"].value_counts().sort_index()
    fig = px.bar(
        cluster_counts,
        title="Cluster Sizes",
        color=cluster_counts.index.astype(str),
        color_discrete_map=CLUSTER_COLORS_STR,
        labels={"index": "Cluster", "value": "Count"},
    )
    fig.update_layout(legend_title_text="Cluster",
                      margin=MARGINS,
                      height=400)
    return fig

def silhouette_values_per_cluster(df: pd.DataFrame) -> go.Figure:
    """
    Creates a silhouette plot highlighting the selected cluster.
    """
    fig = px.box(
    df.sort_values("cluster"),
    x="cluster",
    y="silhouette",
    color="cluster",
    color_discrete_map=CLUSTER_COLORS_STR,
    title="Silhouette Values per Cluster",
    labels={"silhouette": "Silhouette Score"},
)
    fig.update_layout(legend_title_text="Cluster",
                      margin=MARGINS,
                      height=400)
    return fig

def silhouette_plot(df_sil: pd.DataFrame,
                    selected_cluster: int) -> go.Figure:
    """
    Creates a horizontal silhouette plot for all clusters.
    
    Parameters
    ----------
    df_sil : pd.DataFrame
        Must contain 'cluster' and 'silhouette' columns.
    selected_cluster : int
        Cluster to highlight.
    color_map : dict
        Mapping of cluster_id -> colour hex string.

    Returns
    -------
    go.Figure
    """

    df_sil_sorted = df_sil.sort_values(["cluster", "silhouette"])
    clusters = sorted(df_sil_sorted["cluster"].unique())
    color_map = CLUSTER_COLORS_INT
    fig = go.Figure()

    y_offset = 0
    yticks = []
    ytick_labels = []

    for cluster in clusters:
        cluster_values = df_sil_sorted[df_sil_sorted["cluster"] == cluster]["silhouette"]
        n_points = len(cluster_values)

        # Standardised colour from your cluster mapping
        color = color_map.get(cluster, "#333333")  # fallback colour

        # Selected cluster = highlight
        opacity = 0.9 if cluster == selected_cluster else 0.25

        # Add silhouette bar series
        fig.add_trace(go.Bar(
            x=cluster_values,
            y=list(range(y_offset, y_offset + n_points)),
            orientation="h",
            marker=dict(color=color, opacity=opacity),
            hoverinfo="x+y",
            showlegend=False,
        ))

        # Y-axis cluster label position
        yticks.append(y_offset + n_points / 2)
        ytick_labels.append(f"Cluster {cluster}")

        y_offset += n_points  # move to next block

    # Average silhouette score
    avg_sil = df_sil["silhouette"].mean()

    fig.add_vline(
        x=avg_sil,
        line_dash="dash",
        line_color="black",
        annotation_text=f"Avg Silhouette = {avg_sil:.3f}",
        annotation_position="top right"
    )

    fig.update_layout(
        title="Silhouette Plot (Cluster Quality)",
        xaxis_title="Silhouette score",
        yaxis=dict(
            tickmode="array",
            tickvals=yticks,
            ticktext=ytick_labels,
            showgrid=False
        ),
        height=400,
        bargap=0.05,
        margin=MARGINS
    )

    return fig
