# frontend/Live_Simulation.py
import streamlit as st
from backend import simulation
import folium
from streamlit_folium import st_folium

def show():
    st.title("🚍 Live Bus Simulation")

    st.write("Simulating real-time bus movement and occupancy...")

    bus_data = simulation.simulate_bus_movement(bus_id="B1", route="Route 5", steps=5)

    # Show table
    st.dataframe(bus_data)

    # Show on map
    if not bus_data.empty:
        last_lat = bus_data.iloc[-1]["latitude"]
        last_lon = bus_data.iloc[-1]["longitude"]

        m = folium.Map(location=[last_lat, last_lon], zoom_start=14)
        for _, row in bus_data.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5,
                popup=f"Bus {row['bus_id']} | Occ: {row['occupancy']}"
            ).add_to(m)

        st_folium(m, width=700, height=500)
