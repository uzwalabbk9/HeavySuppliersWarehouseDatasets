import pandas as pd
import os

def prepare_inventory():
    print("Loading raw inventory data...")
    df = pd.read_csv('data/raw/inventory_master.csv')

    # Numeric columns
    numeric_cols = [
        'opening_stock', 'reorder_level', 'safety_stock',
        'max_stock', 'current_stock'
    ]

    # Ensure numeric types (safe even if already correct)
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Standardize text fields
    df['product_id'] = df['product_id'].str.upper()
    df['branch_id'] = df['branch_id'].str.upper()
    df['warehouse_bin'] = df['warehouse_bin'].str.upper()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Derived metrics
    df['stock_availability_pct'] = df['current_stock'] / df['max_stock']
    df['reorder_flag'] = (df['current_stock'] <= df['reorder_level']).astype(int)
    df['safety_breach'] = (df['current_stock'] < df['safety_stock']).astype(int)

    # Ensure processed folder exists
    os.makedirs('data/processed', exist_ok=True)

    # Save processed file
    df.to_csv('data/processed/inventory_master.csv', index=False)
    print("Processed inventory_master.csv saved to data/processed/")

if __name__ == "__main__":
    prepare_inventory()
