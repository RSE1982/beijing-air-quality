import streamlit as st
from utils.data_loader import (load_clustered,
                               load_pca_coords,
                               load_silhouette_values,
                               load_cluster_profiles)
from utils.clustering_charts import (make_cluster_radar,
                                     pca_cluster_scatter,
                                     plot_cluster_size,
                                     silhouette_values_per_cluster,
                                     silhouette_plot)

df_clusters = load_clustered()
df_pca = load_pca_coords()
df_sil = load_silhouette_values()
cluster_profiles = load_cluster_profiles()

# Identify some numeric features for radar plots
NUMERIC_FEATURES = [
    "pm25",
    "temperature",
    "pressure",
    "dew_point",
    "wind_speed",
    "dew_point_spread",
    "temp_pres_interaction",
]

selected_cluster = st.session_state.get("selected_cluster", 0)
profile = cluster_profiles.get(selected_cluster, {})


st.title("🧩 Clustering Analysis")

col1, col2 = st.columns([1, 3])
with col1:
    tab1, tab2 = st.tabs(["📊 Overview", "📖 Cluster Profile"])
    with tab1:
        st.subheader("Overview")
        st.markdown("""
        This page summarises the clustering performed in **Notebook 10**:

        - Visualising clusters in **PCA space**
        - Understanding **cluster sizes** & **quality** (silhouette scores)
        - Exploring **cluster-specific feature profiles**
        - Providing **human-readable profiles** loaded from YAML
        """)

        m1, m2 = st.columns(2)
        m3, _ = st.columns(2)
        m1.metric("Total Observations", len(df_clusters))
        m2.metric("Number of Clusters", df_clusters["cluster"].nunique())
        m3.metric("Average Silhouette Score",
                  f"{df_sil['silhouette'].mean():.3f}")
    with tab2:
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
with col2:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 PCA Visualisation",
                                            "📖 Cluster Size",
                                            "📈 Silhouette Values per Cluster",
                                            "📡 Cluster Feature Profile",
                                            "📉 Silhouette Plot"])
    with tab1:
        st.header("🌀 PCA Cluster Visualisation")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(pca_cluster_scatter(df_pca),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            A 2D projection of the clusters using PCA, where each point
            represents an observation positioned based on the most important
            variance directions. Colours indicate cluster membership.

            **Why it matters:**
            PCA reduces dimensionality, making it easier to see whether
            clusters are well separated or overlapping. Clear separation
            suggests that K-Means found meaningful structure, while overlap
            indicates clusters with similar characteristics.

            **Key takeaway:**
            The PCA plot provides a quick visual assessment of cluster
            separability and structure, showing how distinct or blended the
            clusters are in reduced feature space.
            """)
    with tab2:
        st.header("📊 Cluster Size")
        graph, info = st.columns([3, 2])
        with graph:
            cluster_counts = df_clusters["cluster"].value_counts().sort_index()
            st.plotly_chart(plot_cluster_size(df_clusters),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            A bar chart showing how many observations belong to each cluster.

            **Why it matters:**
            Cluster sizes reveal whether some clusters dominate the dataset or
            whether the groups are balanced. Very small clusters may be
            outliers; very large clusters may be too general.

            **Key takeaway:**
            The distribution of cluster sizes helps identify dominant
            clusters, rare patterns, and potential imbalances within the data.
            """)
    with tab3:
        st.header("📈 Silhouette Values per Cluster")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(silhouette_values_per_cluster(df_sil),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            What this shows:
            A boxplot of silhouette scores for each cluster, showing how well
            each point fits within its assigned cluster compared to
            neighbouring clusters.

            **Why it matters:**
            Silhouette values measure cluster quality:

            - High values → tightly grouped, well-separated clusters
            - Low or negative values → overlapping or poorly defined clusters

            Understanding variability within each cluster is crucial for
            evaluating reliability.

            **Key takeaway:**
            Clusters with higher median silhouette scores are stronger and
            more distinct, while clusters with low or wide ranges of
            silhouette values may require re-evaluation.
            """)
    with tab4:
        st.header("📡 Cluster Feature Profiles")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(make_cluster_radar(df_clusters,
                                               selected_cluster,
                                               NUMERIC_FEATURES),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            A radar chart comparing the normalised mean values of key features
            within the selected cluster. Each spike represents a feature
            relative to other clusters.

            **Why it matters:**
            Radar profiles clearly highlight what makes a cluster unique — for
            example, higher PM2.5, lower wind speeds, or distinct temperature
            patterns. This provides human-readable insight into the behaviour
            of each cluster.

            **Key takeaway:**
            Radar charts show each cluster's defining characteristics, helping
            interpret the environmental and pollution patterns that
            differentiate one cluster from another.
            """)
    with tab5:
        st.header("📈 Silhouette Plot (Cluster Quality)")
        graph, info = st.columns([3, 2])
        with graph:
            st.plotly_chart(silhouette_plot(df_sil, selected_cluster),
                            use_container_width=True)
        with info:
            st.markdown("""
            **What this shows:**
            A classic silhouette plot showing individual silhouette scores for
            each sample within each cluster, with an average silhouette
            benchmark line.

            **Why it matters:**
            This plot reveals how consistently each cluster is formed. Tall,
            dense bands with high silhouette scores indicate strong clusters;
            thin or low-value bands indicate weak or overlapping clusters.

            **Key takeaway:**
            The silhouette plot provides a comprehensive view of cluster
            cohesion and separation, highlighting which clusters are
            well-defined and which may require further tuning.
            """)
