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

    /* Remove plot margins */
    div[data-testid="stPlot"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stPlotlyChart"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Force body to not scroll */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        height: 100%;
        overflow: hidden !important;
    }

    /* Allow main content area to scroll *internally* if needed */
    [data-testid="stMain"] {
        overflow-y: auto !important;
        height: calc(100vh - 3rem); /* account for Cloud toolbar */
    }

</style>
""")

# Title of the dashboard
st.title("🌆 Beijing Clean Air Dashboard")
st.write("Analyze Beijing's air quality through\
          various hypotheses and models.")

# Define pages for navigation
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
predictor = st.Page("pages/predictor.py",
                    title="Air Quality Predictor",
                    icon="🤖")

nav = st.navigation([overview, hypothesis1, hypothesis2, hypothesis3,
                     hypothesis4, hypothesis5, clustering, forcasting,
                     modelling, predictor])

current_page = nav.title

# ---------------- Sidebar (filters) ----------------

# Run the navigation
nav.run()
