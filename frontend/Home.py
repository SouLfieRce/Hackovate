# frontend/Home.py
import streamlit as st

def show():
    st.title("🚌 Smart Bus Management System")
    st.write("""
        Welcome to the **Smart Bus Optimization Dashboard**!  
        This tool helps optimize city bus schedules using **real-time data, demand prediction, and simulation**.  
        
        ### Features:
        - 📊 Compare Original vs Optimized schedules  
        - 🔮 Forecast ridership for upcoming hours  
        - 🚍 Simulate live bus movement and occupancy  
        - ⚡ Reduce waiting time & bus bunching  
    """)
    st.success("Use the sidebar to navigate through different modules.")
