import pandas as pd
import numpy as np

def get_sales_data():
    #synthetic sales data gen for 30 days. 3 products
    np.random.seed(42)
    days = pd.date_range(start='2024-01-01', periods=30)
    data = {
        'date': days,
        'product_A': np.random.poisson(20, size=30),
        'product_B': np.random.poisson(35, size=30),
        'product_C': np.random.poisson(15, size=30)
    }
    df = pd.DataFrame(data)
    return df
