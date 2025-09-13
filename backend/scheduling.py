# backend/scheduling.py
import pandas as pd

def optimize_schedule(ticket_df: pd.DataFrame):
    """
    Adjust frequency:
    - High demand → reduce gap
    - Low demand → increase gap
    """
    grouped = ticket_df.groupby(ticket_df["timestamp"].dt.hour)["passengers"].sum()

    schedule = {}
    for hour, demand in grouped.items():
        if demand > 150:      # Peak hours
            schedule[hour] = "Every 5 min"
        elif demand > 80:
            schedule[hour] = "Every 10 min"
        else:
            schedule[hour] = "Every 20 min"

    return schedule
