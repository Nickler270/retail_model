import matplotlib.pyplot as plt

def plot_forecast(df, forecast):
    df.set_index('date', inplace=True)
    plt.figure(figsize=(10, 6))

    for product in df.columns:
        plt.plot(df.index, df[product], label=product)

    for product, value in forecast.items():
        plt.axhline(y=value, linestyle='--', label=f"{product} Forecast", alpha=0.7)

    plt.title("Product Sales and Forecast")
    plt.xlabel("Date")
    plt.ylabel("Units Sold")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/forecast_plot.png")
    plt.show()

