import pandas as pd
import os

def risk_control_analytics():

    print("Starting Risk, Anomaly & Control Analytics...")

    os.makedirs('data/analytics', exist_ok=True)

    stock_ledger = pd.read_csv(
        'data/processed/stock_ledger.csv'
    )

    inventory = pd.read_csv(
        'data/processed/inventory_master.csv'
    )

    purchase_orders = pd.read_csv(
        'data/processed/purchase_orders_header.csv'
    )

    invoices = pd.read_csv(
        'data/processed/invoices.csv'
    )

    # Inventory anomalies
    threshold = (
        stock_ledger['quantity']
        .quantile(0.95)
    )

    inventory_anomalies = (
        stock_ledger[
            stock_ledger['quantity']
            > threshold
        ]
    )

    inventory_anomalies.to_csv(
        'data/analytics/inventory_anomalies.csv',
        index=False
    )

    # Stock shrinkage
    stock_shrinkage = (
        inventory.copy()
    )

    stock_shrinkage['shrinkage'] = (
        stock_shrinkage['opening_stock']
        -
        stock_shrinkage['current_stock']
    )

    stock_shrinkage.to_csv(
        'data/analytics/stock_shrinkage.csv',
        index=False
    )

    # Operational risk
    operational_risk = (
        inventory[
            inventory['current_stock']
            <
            inventory['safety_stock']
        ]
    )

    operational_risk.to_csv(
        'data/analytics/operational_risk.csv',
        index=False
    )

    # Data quality checks
    quality_summary = []

    datasets = {
        "inventory": inventory,
        "stock_ledger": stock_ledger,
        "purchase_orders": purchase_orders,
        "invoices": invoices
    }

    for name, df in datasets.items():

        quality_summary.append({
            "dataset": name,
            "rows": len(df),
            "missing_values":
                df.isnull().sum().sum(),
            "duplicates":
                df.duplicated().sum()
        })

    data_quality_issues = (
        pd.DataFrame(quality_summary)
    )

    data_quality_issues.to_csv(
        'data/analytics/data_quality_issues.csv',
        index=False
    )

    print("""
Generated:

- inventory_anomalies.csv
- stock_shrinkage.csv
- operational_risk.csv
- data_quality_issues.csv
""")

if __name__ == "__main__":
    risk_control_analytics()