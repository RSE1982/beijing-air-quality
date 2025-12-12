import streamlit as st

# Configure the Streamlit page
st.set_page_config(
    page_title="Beijing Clean Air Dashboard",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.html("""
<style>
    /* Remove default page padding */
    .block-container {
        padding-top: 3rem !important;  /* adjust for cloud bar */
        padding-bottom: 0rem !important;
        margin-bottom: 0rem !important;
    }
</style>
""")

weather_vars = ["temperature",
                "dew_point",
                "pressure",
                "rain",
                "wind_speed",
                "relative_humidity"]  # List of weather variables

# Title of the dashboard
st.title("🌆 Beijing Clean Air Dashboard")
st.write("Analyze Beijing's air quality through\
          various hypotheses and models.")

# Define pages for navigation
homepage = st.Page("pages/home.py",
                   title="Home",
                   icon=":material/home:")
about = st.Page("pages/about.py",
                title="About",
                icon=":material/info:")
overview = st.Page("pages/overview.py",
                   title="Overview",
                   icon=":material/overview:")
hypothesis1 = st.Page("pages/hypothesis1.py",
                      title="Hypothesis 1",
                      icon=":material/biotech:")
hypothesis2 = st.Page("pages/hypothesis2.py",
                      title="Hypothesis 2",
                      icon=":material/biotech:")
hypothesis3 = st.Page("pages/hypothesis3.py",
                      title="Hypothesis 3",
                      icon=":material/biotech:")
hypothesis4 = st.Page("pages/hypothesis4.py",
                      title="Hypothesis 4",
                      icon=":material/biotech:")
hypothesis5 = st.Page("pages/hypothesis5.py",
                      title="Hypothesis 5",
                      icon=":material/biotech:")
clustering = st.Page("pages/clustering.py",
                     title="Clustering Analysis",
                     icon=":material/bubble_chart:")
modelling = st.Page("pages/modelling.py",
                    title="Modeling",
                    icon=":material/psychology:")
forcasting = st.Page("pages/forecasting.py",
                     title="Air Quality Forecasting",
                     icon=":material/trending_up:")

# Set up navigation
nav = st.navigation({
    "Dashboard": [
        homepage,
        overview,
        about],

    "Hypotheses": [
        hypothesis1,
        hypothesis2,
        hypothesis3,
        hypothesis4,
        hypothesis5,
    ],

    "Analysis": [
        clustering
    ],

    "Forecasting": [
        modelling,
        forcasting],
})

current_page = nav.title

# Sidebar filters based on the current page
if current_page == "Hypothesis 3":
    st.sidebar.header("Filters for Hypothesis 3")
    weather_filter = st.sidebar.radio(
        "Select Meteorological Variable",
        options=weather_vars,
        index=0,
        format_func=lambda w: w.replace("_", " ").title(),
        key="weather_filter"
    )
if current_page == "Clustering Analysis":
    st.sidebar.header("Cluster Profile")
    cluster_ids = [0, 1, 2, 3, 4, 5, 6, 7]
    default_cluster = cluster_ids[0] if cluster_ids else None

    selected_cluster = st.sidebar.radio(
        "Select a cluster:",
        options=cluster_ids,
        index=0,
        format_func=lambda c: f"Cluster {c}",
        key="selected_cluster"
    )

if current_page == "Air Quality Forecasting":
    st.sidebar.header("Forecast Settings")
    horizon_label = st.sidebar.radio(
        "Select Forecast Horizon:",
        [
            "3 Hours",
            "6 Hours",
            "12 Hours",
            "18 Hours",
            "24 Hours",
            "48 Hours"
        ],
        key="horizon_label"
    )

# Include a footer in the sidebar
st.sidebar.caption("""
    © 2025 Robert Steven Elliott\\
    Beijing Air Quality Capstone\\
    Dataset © Song Chen (2017),
    licensed under CC BY 4.0
""")

# Run the navigation
nav.run()
