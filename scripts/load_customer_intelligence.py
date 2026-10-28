# Load historical customer intelligence into PostgreSQL

from pathlib import Path

import pandas as pd
from dotenv import dotenv_values
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL

# Locate project files
project_root = Path(__file__).resolve().parent.parent

config = dotenv_values(project_root / ".env")

data_path = (
    project_root
    / "data"
    / "processed"
    / "customer_intelligence_historical.parquet"
)

table_name = "customer_intelligence_historical"

# Validate source file and configuration
assert data_path.is_file(), f"Dataset not found: {data_path}"

required_settings = [
    "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"
]

missing_settings = [
    key for key in required_settings if not config.get(key)
]

if missing_settings:
    raise ValueError(f"Missing database settings: {missing_settings}")

# Read validated historical customer data
customers = pd.read_parquet(data_path)

assert len(customers) == 78100
assert customers["customer_unique_id"].is_unique

print("Customer Intelligence PostgreSQL Integration")
print("-" * 55)
print("Source customers:", len(customers))
print("Source columns:", len(customers.columns))

# Configure the database connection
database_url = URL.create(
    "postgresql+psycopg2",
    username=config["DB_USER"],
    password=config["DB_PASSWORD"],
    host=config["DB_HOST"],
    port=int(config["DB_PORT"]),
    database=config["DB_NAME"]
)

engine = create_engine(database_url)

try:
    # Safeguard existing database tables
    inspector = inspect(engine)

    if inspector.has_table(table_name, schema="public"):
        raise RuntimeError(
            f"Table '{table_name}' already exists. "
            "Existing data will not be overwritten."
        )

    # Load into a new table only
    customers.to_sql(
        name=table_name,
        con=engine,
        schema="public",
        if_exists="fail",
        index=False,
        chunksize=2000,
        method="multi"
    )

    # Verify stored customer records
    with engine.connect() as connection:
        stored_records = connection.execute(
            text(
                "SELECT COUNT(*) "
                "FROM public.customer_intelligence_historical"
            )
        ).scalar()

        unique_customers = connection.execute(
            text(
                "SELECT COUNT(DISTINCT customer_unique_id) "
                "FROM public.customer_intelligence_historical"
            )
        ).scalar()

    assert stored_records == len(customers)
    assert unique_customers == len(customers)

    print("\nPostgreSQL Load Validation")
    print("-" * 55)
    print("Target database:", config["DB_NAME"])
    print("Target table:", table_name)
    print("Records loaded:", stored_records)
    print("Unique customers:", unique_customers)
    print("Validation: Passed")

finally:
    engine.dispose()