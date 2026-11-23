
from pathlib import Path

import joblib
import pandas as pd


# Locate the project directories and required files
project_root = Path(__file__).resolve().parent.parent

features_path = (
    project_root / "data" / "processed" / "customer_features_built.pkl"
)

model_path = (
    project_root / "models" / "repeat_purchase_logistic_regression.joblib"
)


# Verify that the required files exist
for file_path in [features_path, model_path]:
    if not file_path.is_file():
        raise FileNotFoundError(f"Required file not found: {file_path}")


# Load the reconstructed customer features and fitted model
customer_features = pd.read_pickle(features_path)
model = joblib.load(model_path)


# Obtain the feature names recorded during model training
if not hasattr(model, "feature_names_in_"):
    raise ValueError("Saved model does not contain feature_names_in_.")

model_features = list(model.feature_names_in_)

missing_columns = [
    column
    for column in model_features
    if column not in customer_features.columns
]

if missing_columns:
    raise ValueError(f"Missing model features: {missing_columns}")


# Validate customer identities and model input availability
assert customer_features["customer_unique_id"].is_unique

model_inputs = customer_features[model_features]

complete_feature_rows = model_inputs.notna().all(axis=1)

scoreable_customers = customer_features.loc[
    complete_feature_rows
].copy()

unscoreable_customers = customer_features.loc[
    ~complete_feature_rows
].copy()


# Report the model input validation results
print("\nCustomer Scoring Input Validation")
print("-" * 45)
print("Total customers:", len(customer_features))
print("Model input features:", len(model_features))
print("Customers with complete features:", len(scoreable_customers))
print("Customers with missing features:", len(unscoreable_customers))
print("Duplicate customers:", customer_features["customer_unique_id"].duplicated().sum())

print("\nMissing model inputs:")
print(model_inputs.isna().sum())

assert len(customer_features) == 78100
assert len(model_features) == 9
assert len(scoreable_customers) + len(unscoreable_customers) == len(customer_features)

print("\nCustomer scoring input validation passed.")


import numpy as np

# Generate probabilities using the existing fitted model pipeline
scoreable_inputs = scoreable_customers[model_features]

predicted_probabilities = model.predict_proba(
    scoreable_inputs
)[:, 1]

# Attach predictions to their corresponding customer records
scored_customers = scoreable_customers[
    ["customer_unique_id", "order_id"]
].copy()

scored_customers["repeat_purchase_propensity"] = predicted_probabilities

# Validate the generated probabilities
print("\nCustomer Probability Validation")
print("-" * 45)
print("Customers scored:", len(scored_customers))
print(
    "Unique customers:",
    scored_customers["customer_unique_id"].nunique()
)

print(
    "Missing probabilities:",
    scored_customers["repeat_purchase_propensity"].isna().sum()
)

print(
    "Minimum probability:",
    round(scored_customers["repeat_purchase_propensity"].min(), 6)
)

print(
    "Maximum probability:",
    round(scored_customers["repeat_purchase_propensity"].max(), 6)
)

print(
    "Average probability:",
    round(scored_customers["repeat_purchase_propensity"].mean(), 6)
)

assert len(scored_customers) == len(scoreable_customers)
assert scored_customers["customer_unique_id"].is_unique
assert np.isfinite(predicted_probabilities).all()
assert scored_customers["repeat_purchase_propensity"].between(0, 1).all()

print("\nCustomer probability validation passed.")


# Create a complete customer-level scoring dataset
customer_scoring_output = customer_features[
    ["customer_unique_id", "order_id"]
].copy()

# Attach probabilities using customer identifiers
customer_scoring_output = customer_scoring_output.merge(
    scored_customers[
        ["customer_unique_id", "repeat_purchase_propensity"]
    ],
    on="customer_unique_id",
    how="left",
    validate="one_to_one"
)

# Identify whether each customer received a model score
customer_scoring_output["scoring_status"] = "not_scored_missing_features"

customer_scoring_output.loc[
    customer_scoring_output["repeat_purchase_propensity"].notna(),
    "scoring_status"
] = "scored"

# Validate the complete scoring population
print("\nComplete Customer Scoring Validation")
print("-" * 45)
print("Total customer records:", len(customer_scoring_output))
print(
    "Unique customers:",
    customer_scoring_output["customer_unique_id"].nunique()
)

print("\nScoring status distribution:")
print(customer_scoring_output["scoring_status"].value_counts())

print(
    "\nMissing probabilities:",
    customer_scoring_output["repeat_purchase_propensity"].isna().sum()
)

assert len(customer_scoring_output) == 78100
assert customer_scoring_output["customer_unique_id"].is_unique
assert (
    customer_scoring_output["scoring_status"].eq("scored").sum()
    == 76197
)
assert (
    customer_scoring_output["scoring_status"].eq(
        "not_scored_missing_features"
    ).sum()
    == 1903
)
assert (
    customer_scoring_output.loc[
        customer_scoring_output["scoring_status"] == "scored",
        "repeat_purchase_propensity"
    ].between(0, 1).all()
)

print("\nComplete customer scoring validation passed.")

# Save validated customer scores to a separate processed dataset
output_path = (
    project_root / "data" / "processed" / "customer_scoring_output.pkl"
)

# Confirm the customer population is complete before exporting
assert len(customer_scoring_output) == 78100
assert customer_scoring_output["customer_unique_id"].is_unique
assert customer_scoring_output["scoring_status"].notna().all()


# Assign propensity segments to customers with valid model scores
segment_labels = [
    "Low Propensity",
    "Medium Propensity",
    "High Propensity"
]

scored_mask = customer_scoring_output["scoring_status"].eq("scored")

scored_probabilities = customer_scoring_output.loc[
    scored_mask, "repeat_purchase_propensity"
]

customer_scoring_output["propensity_segment"] = pd.NA

customer_scoring_output.loc[
    scored_mask, "propensity_segment"
] = pd.qcut(
    scored_probabilities.rank(method="first"),
    q=[0, 0.50, 0.80, 1.00],
    labels=segment_labels
).astype("object")

# Summarise segment assignments
segment_summary = (
    customer_scoring_output.loc[scored_mask]
    .groupby("propensity_segment")
    .agg(
        customers=("customer_unique_id", "nunique"),
        average_propensity=("repeat_purchase_propensity", "mean"),
        minimum_propensity=("repeat_purchase_propensity", "min"),
        maximum_propensity=("repeat_purchase_propensity", "max")
    )
    .reindex(segment_labels)
)

print("\nCustomer Propensity Segmentation Validation")
print("-" * 45)
print(segment_summary)

print(
    "\nCustomers without segments:",
    customer_scoring_output["propensity_segment"].isna().sum()
)

assert segment_summary["customers"].sum() == 76197
assert customer_scoring_output["propensity_segment"].isna().sum() == 1903

print("\nCustomer propensity segmentation validation passed.")

# Export the scoring results
customer_scoring_output.to_pickle(output_path)

# Reload the saved dataset to verify the export
saved_scores = pd.read_pickle(output_path)

assert len(saved_scores) == len(customer_scoring_output)
assert saved_scores["customer_unique_id"].is_unique

pd.testing.assert_frame_equal(
    saved_scores,
    customer_scoring_output,
    check_exact=True
)

print("\nCustomer Scoring Export Validation")
print("-" * 45)
print("Output file:", output_path)
print("File exists:", output_path.is_file())
print("Exported customers:", len(saved_scores))
print("Exported columns:", saved_scores.shape[1])
print("Successfully scored:", saved_scores["scoring_status"].eq("scored").sum())
print(
    "Not scored:",
    saved_scores["scoring_status"].eq(
        "not_scored_missing_features"
    ).sum()
)

print("\nCustomer scoring export completed.")



