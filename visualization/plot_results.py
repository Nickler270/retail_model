import matplotlib.pyplot as plt

def plot_forecast(df, forecast, chart_type="line"):
    df.set_index('date', inplace=True)

    plt.figure(figsize=(10, 6))

    if chart_type == "line":
        for product in df.columns:
            plt.plot(df.index, df[product], label=product)
        for product, value in forecast.items():
            plt.axhline(y=value, linestyle='--', label=f"{product} Forecast", alpha=0.7)

    elif chart_type == "bar":
        df.plot(kind="bar", figsize=(12, 6))
        for product, value in forecast.items():
            plt.axhline(y=value, linestyle='--', label=f"{product} Forecast", alpha=0.7)

    elif chart_type == "hist":
        for product in df.columns:
            plt.hist(df[product], bins=10, alpha=0.5, label=product)
        for product, value in forecast.items():
            plt.axvline(x=value, linestyle='--', label=f"{product} Forecast", alpha=0.7)

    else:
        raise ValueError("Invalid chart type. Choose from: 'line', 'bar', 'hist'.")

    plt.title(f"Product Sales and Forecast ({chart_type.capitalize()} Chart)")
    plt.xlabel("Date" if chart_type != "hist" else "Units Sold")
    plt.ylabel("Units Sold" if chart_type != "hist" else "Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"results/forecast_plot_{chart_type}.png")
    plt.show()
