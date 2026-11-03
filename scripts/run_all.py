
# DATA PREPARATION

from prepare_branches import prepare_branches
from prepare_customers import prepare_customers
from prepare_inventory import prepare_inventory
from prepare_products import prepare_products
from prepare_suppliers import prepare_suppliers
from prepare_invoices import prepare_invoices
from prepare_payments import prepare_payments
from prepare_purchase_orders_header import prepare_purchase_orders_header
from prepare_purchase_orders_lines import prepare_purchase_orders_lines
from prepare_sales_orders_header import prepare_sales_orders_header
from prepare_sales_orders_lines import prepare_sales_orders_lines
from prepare_stock_ledger import prepare_stock_ledger


# CURATED DATASETS

from create_sales_curated import create_sales_curated
from create_procurement_curated import create_procurement_curated
from create_inventory_curated import create_inventory_curated


# PHASE 2 ANALYTICS


from product_inventory_analytics import product_inventory_analytics
from warehouse_analytics import warehouse_analytics
from supplier_procurement_analytics import supplier_procurement_analytics


# PHASE 3 ANALYTICS


from customer_analytics import customer_analytics
from predictive_analytics import predictive_analytics


def run_all():

    print("=" * 60)
    print("STARTING HEAVY SUPPLIERS ANALYTICS PIPELINE")
    print("=" * 60)


    # DATA PREPARATION

    print("\nSTEP 1 : DATA PREPARATION\n")

    prepare_branches()
    prepare_customers()
    prepare_inventory()
    prepare_products()
    prepare_suppliers()
    prepare_invoices()
    prepare_payments()
    prepare_purchase_orders_header()
    prepare_purchase_orders_lines()
    prepare_sales_orders_header()
    prepare_sales_orders_lines()
    prepare_stock_ledger()

   
    # CURATED DATASETS
  
    print("\nSTEP 2 : DATA INTEGRATION\n")

    create_sales_curated()
    create_procurement_curated()
    create_inventory_curated()

    # PRODUCT & INVENTORY ANALYTICS


    print("\nSTEP 3 : PRODUCT & INVENTORY ANALYTICS\n")

    product_inventory_analytics()


    # WAREHOUSE ANALYTICS
 

    print("\nSTEP 4 : WAREHOUSE ANALYTICS\n")

    warehouse_analytics()

    
    # SUPPLIER ANALYTICS

    print("\nSTEP 5 : SUPPLIER & PROCUREMENT ANALYTICS\n")

    supplier_procurement_analytics()


    # CUSTOMER ANALYTICS


    print("\nSTEP 6 : CUSTOMER ANALYTICS\n")

    customer_analytics()

    # FORECASTING & PREDICTIVE ANALYTICS
  

    print("\nSTEP 7 : FORECASTING & PREDICTIVE ANALYTICS\n")

    predictive_analytics()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("""
Outputs Generated:

Processed Layer:
    data/processed/

Curated Layer:
    data/curated/

Analytics Layer:
    data/analytics/

Project ready for:
    - Risk Analytics
    - Power BI Dashboards
    - KPI Framework
    - Final Report
    - Strategic Recommendations
""")


if __name__ == "__main__":
    run_all()