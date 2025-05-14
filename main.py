import os
import json
import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

# exp smoothing -forcasting
def exponential_smoothing(data, alpha=0.3):
    forecast = [data[0]]
    for t in range(1, len(data)):
        forecast.append(alpha * data[t-1] + (1 - alpha) * forecast[t-1])
    return forecast

# LP allocation logic
def allocate_resources(forecasted_demand):
    allocation = {k: max(0, v - 5) for k, v in forecasted_demand.items()}
    return allocation

# Results PLOT
def plot_charts(sales_data, forecast, base_filename):
    plt.style.use("seaborn-v0_8")
    
    # Line Plot
    plt.figure(figsize=(10, 6))
    for product in sales_data:
        plt.plot(sales_data[product], label=f"{product} Actual", linewidth=2)
        plt.plot(forecast[product], linestyle="--", label=f"{product} Forecast")
    plt.title("Line Chart - Forecast vs Actual")
    plt.xlabel("Day")
    plt.ylabel("Sales")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{base_filename}_line.png")
    plt.close()

    # Pie Chart (based on total sales per product)
    plt.figure(figsize=(8, 6))
    totals = {product: sum(values) for product, values in sales_data.items()}
    plt.pie(totals.values(), labels=totals.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Pie Chart - Total Sales Distribution")
    plt.tight_layout()
    plt.savefig(f"{base_filename}_pie.png")
    plt.close()

    # Histogram (distribution of last 7 days)
    plt.figure(figsize=(10, 6))
    for product, values in sales_data.items():
        plt.hist(values[-7:], bins=7, alpha=0.6, label=product)
    plt.title("Histogram - Last 7 Days Sales Distribution")
    plt.xlabel("Units Sold")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{base_filename}_hist.png")
    plt.close()


def load_data(file_path=None):
    if file_path and os.path.exists(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_path)
        elif ext == ".json":
            with open(file_path, "r") as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        else:
            raise ValueError("Unsupported file format. Use .csv or .json")

        df = df.dropna()
        return {col: df[col].values.tolist() for col in df.columns if col.lower() != "day"}
    else:
        # RNDMIZ
        np.random.seed(int(datetime.now().timestamp()) % 100000)
        days = 30
        return {
            "Product A": np.random.poisson(20, days).tolist(),
            "Product B": np.random.poisson(35, days).tolist(),
            "Product C": np.random.poisson(10, days).tolist(),
        }

def main(file_path=None):
    sales_data = load_data(file_path)

    forecast = {
        product: exponential_smoothing(sales)
        for product, sales in sales_data.items()
    }

    forecast_avg = {
        product: np.mean(fcast[-7:]) for product, fcast in forecast.items()
    }

    allocation = allocate_resources(forecast_avg)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("results", exist_ok=True)

    result_file = f"results/results_{timestamp}.txt"
    plot_file = f"results/forecast_plot_{timestamp}.png"

    with open(result_file, "w") as f:
        f.write("Forecast (7-day avg):\n")
        for k, v in forecast_avg.items():
            f.write(f"{k}: {v:.2f}\n")
        f.write("\nResource Allocation:\n")
        for k, v in allocation.items():
            f.write(f"{k}: {v:.2f}\n")

    plot_charts(sales_data, forecast, f"results/forecast_plot_{timestamp}")

    print(f"RESULT_FILE::{result_file}")
    print(f"PLOT_FILE_LINE::results/forecast_plot_{timestamp}_line.png")
    print(f"PLOT_FILE_PIE::results/forecast_plot_{timestamp}_pie.png")
    print(f"PLOT_FILE_HIST::results/forecast_plot_{timestamp}_hist.png")

    
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    main(input_file)
