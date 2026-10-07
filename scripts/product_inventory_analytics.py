import pandas as pd
import os

def product_inventory_analytics():

    print("Starting Product & Inventory Analytics...")

    os.makedirs('data/analytics', exist_ok=True)

    # ==========================
    # Load Curated Datasets
    # ==========================

    sales = pd.read_csv(
        'data/curated/sales_curated.csv'
    )

    inventory = pd.read_csv(
        'data/curated/inventory_curated.csv'
    )

    ledger = pd.read_csv(
        'data/processed/stock_ledger.csv'
    )

    # ==========================
    # 1. Product Performance
    # ==========================

    product_performance = (
        sales.groupby('product_id')
        .agg(
            total_units_sold=('quantity', 'sum'),
            total_revenue=('line_grand_total', 'sum')
        )
        .reset_index()
        .sort_values(
            'total_revenue',
            ascending=False
        )
    )

    product_performance.to_csv(
        'data/analytics/product_performance.csv',
        index=False
    )

    # ==========================
    # 2. Inventory Turnover
    # ==========================

    inventory_turnover = (
        sales.groupby('product_id')['quantity']
        .sum()
        .reset_index()
    )

    avg_inventory = (
        inventory.groupby('product_id')
        ['current_stock']
        .mean()
        .reset_index()
    )

    inventory_turnover = inventory_turnover.merge(
        avg_inventory,
        on='product_id',
        how='left'
    )

    inventory_turnover['inventory_turnover'] = (
        inventory_turnover['quantity']
        /
        inventory_turnover['current_stock']
    )

    inventory_turnover.to_csv(
        'data/analytics/inventory_turnover.csv',
        index=False
    )

    # ==========================
    # 3. ABC Classification
    # ==========================

    abc = (
        sales.groupby('product_id')
        ['line_grand_total']
        .sum()
        .reset_index()
        .sort_values(
            'line_grand_total',
            ascending=False
        )
    )

    abc['cum_pct'] = (
        abc['line_grand_total']
        .cumsum()
        /
        abc['line_grand_total'].sum()
    )

    abc['class'] = 'C'

    abc.loc[
        abc['cum_pct'] <= 0.80,
        'class'
    ] = 'A'

    abc.loc[
        (abc['cum_pct'] > 0.80)
        &
        (abc['cum_pct'] <= 0.95),
        'class'
    ] = 'B'

    abc.to_csv(
        'data/analytics/abc_classification.csv',
        index=False
    )

    # ==========================
    # 4. Stock Health
    # ==========================

    inventory['stock_health'] = 'Healthy'

    inventory.loc[
        inventory['current_stock']
        < inventory['safety_stock_x'],
        'stock_health'
    ] = 'Critical'

    inventory.loc[
        inventory['current_stock']
        > inventory['max_stock'],
        'stock_health'
    ] = 'Overstock'

    inventory.to_csv(
        'data/analytics/stock_health.csv',
        index=False
    )

    # ==========================
    # 5. Demand Trends
    # ==========================

    sales['order_date'] = pd.to_datetime(
        sales['order_date']
    )

    sales['year_month'] = (
        sales['order_date']
        .dt.to_period('M')
    )

    demand_trends = (
        sales.groupby(
            ['year_month', 'product_id']
        )['quantity']
        .sum()
        .reset_index()
    )

    demand_trends.to_csv(
        'data/analytics/demand_trends.csv',
        index=False
    )

    # ==========================
    # 6. Inventory Aging
    # ==========================

    ledger['movement_date'] = pd.to_datetime(
        ledger['movement_date']
    )

    ledger['days_since_movement'] = (
        pd.Timestamp.today()
        - ledger['movement_date']
    ).dt.days

    ledger['aging_bucket'] = pd.cut(
        ledger['days_since_movement'],
        bins=[0, 30, 90, 180, 99999],
        labels=[
            '0-30',
            '31-90',
            '91-180',
            '180+'
        ]
    )

    ledger.to_csv(
        'data/analytics/inventory_aging.csv',
        index=False
    )

    print("\nAnalytics files created successfully!")

    print("""
Generated:
- product_performance.csv
- inventory_turnover.csv
- abc_classification.csv
- stock_health.csv
- demand_trends.csv
- inventory_aging.csv
""")

if __name__ == "__main__":
    product_inventory_analytics()