# backend/data_cleaning.py
import pandas as pd

def clean_ticket_data(df: pd.DataFrame):
    # Drop duplicates
    df = df.drop_duplicates()

    # Fill missing passenger counts with median
    df["passengers"] = df["passengers"].fillna(df["passengers"].median())

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # Remove outliers (e.g., > 200 passengers in one ticket = invalid)
    df = df[df["passengers"] <= 200]

    return df
