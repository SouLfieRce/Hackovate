# frontend/Prediction.py
import streamlit as st
from backend import prediction
import pandas as pd

def show():
    st.title("🔮 Passenger Demand Prediction")

    forecast_df = prediction.get_forecast()

    st.line_chart(forecast_df.set_index("hour"))

    st.dataframe(forecast_df)

    st.success("✅ Forecast generated using simple ML model.")
