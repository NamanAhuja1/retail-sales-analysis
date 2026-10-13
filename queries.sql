USE retail_sales_project;

-- 1. Total sales and profit.
SELECT SUM(sale_price) AS total_sales, SUM(profit) AS total_profit
FROM orders;

-- 2. Top 5 products by sales revenue.
SELECT product_id, SUM(sale_price) AS total_sales
FROM orders
GROUP BY product_id
ORDER BY total_sales DESC, product_id
LIMIT 5;

-- 3. Sales and profit by region.
SELECT region, SUM(sale_price) AS total_sales, SUM(profit) AS total_profit
FROM orders
GROUP BY region
ORDER BY total_sales DESC;

-- 4. Sales and profit by category.
SELECT category, SUM(sale_price) AS total_sales, SUM(profit) AS total_profit
FROM orders
GROUP BY category
ORDER BY total_profit DESC;

-- 5. Monthly sales and profit (include the year).
SELECT DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
       SUM(sale_price) AS total_sales, SUM(profit) AS total_profit
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month;
