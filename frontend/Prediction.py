# frontend/Prediction.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import prediction

def show():
    st.title("🔮 Passenger Demand Prediction")

    st.write("This page shows forecasted vs actual ridership for upcoming hours.")

    # Dummy data (replace with actual backend call)
    forecast_df = prediction.get_forecast()

    st.line_chart(forecast_df)

    st.info("Model predicts passenger demand for the next few hours.")
