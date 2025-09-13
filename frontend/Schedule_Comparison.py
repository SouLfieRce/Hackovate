# frontend/Schedule_Comparison.py
import streamlit as st
from backend import database, data_cleaning, scheduling

def show():
    st.title("📊 Schedule Comparison")

    ticket_data = database.fetch_ticket_data()

    if ticket_data.empty:
        st.warning("No ticket sales data available.")
        return

    # Clean data
    clean_data = data_cleaning.clean_ticket_data(ticket_data)

    # Original schedule (just dummy fixed)
    st.subheader("🕒 Original Schedule (Static)")
    st.write("Every 15 minutes for all routes.")

    # Optimized schedule
    st.subheader("⚡ Optimized Schedule (Dynamic)")
    optimized = scheduling.optimize_schedule(clean_data)

    for hour, freq in optimized.items():
        st.write(f"Hour {hour}: {freq}")

    st.success("✅ Schedule optimized based on demand!")
