# backend/prediction.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def get_forecast():
    # Dummy dataset for demo
    data = {
        "hour": list(range(0, 24)),
        "passengers": [np.random.randint(20, 100) for _ in range(24)]
    }
    df = pd.DataFrame(data)

    # Simple linear regression forecast
    X = df[["hour"]]
    y = df["passengers"]

    model = LinearRegression()
    model.fit(X, y)

    # Predict next 6 hours
    future_hours = np.array(range(24, 30)).reshape(-1, 1)
    forecast = model.predict(future_hours)

    forecast_df = pd.DataFrame({
        "hour": list(range(24, 30)),
        "forecast_passengers": forecast.astype(int)
    })
    return forecast_df
