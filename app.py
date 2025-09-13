# app.py
import streamlit as st
from frontend import Home, Schedule_Comparison, Prediction, Live_Simulation
from backend import database

# Setup DB
database.create_tables()

st.set_page_config(page_title="Smart Bus Optimization", page_icon="🚌", layout="wide")

st.sidebar.title("🚌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Schedule Comparison", "Prediction", "Live Simulation"])

if page == "Home":
    Home.show()
elif page == "Schedule Comparison":
    Schedule_Comparison.show()
elif page == "Prediction":
    Prediction.show()
elif page == "Live Simulation":
    Live_Simulation.show()
