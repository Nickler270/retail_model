def forecast_demand(df):
    forecast = {}
    for product in df.columns[1:]:
        # Simple 3-day moving average forecast
        forecast[product] = df[product].rolling(3).mean().iloc[-1]
    return forecast
