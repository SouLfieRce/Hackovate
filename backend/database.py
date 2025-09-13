# backend/database.py
import sqlite3
import pandas as pd

DB_NAME = "data/smart_bus.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Ticket sales table
    cur.execute('''CREATE TABLE IF NOT EXISTS ticket_sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        route TEXT,
                        timestamp DATETIME,
                        passengers INTEGER
                    )''')

    # GPS logs
    cur.execute('''CREATE TABLE IF NOT EXISTS gps_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bus_id TEXT,
                        route TEXT,
                        timestamp DATETIME,
                        latitude REAL,
                        longitude REAL
                    )''')

    conn.commit()
    conn.close()

def insert_ticket(route, timestamp, passengers):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ticket_sales (route, timestamp, passengers) VALUES (?, ?, ?)",
                (route, timestamp, passengers))
    conn.commit()
    conn.close()

def fetch_ticket_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM ticket_sales", conn)
    conn.close()
    return df
