import pandas as pd
import os

def customer_analytics():

    print("Starting Customer Analytics...")

    os.makedirs('data/analytics', exist_ok=True)

    # =====================================
    # Load Data
    # =====================================

    sales = pd.read_csv(
        'data/curated/sales_curated.csv'
    )

    customers = pd.read_csv(
        'data/processed/customers.csv'
    )

    sales['order_date'] = pd.to_datetime(
        sales['order_date']
    )

    # =====================================
    # 1. Customer Purchase Behaviour
    # =====================================

    customer_behaviour = (
        sales.groupby('customer_id')
        .agg(
            total_orders=('so_id', 'nunique'),
            total_quantity=('quantity', 'sum'),
            total_revenue=('line_grand_total', 'sum')
        )
        .reset_index()
    )

    customer_behaviour.to_csv(
        'data/analytics/customer_purchase_behaviour.csv',
        index=False
    )

    # =====================================
    # 2. RFM Analysis
    # =====================================

    snapshot_date = (
        sales['order_date'].max()
        + pd.Timedelta(days=1)
    )

    rfm = (
        sales.groupby('customer_id')
        .agg({
            'order_date':
            lambda x:
            (snapshot_date - x.max()).days,

            'so_id':'nunique',

            'line_grand_total':'sum'
        })
    )

    rfm.columns = [
        'Recency',
        'Frequency',
        'Monetary'
    ]

    rfm = rfm.reset_index()

    rfm.to_csv(
        'data/analytics/customer_rfm.csv',
        index=False
    )

    # =====================================
    # 3. Customer Segmentation
    # =====================================

    rfm['segment'] = 'Bronze'

    rfm.loc[
        rfm['Monetary']
        > rfm['Monetary'].quantile(.50),
        'segment'
    ] = 'Silver'

    rfm.loc[
        rfm['Monetary']
        > rfm['Monetary'].quantile(.80),
        'segment'
    ] = 'Gold'

    rfm.to_csv(
        'data/analytics/customer_segments.csv',
        index=False
    )

    # =====================================
    # 4. Customer Lifetime Value
    # =====================================

    customers['clv'] = (
        customers['total_purchase_value']
        /
        customers['customer_tenure_years']
    )

    customers[
        ['customer_id', 'clv']
    ].to_csv(
        'data/analytics/customer_clv.csv',
        index=False
    )

    # =====================================
    # 5. Customer Retention
    # =====================================

    customers['retained'] = (
        customers['days_since_last_purchase']
        <= 90
    ).astype(int)

    customers[
        ['customer_id', 'retained']
    ].to_csv(
        'data/analytics/customer_retention.csv',
        index=False
    )

    # =====================================
    # 6. Customer Churn
    # =====================================

    customers['churn_risk'] = (
        customers['days_since_last_purchase']
        > 180
    ).astype(int)

    customers[
        ['customer_id', 'churn_risk']
    ].to_csv(
        'data/analytics/customer_churn.csv',
        index=False
    )

    # =====================================
    # 7. High Value Customers
    # =====================================

    high_value = (
        customers.sort_values(
            'total_purchase_value',
            ascending=False
        )
        .head(20)
    )

    high_value.to_csv(
        'data/analytics/high_value_customers.csv',
        index=False
    )

    # =====================================
    # 8. Customer Credit Risk
    # =====================================

    customers['credit_risk'] = 'Low'

    customers.loc[
        customers[
            'credit_utilization_pct'
        ] > 0.80,
        'credit_risk'
    ] = 'High'

    customers[
        ['customer_id', 'credit_risk']
    ].to_csv(
        'data/analytics/customer_credit_risk.csv',
        index=False
    )

    print("\nCustomer Analytics Completed!")

if __name__ == "__main__":
    customer_analytics()