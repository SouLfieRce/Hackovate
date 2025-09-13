# app.py
import streamlit as st
from utils import config

# Set Streamlit page settings
st.set_page_config(
    page_title="Smart Bus Optimization",
    page_icon="🚌",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("🚌 Smart Bus Optimization")
page = st.sidebar.radio("Go to", [
    "Home",
    "Schedule Comparison",
    "Prediction",
    "Live Simulation"
])

# Import frontend pages
from frontend import Home, Schedule_Comparison, Prediction, Live_Simulation

# Page Routing
if page == "Home":
    Home.show()
elif page == "Schedule Comparison":
    Schedule_Comparison.show()
elif page == "Prediction":
    Prediction.show()
elif page == "Live Simulation":
    Live_Simulation.show()
