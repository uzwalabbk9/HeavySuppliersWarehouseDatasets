import pandas as pd
import os

def prepare_sales_orders_header():

    print("Loading raw sales orders header data...")

    df = pd.read_csv('data/raw/sales_orders_header.csv')

    # ==================================
    # 1. Standardize Text Columns
    # ==================================

    text_cols = [
        'so_id',
        'customer_id',
        'branch_id',
        'order_status',
        'payment_terms',
        'sales_channel'
    ]

    for col in text_cols:
        df[col] = df[col].str.upper().str.strip()

    # ==================================
    # 2. Convert Date Columns
    # ==================================

    df['order_date'] = pd.to_datetime(
        df['order_date'],
        errors='coerce'
    )

    df['delivery_date'] = pd.to_datetime(
        df['delivery_date'],
        errors='coerce'
    )

    # ==================================
    # 3. Remove Duplicates
    # ==================================

    df.drop_duplicates(inplace=True)

    # ==================================
    # 4. Validation Checks
    # ==================================

    print("\n=== DUPLICATE SALES ORDERS ===")
    print(df['so_id'].duplicated().sum())

    print("\n=== ORDER STATUS VALUES ===")
    print(df['order_status'].unique())

    print("\n=== SALES CHANNEL VALUES ===")
    print(df['sales_channel'].unique())

    # ==================================
    # 5. Save Processed Data
    # ==================================

    os.makedirs('data/processed', exist_ok=True)

    df.to_csv(
        'data/processed/sales_orders_header.csv',
        index=False
    )

    print("\nProcessed sales_orders_header.csv saved successfully!")

if __name__ == "__main__":
    prepare_sales_orders_header()