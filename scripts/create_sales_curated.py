import pandas as pd
import os

def create_sales_curated():

    os.makedirs('data/curated', exist_ok=True)

    so_header = pd.read_csv(
        'data/processed/sales_orders_header.csv'
    )

    so_lines = pd.read_csv(
        'data/processed/sales_orders_lines.csv'
    )

    customers = pd.read_csv(
        'data/processed/customers.csv'
    )

    products = pd.read_csv(
        'data/processed/products.csv'
    )

    sales_curated = (
        so_lines
        .merge(so_header, on='so_id', how='left')
        .merge(customers, on='customer_id', how='left')
        .merge(products, on='product_id', how='left')
    )

    sales_curated.to_csv(
        'data/curated/sales_curated.csv',
        index=False
    )

    print("sales_curated.csv created")