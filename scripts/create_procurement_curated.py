import pandas as pd
import os

def create_procurement_curated():

    os.makedirs('data/curated', exist_ok=True)

    po_header = pd.read_csv(
        'data/processed/purchase_orders_header.csv'
    )

    po_lines = pd.read_csv(
        'data/processed/purchase_orders_lines.csv'
    )

    suppliers = pd.read_csv(
        'data/processed/suppliers.csv'
    )

    products = pd.read_csv(
        'data/processed/products.csv'
    )

    procurement_curated = (
        po_lines
        .merge(po_header, on='po_id', how='left')
        .merge(suppliers, on='supplier_id', how='left')
        .merge(products, on='product_id', how='left')
    )

    procurement_curated.to_csv(
        'data/curated/procurement_curated.csv',
        index=False
    )

    print("procurement_curated.csv created")
