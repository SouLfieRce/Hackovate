# backend/simulation.py
import time
import random
import pandas as pd

def simulate_bus_movement(bus_id, route, steps=10):
    """
    Simulates bus GPS + occupancy for demo
    """
    lat, lon = 12.9716, 77.5946  # Bangalore approx
    data = []

    for i in range(steps):
        lat += random.uniform(-0.001, 0.001)
        lon += random.uniform(-0.001, 0.001)
        occupancy = random.randint(10, 80)

        data.append({
            "bus_id": bus_id,
            "route": route,
            "latitude": lat,
            "longitude": lon,
            "occupancy": occupancy,
            "timestamp": pd.Timestamp.now()
        })

        time.sleep(0.5)  # mimic real-time feed

    return pd.DataFrame(data)
