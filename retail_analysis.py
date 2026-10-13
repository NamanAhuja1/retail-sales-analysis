import sys
from getpass import getpass

import pandas as pd

# 1. Read the CSV file.
df = pd.read_csv('orders.csv', na_values=['Not Available', 'unknown'])
print('First five rows:')
print(df.head())
print('\nOriginal shape:', df.shape)

# 2. Make column names easier to use.
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# 3. Remove duplicate rows and handle missing values.
df = df.drop_duplicates().copy()
df['ship_mode'] = df['ship_mode'].fillna('Unknown')
df = df.dropna(subset=[
    'order_id', 'order_date', 'product_id', 'region', 'category',
    'quantity', 'list_price', 'cost_price', 'discount_percent'
]).copy()
if df.empty:
    raise ValueError('No usable rows remain. Check your CSV file.')
print('Cleaned shape:', df.shape)

# 4. Convert dates and calculate new columns.
# Prices are treated as totals for each row, not per-unit prices.
df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d')
df['discount'] = (df['list_price'] * df['discount_percent'] / 100).round(2)
df['sale_price'] = (df['list_price'] - df['discount']).round(2)
df['profit'] = (df['sale_price'] - df['cost_price']).round(2)

# 5. Use basic Pandas operations to summarize the data.
print('\nTotal sales:', round(df['sale_price'].sum(), 2))
print('Total profit:', round(df['profit'].sum(), 2))
print('\nSales by region:')
print(df.groupby('region')['sale_price'].sum().sort_values(ascending=False))
print('\nProfit by category:')
print(df.groupby('category')['profit'].sum().sort_values(ascending=False))
df.to_csv('cleaned_orders.csv', index=False)
print('\nSaved cleaned_orders.csv')

# Optional: run only the Pandas part before setting up MySQL.
if '--clean-only' in sys.argv:
    sys.exit(0)

# 6. Connect Python to your local MySQL server.
import mysql.connector

username = input('\nMySQL username (press Enter for root): ').strip() or 'root'
password = getpass('MySQL password: ')
connection = mysql.connector.connect(
    host='localhost', port=3306, user=username, password=password
)
cursor = connection.cursor()

try:
    cursor.execute('CREATE DATABASE IF NOT EXISTS retail_sales_project')
    cursor.execute('USE retail_sales_project')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id BIGINT,
            order_date DATE,
            region VARCHAR(100),
            category VARCHAR(100),
            product_id VARCHAR(100),
            quantity INT,
            sale_price DECIMAL(18, 2),
            profit DECIMAL(18, 2)
        ) ENGINE=InnoDB
    ''')

    # Reload only this project's orders table on each run.
    cursor.execute('DELETE FROM orders')
    columns = ['order_id', 'order_date', 'region', 'category',
               'product_id', 'quantity', 'sale_price', 'profit']
    rows = []
    for row in df[columns].itertuples(index=False, name=None):
        rows.append((int(row[0]), row[1].date(), str(row[2]), str(row[3]),
                     str(row[4]), int(row[5]), float(row[6]), float(row[7])))

    cursor.executemany('''
        INSERT INTO orders
        (order_id, order_date, region, category, product_id, quantity, sale_price, profit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', rows)
    connection.commit()
    print(f'Loaded {len(rows)} rows into MySQL.')

    # 7. Run a simple SQL query from Python.
    cursor.execute('SELECT COUNT(*), SUM(sale_price), SUM(profit) FROM orders')
    print('MySQL row count, total sales, total profit:', cursor.fetchone())
except Exception:
    connection.rollback()
    raise
finally:
    cursor.close()
    connection.close()
