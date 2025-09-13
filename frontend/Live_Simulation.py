"""
Real-time Bus Updates + Map using Streamlit

How to use:
1. Save this file as `streamlit_realtime_bus_map.py`.
2. Install dependencies:
   pip install streamlit pandas requests pydeck python-dotenv
3. If you have a real-time bus positions API, set its URL in the sidebar or in a .env file as BUS_API_URL.
   The expected JSON format (one object per vehicle) is:
   [
     {
       "id": "vehicle_123",
       "lat": 23.0225,
       "lon": 72.5714,
       "route": "5A",
       "speed": 28.2,
       "bearing": 120,
       "timestamp": "2025-09-13T08:12:03Z"
     },
     ...
   ]

4. Run:
   streamlit run streamlit_realtime_bus_map.py

This app will poll the API every `refresh_interval` seconds by default and update the map.
If no API URL is provided, the app will run a local simulated stream (good for testing).

"""

import streamlit as st
import pandas as pd
import requests
import time
import pydeck as pdk
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import random

load_dotenv()

# ------------------------
# Helper functions
# ------------------------

def fetch_bus_data(api_url: str, timeout=5):
    """Fetch bus data from a REST endpoint returning JSON array of vehicle objects."""
    try:
        resp = requests.get(api_url, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Expecting list of dicts
        if isinstance(data, dict):
            # maybe wrapped
            candidates = None
            for key in ("vehicles", "data", "results"):
                if key in data:
                    candidates = data[key]
                    break
            if candidates is not None:
                data = candidates
            else:
                # fallback: try to extract list values
                data = [data]
        return data
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")
        return []


def simulate_bus_data(center=(23.0225,72.5714), n=8):
    """Create simulated moving bus data around a center point (lat, lon)."""
    lat0, lon0 = center
    vehicles = []
    for i in range(n):
        vid = f"BUS_{100+i}"
        # random walk offsets
        lat = lat0 + random.uniform(-0.02, 0.02) + 0.001 * (time.time() % 10 - 5) / 5
        lon = lon0 + random.uniform(-0.02, 0.02) + 0.001 * (time.time() % 10 - 5) / 5
        route = random.choice(["5A", "12B", "Express1", "C1"])
        speed = max(0, random.gauss(20, 6))
        bearing = random.uniform(0, 360)
        timestamp = datetime.now(timezone.utc).isoformat()
        vehicles.append({
            "id": vid,
            "lat": lat,
            "lon": lon,
            "route": route,
            "speed": round(speed, 1),
            "bearing": round(bearing, 1),
            "timestamp": timestamp,
        })
    return vehicles


def to_dataframe(vehicles):
    """Normalize vehicle list into a pandas DataFrame.
    Handles some common field names for lat/lon.
    """
    if not vehicles:
        return pd.DataFrame(columns=["id", "lat", "lon", "route", "speed", "bearing", "timestamp"])

    rows = []
    for v in vehicles:
        vid = v.get("id") or v.get("vehicle_id") or v.get("vid")
        lat = v.get("lat") or v.get("latitude") or v.get("y")
        lon = v.get("lon") or v.get("lng") or v.get("longitude") or v.get("x")
        route = v.get("route") or v.get("route_id") or v.get("line") or "-"
        speed = v.get("speed") or v.get("velocity") or 0
        bearing = v.get("bearing") or v.get("heading") or 0
        ts = v.get("timestamp") or v.get("time") or v.get("last_update") or datetime.now(timezone.utc).isoformat()
        try:
            # try parsing numeric lat/lon
            lat = float(lat)
            lon = float(lon)
        except Exception:
            continue
        rows.append({"id": str(vid), "lat": lat, "lon": lon, "route": str(route), "speed": float(speed), "bearing": float(bearing), "timestamp": ts})
    df = pd.DataFrame(rows)
    return df


def make_pydeck(df, initial_view_state=None):
    """Create a pydeck map with bus markers and small popups."""
    if initial_view_state is None:
        if len(df):
            center_lat = float(df['lat'].mean())
            center_lon = float(df['lon'].mean())
            initial_view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=12, pitch=0)
        else:
            # fallback to Ahmedabad center (example)
            initial_view_state = pdk.ViewState(latitude=23.0225, longitude=72.5714, zoom=12, pitch=0)

    # Prepare data for pydeck
    df_copy = df.copy()
    df_copy['position'] = df_copy[['lon', 'lat']].values.tolist()
    df_copy['tooltip'] = df_copy.apply(lambda r: f"{r['id']} — Route: {r['route']}\nSpeed: {r['speed']} km/h\nTime: {r['timestamp']}", axis=1)

    scatter = pdk.Layer(
        "ScatterplotLayer",
        data=df_copy,
        get_position="position",
        get_fill_color="[255 - (speed * 6 % 255), speed * 6 % 255, 120]",
        get_radius=80,
        pickable=True,
        auto_highlight=True,
    )

    icon_data = df_copy.copy()
    # Icon layer expects a URL or predefined mapping. We'll use a simple circle via ScatterplotLayer for now.

    tooltip = {"html": "<b>{id}</b><br/>{tooltip}", "style": {"backgroundColor": "steelblue", "color": "white"}}

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
        initial_view_state=initial_view_state,
        layers=[scatter],
        tooltip=tooltip,
    )

    return deck


# ------------------------
# Streamlit App
# ------------------------

st.set_page_config(page_title="Real-time Bus Map", layout="wide")

st.title("🚌 Real-time Bus Updates — Map View")

# Sidebar controls
st.sidebar.header("Settings")
DEFAULT_API = os.getenv("BUS_API_URL", "")
api_url = st.sidebar.text_input("Bus positions API URL (leave empty to simulate)", value=DEFAULT_API)
refresh_interval = st.sidebar.number_input("Refresh interval (seconds)", min_value=1, max_value=60, value=5, step=1)
show_table = st.sidebar.checkbox("Show raw data table", value=True)

route_filter = st.sidebar.text_input("Filter by route (comma separated, leave empty for all)")
min_speed = st.sidebar.number_input("Minimum speed (km/h) filter", min_value=0.0, value=0.0)

st.sidebar.markdown("---")
if api_url:
    st.sidebar.write("Fetching from:")
    st.sidebar.code(api_url)
else:
    st.sidebar.info("No API URL provided — running simulated stream.")

# Session state setup
if 'last_fetch' not in st.session_state:
    st.session_state.last_fetch = None
if 'last_df' not in st.session_state:
    st.session_state.last_df = pd.DataFrame()

# Fetch once immediately (or simulate)
with st.spinner("Fetching vehicle positions..."):
    if api_url.strip():
        raw = fetch_bus_data(api_url.strip())
    else:
        raw = simulate_bus_data()

    df = to_dataframe(raw)
    st.session_state.last_fetch = datetime.now(timezone.utc).isoformat()
    st.session_state.last_df = df

# Apply filters
if route_filter.strip():
    wanted = set([r.strip() for r in route_filter.split(',') if r.strip()])
    if wanted:
        df = df[df['route'].isin(wanted)]

if min_speed > 0:
    df = df[df['speed'] >= min_speed]

# Layout: map on left, controls + list on right
left_col, right_col = st.columns([3, 1])

with left_col:
    st.subheader("Live map")
    if df.empty:
        st.info("No vehicles to display for the selected filters.")
    deck = make_pydeck(df)
    st.pydeck_chart(deck)

with right_col:
    st.subheader("Vehicles")
    st.write(f"Last fetch (UTC): {st.session_state.last_fetch}")
    if df.empty:
        st.write("No vehicles match the current filters.")
    else:
        st.dataframe(df[['id', 'route', 'speed', 'lat', 'lon', 'timestamp']].sort_values(by='route'))

# Optional raw table
if show_table:
    st.markdown("---")
    st.subheader("Raw vehicle data")
    st.write("(You can copy/download this table)")
    st.dataframe(st.session_state.last_df)

# Auto-refresh area: instruct Streamlit to rerun
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 6])
with col1:
    if st.button("Refresh now"):
        st.experimental_rerun()
with col2:
    st.write(f"Auto-refresh every {refresh_interval} s")

# This is the minimal 'real-time' loop via Streamlit's `st.experimental_rerun()` + timer.
# We'll trigger a rerun after `refresh_interval` seconds using st.experimental_sleep if available.
try:
    # For Streamlit >=1.18, st.experimental_sleep is available; else use time.sleep + rerun pattern
    st.experimental_sleep(refresh_interval)
    # After sleep, re-run the script
    st.experimental_rerun()
except Exception:
    # Fallback: use time.sleep then rerun (works but blocks)
    time.sleep(refresh_interval)
    st.experimental_rerun()
