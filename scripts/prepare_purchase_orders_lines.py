import pandas as pd
import os

def prepare_purchase_orders_lines():

    print("Loading raw purchase order lines data...")

    df = pd.read_csv('data/raw/purchase_orders_lines.csv')

    # ==================================
    # 1. Standardize Text Columns
    # ==================================
    df['po_id'] = df['po_id'].str.upper().str.strip()
    df['product_id'] = df['product_id'].str.upper().str.strip()

    # ==================================
    # 2. Validation Calculations
    # ==================================

    # Calculate expected line total
    df['calculated_line_total'] = (
        df['quantity'] * df['unit_cost']
    )

    # Calculate expected GST
    df['calculated_gst'] = (
        df['calculated_line_total']
        * (df['gst_rate'] / 100)
    )

    # Calculate expected grand total
    df['calculated_grand_total'] = (
        df['calculated_line_total']
        + df['calculated_gst']
    )

    # ==================================
    # 3. Variance Checks
    # ==================================

    df['line_total_variance'] = (
        df['line_total']
        - df['calculated_line_total']
    )

    df['gst_variance'] = (
        df['gst_amount']
        - df['calculated_gst']
    )

    df['grand_total_variance'] = (
        df['line_grand_total']
        - df['calculated_grand_total']
    )

    # ==================================
    # 4. Procurement Features
    # ==================================

    # Actual GST %
    df['actual_gst_pct'] = (
        df['gst_amount']
        / df['line_total']
    ) * 100

    # High-value line item
    median_value = df['line_grand_total'].median()

    df['high_value_line'] = (
        df['line_grand_total'] > median_value
    ).astype(int)

    # Bulk order indicator
    median_qty = df['quantity'].median()

    df['bulk_order_flag'] = (
        df['quantity'] > median_qty
    ).astype(int)

    # ==================================
    # 5. Remove Duplicates
    # ==================================

    df.drop_duplicates(inplace=True)

    # ==================================
    # 6. Validation Checks
    # ==================================

    print("\n=== DUPLICATE PO LINES ===")
    print(df.duplicated(
        subset=['po_id', 'line_number']
    ).sum())

    print("\n=== UNIQUE PRODUCTS ===")
    print(df['product_id'].nunique())

    print("\n=== PURCHASE SPEND ===")
    print(df['line_grand_total'].sum())

    print("\n=== AVERAGE LINE VALUE ===")
    print(df['line_grand_total'].mean())

    # ==================================
    # 7. Save Processed Data
    # ==================================

    os.makedirs('data/processed', exist_ok=True)

    df.to_csv(
        'data/processed/purchase_orders_lines.csv',
        index=False
    )

    print("\nProcessed purchase_orders_lines.csv saved successfully!")

if __name__ == "__main__":
    prepare_purchase_orders_lines()