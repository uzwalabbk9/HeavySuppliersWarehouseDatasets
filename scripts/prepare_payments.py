import pandas as pd
import os

def prepare_payments():
    print("Loading raw payments data...")
    df = pd.read_csv('data/raw/payments.csv')

    # ============================
    # 1. Standardize text columns
    # ============================
    text_cols = ['payment_id', 'invoice_id', 'payment_method']

    for col in text_cols:
        df[col] = df[col].str.upper()

    # ============================
    # 2. Convert date column
    # ============================
    df['payment_date'] = pd.to_datetime(df['payment_date'], errors='coerce')

    # ============================
    # 3. Derived metrics
    # ============================

    # A. Payment year, month, quarter
    df['payment_year'] = df['payment_date'].dt.year
    df['payment_month'] = df['payment_date'].dt.month
    df['payment_quarter'] = df['payment_date'].dt.quarter

    # B. Weekday name
    df['payment_weekday'] = df['payment_date'].dt.day_name()

    # C. High-value payment flag
    df['high_value_flag'] = (
        df['payment_amount'] > df['payment_amount'].median()
    ).astype(int)

    # D. Payment method category
    df['payment_method_category'] = df['payment_method'].replace({
        'CREDIT CARD': 'CARD',
        'DEBIT CARD': 'CARD',
        'BANK TRANSFER': 'BANK',
        'CASH': 'CASH'
    })

    # ============================
    # 4. Remove duplicates
    # ============================
    df.drop_duplicates(inplace=True)

    # ============================
    # 5. Validation checks
    # ============================
    print("\n=== DUPLICATE PAYMENT IDs ===")
    print(df['payment_id'].duplicated().sum())

    print("\n=== PAYMENT METHODS ===")
    print(df['payment_method'].unique())

    print("\n=== DATE CHECK ===")
    print(df['payment_date'].head())

    print("\n=== NUMERIC SUMMARY ===")
    print(df['payment_amount'].describe())

    # ============================
    # 6. Save processed file
    # ============================
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/payments.csv', index=False)

    print("\nProcessed payments.csv saved to data/processed/")

if __name__ == "__main__":
    prepare_payments()
