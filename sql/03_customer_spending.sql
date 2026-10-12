-- Customer Intelligence Platform V2
-- Customer-level spending summary for delivered orders
-- Payment records are aggregated before joining to avoid duplication.

CREATE OR REPLACE VIEW public.customer_spending AS
WITH payment_totals AS (
    SELECT
        order_id,
        SUM(payment_value) AS total_payment_value
    FROM public.olist_order_payments
    GROUP BY order_id
)
SELECT
    c.customer_unique_id,
    MAX(c.customer_city)::VARCHAR(100) AS customer_city,
    MAX(c.customer_state)::VARCHAR(2) AS customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(p.total_payment_value) AS total_spent
FROM public.olist_customers AS c
INNER JOIN public.olist_orders AS o
    ON c.customer_id = o.customer_id
INNER JOIN payment_totals AS p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id;
