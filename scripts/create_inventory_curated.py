import pandas as pd
import os

def create_inventory_curated():

    os.makedirs('data/curated', exist_ok=True)

    inventory = pd.read_csv(
        'data/processed/inventory_master.csv'
    )

    products = pd.read_csv(
        'data/processed/products.csv'
    )

    branches = pd.read_csv(
        'data/processed/branches.csv'
    )

    inventory_curated = (
        inventory
        .merge(
            products,
            on='product_id',
            how='left',
            suffixes=('', '_product')
        )
        .merge(
            branches,
            on='branch_id',
            how='left'
        )
    )

    inventory_curated.to_csv(
        'data/curated/inventory_curated.csv',
        index=False
    )

    print("inventory_curated.csv created")