-- Customer Intelligence Platform V2
-- Validate customer-level uniqueness and segmentation.

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_unique_id) AS unique_customers,
    COUNT(*) - COUNT(DISTINCT customer_unique_id) AS duplicate_rows
FROM public.customer_segments;

-- Check the number of customers in each segment.

SELECT
    customer_segment,
    COUNT(*) AS total_customers
FROM public.customer_segments
GROUP BY customer_segment
ORDER BY total_customers DESC;