create database internship;
use internship;
select * from final_data;
ALTER TABLE final_data
CHANGE COLUMN `ï»¿Order_Number` `Order_Number` TEXT;
CREATE TABLE cancelled_orders AS
SELECT *
FROM orders
WHERE order_status = 'cancelled';

select * from cancelled_orders;

SELECT ORDER_NUMBER,ORDER_DATE,PURCHASED_BY,CUSTOMER_NAME,CITY,PINCODE,CONTACT_NUMBER,ORDER_STATUS,DISCOUNT,DELIVERY_CHARGES,AMOUNT_PAID FROM final_data;
SELECT  distinct ORDER_NUMBER,ORDER_DATE,PURCHASED_BY,CUSTOMER_NAME,CITY,PINCODE,CONTACT_NUMBER,ORDER_STATUS,DISCOUNT,DELIVERY_CHARGES,AMOUNT_PAID FROM final_data;
create table quantity as (select order_number,quantity,sku from final_data);



select * from quantity;

-- Find out how many orders are in each status:
SELECT ORDER_STATUS, COUNT(*) AS order_count
FROM final_data
GROUP BY ORDER_STATUS;

-- order complete table
   select * from final_data where order_status="ORDER COMPLETE";
CREATE TABLE COMPLETE_orders AS
SELECT *
FROM orders
WHERE order_status = 'ORDER COMPLETE';

-- Find out which cities have the most orders:

SELECT CITY, COUNT(*) AS number_of_orders
FROM final_data
GROUP BY CITY
ORDER BY number_of_orders DESC;
-- avg lifespan
SELECT 
    CUSTOMER_NAME,
    SUM(AMOUNT_PAID) AS LifetimeValue
FROM final_data
GROUP BY CUSTOMER_NAME;
-- avg orer value by month
SELECT 
    DATE_FORMAT(ORDER_DATE, '%Y-%m') AS YearMonth,
    AVG(AMOUNT_PAID) AS AvgOrderValue
FROM final_data
GROUP BY YearMonth
ORDER BY YearMonth;

-- monthly sales performance
SELECT 
    DATE_FORMAT(ORDER_DATE, '%Y-%m') AS YearMonth,
    COUNT(*) AS TotalOrders,
    SUM(AMOUNT_PAID) AS TotalSales,
    AVG(AMOUNT_PAID) AS AvgOrderValue
FROM final_data
GROUP BY YearMonth
ORDER BY YearMonth;


-- Convert Order Date to Month-Year format and create a temporary table
CREATE TEMPORARY TABLE temp_customer_activity AS
SELECT 
    CUSTOMER_NAME,
    DATE_FORMAT(STR_TO_DATE(ORDER_DATE, '%d-%m-%Y'), '%Y-%m') AS YearMonth
FROM final_data;


-- Step 2: Calculate customer activity counts per month
CREATE TEMPORARY TABLE customer_activity AS
SELECT CUSTOMER_NAME, YearMonth, COUNT(*) AS ActivityCount
FROM temp_customer_activity
GROUP BY CUSTOMER_NAME, YearMonth;
-- Step 3: Pivot table to have YearMonth as columns and ActivityCount as values
CREATE TEMPORARY TABLE customer_pivot AS
SELECT 
    CUSTOMER_NAME,
    MAX(CASE WHEN YearMonth = 'YYYY-MM' THEN ActivityCount ELSE 0 END) AS YYYY_MM,
    MAX(CASE WHEN YearMonth = 'YYYY-MM' THEN ActivityCount ELSE 0 END) AS YYYY_MM,
    ...
    MAX(CASE WHEN YearMonth = 'YYYY-MM' THEN ActivityCount ELSE 0 END) AS YYYY_MM
FROM customer_activity
GROUP BY CUSTOMER_NAME;

