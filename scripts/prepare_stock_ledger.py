import pandas as pd
import os

def prepare_stock_ledger():

    print("Loading raw stock ledger data...")

    df = pd.read_csv('data/raw/stock_ledger.csv')

    # ==================================
    # 1. Standardize Text Columns
    # ==================================

    text_cols = [
        'movement_id',
        'product_id',
        'branch_id',
        'movement_type',
        'reference_type',
        'reference_id'
    ]

    for col in text_cols:
        df[col] = df[col].str.upper().str.strip()

    # ==================================
    # 2. Convert Date Column
    # ==================================

    df['movement_date'] = pd.to_datetime(
        df['movement_date'],
        errors='coerce'
    )

    # ==================================
    # 3. Remove Duplicates
    # ==================================

    df.drop_duplicates(inplace=True)

    # ==================================
    # 4. Validation Checks
    # ==================================

    print("\n=== DUPLICATE MOVEMENT IDs ===")
    print(df['movement_id'].duplicated().sum())

    print("\n=== MOVEMENT TYPES ===")
    print(df['movement_type'].unique())

    print("\n=== REFERENCE TYPES ===")
    print(df['reference_type'].unique())

    print("\n=== NUMERIC SUMMARY ===")
    print(
        df[
            [
                'quantity',
                'running_balance'
            ]
        ].describe()
    )

    # ==================================
    # 5. Save Processed Data
    # ==================================

    os.makedirs('data/processed', exist_ok=True)

    df.to_csv(
        'data/processed/stock_ledger.csv',
        index=False
    )

    print("\nProcessed stock_ledger.csv saved successfully!")

if __name__ == "__main__":
    prepare_stock_ledger()