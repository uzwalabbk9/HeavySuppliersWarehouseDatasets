import pandas as pd
import os

def warehouse_analytics():

    print("Starting Warehouse Operations & Efficiency Analytics...")

    os.makedirs('data/analytics', exist_ok=True)

    # ======================================
    # Load Data
    # ======================================

    branches = pd.read_csv(
        'data/processed/branches.csv'
    )

    inventory = pd.read_csv(
        'data/processed/inventory_master.csv'
    )

    stock_ledger = pd.read_csv(
        'data/processed/stock_ledger.csv'
    )

    po_header = pd.read_csv(
        'data/processed/purchase_orders_header.csv'
    )

    # ======================================
    # 1. Warehouse Space Utilisation
    # ======================================

    branch_stock = (
        inventory.groupby('branch_id')
        ['current_stock']
        .sum()
        .reset_index()
    )

    warehouse_utilisation = (
        branch_stock.merge(
            branches[
                [
                    'branch_id',
                    'warehouse_capacity'
                ]
            ],
            on='branch_id',
            how='left'
        )
    )

    warehouse_utilisation[
        'utilisation_pct'
    ] = (
        warehouse_utilisation['current_stock']
        /
        warehouse_utilisation['warehouse_capacity']
    ) * 100

    warehouse_utilisation.to_csv(
        'data/analytics/warehouse_space_utilisation.csv',
        index=False
    )

    # ======================================
    # 2. Warehouse Throughput
    # ======================================

    warehouse_throughput = (
        stock_ledger.groupby('branch_id')
        .size()
        .reset_index(
            name='total_movements'
        )
    )

    warehouse_throughput.to_csv(
        'data/analytics/warehouse_throughput.csv',
        index=False
    )

    # ======================================
    # 3. Warehouse Capacity Analysis
    # ======================================

    warehouse_capacity = (
        warehouse_utilisation.copy()
    )

    warehouse_capacity[
        'available_capacity'
    ] = (
        warehouse_capacity['warehouse_capacity']
        -
        warehouse_capacity['current_stock']
    )

    warehouse_capacity.to_csv(
        'data/analytics/warehouse_capacity_analysis.csv',
        index=False
    )

    # ======================================
    # 4. Warehouse Performance Score
    # ======================================

    warehouse_score = (
        warehouse_utilisation.copy()
    )

    warehouse_score[
        'performance_score'
    ] = warehouse_score[
        'utilisation_pct'
    ].round(2)

    warehouse_score.to_csv(
        'data/analytics/warehouse_performance_score.csv',
        index=False
    )

    # ======================================
    # 5. Operational Bottlenecks
    # ======================================

    bottlenecks = (
        po_header[
            po_header['delay_flag'] == 1
        ]
    )

    bottlenecks.to_csv(
        'data/analytics/operational_bottlenecks.csv',
        index=False
    )

    # ======================================
    # 6. Warehouse Benchmarking
    # ======================================

    warehouse_benchmark = (
        warehouse_utilisation
        .sort_values(
            'utilisation_pct',
            ascending=False
        )
    )

    warehouse_benchmark[
        'rank'
    ] = range(
        1,
        len(warehouse_benchmark) + 1
    )

    warehouse_benchmark.to_csv(
        'data/analytics/warehouse_benchmarking.csv',
        index=False
    )

    print("\nWarehouse Analytics Completed!")

    print("""
Generated:

1. warehouse_space_utilisation.csv
2. warehouse_throughput.csv
3. warehouse_capacity_analysis.csv
4. warehouse_performance_score.csv
5. operational_bottlenecks.csv
6. warehouse_benchmarking.csv
""")

if __name__ == "__main__":
    warehouse_analytics()