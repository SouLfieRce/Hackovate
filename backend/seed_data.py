# backend/seed_data.py
import random
import pandas as pd
from datetime import datetime, timedelta
from backend import database

def seed_ticket_sales(n=50):
    """
    Inserts random ticket sales into DB
    """
    routes = ["Route 1", "Route 2", "Route 3", "Route 5"]
    now = datetime.now()

    for _ in range(n):
        route = random.choice(routes)
        timestamp = now - timedelta(hours=random.randint(0, 48))  # last 2 days
        passengers = random.randint(10, 80)

        database.insert_ticket(route, timestamp, passengers)

    print(f"✅ Inserted {n} random ticket sales records")

def seed_gps_logs():
    """
    Just an example placeholder (you can expand later)
    """
    # For simplicity, let’s just say buses are around Bangalore
    gps_data = [
        ("B1", "Route 1", 12.9716, 77.5946),
        ("B2", "Route 2", 12.9612, 77.5845),
        ("B3", "Route 3", 12.9810, 77.6040),
    ]

    conn = database.get_connection()
    cur = conn.cursor()

    for bus_id, route, lat, lon in gps_data:
        cur.execute("INSERT INTO gps_logs (bus_id, route, timestamp, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
                    (bus_id, route, datetime.now(), lat, lon))

    conn.commit()
    conn.close()
    print("✅ Inserted sample GPS logs")

if __name__ == "__main__":
    database.create_tables()
    seed_ticket_sales(100)
    seed_gps_logs()
