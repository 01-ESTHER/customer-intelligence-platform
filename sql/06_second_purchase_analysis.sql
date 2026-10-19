-- Metric Definitions:
--
-- Repeat Customer:
-- A customer identified by customer_unique_id
-- who has made at least two delivered purchases.
--
-- Days to Second Purchase:
-- The time in days between a customer's first
-- and second delivered purchases.
--
-- Average and Median Days to Second Purchase:
-- Calculated only for customers with at least
-- two delivered purchases.
-- Customer Intelligence Platform V2
-- Second-Purchase Behaviour Analysis
--
-- Business Question:
-- How long does it take customers to make
-- their second delivered purchase?
--
-- Analysis:
-- 1. Identify each customer's purchase sequence.
-- 2. Calculate the days between purchases.
-- 3. Identify customers who made a second purchase.
-- 4. Calculate the average and median time
--    between first and second purchases.
--
-- Scope:
-- Delivered orders only.
-- Customers identified using customer_unique_id.

-- Step 1: Identify each customer's purchase sequence
-- and calculate their previous purchase date.

CREATE OR REPLACE VIEW public.customer_purchase_history AS

SELECT
    c.customer_unique_id,
    o.order_id,
    o.order_purchase_timestamp,

    ROW_NUMBER() OVER (
        PARTITION BY c.customer_unique_id
        ORDER BY o.order_purchase_timestamp, o.order_id
    ) AS purchase_number,

    LAG(o.order_purchase_timestamp) OVER (
        PARTITION BY c.customer_unique_id
        ORDER BY o.order_purchase_timestamp, o.order_id
    ) AS previous_purchase

FROM public.olist_customers AS c

INNER JOIN public.olist_orders AS o
    ON c.customer_id = o.customer_id

WHERE o.order_status = 'delivered';

-- Step 2: Calculate second-purchase timing
-- for customers who made at least two delivered purchases.
-- Exploratory validation query.
-- The reporting view used by Power BI is created below.s
SELECT
    COUNT(*) AS repeat_customers,

    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                order_purchase_timestamp - previous_purchase
            )) / 86400
        )::NUMERIC,
        2
    ) AS average_days_to_second_purchase,

    ROUND(
        PERCENTILE_CONT(0.5) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (
                order_purchase_timestamp - previous_purchase
            )) / 86400
        )::NUMERIC,
        2
    ) AS median_days_to_second_purchase

FROM public.customer_purchase_history

WHERE purchase_number = 2;

CREATE OR REPLACE VIEW public.second_purchase_metrics AS

SELECT
    COUNT(*) AS repeat_customers,

    ROUND(
        AVG(
            EXTRACT(EPOCH FROM (
                order_purchase_timestamp - previous_purchase
            )) / 86400
        )::NUMERIC,
        2
    ) AS average_days_to_second_purchase,

    ROUND(
        PERCENTILE_CONT(0.5) WITHIN GROUP (
            ORDER BY EXTRACT(EPOCH FROM (
                order_purchase_timestamp - previous_purchase
            )) / 86400
        )::NUMERIC,
        2
    ) AS median_days_to_second_purchase

FROM public.customer_purchase_history

WHERE purchase_number = 2;

-- Step 3: Second-purchase timing distribution
-- Group returning customers by the number of days
-- between their first and second delivered purchases.
--
-- Timing groups:
-- 0-30 days
-- 31-60 days
-- 61-90 days
-- More than 90 days
CREATE OR REPLACE VIEW public.second_purchase_timing AS

WITH second_purchases AS (
    SELECT
        customer_unique_id,
        EXTRACT(EPOCH FROM (
            order_purchase_timestamp - previous_purchase
        )) / 86400 AS days_to_second_purchase
    FROM public.customer_purchase_history
    WHERE purchase_number = 2
)

SELECT
    CASE
        WHEN days_to_second_purchase <= 30 THEN '0-30 days'
        WHEN days_to_second_purchase <= 60 THEN '31-60 days'
        WHEN days_to_second_purchase <= 90 THEN '61-90 days'
        ELSE 'More than 90 days'
    END AS purchase_timing_group,

COUNT(*) AS total_customers,

CASE
    WHEN days_to_second_purchase <= 30 THEN 1
    WHEN days_to_second_purchase <= 60 THEN 2
    WHEN days_to_second_purchase <= 90 THEN 3
    ELSE 4
END AS sort_order

FROM second_purchases
GROUP BY purchase_timing_group, sort_order;
-- Step 4: Validate second-purchase reporting metrics.
-- Expected results: 2801 customers, 81.21 average days,
-- and 28.98 median days.

SELECT
    repeat_customers,
    average_days_to_second_purchase,
    median_days_to_second_purchase
FROM public.second_purchase_metrics;

-- Analysis Limitations:
--
-- 1. The analysis uses historical Olist order data.
--
-- 2. Only delivered orders are included.
--    Cancelled and other non-delivered orders are excluded.
--
-- 3. Average and median second-purchase times are
--    calculated only for customers who returned.
--
-- 4. Customers who purchased near the end of the
--    dataset had less time to make a second purchase.
--    This may affect the observed repeat customer rate.
--
-- 5. These findings describe customer behaviour.
--    They do not establish why customers returned
--    or whether a marketing intervention would help.