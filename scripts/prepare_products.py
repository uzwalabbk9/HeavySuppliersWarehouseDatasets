import pandas as pd
import os

def prepare_products():
    print("Loading raw products data...")
    df = pd.read_csv('data/raw/products.csv')

    # ============================
    # 1. Standardize text columns
    # ============================
    text_cols = [
        'product_id', 'product_name', 'category', 'machine_type',
        'brand', 'model_compatibility', 'dimensions_cm',
        'material_type', 'criticality_level'
    ]

    for col in text_cols:
        df[col] = df[col].str.title()

    # ============================
    # 2. Parse dimensions (L x W x H)
    # ============================
    dims = df['dimensions_cm'].str.lower().str.split('x', expand=True)
    df['length_cm'] = pd.to_numeric(dims[0], errors='coerce')
    df['width_cm'] = pd.to_numeric(dims[1], errors='coerce')
    df['height_cm'] = pd.to_numeric(dims[2], errors='coerce')

    # ============================
    # 3. Derived metrics
    # ============================

    # A. Margin amount
    df['margin_amount'] = df['unit_price'] - df['unit_cost']

    # B. GST amount
    df['gst_amount'] = df['unit_price'] * (df['gst_rate'] / 100)

    # C. Landed price (price + GST)
    df['landed_price'] = df['unit_price'] + df['gst_amount']

    # D. Volume (cm³)
    df['volume_cm3'] = (
        df['length_cm'] * df['width_cm'] * df['height_cm']
    )

    # E. Stock buffer %
    df['stock_buffer_pct'] = (
        df['safety_stock'] / df['max_stock_level']
    )

    # F. Lead time risk flag
    df['lead_time_risk_flag'] = (
        df['lead_time_days'] > df['reorder_level']
    ).astype(int)

    # ============================
    # 4. Remove duplicates
    # ============================
    df.drop_duplicates(inplace=True)

    # ============================
    # 5. Validation checks
    # ============================
    print("\n=== DUPLICATE PRODUCT IDs ===")
    print(df['product_id'].duplicated().sum())

    print("\n=== CATEGORY VALUES ===")
    print(df['category'].unique())

    print("\n=== CRITICALITY LEVELS ===")
    print(df['criticality_level'].unique())

    # ============================
    # 6. Save processed file
    # ============================
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/products.csv', index=False)

    print("\nProcessed products.csv saved to data/processed/")

if __name__ == "__main__":
    prepare_products()
