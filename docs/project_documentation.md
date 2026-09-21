# Heavy Suppliers Warehouse Data Foundation & Preparation

## 1. Data Profiling & Structure Analysis

The raw datasets were analysed using:

- head()
- info()
- describe()
- isnull().sum()

The analysis helped identify:
- Data types
- Missing values
- Dataset dimensions
- Column structures
- Data quality issues

---

## 2. Data Cleaning & Quality Improvement

The following cleaning activities were performed:

- Standardized text columns to uppercase
- Converted date columns to datetime format
- Removed duplicate records
- Handled missing values
- Validated column data types

Processed datasets were saved in:

data/processed/

---

## 3. Data Integration & Dataset Merging

Integrated datasets were created:

### sales_curated.csv

Merged:

- sales_orders_header
- sales_orders_lines
- customers
- products

### procurement_curated.csv

Merged:

- purchase_orders_header
- purchase_orders_lines
- suppliers
- products

### inventory_curated.csv

Merged:

- inventory_master
- products
- branches

Curated datasets were saved in:

data/curated/

---

## 4. Feature Engineering for Analytics

Created analytical features including:

### Customers

- customer_tenure_years
- days_since_last_purchase
- credit_utilization_pct

### Inventory

- stock_availability_pct
- reorder_flag
- safety_breach

### Products

- margin_amount
- gst_amount
- landed_price
- volume_cm3
- stock_buffer_pct
- lead_time_risk_flag

### Invoices

- days_to_due
- days_overdue
- overdue_flag
- gst_pct

### Payments

- payment_year
- payment_month
- payment_quarter
- payment_weekday
- high_value_flag

### Purchase Orders

- lead_time_days
- delay_days
- delay_flag
- on_time_flag

---

## 5. Data Validation & Consistency Checks

Validation activities included:

- Duplicate record checks
- Missing value checks
- Data type validation
- Numeric summaries
- Business rule verification
- GST and total calculations validation

---

## 6. Data Dictionary & Documentation

A comprehensive data dictionary was created to document:

- Column names
- Data types
- Business definitions
- Derived features

Documentation Location:

docs/data_dictionary.md

---

## Data Architecture

Raw Layer:
data/raw/

Processed Layer:
data/processed/

Curated Layer:
data/curated/

Documentation Layer:
docs/

---

## Deliverables

Completed Outputs:

- Processed datasets
- Curated datasets
- Data preparation notebooks
- Automation scripts
- Data dictionary
- Project documentation

The prepared data foundation provides a clean, validated, and analytics-ready environment for reporting, dashboarding, forecasting, and advanced analytics.