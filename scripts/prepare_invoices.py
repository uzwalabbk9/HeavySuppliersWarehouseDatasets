import pandas as pd
import os

def prepare_invoices():
    print("Loading raw invoices data...")
    df = pd.read_csv('data/raw/invoices.csv')

    # ============================
    # 1. Standardize text columns
    # ============================
    text_cols = [
        'invoice_id', 'so_id', 'customer_id',
        'branch_id', 'payment_status'
    ]

    for col in text_cols:
        df[col] = df[col].str.upper()

    # ============================
    # 2. Convert date columns
    # ============================
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
    df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')

    # ============================
    # 3. Derived metrics
    # ============================

    # A. Days to due date
    df['days_to_due'] = (
        (df['due_date'] - df['invoice_date']).dt.days
    )

    # B. Days overdue
    df['days_overdue'] = (
        (pd.Timestamp.today() - df['due_date']).dt.days
    )

    # C. Overdue flag
    df['overdue_flag'] = (
        (df['payment_status'] != 'PAID') &
        (df['days_overdue'] > 0)
    ).astype(int)

    # D. GST percentage
    df['gst_pct'] = (
        df['total_gst_amount'] / df['total_order_value']
    )

    # ============================
    # 4. Remove duplicates
    # ============================
    df.drop_duplicates(inplace=True)

    # ============================
    # 5. Validation checks
    # ============================
    print("\n=== DUPLICATE INVOICE IDs ===")
    print(df['invoice_id'].duplicated().sum())

    print("\n=== PAYMENT STATUS VALUES ===")
    print(df['payment_status'].unique())

    print("\n=== DATE CHECK ===")
    print(df[['invoice_date', 'due_date']].head())

    # ============================
    # 6. Save processed file
    # ============================
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/invoices.csv', index=False)

    print("\nProcessed invoices.csv saved to data/processed/")

if __name__ == "__main__":
    prepare_invoices()

