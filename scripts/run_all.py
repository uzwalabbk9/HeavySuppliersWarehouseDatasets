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


def run_all():

    print("=" * 50)
    print("STARTING DATA PREPARATION PIPELINE")
    print("=" * 50)

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

    print("\n" + "=" * 50)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 50)


if __name__ == "__main__":
    run_all()