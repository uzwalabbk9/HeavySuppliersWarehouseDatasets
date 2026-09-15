import pandas as pd
import os

def prepare_customers():
    print("Loading raw customers data...")
    df = pd.read_csv('data/raw/customers.csv')

    # ============================
    # 1. Standardize text columns
    # ============================
    text_cols = [
        'customer_id', 'customer_type', 'industry_segment',
        'city', 'state', 'region', 'branch_id', 'payment_terms'
    ]

    for col in text_cols:
        df[col] = df[col].str.title()

    # ============================
    # 2. Convert date columns
    # ============================
    df['customer_since'] = pd.to_datetime(df['customer_since'], errors='coerce')
    df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'], errors='coerce')

    # ============================
    # 3. Derived metrics
    # ============================

    # A. Customer tenure (in years)
    df['customer_tenure_years'] = (
        (pd.Timestamp.today() - df['customer_since']).dt.days / 365
    )

    # B. Days since last purchase
    df['days_since_last_purchase'] = (
        (pd.Timestamp.today() - df['last_purchase_date']).dt.days
    )

    # C. Credit utilization %
    df['credit_utilization_pct'] = (
        df['current_balance'] / df['credit_limit']
    )

    # D. Average purchase value
    df['avg_purchase_value'] = (
        df['total_purchase_value'] / df['customer_tenure_years'].replace(0, 1)
    )

    # ============================
    # 4. Remove duplicates
    # ============================
    df.drop_duplicates(inplace=True)

    # ============================
    # 5. Validation checks
    # ============================
    print("\n=== DUPLICATE CUSTOMER IDs ===")
    print(df['customer_id'].duplicated().sum())

    print("\n=== REGION VALUES ===")
    print(df['region'].unique())

    print("\n=== DATE CONVERSION CHECK ===")
    print(df[['customer_since', 'last_purchase_date']].head())

    # ============================
    # 6. Save processed file
    # ============================
    os.makedirs('../data/processed', exist_ok=True)
    df.to_csv('data/processed/customers.csv', index=False)

    print("\nProcessed customers.csv saved to data/processed/")

if __name__ == "__main__":
    prepare_customers()
