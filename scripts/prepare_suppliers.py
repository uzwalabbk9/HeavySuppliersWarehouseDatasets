import pandas as pd
import os

def prepare_suppliers():

    print("Loading raw suppliers data...")

    df = pd.read_csv('data/raw/suppliers.csv')

    # Standardize text columns
    text_cols = [
        'supplier_id',
        'supplier_name',
        'supplier_type',
        'product_category',
        'city',
        'province',
        'region',
        'china_tax_id'
    ]

    for col in text_cols:
        df[col] = df[col].str.upper().str.strip()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Validation checks
    print("\n=== DUPLICATE SUPPLIER IDs ===")
    print(df['supplier_id'].duplicated().sum())

    print("\n=== SUPPLIER TYPES ===")
    print(df['supplier_type'].unique())

    print("\n=== REGIONS ===")
    print(df['region'].unique())

    # Save processed data
    os.makedirs('data/processed', exist_ok=True)

    df.to_csv(
        'data/processed/suppliers.csv',
        index=False
    )

    print("\nProcessed suppliers.csv saved successfully!")

if __name__ == "__main__":
    prepare_suppliers()