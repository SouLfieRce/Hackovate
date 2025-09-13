# frontend/Home.py
import streamlit as st
from backend import database

def show():
    st.title("🚌 Smart Bus Management System")
    st.write("""
        Welcome to the **Smart Bus Optimization Dashboard**.  
        This system uses **SQL + Python backend + ML + Simulation** to make buses run smarter.  
    """)

    # Show quick stats from DB
    ticket_data = database.fetch_ticket_data()

    if not ticket_data.empty:
        st.metric("Total Tickets Recorded", len(ticket_data))
        st.metric("Unique Routes", ticket_data["route"].nunique())
    else:
        st.warning("⚠ No ticket data available. Please insert some records into the database.")
