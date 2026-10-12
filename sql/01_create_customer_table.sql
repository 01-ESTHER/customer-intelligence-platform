SELECT current_database();
CREATE TABLE olist_customers (
     customer_id VARCHAR(50),
	 customer_unique_id VARCHAR(50),
	 customer_zip_code_prefix VARCHAR(5),
	 customer_city VARCHAR(100),
	 customer_state VARCHAR(2)
);
SELECT COUNT(*)
FROM olist_customers;