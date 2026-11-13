from pathlib import Path
import pandas as pd
import numpy as np
# Locate project directories
project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"

# Define the original Olist source files
source_files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
}


# Load and retain each source dataset
datasets = {}

print("\nRaw Olist Data Loading")
print("-" * 45)

for name, filename in source_files.items():
    file_path = data_dir / filename

    if not file_path.is_file():
        raise FileNotFoundError(f"Missing source file: {file_path}")

    datasets[name] = pd.read_csv(file_path)
    print(f"{name}: {datasets[name].shape}")

# Make source datasets available for subsequent transformations
customers = datasets["customers"]
orders = datasets["orders"]
order_items = datasets["order_items"]
payments = datasets["payments"]
products = datasets["products"]

print("\nAll source datasets loaded successfully.")



# Validate required columns in the source datasets
required_columns = {
    "customers": ["customer_id", "customer_unique_id"],
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
    ],
    "order_items": ["order_id", "product_id", "price", "freight_value"],
    "payments": ["order_id", "payment_type", "payment_value"],
    "products": ["product_id", "product_category_name"],
}

for name, filename in source_files.items():
    dataset = pd.read_csv(data_dir / filename)

    missing_columns = [
        column
        for column in required_columns[name]
        if column not in dataset.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{name} is missing required columns: {missing_columns}"
        )

    print(f"{name}: Required columns verified")

print("\nSource schema validation passed.")


# Connect orders to their customer identities
customer_orders = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="one_to_one"
)

# Convert order purchase timestamps to datetime
customer_orders["order_purchase_timestamp"] = pd.to_datetime(
    customer_orders["order_purchase_timestamp"],
    errors="coerce"
)

# Validate the customer-order dataset
print("\nCustomer-Order Integration")
print("-" * 45)
print("Customer-order records:", len(customer_orders))

missing_customers = customer_orders["customer_unique_id"].isna().sum()
missing_dates = customer_orders["order_purchase_timestamp"].isna().sum()
duplicate_orders = customer_orders["order_id"].duplicated().sum()

print("Missing customer identities:", missing_customers)
print("Missing purchase timestamps:", missing_dates)
print("Duplicate order IDs:", duplicate_orders)
print(
    "Unique customers:",
    customer_orders["customer_unique_id"].nunique()
)

assert missing_customers == 0, "Missing customer identities detected"
assert missing_dates == 0, "Missing purchase timestamps detected"
assert duplicate_orders == 0, "Duplicate order IDs detected"

print("\nCustomer-order integration validation passed.")


# Arrange all customer orders chronologically
# Include every order status when identifying the first order
all_orders_sorted = customer_orders.sort_values(
    by=[
        "customer_unique_id",
        "order_purchase_timestamp",
        "order_id"
    ]
).copy()

# Assign a chronological order number per customer
all_orders_sorted["order_number"] = (
    all_orders_sorted
    .groupby("customer_unique_id")
    .cumcount() + 1
)

# Identify each customer's first recorded order
first_recorded_orders = all_orders_sorted[
    all_orders_sorted["order_number"] == 1
].copy()

# Validate the first-order population
print("\nFirst Recorded Order Identification")
print("-" * 45)
print("First recorded orders:", len(first_recorded_orders))
print(
    "Unique customers:",
    first_recorded_orders["customer_unique_id"].nunique()
)
print(
    "Duplicate customers:",
    first_recorded_orders["customer_unique_id"].duplicated().sum()
)

print("\nFirst recorded order statuses:")
print(first_recorded_orders["order_status"].value_counts())

assert len(first_recorded_orders) == 96096
assert first_recorded_orders["customer_unique_id"].is_unique

print("\nFirst recorded order validation passed.")


# Define the historical observation cutoff and follow-up windows
observation_cutoff = pd.Timestamp("2018-08-31 23:59:59")
prediction_window = pd.Timedelta(days=60)
delivery_buffer = pd.Timedelta(days=30)

# Calculate the latest eligible first-order timestamps
latest_eligible_date = observation_cutoff - prediction_window

latest_buffered_first_order = (
    observation_cutoff
    - prediction_window
    - delivery_buffer
)

# Identify customers with a complete 60-day observation window
eligible_first_orders = first_recorded_orders[
    first_recorded_orders["order_purchase_timestamp"]
    <= latest_eligible_date
].copy()

# Apply the additional delivery buffer
buffered_eligible_customers = first_recorded_orders[
    first_recorded_orders["order_purchase_timestamp"]
    <= latest_buffered_first_order
].copy()

# Validate the eligibility populations
print("\nCustomer Eligibility Validation")
print("-" * 45)
print("Observation cutoff:", observation_cutoff)
print("Latest eligible date:", latest_eligible_date)
print("Latest buffered date:", latest_buffered_first_order)
print("Original customers:", len(first_recorded_orders))
print("Eligible customers:", len(eligible_first_orders))
print("Buffered eligible customers:", len(buffered_eligible_customers))

print(
    "Customers excluded by the buffer:",
    len(eligible_first_orders) - len(buffered_eligible_customers)
)

assert buffered_eligible_customers["customer_unique_id"].is_unique
assert len(buffered_eligible_customers) <= len(eligible_first_orders)

print("\nCustomer eligibility validation passed.")


# Identify subsequent delivered orders
subsequent_delivered_orders = all_orders_sorted[
    (all_orders_sorted["order_number"] > 1)
    & (all_orders_sorted["order_status"] == "delivered")
].copy()

# Connect subsequent orders to each customer's first purchase date
all_return_candidates = subsequent_delivered_orders[
    [
        "customer_unique_id",
        "order_purchase_timestamp",
        "order_delivered_customer_date"
    ]
].merge(
    eligible_first_orders[
        ["customer_unique_id", "order_purchase_timestamp"]
    ].rename(
        columns={
            "order_purchase_timestamp": "first_order_date"
        }
    ),
    on="customer_unique_id",
    how="inner",
    validate="many_to_one"
)

# Calculate days between the first and subsequent purchases
all_return_candidates["days_since_first_order"] = (
    all_return_candidates["order_purchase_timestamp"]
    - all_return_candidates["first_order_date"]
).dt.total_seconds() / 86400

# Select purchases made within the 60-day observation window
qualifying_orders = all_return_candidates[
    all_return_candidates["days_since_first_order"].between(
        0, 60, inclusive="both"
    )
].copy()

# Confirm actual delivery dates
qualifying_orders["order_delivered_customer_date"] = pd.to_datetime(
    qualifying_orders["order_delivered_customer_date"],
    errors="coerce"
)

qualifying_customer_ids = qualifying_orders.loc[
    qualifying_orders["order_delivered_customer_date"] <= observation_cutoff,
    "customer_unique_id"
].unique()

# Create the initial target for the buffered eligible population
buffered_modelling_customers = buffered_eligible_customers.copy()

buffered_modelling_customers["repeat_purchase_60d"] = (
    buffered_modelling_customers["customer_unique_id"]
    .isin(qualifying_customer_ids)
    .astype(int)
)

# Validate the repeat-purchase target
print("\nRepeat-Purchase Target Validation")
print("-" * 45)
print("Buffered customers:", len(buffered_modelling_customers))
print("Qualifying repeat customers:", int(
    buffered_modelling_customers["repeat_purchase_60d"].sum()
))

print("\nTarget distribution:")
print(
    buffered_modelling_customers["repeat_purchase_60d"].value_counts()
)

assert buffered_modelling_customers["customer_unique_id"].is_unique
assert len(buffered_modelling_customers) == 78125
assert buffered_modelling_customers["repeat_purchase_60d"].notna().all()

print("\nRepeat-purchase target validation passed.")


# Identify subsequent orders for buffered eligible customers
buffered_customer_orders = all_orders_sorted[
    all_orders_sorted["customer_unique_id"].isin(
        buffered_modelling_customers["customer_unique_id"]
    )
    & (all_orders_sorted["order_number"] > 1)
].copy()

# Attach each customer's first recorded order date
buffered_customer_orders = buffered_customer_orders.merge(
    buffered_modelling_customers[
        ["customer_unique_id", "order_purchase_timestamp"]
    ].rename(
        columns={"order_purchase_timestamp": "first_order_date"}
    ),
    on="customer_unique_id",
    how="inner",
    validate="many_to_one"
)

# Calculate the time between first and subsequent purchases
buffered_customer_orders["days_since_first_order"] = (
    buffered_customer_orders["order_purchase_timestamp"]
    - buffered_customer_orders["first_order_date"]
).dt.total_seconds() / 86400

# Retain subsequent purchases made within 60 days
buffered_60d_orders = buffered_customer_orders[
    buffered_customer_orders["days_since_first_order"].between(
        0, 60, inclusive="both"
    )
].copy()

# Identify unresolved subsequent orders
unresolved_statuses = [
    "shipped",
    "processing",
    "invoiced",
    "created",
    "approved"
]

unresolved_orders = buffered_60d_orders[
    buffered_60d_orders["order_status"].isin(unresolved_statuses)
].copy()

# Identify customers with unresolved orders and negative labels
unresolved_customer_ids = unresolved_orders[
    "customer_unique_id"
].unique()

unresolved_customer_audit = buffered_modelling_customers[
    buffered_modelling_customers["customer_unique_id"].isin(
        unresolved_customer_ids
    )
].copy()

uncertain_customer_ids = unresolved_customer_audit.loc[
    unresolved_customer_audit["repeat_purchase_60d"] == 0,
    "customer_unique_id"
]

# Exclude uncertain negative labels from the modelling population
clean_modelling_customers = buffered_modelling_customers[
    ~buffered_modelling_customers["customer_unique_id"].isin(
        uncertain_customer_ids
    )
].copy()

# Validate the cleaned modelling population
print("\nCleaned Modelling Population Validation")
print("-" * 45)
print("Original buffered customers:", len(buffered_modelling_customers))
print("Unresolved subsequent orders:", len(unresolved_orders))
print("Uncertain customers excluded:", len(uncertain_customer_ids))
print("Cleaned modelling customers:", len(clean_modelling_customers))
print("Confirmed repeat purchasers:", int(
    clean_modelling_customers["repeat_purchase_60d"].sum()
))
print(
    "Repeat-purchase rate:",
    round(clean_modelling_customers["repeat_purchase_60d"].mean() * 100, 2),
    "%"
)

assert len(uncertain_customer_ids) == 25
assert len(clean_modelling_customers) == 78100
assert clean_modelling_customers["customer_unique_id"].is_unique
assert clean_modelling_customers["repeat_purchase_60d"].sum() == 1589

print("\nCleaned modelling population validation passed.")


# Select the first-order information used for feature engineering
feature_columns = [
    "customer_unique_id",
    "order_id",
    "order_purchase_timestamp",
    "customer_city",
    "customer_state",
    "customer_zip_code_prefix",
    "repeat_purchase_60d"
]

customer_features = clean_modelling_customers[
    feature_columns
].copy()

# Derive purchase-time features from the first recorded order
customer_features["purchase_month"] = (
    customer_features["order_purchase_timestamp"].dt.month
)

customer_features["purchase_day_of_week"] = (
    customer_features["order_purchase_timestamp"].dt.dayofweek
)

customer_features["purchase_hour"] = (
    customer_features["order_purchase_timestamp"].dt.hour
)

# Validate customer-level feature construction
print("\nInitial Customer Feature Validation")
print("-" * 45)
print("Customer feature records:", len(customer_features))
print("Feature columns:", customer_features.shape[1])
print(
    "Duplicate customers:",
    customer_features["customer_unique_id"].duplicated().sum()
)

time_features = [
    "purchase_month",
    "purchase_day_of_week",
    "purchase_hour"
]

print("\nMissing purchase-time features:")
print(customer_features[time_features].isna().sum())

assert len(customer_features) == 78100
assert customer_features["customer_unique_id"].is_unique
assert customer_features[time_features].notna().all().all()

print("\nInitial customer feature validation passed.")


# Aggregate order items into one record per order
order_basket_features = (
    order_items
    .groupby("order_id")
    .agg(
        first_order_item_count=("order_item_id", "count"),
        first_order_product_count=("product_id", "nunique"),
        first_order_seller_count=("seller_id", "nunique"),
        first_order_item_value=("price", "sum")
    )
    .reset_index()
)

# Confirm the basket aggregation has one record per order
assert order_basket_features["order_id"].is_unique

# Join basket features to each customer's first recorded order
customer_features = customer_features.merge(
    order_basket_features,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# Validate basket feature construction
basket_columns = [
    "first_order_item_count",
    "first_order_product_count",
    "first_order_seller_count",
    "first_order_item_value"
]

print("\nFirst-Order Basket Feature Validation")
print("-" * 45)
print("Customer records:", len(customer_features))
print("Feature columns:", customer_features.shape[1])
print(
    "Duplicate customers:",
    customer_features["customer_unique_id"].duplicated().sum()
)

print("\nMissing basket features:")
print(customer_features[basket_columns].isna().sum())

print(
    "\nInvalid product counts:",
    int((
        customer_features["first_order_product_count"]
        > customer_features["first_order_item_count"]
    ).sum())
)


# Validate product counts only where basket information exists
valid_basket_rows = customer_features[
    [
        "first_order_item_count",
        "first_order_product_count"
    ]
].notna().all(axis=1)

assert (
    customer_features.loc[
        valid_basket_rows, "first_order_product_count"
    ]
    <= customer_features.loc[
        valid_basket_rows, "first_order_item_count"
    ]
).all()

print("\nFirst-order basket feature validation passed.")


# Calculate total recorded freight charges for each order
order_freight_features = (
    order_items
    .groupby("order_id")
    .agg(
        first_order_freight_value=("freight_value", "sum")
    )
    .reset_index()
)

# Confirm one freight record per order
assert order_freight_features["order_id"].is_unique

# Add freight information to the customer feature dataset
customer_features = customer_features.merge(
    order_freight_features,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# Calculate total first-order basket value
customer_features["first_order_total_basket_value"] = (
    customer_features["first_order_item_value"]
    + customer_features["first_order_freight_value"]
)

# Validate the financial features
financial_features = [
    "first_order_item_value",
    "first_order_freight_value",
    "first_order_total_basket_value"
]

print("\nFirst-Order Freight Feature Validation")
print("-" * 45)
print("Customer records:", len(customer_features))
print("Feature columns:", customer_features.shape[1])
print("Duplicate customers:", customer_features["customer_unique_id"].duplicated().sum())

print("\nMissing financial values:")
print(customer_features[financial_features].isna().sum())

print("\nNegative financial values:")
print((customer_features[financial_features] < 0).sum())

assert len(customer_features) == 78100
assert customer_features["customer_unique_id"].is_unique
assert not (customer_features[financial_features].dropna() < 0).any().any()

print("\nFirst-order freight feature validation passed.")


# Create the log-transformed first-order basket value
customer_features["first_order_total_basket_value_log"] = (
    np.log1p(customer_features["first_order_total_basket_value"])
)

# Validate the log transformation
print("\nLog-Transformed Basket Feature Validation")
print("-" * 45)
print("Customer records:", len(customer_features))
print("Feature columns:", customer_features.shape[1])

print(
    "Missing log-transformed values:",
    customer_features["first_order_total_basket_value_log"].isna().sum()
)

print(
    "Negative log-transformed values:",
    (
        customer_features["first_order_total_basket_value_log"] < 0
    ).sum()
)

# Ensure missing basket values remain missing after transformation
assert len(customer_features) == 78100
assert customer_features["customer_unique_id"].is_unique
assert (
    customer_features["first_order_total_basket_value_log"].isna().sum()
    == customer_features["first_order_total_basket_value"].isna().sum()
)

print("\nLog-transformed basket feature validation passed.")


# Identify payment records associated with customers' first orders
first_order_payments = payments[
    payments["order_id"].isin(customer_features["order_id"])
].copy()

# Create binary payment-method indicators for each order
payment_method_features = pd.crosstab(
    first_order_payments["order_id"],
    first_order_payments["payment_type"]
)

payment_method_features = (
    payment_method_features > 0
).astype(int)

# Rename payment indicators to match the original notebook
payment_method_features = payment_method_features.rename(
    columns={
        "credit_card": "uses_credit_card",
        "boleto": "uses_boleto",
        "voucher": "uses_voucher",
        "debit_card": "uses_debit_card"
    }
).reset_index()

# Validate one payment-method record per order
assert payment_method_features["order_id"].is_unique

# Merge payment indicators with customer features
customer_features = customer_features.merge(
    payment_method_features,
    on="order_id",
    how="left",
    validate="one_to_one"
)

payment_columns = [
    "uses_credit_card",
    "uses_boleto",
    "uses_voucher",
    "uses_debit_card"
]

# Validate payment-method feature construction
print("\nFirst-Order Payment Method Validation")
print("-" * 45)
print("Customer records:", len(customer_features))
print("Feature columns:", customer_features.shape[1])
print(
    "First orders with payment records:",
    first_order_payments["order_id"].nunique()
)
print(
    "First orders without payment records:",
    len(customer_features)
    - first_order_payments["order_id"].nunique()
)
print(
    "Duplicate customers:",
    customer_features["customer_unique_id"].duplicated().sum()
)

print("\nMissing payment indicators:")
print(customer_features[payment_columns].isna().sum())

assert len(customer_features) == 78100
assert customer_features["customer_unique_id"].is_unique
assert all(column in customer_features.columns for column in payment_columns)

print("\nFirst-order payment method validation passed.")


# Aggregate first-order payment instalment information
payment_installment_features = (
    first_order_payments
    .groupby("order_id")
    .agg(
        first_order_max_installments=("payment_installments", "max"),
        first_order_payment_entries=("payment_sequential", "count")
    )
    .reset_index()
)

# Validate one payment summary per order
assert payment_installment_features["order_id"].is_unique

# Add payment instalment features to customer records
customer_features = customer_features.merge(
    payment_installment_features,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# Validate the updated customer dataset
installment_columns = [
    "first_order_max_installments",
    "first_order_payment_entries"
]

print("\nFirst-Order Payment Instalment Validation")
print("-" * 45)
print("Customer records:", len(customer_features))
print("Feature columns:", customer_features.shape[1])
print(
    "Duplicate customers:",
    customer_features["customer_unique_id"].duplicated().sum()
)

print("\nMissing payment instalment features:")
print(customer_features[installment_columns].isna().sum())

print(
    "\nOrders with zero instalments:",
    (customer_features["first_order_max_installments"] == 0).sum()
)

assert len(customer_features) == 78100
assert customer_features["customer_unique_id"].is_unique
assert (
    customer_features["first_order_payment_entries"].dropna() >= 1
).all()

print("\nFirst-order payment instalment validation passed.")


# Count distinct recorded payment methods per customer
customer_features["payment_method_count"] = (
    customer_features[payment_columns].sum(
        axis=1,
        min_count=1
    )
)

# Join order items to their recorded product categories
order_items_products = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left",
    validate="many_to_one"
)

# Select items associated with customers' first recorded orders
first_order_product_items = order_items_products[
    order_items_products["order_id"].isin(
        customer_features["order_id"]
    )
].copy()

# Count distinct recorded categories for each first order
order_category_features = (
    first_order_product_items
    .groupby("order_id")
    .agg(
        first_order_category_count=("product_category_name", "nunique")
    )
    .reset_index()
)

customer_features = customer_features.merge(
    order_category_features,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# Calculate merchandise value contributed by each product category
category_order_values = (
    first_order_product_items
    .dropna(subset=["product_category_name"])
    .groupby(
        ["order_id", "product_category_name"],
        as_index=False
    )
    .agg(category_value=("price", "sum"))
)

# Select the highest-value category, using category name to break ties
category_order_values = category_order_values.sort_values(
    by=["order_id", "category_value", "product_category_name"],
    ascending=[True, False, True]
)

primary_order_categories = (
    category_order_values
    .drop_duplicates(subset="order_id", keep="first")
    [["order_id", "product_category_name", "category_value"]]
    .rename(
        columns={
            "product_category_name": "first_order_primary_category",
            "category_value": "primary_category_value"
        }
    )
)

customer_features = customer_features.merge(
    primary_order_categories,
    on="order_id",
    how="left",
    validate="one_to_one"
)

# Calculate the proportion of merchandise value in the primary category
customer_features["first_order_primary_category_share"] = (
    customer_features["primary_category_value"]
    / customer_features["first_order_item_value"]
)

# Combine city and state into a distinct geographical identifier
customer_features["customer_city_state"] = (
    customer_features["customer_city"].str.strip().str.lower()
    + "_"
    + customer_features["customer_state"].str.strip().str.upper()
)

# Validate the completed customer feature structure
print("\nComplete Feature Engineering Validation")
print("-" * 45)
print("Customer records:", len(customer_features))
print("Feature columns:", len(customer_features.columns))
print("Duplicate customers:", customer_features["customer_unique_id"].duplicated().sum())
print("Confirmed repeat purchasers:", int(customer_features["repeat_purchase_60d"].sum()))
print("Missing primary categories:", customer_features["first_order_primary_category"].isna().sum())
print("Missing category counts:", customer_features["first_order_category_count"].isna().sum())
print("Missing city-state values:", customer_features["customer_city_state"].isna().sum())

assert len(customer_features) == 78100
assert len(customer_features.columns) == 29
assert customer_features["customer_unique_id"].is_unique
assert customer_features["repeat_purchase_60d"].sum() == 1589
assert customer_features["first_order_primary_category"].isna().sum() == 1903
assert customer_features["first_order_category_count"].isna().sum() == 642
assert customer_features["customer_city_state"].notna().all()

print("\nComplete feature engineering validation passed.")


# Load the preserved reference dataset from Notebook 02
reference_path = (
    data_dir / "processed" / "customer_features_reference.pkl"
)

reference_features = pd.read_pickle(reference_path)

# Compare dataset dimensions and column names
print("\nReference Dataset Comparison")
print("-" * 45)
print("Original shape:", reference_features.shape)
print("Reconstructed shape:", customer_features.shape)

missing_columns = sorted(
    set(reference_features.columns) - set(customer_features.columns)
)
extra_columns = sorted(
    set(customer_features.columns) - set(reference_features.columns)
)

print("Missing columns:", missing_columns)
print("Extra columns:", extra_columns)

# Compare customer identifiers independently of row ordering
customer_key = "customer_unique_id"

missing_customers = set(reference_features[customer_key]) - set(
    customer_features[customer_key]
)
extra_customers = set(customer_features[customer_key]) - set(
    reference_features[customer_key]
)

print("Missing customers:", len(missing_customers))
print("Extra customers:", len(extra_customers))

if missing_columns or extra_columns or missing_customers or extra_customers:
    print("\nReference comparison requires investigation.")
else:
    # Align records and columns before comparing individual values
    original = reference_features.set_index(customer_key).sort_index()
    rebuilt = customer_features.set_index(customer_key).sort_index()
    rebuilt = rebuilt[original.columns]

    differences = {}

    for column in original.columns:
        left = original[column]
        right = rebuilt[column]

        if pd.api.types.is_numeric_dtype(left) and pd.api.types.is_numeric_dtype(right):
            matching = np.isclose(
                left.to_numpy(dtype=float),
                right.to_numpy(dtype=float),
                rtol=1e-9,
                atol=1e-9,
                equal_nan=True
            )
        else:
            matching = (
                left.eq(right)
                | (left.isna() & right.isna())
            ).fillna(False).to_numpy(dtype=bool)

        mismatch_count = int((~matching).sum())

        if mismatch_count:
            differences[column] = mismatch_count

    print("Columns with different values:", len(differences))
    print("Value differences by column:", differences)

    if not differences:
        print("\nReference dataset comparison passed.")
    else:
        print("\nFeature differences require investigation.")


# Export reconstructed features only after reference validation passes
if (
    not missing_columns
    and not extra_columns
    and not missing_customers
    and not extra_customers
    and not differences
):
    output_path = (
        data_dir / "processed" / "customer_features_rebuilt.pkl"
    )

    customer_features.to_pickle(output_path)

    print("\nValidated Feature Export")
    print("-" * 45)
    print("Output file:", output_path)
    print("File exists:", output_path.is_file())
    print("Exported customers:", len(customer_features))
    print("Exported columns:", customer_features.shape[1])

    assert output_path.is_file()
    print("\nValidated feature export completed.")
else:
    raise AssertionError(
        "Feature export blocked because the reference comparison failed."
    )










