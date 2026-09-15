import pandas as pd
import os

def prepare_branches():
    print("Loading raw branches data...")
    df = pd.read_csv('data/raw/branches.csv')

    # Fix warehouse_capacity ("45230 sqft") → integer
    df['warehouse_capacity'] = (
        df['warehouse_capacity']
        .astype(str)
        .str.replace(' sqft', '', regex=False)
        .astype(int)
    )

    # Convert Yes/No → boolean
    df['service_center_available'] = df['service_center_available'].map({'Yes': 1, 'No': 0})

    # Numeric columns that actually exist
    numeric_cols = [
    'manager_id',
    'total_employees',
    'avg_monthly_revenue',
    'monthly_operational_cost'
    ]


    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Handle missing values
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    df['warehouse_type'] = df['warehouse_type'].fillna(df['warehouse_type'].mode()[0])
    df['region'] = df['region'].fillna(df['region'].mode()[0])

    # Standardize categories
    df['region'] = df['region'].str.title()
    df['warehouse_type'] = df['warehouse_type'].str.title()
    df['city'] = df['city'].str.title()
    df['state'] = df['state'].str.title()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Derived metrics using EXISTING columns
    df['revenue_per_sqft'] = df['avg_monthly_revenue'] / df['warehouse_capacity']
    df['cost_revenue_ratio'] = df['monthly_operational_cost'] / df['avg_monthly_revenue']

    # Ensure processed folder exists
    os.makedirs('data/processed', exist_ok=True)

    # Save processed file
    df.to_csv('data/processed/branches.csv', index=False)
    print("Processed branches.csv saved to data/processed/")

if __name__ == "__main__":
    prepare_branches()
