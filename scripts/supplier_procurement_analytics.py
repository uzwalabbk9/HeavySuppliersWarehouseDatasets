import pandas as pd
import os

def supplier_procurement_analytics():

    print("Starting Supplier & Procurement Analytics...")

    os.makedirs('data/analytics', exist_ok=True)

    # =====================================
    # Load Data
    # =====================================

    suppliers = pd.read_csv(
        'data/processed/suppliers.csv'
    )

    procurement = pd.read_csv(
        'data/curated/procurement_curated.csv'
    )

    # =====================================
    # 1. Supplier Contribution Analysis
    # =====================================

    supplier_contribution = (
        procurement.groupby('supplier_id')
        ['line_grand_total']
        .sum()
        .reset_index()
        .rename(
            columns={
                'line_grand_total':
                'total_procurement_spend'
            }
        )
        .sort_values(
            'total_procurement_spend',
            ascending=False
        )
    )

    supplier_contribution.to_csv(
        'data/analytics/supplier_contribution.csv',
        index=False
    )

    # =====================================
    # 2. Supplier Reliability Analysis
    # =====================================

    supplier_reliability = (
        suppliers[
            [
                'supplier_id',
                'supplier_name',
                'lead_time_days',
                'reliability_score'
            ]
        ]
        .sort_values(
            'reliability_score',
            ascending=False
        )
    )

    supplier_reliability.to_csv(
        'data/analytics/supplier_reliability.csv',
        index=False
    )

    # =====================================
    # 3. Supplier Performance Comparison
    # =====================================

    supplier_performance = (
        suppliers.copy()
    )

    supplier_performance[
        'performance_score'
    ] = (
        supplier_performance['reliability_score']
        /
        supplier_performance['lead_time_days']
    )

    supplier_performance = (
        supplier_performance.sort_values(
            'performance_score',
            ascending=False
        )
    )

    supplier_performance.to_csv(
        'data/analytics/supplier_performance.csv',
        index=False
    )

    # =====================================
    # 4. Supplier Dependency Risk Analysis
    # =====================================

    dependency = (
        supplier_contribution.copy()
    )

    dependency[
        'spend_pct'
    ] = (
        dependency['total_procurement_spend']
        /
        dependency[
            'total_procurement_spend'
        ].sum()
    ) * 100

    dependency.to_csv(
        'data/analytics/supplier_dependency_risk.csv',
        index=False
    )

    # =====================================
    # 5. Critical Supplier Identification
    # =====================================

    critical_suppliers = (
        dependency.merge(
            suppliers,
            on='supplier_id',
            how='left'
        )
    )

    critical_suppliers = (
        critical_suppliers[
            (
                critical_suppliers[
                    'spend_pct'
                ] > 10
            )
            &
            (
                critical_suppliers[
                    'reliability_score'
                ] < 8
            )
        ]
    )

    critical_suppliers.to_csv(
        'data/analytics/critical_suppliers.csv',
        index=False
    )

    # =====================================
    # 6. Supplier Diversification Analysis
    # =====================================

    supplier_diversification = (
        suppliers.groupby(
            'product_category'
        )
        .size()
        .reset_index(
            name='supplier_count'
        )
    )

    supplier_diversification.to_csv(
        'data/analytics/supplier_diversification.csv',
        index=False
    )

    # =====================================
    # Complete
    # =====================================

    print("\nSupplier & Procurement Analytics Completed!")

    print("""
Generated:

1. supplier_contribution.csv
2. supplier_reliability.csv
3. supplier_performance.csv
4. supplier_dependency_risk.csv
5. critical_suppliers.csv
6. supplier_diversification.csv
""")

if __name__ == "__main__":
    supplier_procurement_analytics()