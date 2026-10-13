# Retail Sales & Profitability Analysis

A simple project using Python, Pandas and MySQL to clean retail order data, calculate sales and profit, and answer basic business questions.

## What the project demonstrates

- Importing a CSV with Pandas.
- Viewing data with head() and shape.
- Renaming columns, removing duplicates and handling missing values.
- Converting dates with to_datetime().
- Calculating discount, sales and profit columns.
- Summarizing data with groupby(), sum() and sort_values().
- Connecting Python to MySQL and inserting records.
- Analyzing data with SELECT, SUM, GROUP BY, ORDER BY and LIMIT.

## Files

| File | Purpose |
| --- | --- |
| retail_analysis.py | Clean the CSV, calculate metrics, load MySQL and run a query |
| queries.sql | Five simple business queries |
| requirements.txt | The two Python packages needed |
| sample_orders.csv | Six fictional rows for trying the project |
| START_HERE.md | Setup and GitHub upload instructions |

## Dataset

Download the CSV from the [retail orders dataset](https://www.kaggle.com/datasets/ankitbansal06/retail-orders/) and put orders.csv next to the Python script. The dataset itself is not included in this repository.

For a practice run, copy sample_orders.csv to orders.csv. The sample is fictional and should not be presented as actual business findings.

Expected source columns include Order Id, Order Date, Ship Mode, Region, Category, Product Id, Quantity, List Price, Cost Price and Discount Percent. Other source columns can remain in the CSV.

## Run

```bash
python -m pip install -r requirements.txt
python retail_analysis.py
```

Enter your local MySQL username and password when asked. Passwords are not stored in the script. Follow START_HERE.md for the full setup.

To try just the Pandas part:

```bash
python retail_analysis.py --clean-only
```

## Calculations

```text
discount = list_price × discount_percent / 100
sale_price = list_price − discount
profit = sale_price − cost_price
```

This project assumes List Price and Cost Price are totals for each row. Quantity is not multiplied into these amounts. Confirm this assumption against the dataset before interpreting results. For documented per-unit prices, multiply both price fields by quantity before calculating the discount.

Profit only subtracts the provided cost; it does not separately include operating expenses, taxes or returns. This is a beginner demonstration using rounded Pandas calculations.

Exact duplicates are removed. Missing Ship Mode values become Unknown. Rows missing required analysis fields are dropped; the script prints row counts before and after cleaning. Invalid dates stop execution so they can be corrected.

Every full run reloads the orders table in the dedicated retail_sales_project database. It uses DELETE and INSERT in a transaction to avoid accumulating duplicate copies. No other database is used.

## SQL questions

1. What are total sales and profit?
2. Which five products generate the most sales revenue?
3. What are sales and profit by region?
4. What are sales and profit by category?
5. What are sales and profit by month?

## Results

After running your actual dataset, add your total sales/profit, strongest region, leading category and top product here. Include a screenshot of a query result. Do not use the fictional sample values as real findings.
