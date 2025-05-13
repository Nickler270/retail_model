# -*- coding: utf-8 -*-
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Simulated forecasting using exponential smoothing
def exponential_smoothing(data, alpha=0.3):
    forecast = [data[0]]
    for t in range(1, len(data)):
        forecast.append(alpha * data[t-1] + (1 - alpha) * forecast[t-1])
    return forecast

# dummy LP func 
def allocate_resources(forecasted_demand):
    allocation = {k: max(0, v - 5) for k, v in forecasted_demand.items()} 
    return allocation

def plot_forecast(sales_data, forecast, filename):
    plt.figure(figsize=(10, 6))
    for product in sales_data:
        plt.plot(sales_data[product], label=f"{product} Actual", linewidth=2)
        plt.plot(forecast[product], linestyle="--", label=f"{product} Forecast")
    plt.title("Forecast vs Actual")
    plt.xlabel("Day")
    plt.ylabel("Sales")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main():
    np.random.seed(42)
    days = 30
    sales_data = {
        "Product A": np.random.poisson(20, days),
        "Product B": np.random.poisson(35, days),
        "Product C": np.random.poisson(10, days),
    }

    # Forecast each prod
    forecast = {
        product: exponential_smoothing(sales)
        for product, sales in sales_data.items()
    }

    # avr of last 7 days of forecast for alloc
    forecast_avg = {
        product: np.mean(fcast[-7:]) for product, fcast in forecast.items()
    }

    allocation = allocate_resources(forecast_avg)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("results", exist_ok=True)

    result_file = f"results/results_{timestamp}.txt"
    plot_file = f"results/forecast_plot_{timestamp}.png"

    with open(result_file, "w") as f:
        f.write("Forecast:\n")
        for k, v in forecast_avg.items():
            f.write(f"{k}: {v:.2f}\n")
        f.write("\nAllocation:\n")
        for k, v in allocation.items():
            f.write(f"{k}: {v:.2f}\n")

    # plot_save
    plot_forecast(sales_data, forecast, plot_file)

    # filepass
    print(f"RESULT_FILE::{result_file}")
    print(f"PLOT_FILE::{plot_file}")

if __name__ == "__main__":
    main()
