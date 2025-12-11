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
                "relative_humidity"] # List of weather variables

# Title of the dashboard
st.title("🌆 Beijing Clean Air Dashboard")
st.write("Analyze Beijing's air quality through\
          various hypotheses and models.")

# Define pages for navigation
homepage = st.Page("pages/home.py",
                   title="Home",
                   icon="🏠")
about = st.Page("pages/about.py",
                title="About",
                icon="ℹ️")
overview = st.Page("pages/overview.py",
                   title="Overview",
                   icon="🏠")
hypothesis1 = st.Page("pages/hypothesis1.py",
                      title="Hypothesis 1",
                      icon="❓")
hypothesis2 = st.Page("pages/hypothesis2.py",
                      title="Hypothesis 2",
                      icon="❓")
hypothesis3 = st.Page("pages/hypothesis3.py",
                      title="Hypothesis 3",
                      icon="❓")
hypothesis4 = st.Page("pages/hypothesis4.py",
                      title="Hypothesis 4",
                      icon="❓")
hypothesis5 = st.Page("pages/hypothesis5.py",
                      title="Hypothesis 5",
                      icon="❓")
clustering = st.Page("pages/clustering.py",
                     title="Clustering Analysis",
                     icon="📊")
modelling = st.Page("pages/modelling.py",
                    title="Modeling",
                    icon="🧠")
forcasting = st.Page("pages/forecasting.py",
                     title="Air Quality Forecasting",
                     icon="📈")

nav = st.navigation({
    "🏠 Dashboard": [
        homepage,
        overview,
        about],   # top-level page, NOT a list

    "🔬 Hypotheses": [         # submenu, MUST be a list
        hypothesis1,
        hypothesis2,
        hypothesis3,
        hypothesis4,
        hypothesis5,
    ],

    "📊 Analysis": [           # submenu, MUST be a list
        clustering,
        modelling,
    ],

    "📈 Forecasting": [forcasting],  # top-level page, NOT a list
})

current_page = nav.title

# ---------------- Sidebar (filters) ----------------

if current_page == "Hypothesis 3":
    st.sidebar.header("Filters for Hypothesis 3")
    st.sidebar.write("Adjust the parameters below to filter the data displayed in Hypothesis 3 analysis.")
    weather_filter = st.sidebar.selectbox(
        "Select Meteorological Variable",
        weather_vars,
        index=0,
        key="weather_filter"
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
