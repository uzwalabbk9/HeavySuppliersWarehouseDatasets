import pandas as pd
import os

def prepare_purchase_orders_header():
    print("Loading raw purchase order header data...")
    df = pd.read_csv('data/raw/purchase_orders_header.csv')

    # ============================
    # 1. Standardize text columns
    # ============================
    text_cols = ['po_id', 'supplier_id', 'branch_id', 'po_status']

    for col in text_cols:
        df[col] = df[col].str.upper()

    # ============================
    # 2. Convert date columns
    # ============================
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date'], errors='coerce')
    df['received_date'] = pd.to_datetime(df['received_date'], errors='coerce')

    # ============================
    # 3. Handle missing received_date
    # ============================
    df['received_date'] = df['received_date'].fillna(pd.NaT)

    # ============================
    # 4. Derived metrics
    # ============================

    # A. Lead time (days)
    df['lead_time_days'] = (
        (df['received_date'] - df['order_date']).dt.days
    )

    # B. Delay (days)
    df['delay_days'] = (
        (df['received_date'] - df['expected_delivery_date']).dt.days
    )

    # C. Delay flag
    df['delay_flag'] = (df['delay_days'] > 0).astype(int)

    # D. On-time delivery flag
    df['on_time_flag'] = (df['delay_days'] <= 0).astype(int)

    # E. GST percentage
    df['gst_pct'] = df['total_gst_amount'] / df['total_cost']

    # ============================
    # 5. Remove duplicates
    # ============================
    df.drop_duplicates(inplace=True)

    # ============================
    # 6. Validation checks
    # ============================
    print("\n=== DUPLICATE PO IDs ===")
    print(df['po_id'].duplicated().sum())

    print("\n=== PO STATUS VALUES ===")
    print(df['po_status'].unique())

    print("\n=== DATE CHECK ===")
    print(df[['order_date', 'expected_delivery_date', 'received_date']].head())

    # ============================
    # 7. Save processed file
    # ============================
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/purchase_orders_header.csv', index=False)

    print("\nProcessed purchase_orders_header.csv saved to data/processed/")

if __name__ == "__main__":
    prepare_purchase_orders_header()
