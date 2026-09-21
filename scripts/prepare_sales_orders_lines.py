import pandas as pd
import os

def prepare_sales_orders_lines():

    print("Loading raw sales order lines data...")

    df = pd.read_csv('data/raw/sales_orders_lines.csv')

    # ==================================
    # 1. Standardize Text Columns
    # ==================================

    text_cols = [
        'so_id',
        'product_id'
    ]

    for col in text_cols:
        df[col] = df[col].str.upper().str.strip()

    # ==================================
    # 2. Remove Duplicates
    # ==================================

    df.drop_duplicates(inplace=True)

    # ==================================
    # 3. Validation Checks
    # ==================================

    print("\n=== DUPLICATE SALES ORDER LINES ===")
    print(
        df.duplicated(
            subset=['so_id', 'line_number']
        ).sum()
    )

    print("\n=== UNIQUE PRODUCTS ===")
    print(df['product_id'].nunique())

    print("\n=== NUMERIC SUMMARY ===")
    print(
        df[
            [
                'quantity',
                'unit_price',
                'gst_rate',
                'line_total',
                'gst_amount',
                'line_grand_total'
            ]
        ].describe()
    )

    # ==================================
    # 4. Save Processed Data
    # ==================================

    os.makedirs('data/processed', exist_ok=True)

    df.to_csv(
        'data/processed/sales_orders_lines.csv',
        index=False
    )

    print("\nProcessed sales_orders_lines.csv saved successfully!")

if __name__ == "__main__":
    prepare_sales_orders_lines()