import pandas as pd
import os

def predictive_analytics():

    print("Starting Forecasting & Predictive Analytics...")

    os.makedirs('data/analytics', exist_ok=True)

    # =====================================
    # Load Data
    # =====================================

    sales = pd.read_csv(
        'data/curated/sales_curated.csv'
    )

    inventory = pd.read_csv(
        'data/processed/inventory_master.csv'
    )

    sales['order_date'] = pd.to_datetime(
        sales['order_date']
    )

    # =====================================
    # 1. Product Demand Forecasting
    # =====================================

    sales['month'] = (
        sales['order_date']
        .dt.to_period('M')
    )

    product_demand_forecast = (
        sales.groupby(
            ['month', 'product_id']
        )['quantity']
        .sum()
        .reset_index()
    )

    product_demand_forecast.to_csv(
        'data/analytics/product_demand_forecast.csv',
        index=False
    )

    # =====================================
    # 2. Inventory Level Forecasting
    # =====================================

    future_demand = (
        sales.groupby('product_id')
        ['quantity']
        .mean()
        .reset_index()
    )

    inventory_forecast = (
        inventory.merge(
            future_demand,
            on='product_id',
            how='left'
        )
    )

    inventory_forecast[
        'forecast_stock'
    ] = (
        inventory_forecast['current_stock']
        -
        inventory_forecast['quantity']
    )

    inventory_forecast.to_csv(
        'data/analytics/inventory_forecast.csv',
        index=False
    )

    # =====================================
    # 3. Stockout Risk Prediction
    # =====================================

    inventory['stockout_prediction'] = (
        inventory['current_stock']
        <
        inventory['safety_stock']
    ).astype(int)

    inventory.to_csv(
        'data/analytics/stockout_prediction.csv',
        index=False
    )

    # =====================================
    # 4. Reorder Point Optimisation
    # =====================================

    inventory[
        'recommended_reorder_point'
    ] = (
        inventory['safety_stock']
        +
        (
            inventory['reorder_level']
            * 0.20
        )
    )

    inventory.to_csv(
        'data/analytics/reorder_optimization.csv',
        index=False
    )

    # =====================================
    # 5. Safety Stock Optimisation
    # =====================================

    inventory[
        'recommended_safety_stock'
    ] = (
        inventory['current_stock']
        * 0.25
    ).round()

    inventory.to_csv(
        'data/analytics/safety_stock_optimization.csv',
        index=False
    )

    # =====================================
    # 6. Scenario-Based Forecasting
    # =====================================

    scenario_forecast = (
        inventory.copy()
    )

    scenario_forecast[
        'best_case_stock'
    ] = (
        scenario_forecast['current_stock']
        * 1.20
    )

    scenario_forecast[
        'worst_case_stock'
    ] = (
        scenario_forecast['current_stock']
        * 0.80
    )

    scenario_forecast.to_csv(
        'data/analytics/scenario_forecast.csv',
        index=False
    )

    # =====================================
    # Complete
    # =====================================

    print("\nForecasting & Predictive Analytics Completed!")

    print("""
Generated:

1. product_demand_forecast.csv
2. inventory_forecast.csv
3. stockout_prediction.csv
4. reorder_optimization.csv
5. safety_stock_optimization.csv
6. scenario_forecast.csv
""")

if __name__ == "__main__":
    predictive_analytics()