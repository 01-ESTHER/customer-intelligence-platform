-- Customer Intelligence Platform V2
-- Segment customers by delivered order frequency and spending.

CREATE OR REPLACE VIEW public.customer_segments AS
SELECT
    customer_unique_id,
    customer_city,
    customer_state,
    total_orders,
    total_spent,
    CASE
        WHEN total_orders >= 2
            THEN 'Repeat Customer'
        WHEN total_spent >= 500
            THEN 'High-Value One-Time Customer'
        ELSE 'Other One-Time Customer'
    END AS customer_segment
FROM public.customer_spending;